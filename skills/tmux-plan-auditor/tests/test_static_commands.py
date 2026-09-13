"""Tests for static command detection."""

import json
from pathlib import Path

from resources.agents.testing_static_agent import _detect_static_commands


class TestDetectStaticCommands:
    def test_node_project_with_lint(self, tmp_path: Path):
        pkg = tmp_path / "package.json"
        pkg.write_text(
            json.dumps(
                {"scripts": {"lint": "eslint .", "typecheck:app": "tsc --noEmit"}}
            )
        )
        (tmp_path / "bun.lockb").touch()
        cmds, error = _detect_static_commands(str(tmp_path))
        assert error is None
        assert ["bun", "run", "lint"] in cmds
        assert ["bun", "run", "typecheck:app"] in cmds

    def test_python_project(self, tmp_path: Path):
        pyproject = tmp_path / "pyproject.toml"
        pyproject.write_text("[tool.pytest.ini_options]\n")
        cmds, error = _detect_static_commands(str(tmp_path))
        assert error is None
        assert ["pytest", "--co", "-q"] in cmds

    def test_no_project_files(self, tmp_path: Path):
        cmds, error = _detect_static_commands(str(tmp_path))
        assert cmds == []
        assert error is None

    def test_invalid_package_json(self, tmp_path: Path):
        pkg = tmp_path / "package.json"
        pkg.write_text("{invalid json")
        cmds, error = _detect_static_commands(str(tmp_path))
        assert cmds == []
        assert error is not None
        assert "Invalid package.json" in error
