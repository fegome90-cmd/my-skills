"""Subprocess checks for the portable JSON CLI contract."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from typing import Any


PACKAGE_ROOT = Path(__file__).resolve().parents[1]
ENGINE_SCRIPT = PACKAGE_ROOT / "scripts" / "color_engine.py"
FIXTURE = Path(__file__).resolve().parent / "fixtures" / "synthetic-wada-test-data.json"
EVIDENCE_DIR = PACKAGE_ROOT.parents[1] / ".release-evidence" / "color-engine-2.0.0"


class ColorEngineCliTests(unittest.TestCase):
    def setUp(self) -> None:
        EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)
        self.temp_dir = tempfile.TemporaryDirectory(dir=str(EVIDENCE_DIR))
        self.addCleanup(self.temp_dir.cleanup)
        self.temporary_path = Path(self.temp_dir.name)

    def run_cli(self, *args: str, cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(ENGINE_SCRIPT), *args],
            cwd=str(cwd or self.temporary_path),
            env={"PYTHONDONTWRITEBYTECODE": "1"},
            text=True,
            capture_output=True,
            check=False,
        )

    def assert_json_error(self, result: subprocess.CompletedProcess[str]) -> dict[str, Any]:
        self.assertEqual(result.returncode, 1, result)
        self.assertEqual(result.stdout, "")
        payload = json.loads(result.stderr)
        self.assertEqual(set(payload), {"error"})
        self.assertIsInstance(payload["error"], str)
        self.assertTrue(payload["error"])
        return payload

    def test_help_is_successful_and_prints_usage_to_stdout(self) -> None:
        for flag in ("--help", "-h"):
            with self.subTest(flag=flag):
                result = self.run_cli(flag)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertTrue(result.stdout.strip())
                self.assertEqual(result.stderr, "")

    def test_contrast_and_hsl_harmony_return_json_on_stdout(self) -> None:
        contrast = self.run_cli("contrast", "#000", "#fff")
        self.assertEqual(contrast.returncode, 0, contrast.stderr)
        self.assertEqual(contrast.stderr, "")
        self.assertEqual(json.loads(contrast.stdout)["ratio"], 21.0)
        self.assertIn("passes_AAA_large", json.loads(contrast.stdout))

        harmony = self.run_cli("harmony", "abc", "triadic")
        self.assertEqual(harmony.returncode, 0, harmony.stderr)
        self.assertEqual(harmony.stderr, "")
        self.assertEqual(json.loads(harmony.stdout)[0], "#AABBCC")

    def test_scale_and_monochromatic_commands_return_canonical_steps(self) -> None:
        scale_result = self.run_cli("scale", "#3B82F6")
        self.assertEqual(scale_result.returncode, 0, scale_result.stderr)
        scale = json.loads(scale_result.stdout)
        self.assertEqual(list(scale["steps"]), ["50", "100", "200", "300", "400", "500", "600", "700", "800", "900", "950"])
        self.assertEqual(scale["steps"]["500"], "#3B82F6")

        mono_result = self.run_cli("harmony", "#3B82F6", "monochromatic")
        self.assertEqual(mono_result.returncode, 0, mono_result.stderr)
        self.assertEqual(
            json.loads(mono_result.stdout),
            [scale["steps"][step] for step in ("100", "300", "500", "700", "900")],
        )

    def test_wada_cli_queries_explicit_synthetic_dataset(self) -> None:
        palette = self.run_cli("wada", "--id", "7", "--dataset", str(FIXTURE))
        self.assertEqual(palette.returncode, 0, palette.stderr)
        self.assertEqual(json.loads(palette.stdout)["color_count"], 2)
        self.assertEqual(
            [color["name"] for color in json.loads(palette.stdout)["colors"]],
            ["Fictional Blue", "Blue"],
        )

        matches = self.run_cli("wada", "--name", "blue", "--dataset", str(FIXTURE))
        self.assertEqual(matches.returncode, 0, matches.stderr)
        self.assertEqual(
            [item["name"] for item in json.loads(matches.stdout)["matches"]],
            ["Blue", "Fictional Blue", "Bluegreen"],
        )
        exact = self.run_cli(
            "wada", "--name", "blue", "--exact", "--dataset", str(FIXTURE)
        )
        self.assertEqual(exact.returncode, 0, exact.stderr)
        self.assertEqual([item["name"] for item in json.loads(exact.stdout)["matches"]], ["Blue"])

    def test_wada_default_has_no_implicit_or_bundled_dataset(self) -> None:
        result = self.run_cli("wada", "--id", "7")
        error = self.assert_json_error(result)
        self.assertIn("--dataset", error["error"])
        self.assertIn("not bundled", error["error"])

    def test_cli_errors_are_json_on_stderr_with_empty_stdout_and_exit_one(self) -> None:
        invalid_cases = (
            (),
            ("unknown",),
            ("contrast",),
            ("contrast", "#xyz", "#fff"),
            ("harmony", "#3B82F6", "unsupported"),
            ("harmony", "#3B82F6", "triadic", "--space", "hsv"),
            ("scale",),
            ("wada",),
            ("wada", "--id", "not-an-id"),
            ("wada", "--id", "7", "--exact"),
            ("wada", "--name", "blue", "--exact"),
            ("wada", "--id", "7", "--dataset"),
        )
        for args in invalid_cases:
            with self.subTest(args=args):
                self.assert_json_error(self.run_cli(*args))

    def test_invalid_external_dataset_is_reported_as_json_error(self) -> None:
        malformed = self.temporary_path / "malformed.json"
        malformed.write_text("{not json", encoding="utf-8")
        result = self.run_cli("wada", "--id", "7", "--dataset", str(malformed))
        self.assertIn("valid JSON", self.assert_json_error(result)["error"])

    def test_legacy_case_variants_match_canonical_cli_output(self) -> None:
        contrast_args = ("contrast", "#414141", "#FFFFFF")
        canonical_contrast = self.run_cli(*contrast_args)
        self.assertEqual(canonical_contrast.returncode, 0, canonical_contrast.stderr)
        self.assertEqual(canonical_contrast.stderr, "")
        self.assertEqual(
            set(json.loads(canonical_contrast.stdout)),
            {
                "ratio",
                "passes_AA_normal",
                "passes_AA_large",
                "passes_AAA_normal",
                "passes_AAA_large",
            },
        )

        for command in ("CONTRAST", "CoNtRaSt"):
            with self.subTest(command=command):
                variant = self.run_cli(command, *contrast_args[1:])
                self.assertEqual(variant.returncode, canonical_contrast.returncode)
                self.assertEqual(variant.stdout, canonical_contrast.stdout)
                self.assertEqual(variant.stderr, canonical_contrast.stderr)

        for harmony_type in ("complementary", "analogous", "triadic"):
            canonical_args = ("harmony", "#336699", harmony_type)
            canonical = self.run_cli(*canonical_args)
            self.assertEqual(canonical.returncode, 0, canonical.stderr)
            self.assertEqual(canonical.stderr, "")

            variants = (
                ("harmony", "#336699", harmony_type.upper()),
                ("harmony", "#336699", harmony_type.capitalize()),
            )
            for args in variants:
                with self.subTest(args=args):
                    result = self.run_cli(*args)
                    self.assertEqual(result.returncode, canonical.returncode)
                    self.assertEqual(result.stdout, canonical.stdout)
                    self.assertEqual(result.stderr, canonical.stderr)

        canonical_triadic = self.run_cli("harmony", "#336699", "triadic")
        combined_variant = self.run_cli("HARMONY", "#336699", "TRIADIC")
        self.assertEqual(combined_variant.returncode, canonical_triadic.returncode)
        self.assertEqual(combined_variant.stdout, canonical_triadic.stdout)
        self.assertEqual(combined_variant.stderr, canonical_triadic.stderr)


if __name__ == "__main__":
    unittest.main()
