"""Behavior tests for the portable color engine API."""

from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path
from typing import Any, cast


PACKAGE_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = PACKAGE_ROOT / "scripts"
FIXTURES_DIR = Path(__file__).resolve().parent / "fixtures"
ENGINE_SPEC = importlib.util.spec_from_file_location("color_engine", SCRIPTS_DIR / "color_engine.py")
if ENGINE_SPEC is None or ENGINE_SPEC.loader is None:
    raise RuntimeError("Unable to load color_engine.py for tests")
ENGINE_MODULE = cast(Any, importlib.util.module_from_spec(ENGINE_SPEC))
ENGINE_SPEC.loader.exec_module(ENGINE_MODULE)
ColorEngine = ENGINE_MODULE.ColorEngine


class ColorEngineTests(unittest.TestCase):
    def test_contrast_preserves_all_five_flags_and_aaa_large_semantics(self) -> None:
        result = ColorEngine.check_contrast("#000000", "#767676")
        self.assertEqual(
            set(result),
            {
                "ratio",
                "passes_AA_normal",
                "passes_AA_large",
                "passes_AAA_normal",
                "passes_AAA_large",
            },
        )
        self.assertTrue(result["passes_AA_normal"])
        self.assertTrue(result["passes_AAA_large"])
        self.assertFalse(result["passes_AAA_normal"])
        self.assertTrue(ColorEngine.check_contrast("#000000", "#606060")["passes_AA_large"])
        self.assertFalse(ColorEngine.check_contrast("#000000", "#606060")["passes_AAA_large"])

    def test_contrast_rounds_display_but_uses_raw_ratio_for_flags(self) -> None:
        # Raw contrast is about 4.49856:1, although its displayed ratio rounds to 4.50.
        result = ColorEngine.check_contrast("#6E757C", "#000000")
        self.assertEqual(result["ratio"], 4.5)
        self.assertFalse(result["passes_AA_normal"])
        self.assertFalse(result["passes_AAA_large"])
        self.assertTrue(result["passes_AA_large"])

    def test_contrast_invalid_input_raises_value_error(self) -> None:
        with self.assertRaises(ValueError):
            ColorEngine.check_contrast("#xyz", "#FFFFFF")

    def test_contrast_result_type_remains_exported(self) -> None:
        result_type = getattr(ENGINE_MODULE, "ContrastResult", None)
        self.assertIsNotNone(result_type, "ContrastResult must remain part of the public API")
        self.assertEqual(
            getattr(result_type, "_fields", None),
            (
                "ratio",
                "passes_AA_normal",
                "passes_AA_large",
                "passes_AAA_normal",
                "passes_AAA_large",
            ),
        )

    def test_hex_accepts_rgb_and_long_forms_without_alpha(self) -> None:
        self.assertEqual(ColorEngine.validate_hex("#abc"), "#AABBCC")
        self.assertEqual(ColorEngine.validate_hex("a1B2c3"), "#A1B2C3")

    def test_hex_rejects_malformed_and_alpha_forms(self) -> None:
        for value in ("", "#", "#12", "#12345", "#1234567", "#12345678", "##123456", "#GGG", " 123456"):
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    ColorEngine.validate_hex(value)

    def test_legacy_hsl_harmony_golden_values_are_preserved(self) -> None:
        expected = {
            "complementary": ["#3B82F6", "#F6AF3B"],
            "analogous": ["#3B82F6", "#513BF6", "#3BE0F6"],
            "triadic": ["#3B82F6", "#F63B82", "#82F63B"],
        }
        for harmony, colors in expected.items():
            with self.subTest(harmony=harmony):
                self.assertEqual(ColorEngine.generate_harmony("#3B82F6", harmony), colors)

    def test_oklch_harmony_returns_supported_cardinality_and_normalized_base(self) -> None:
        for harmony, count in (("complementary", 2), ("analogous", 3), ("triadic", 3)):
            with self.subTest(harmony=harmony):
                result = ColorEngine.generate_harmony("abc", harmony, space="oklch")
                self.assertEqual(len(result), count)
                self.assertEqual(result[0], "#AABBCC")

    def test_achromatic_harmonies_repeat_normalized_base(self) -> None:
        for harmony, count in (("complementary", 2), ("analogous", 3), ("triadic", 3)):
            with self.subTest(harmony=harmony):
                self.assertEqual(
                    ColorEngine.generate_harmony("#777", harmony),
                    ["#777777"] * count,
                )

    def test_monochromatic_harmony_uses_five_canonical_scale_steps(self) -> None:
        scale = ColorEngine.generate_scale("#3B82F6")
        expected = [scale["steps"][step] for step in ("100", "300", "500", "700", "900")]
        self.assertEqual(ColorEngine.generate_harmony("#3B82F6", "monochromatic"), expected)
        with self.assertRaises(ValueError):
            ColorEngine.generate_harmony("#3B82F6", "monochromatic", space="hsl")

    def test_harmony_rejects_non_string_space_for_every_harmony(self) -> None:
        invalid_spaces = (0, False, [], {}, b"oklch", object())
        harmonies = ("complementary", "analogous", "triadic", "monochromatic")
        for harmony in harmonies:
            for space in invalid_spaces:
                with self.subTest(harmony=harmony, space_type=type(space).__name__):
                    with self.assertRaisesRegex(ValueError, "Harmony space must be a string or None"):
                        ColorEngine.generate_harmony("#3B82F6", harmony, space=space)

    def test_harmony_space_none_and_mixed_case_aliases_preserve_outputs(self) -> None:
        base = "#3B82F6"
        for harmony in ("complementary", "analogous", "triadic", "monochromatic"):
            default = ColorEngine.generate_harmony(base, harmony)
            with self.subTest(harmony=harmony, space=None):
                self.assertEqual(ColorEngine.generate_harmony(base, harmony, space=None), default)

            if harmony == "monochromatic":
                self.assertEqual(ColorEngine.generate_harmony(base, harmony, space="OKLCH"), default)
                continue

            for space in ("hsl", "HSL"):
                with self.subTest(harmony=harmony, space=space):
                    self.assertEqual(ColorEngine.generate_harmony(base, harmony, space=space), default)
            for space in ("oklch", "OKLCH"):
                with self.subTest(harmony=harmony, space=space):
                    self.assertEqual(
                        ColorEngine.generate_harmony(base, harmony, space=space),
                        ColorEngine.generate_harmony(base, harmony, space="oklch"),
                    )

    def test_scale_has_eleven_ordered_steps_and_exact_base_anchor(self) -> None:
        result = ColorEngine.generate_scale("#3B82F6")
        self.assertEqual(set(result), {"base", "space", "anchor", "steps", "collapsed_steps"})
        self.assertEqual(
            list(result["steps"]),
            ["50", "100", "200", "300", "400", "500", "600", "700", "800", "900", "950"],
        )
        self.assertEqual(result["steps"]["500"], "#3B82F6")
        self.assertEqual(result["anchor"], 500)
        self.assertEqual(result["space"], "oklch")

    def test_wada_palette_uses_explicit_synthetic_dataset_and_preserves_order(self) -> None:
        dataset = FIXTURES_DIR / "synthetic-wada-test-data.json"
        result = ColorEngine.wada_palette(7, dataset_path=dataset)
        self.assertEqual(
            result,
            {
                "palette": 7,
                "color_count": 2,
                "colors": [
                    {"name": "Fictional Blue", "hex": "#123456", "rgb": [18, 52, 86]},
                    {"name": "Blue", "hex": "#0000FF", "rgb": [0, 0, 255]},
                ],
            },
        )

    def test_wada_name_query_puts_exact_match_first_then_all_substrings(self) -> None:
        dataset = FIXTURES_DIR / "synthetic-wada-test-data.json"
        result = ColorEngine.wada_color("blue", dataset_path=dataset)
        self.assertEqual(
            [match["name"] for match in result["matches"]],
            ["Blue", "Fictional Blue", "Bluegreen"],
        )
        self.assertEqual(
            [[palette["palette"] for palette in match["palettes"]] for match in result["matches"]],
            [[7, 8], [7], [8]],
        )
        self.assertEqual(
            result["matches"][0]["palettes"][0]["members"],
            [{"name": "Fictional Blue", "hex": "#123456"}],
        )

    def test_wada_exact_name_query_excludes_substrings(self) -> None:
        result = ColorEngine.wada_color(
            "blue", exact=True, dataset_path=FIXTURES_DIR / "synthetic-wada-test-data.json"
        )
        self.assertEqual([match["name"] for match in result["matches"]], ["Blue"])

    def test_wada_data_is_not_implicitly_bundled(self) -> None:
        with self.assertRaisesRegex(ValueError, "not bundled|--dataset"):
            ENGINE_MODULE.load_wada_dataset()

    def test_wada_rejects_unknown_palette_and_missing_name(self) -> None:
        dataset = FIXTURES_DIR / "synthetic-wada-test-data.json"
        with self.assertRaisesRegex(ValueError, "not found"):
            ColorEngine.wada_palette(999, dataset_path=dataset)
        with self.assertRaisesRegex(ValueError, "matches"):
            ColorEngine.wada_color("nonexistent", dataset_path=dataset)


if __name__ == "__main__":
    unittest.main()
