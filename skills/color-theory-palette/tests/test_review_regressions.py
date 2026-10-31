import colorsys
import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
PALETTE_DIR = ROOT / "skills" / "color-theory-palette"
CATALOG_PATH = PALETTE_DIR / "references" / "palettes-and-harmonies-catalog.md"
COLOR_SKILL_PATH = PALETTE_DIR / "SKILL.md"
TOKENS_PATH = ROOT / "skills" / "design-tokens-components" / "references" / "token-tree-and-crd-templates.md"
LAYOUT_PATH = ROOT / "skills" / "layout-grid-hierarchy" / "references" / "layout-patterns-25.md"
TYPE_SKILL_PATH = ROOT / "skills" / "typography-scales-microtype" / "SKILL.md"
TYPE_REFERENCE_PATH = ROOT / "skills" / "typography-scales-microtype" / "references" / "scales-and-css-recipes.md"
MOTION_SKILL_PATH = ROOT / "skills" / "ui-motion-and-handoff" / "SKILL.md"
MOTION_REFERENCE_PATH = ROOT / "skills" / "ui-motion-and-handoff" / "references" / "anti-slop-and-a11y-checklist.md"


def text(path):
    return path.read_text(encoding="utf-8")


def require_match(pattern, value):
    match = re.search(pattern, value)
    if match is None:
        raise AssertionError(f"pattern not found: {pattern}")
    return match


def fenced(markdown, language):
    opening = f"```{language}"
    if opening not in markdown:
        raise AssertionError(f"missing fenced {language} block")
    return markdown.split(opening, 1)[1].split("```", 1)[0].strip("\r\n")


def css_rule(css, selector):
    start = css.index(selector)
    opening = css.index("{", start)
    depth = 1
    for index in range(opening + 1, len(css)):
        if css[index] == "{":
            depth += 1
        elif css[index] == "}":
            depth -= 1
            if depth == 0:
                return css[opening + 1:index]
    raise AssertionError(f"unclosed CSS rule: {selector}")


def css_declarations(block):
    return dict(re.findall(r"(?m)^\s*(--[\w-]+)\s*:\s*([^;]+);", block))


def css_properties(block):
    return dict(re.findall(r"(?m)^\s*([\w-]+)\s*:\s*([^;]+);", block))


def resolve_css(value, variables):
    value = value.strip()
    match = re.fullmatch(r"var\((--[\w-]+)\)", value)
    if match:
        name = match.group(1)
        if name not in variables:
            raise AssertionError(f"undefined CSS variable: {name}")
        return resolve_css(variables[name], variables)
    return value


def rgb(hex_color):
    value = hex_color.strip().removeprefix("#")
    return tuple(int(value[index:index + 2], 16) for index in (0, 2, 4))


def luminance(color):
    channels = [component / 255 for component in color]
    linear = [channel / 12.92 if channel <= 0.04045 else ((channel + 0.055) / 1.055) ** 2.4 for channel in channels]
    return 0.2126 * linear[0] + 0.7152 * linear[1] + 0.0722 * linear[2]


def contrast(first, second):
    high, low = sorted((luminance(first), luminance(second)), reverse=True)
    return (high + 0.05) / (low + 0.05)


def rgba_white_over_surface(value, surface):
    match = re.fullmatch(r"rgba\(\s*255\s*,\s*255\s*,\s*255\s*,\s*([0-9.]+)\s*\)", value)
    if not match:
        return rgb(value)
    alpha = float(match.group(1))
    return tuple(round(alpha * 255 + (1 - alpha) * component) for component in surface)


def catalog_neutral_rows(catalog):
    rows = []
    for line in catalog.splitlines():
        match = re.match(r"\|\s*\*\*`(\d+)`\*\*\s*\|\s*`(#[0-9A-Fa-f]{6})`\s*\|\s*`(#[0-9A-Fa-f]{6})`", line)
        if match:
            rows.append((match.group(1), match.group(2), match.group(3)))
    return rows


def resolve_json_ref(document, reference):
    path = reference.strip("{}").split(".")
    node = document
    for segment in path:
        node = node[segment]
    value = node.get("$value") if isinstance(node, dict) else None
    if isinstance(value, str) and value.startswith("{"):
        return resolve_json_ref(document, value)
    return value if value is not None else node


class ReviewRegressionTests(unittest.TestCase):
    def test_catalog_neutral_saturation_is_reported_as_step_dependent(self):
        catalog = text(CATALOG_PATH)
        rows = catalog_neutral_rows(catalog)
        self.assertEqual(len(rows), 20)
        saturations = [colorsys.rgb_to_hsv(*(component / 255 for component in rgb(neutral)))[1] * 100 for _, _, neutral in rows]
        self.assertLess(min(saturations), 4)
        self.assertGreater(max(saturations), 8)
        self.assertEqual(catalog.count("S HSB varía por paso"), 2)
        self.assertNotIn("S: 4-8%", catalog)
        self.assertNotIn("S: 4-7%", catalog)

        skill = text(COLOR_SKILL_PATH)
        budget = skill.split("**60% Dominante", 1)[1].split("**30% Secundario", 1)[0]
        self.assertIn("objetivo contextual", budget.lower())
        self.assertIn("no universal", budget.lower())
        self.assertIn("2%-8%", skill)

    def test_dual_theme_declares_its_cold_catalog_primitives(self):
        catalog = text(CATALOG_PATH)
        css = fenced(catalog, "css")
        light = css_declarations(css_rule(css, ':root,\n[data-theme="light"]'))
        variables = {**light, **css_declarations(css_rule(css, '[data-theme="dark"]'))}
        references = re.findall(r"var\((--[\w-]+)\)", css)
        self.assertTrue(references)
        self.assertTrue(set(references).issubset(variables), sorted(set(references) - set(variables)))

        cold = {}
        cold_palette = catalog.split("## 2.", 1)[0]
        for step, primary, neutral in catalog_neutral_rows(cold_palette):
            cold[f"--primary-{step}"] = primary
            cold[f"--neutral-{step}"] = neutral
        for token in ("--primary-300", "--primary-400", "--primary-600", "--primary-700"):
            self.assertEqual(light[token], cold[token])
        for step in ("100", "150", "200", "300", "400", "500", "600", "700", "800", "900"):
            token = f"--neutral-{step}"
            self.assertEqual(light[token], cold[token])
        self.assertIn("fría", catalog.lower())
        self.assertIn("cálida", catalog.lower())

    def test_strong_borders_have_three_to_one_on_effective_light_and_dark_surfaces(self):
        catalog = text(CATALOG_PATH)
        css = fenced(catalog, "css")
        root = css_declarations(css_rule(css, ':root,\n[data-theme="light"]'))
        dark = css_declarations(css_rule(css, '[data-theme="dark"]'))
        light_vars = {**root}
        dark_vars = {**root, **dark}

        light_border = rgb(resolve_css(light_vars["--border-strong"], light_vars))
        for token in ("--surface-canvas", "--surface-subtle", "--surface-card", "--surface-elevated"):
            surface = rgb(resolve_css(light_vars[token], light_vars))
            self.assertGreaterEqual(contrast(light_border, surface), 3, token)

        dark_border = resolve_css(dark_vars["--border-strong"], dark_vars)
        for token in ("--surface-canvas", "--surface-subtle", "--surface-card", "--surface-elevated"):
            surface = rgb(resolve_css(dark_vars[token], dark_vars))
            rendered_border = rgba_white_over_surface(dark_border, surface)
            self.assertGreaterEqual(contrast(rendered_border, surface), 3, token)
        self.assertIn("bordes esenciales", catalog.lower())
        self.assertIn("decorativos", catalog.lower())

    def test_dark_muted_text_meets_normal_text_contrast_on_all_defined_surfaces(self):
        catalog = text(CATALOG_PATH)
        css = fenced(catalog, "css")
        root = css_declarations(css_rule(css, ':root,\n[data-theme="light"]'))
        dark = css_declarations(css_rule(css, '[data-theme="dark"]'))
        variables = {**root, **dark}
        foreground = rgb(resolve_css(variables["--text-muted"], variables))
        for token in ("--surface-canvas", "--surface-subtle", "--surface-card", "--surface-elevated"):
            background = rgb(resolve_css(variables[token], variables))
            self.assertGreaterEqual(contrast(foreground, background), 4.5, token)

    def test_mapped_surface_tokens_reference_alias_layer(self):
        tokens = text(TOKENS_PATH)
        document = json.loads(fenced(tokens, "json"))
        mapped = document["mapped"]["surface"]
        aliases = document["alias"]["surface"]
        self.assertTrue({"canvas", "card", "card-hover"}.issubset(aliases))
        for name, token in mapped.items():
            self.assertTrue(token["$value"].startswith("{alias.surface."), name)
            modes = token["$extensions"]["mode"]
            self.assertTrue(all(value.startswith("{alias.surface.") for value in modes.values()), name)
            self.assertTrue(resolve_json_ref(document, token["$value"]))
            for reference in modes.values():
                self.assertTrue(resolve_json_ref(document, reference))

    def test_layout_grid_max_width_includes_its_padding(self):
        layout = text(LAYOUT_PATH)
        css = fenced(layout, "css")
        declarations = css_properties(css_rule(css, ".layout-grid"))
        root = css_declarations(css_rule(css, ":root"))
        self.assertEqual(declarations.get("box-sizing"), "border-box")
        maximum = float(resolve_css(declarations["max-width"], root).removesuffix("px"))
        padding = float(resolve_css(declarations["padding-inline"], root).removesuffix("px"))
        self.assertGreater(maximum - 2 * padding, 0)

    def test_harmonic_scale_sizes_are_optical_approximations_not_exact_grid_rounding(self):
        reference = text(TYPE_REFERENCE_PATH)
        self.assertIn("ajustes ópticos", reference.lower())
        self.assertNotIn("redond. 4px", reference)
        rows = []
        for line in reference.splitlines():
            cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
            if len(cells) >= 4 and cells[0].startswith("`--text-"):
                exponent = int(require_match(r"[+-]?\d+", cells[1]).group())
                desktop = int(require_match(r"(\d+)px", cells[2]).group(1))
                mobile = int(require_match(r"(\d+)px", cells[3]).group(1))
                rows.append((exponent, desktop, mobile))
        self.assertGreaterEqual(len(rows), 8)
        for exponent, desktop, mobile in rows:
            with self.subTest(exponent=exponent):
                self.assertLessEqual(abs(desktop - 16 * 1.272 ** exponent), 3)
                self.assertLessEqual(abs(mobile - 16 * 1.174 ** exponent), 3)
        self.assertTrue(any(desktop == 12 for _, desktop, _ in rows))
        self.assertIn("ajuste óptico", text(TYPE_SKILL_PATH).lower())

    def test_microtype_roles_have_an_explicit_project_color_system_dependency(self):
        reference = text(TYPE_REFERENCE_PATH)
        css = fenced(reference, "css")
        self.assertIn("sistema de roles de color provisto por el proyecto", css.lower())
        self.assertIn("--text-primary", css)
        self.assertIn("--text-secondary", css)

    def test_text_spacing_requires_all_overrides_and_rendered_content_check(self):
        for path in (TYPE_REFERENCE_PATH, TYPE_SKILL_PATH, MOTION_REFERENCE_PATH):
            with self.subTest(path=path.name):
                content = text(path).lower()
                for requirement in ("line-height: 1.5", "2em", "letter-spacing: 0.12em", "word-spacing: 0.16em"):
                    self.assertIn(requirement, content)
                self.assertIn("simultáneamente", content)
                self.assertIn("not verified", content)
                self.assertIn("render", content)
                self.assertIn("contenido", content)
                self.assertIn("función", content)
                self.assertIn("no basta", content)

    def test_skeleton_copy_limits_claim_to_component_shifts_not_page_cls(self):
        for path in (MOTION_REFERENCE_PATH, MOTION_SKILL_PATH):
            with self.subTest(path=path.name):
                content = text(path).lower()
                self.assertNotIn("cls = 0", content)
                self.assertIn("reducir saltos dentro del componente", content)
                self.assertIn("cls de página", content)
                self.assertIn("medición", content)


if __name__ == "__main__":
    unittest.main()
