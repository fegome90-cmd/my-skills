"""Shared fixtures for tmux-plan-auditor tests."""

import sys
from pathlib import Path

import pytest

# Ensure resources package is importable
SKILL_DIR = Path(__file__).parent.parent
if str(SKILL_DIR) not in sys.path:
    sys.path.insert(0, str(SKILL_DIR))


@pytest.fixture
def skill_dir():
    return SKILL_DIR


@pytest.fixture
def tmp_plan(tmp_path: Path) -> Path:
    """Create a temporary plan file."""
    plan = tmp_path / "plan.md"
    plan.write_text("# Test Plan\n\n- Add Rich terminal support\n")
    return plan


@pytest.fixture
def empty_plan(tmp_path: Path) -> Path:
    plan = tmp_path / "empty.md"
    plan.write_text("")
    return plan


@pytest.fixture
def web_api_plan(tmp_path: Path) -> Path:
    plan = tmp_path / "api.md"
    plan.write_text(
        "# API Plan\n\n- Add FastAPI endpoint for users\n- Include structured logging\n"
    )
    return plan


@pytest.fixture
def tui_rich_plan(tmp_path: Path) -> Path:
    plan = tmp_path / "tui.md"
    plan.write_text(
        "# TUI Plan\n\n- Use Rich for terminal output\n- Add Textual components\n"
    )
    return plan
