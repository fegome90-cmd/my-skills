import os
from pathlib import Path
import subprocess
import sys
import unittest


HELPER = Path(__file__).resolve().parents[1] / "scripts" / "contrast_check.py"


def run_cli(*args):
    return subprocess.run(
        [sys.executable, "-B", str(HELPER), *args],
        capture_output=True,
        text=True,
        env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
        check=False,
    )


class ContrastCliTests(unittest.TestCase):
    def test_ramp_does_not_approve_rounded_600_contrast_failure(self):
        result = run_cli("ramp", "#1AA800")

        self.assertEqual(result.returncode, 0, result.stderr)
        row = next(
            line.split()
            for line in result.stdout.splitlines()
            if line.split()[:2] == ["600", "#158A00"]
        )
        self.assertEqual(
            row[-1],
            "no",
            "#158A00 has 4.499411115573:1 against white; rounded display must not approve it",
        )

    def test_black_and_white_have_contrast_ratio_21(self):
        result = run_cli("pair", "#FFFFFF", "#000000")

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(
            result.stdout.strip(),
            "#FFFFFF sobre #000000: 21.00:1 -> AA texto, AAA texto, AA grande/UI",
        )

    def test_identical_short_hex_has_contrast_ratio_one(self):
        result = run_cli("pair", "#ABC", "#ABC")

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(
            result.stdout.strip(),
            "#ABC sobre #ABC: 1.00:1 -> falla AA texto, falla grande/UI",
        )

    def test_unprefixed_short_hex_is_accepted(self):
        result = run_cli("pair", "ABC", "#abc")

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("1.00:1 -> falla AA texto, falla grande/UI", result.stdout)

    def test_near_threshold_display_rounding_does_not_pass_normal_text(self):
        result = run_cli("pair", "#158A00", "#FFFFFF")

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(
            result.stdout.strip(),
            "#158A00 sobre #FFFFFF: 4.50:1 -> falla AA texto, AA grande/UI",
        )

    def test_pair_and_ramp_agree_for_emitted_hex_colors(self):
        bases = ("#1AA800", "#3B82F6", "#FACC15", "#E11D48")
        step_names = {"100", "150", "200", "300", "400", "500", "600", "700", "800", "900"}

        for base in bases:
            with self.subTest(base=base):
                ramp = run_cli("ramp", base)
                self.assertEqual(ramp.returncode, 0, ramp.stderr)
                rows = {
                    fields[0]: fields
                    for line in ramp.stdout.splitlines()
                    if (fields := line.split())
                    and fields[0] in step_names
                    and fields[1].startswith("#")
                }
                self.assertEqual(set(rows), step_names)
                ink = rows["900"][1]

                for name, fields in rows.items():
                    with self.subTest(step=name):
                        against_white = run_cli("pair", fields[1], "#FFFFFF")
                        self.assertEqual(against_white.returncode, 0, against_white.stderr)
                        displayed_ratio, pair_verdict = against_white.stdout.split(": ", 1)[1].split(":1 -> ", 1)
                        self.assertEqual(displayed_ratio, fields[2])
                        self.assertEqual(fields[4], "si" if pair_verdict.startswith("AA texto") else "no")

                        against_ink = run_cli("pair", fields[1], ink)
                        self.assertEqual(against_ink.returncode, 0, against_ink.stderr)
                        ink_ratio = against_ink.stdout.split(": ", 1)[1].split(":1 -> ", 1)[0]
                        self.assertEqual(ink_ratio, fields[3])

    def test_invalid_hex_is_reported_without_traceback_for_ramp_and_pair(self):
        for value in ("GGGGGG", "#12AB", "##ABC", "##AABBCC"):
            cases = (
                ("ramp", (value,)),
                ("pair", (value, "#FFFFFF")),
                ("pair", ("#000000", value)),
            )
            for command, arguments in cases:
                with self.subTest(value=value, command=command, arguments=arguments):
                    result = run_cli(command, *arguments)

                    self.assertNotEqual(result.returncode, 0)
                    self.assertEqual(result.stdout, "")
                    self.assertEqual(len(result.stderr.splitlines()), 1, result.stderr)
                    self.assertIn(value, result.stderr)
                    self.assertNotIn("Traceback", result.stderr)


if __name__ == "__main__":
    unittest.main()
