"""Tests for color engine contrast and harmony calculations."""

import pytest
import sys
from pathlib import Path

# Add scripts directory to sys.path
scripts_dir = Path(__file__).resolve().parent.parent / "scripts"
sys.path.insert(0, str(scripts_dir))

from color_engine import ColorEngine, ContrastResult


def test_contrast_result_includes_aaa_large():
    """Verify that ContrastResult includes passes_AAA_large."""
    # #000000 on #767676 has ratio ~4.54:1 (passes AA normal and AAA large, but not AAA normal)
    res = ColorEngine.check_contrast("#000000", "#767676")
    assert "passes_AAA_large" in res
    assert res["passes_AAA_large"] is True
    assert res["passes_AA_normal"] is True
    assert res["passes_AAA_normal"] is False


def test_contrast_result_fails_aaa_large_when_below_threshold():
    """Verify that passes_AAA_large is False when ratio is below 4.5:1."""
    # #000000 on #606060 has ratio ~3.34:1 (passes AA large, fails AAA large)
    res = ColorEngine.check_contrast("#000000", "#606060")
    assert "passes_AAA_large" in res
    assert res["passes_AA_large"] is True
    assert res["passes_AAA_large"] is False
    assert res["passes_AA_normal"] is False
    assert res["passes_AAA_normal"] is False
