"""Independent numeric and contract tests for OKLab/OKLCH."""

from __future__ import annotations

import importlib.util
import math
import unittest
from pathlib import Path
from typing import Any, cast


SCRIPTS_DIR = Path(__file__).resolve().parents[1] / "scripts"
SPACES_SPEC = importlib.util.spec_from_file_location("color_spaces", SCRIPTS_DIR / "color_spaces.py")
if SPACES_SPEC is None or SPACES_SPEC.loader is None:
    raise RuntimeError("Unable to load color_spaces.py for tests")
SPACES = cast(Any, importlib.util.module_from_spec(SPACES_SPEC))
SPACES_SPEC.loader.exec_module(SPACES)


class ColorSpacesTests(unittest.TestCase):
    @staticmethod
    def normalized_rgb(hex_code: str) -> tuple[float, float, float]:
        value = hex_code.removeprefix("#")
        return tuple(int(value[index : index + 2], 16) / 255.0 for index in (0, 2, 4))  # type: ignore[return-value]

    def test_published_xyz_to_oklab_reference_vectors(self) -> None:
        vectors = (
            ((0.950, 1.000, 1.089), (1.000, 0.000, 0.000)),
            ((1.000, 0.000, 0.000), (0.450, 1.236, -0.019)),
            ((0.000, 1.000, 0.000), (0.922, -0.671, 0.263)),
            ((0.000, 0.000, 1.000), (0.153, -1.415, -0.449)),
        )
        for xyz, expected in vectors:
            with self.subTest(xyz=xyz):
                for actual, wanted in zip(SPACES.xyz_to_oklab(xyz), expected):
                    self.assertAlmostEqual(actual, wanted, delta=0.0015)

    def test_srgb_roundtrip_is_within_one_eight_bit_channel(self) -> None:
        for hex_code in ("#3B82F6", "#FCB315", "#00FFFF", "#808080", "#000000", "#FFFFFF"):
            with self.subTest(hex_code=hex_code):
                original = self.normalized_rgb(hex_code)
                reconstructed = SPACES.oklab_to_srgb(SPACES.srgb_to_oklab(original))
                for source, result in zip(original, reconstructed):
                    self.assertLessEqual(abs(round(source * 255) - round(result * 255)), 1)

    def test_achromatic_oklch_uses_no_hue(self) -> None:
        lightness, chroma, hue = SPACES.oklab_to_oklch((0.5, 1e-8, -1e-8))
        self.assertAlmostEqual(lightness, 0.5)
        self.assertLessEqual(chroma, 1e-7)
        self.assertIsNone(hue)

    def test_gamut_mapper_preserves_chroma_and_returns_converged_bracket(self) -> None:
        seed_lab = SPACES.srgb_to_oklab(self.normalized_rgb("#3B82F6"))
        seed_lch = SPACES.oklab_to_oklch(seed_lab)
        preserved = SPACES.gamut_map_oklch(seed_lch)
        self.assertFalse(preserved.was_mapped)
        self.assertEqual(preserved.chroma, seed_lch[1])

        target = (0.7, 0.5, 180.0)
        self.assertFalse(SPACES.is_in_srgb_gamut(SPACES.oklch_to_srgb(target)))
        mapped = SPACES.gamut_map_oklch(target)
        self.assertTrue(mapped.was_mapped)
        self.assertLessEqual(mapped.iterations, 32)
        self.assertLessEqual(mapped.upper_chroma - mapped.lower_chroma, 1e-7)
        self.assertTrue(
            SPACES.is_in_srgb_gamut(
                SPACES.oklch_to_srgb((target[0], mapped.lower_chroma, target[2]))
            )
        )
        self.assertFalse(
            SPACES.is_in_srgb_gamut(
                SPACES.oklch_to_srgb((target[0], mapped.upper_chroma, target[2]))
            )
        )

    def test_scale_keys_anchor_and_monotonicity_for_extremes(self) -> None:
        expected_steps = ["50", "100", "200", "300", "400", "500", "600", "700", "800", "900", "950"]
        for hex_code in ("#3B82F6", "#FCB315", "#00FFFF", "#808080", "#000000", "#FFFFFF"):
            with self.subTest(hex_code=hex_code):
                base_lab = SPACES.srgb_to_oklab(self.normalized_rgb(hex_code))
                scale = SPACES.generate_scale(hex_code, base_lab)
                self.assertEqual(scale["base"], hex_code)
                self.assertEqual(scale["space"], "oklch")
                self.assertEqual(scale["anchor"], 500)
                self.assertEqual(list(scale["steps"]), expected_steps)
                self.assertEqual(scale["steps"]["500"], hex_code)

                lightnesses = []
                seen = set()
                collapsed = []
                for step, output in scale["steps"].items():
                    self.assertRegex(output, r"^#[0-9A-F]{6}$")
                    lightnesses.append(SPACES.srgb_to_oklab(self.normalized_rgb(output))[0])
                    if output in seen:
                        collapsed.append(step)
                    seen.add(output)
                self.assertEqual(scale["collapsed_steps"], collapsed)
                self.assertTrue(
                    all(left + 0.002 >= right for left, right in zip(lightnesses, lightnesses[1:])),
                    lightnesses,
                )

    def test_scale_targets_follow_frozen_plan_curve(self) -> None:
        base_lab = SPACES.srgb_to_oklab(self.normalized_rgb("#3B82F6"))
        targets = SPACES.scale_targets(base_lab)
        base_l, base_c, base_h = SPACES.oklab_to_oklch(base_lab)
        light_factors = {"50": 0.96, "100": 0.88, "200": 0.72, "300": 0.52, "400": 0.28}
        dark_factors = {"600": 0.15, "700": 0.30, "800": 0.45, "900": 0.60, "950": 0.75}
        self.assertEqual(targets["500"], (base_l, base_c, base_h))
        for step, factor in light_factors.items():
            self.assertAlmostEqual(targets[step][0], base_l + (1 - base_l) * factor)
            self.assertAlmostEqual(targets[step][1], base_c * (1 - factor))
        for step, factor in dark_factors.items():
            self.assertAlmostEqual(targets[step][0], base_l * (1 - factor))
            self.assertAlmostEqual(targets[step][1], base_c * (1 - factor))

    def test_invalid_nonfinite_and_nonconvergent_inputs_raise(self) -> None:
        invalid_values: Any = None
        invalid_calls = (
            lambda: SPACES.srgb_to_oklab((math.nan, 0.0, 0.0)),
            lambda: SPACES.xyz_to_oklab((0.0, math.inf, 1.0)),
            lambda: SPACES.srgb_to_oklab(invalid_values),
            lambda: SPACES.xyz_to_oklab(invalid_values),
            lambda: SPACES.oklch_to_oklab(invalid_values),
            lambda: SPACES.gamut_map_oklch(invalid_values),
            lambda: SPACES.oklch_to_srgb((0.5, -0.1, 30.0)),
            lambda: SPACES.oklch_to_srgb((0.5, 0.1, math.nan)),
            lambda: SPACES.gamut_map_oklch((0.7, 1e300, 50.0)),
        )
        for call in invalid_calls:
            with self.subTest(call=call):
                with self.assertRaises(ValueError):
                    call()

    def test_gamut_tolerance_only_absorbs_float_noise(self) -> None:
        self.assertTrue(SPACES.is_in_srgb_gamut((-5e-8, 1.00000005, 0.5)))
        self.assertFalse(SPACES.is_in_srgb_gamut((-2e-7, 0.5, 0.5)))
        self.assertFalse(SPACES.is_in_srgb_gamut((0.5, 1.0000002, 0.5)))


if __name__ == "__main__":
    unittest.main()
