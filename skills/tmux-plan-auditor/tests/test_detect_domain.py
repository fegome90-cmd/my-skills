"""Tests for detect_plan_domain()."""

import pytest

from resources.agents.base_agent import detect_plan_domain


class TestDetectPlanDomain:
    def test_tui_rich_detection(self):
        lines = ["# TUI Plan", "Use Rich for terminal output"]
        assert detect_plan_domain(lines) == "tui-rich"

    def test_textual_detection(self):
        lines = ["# Plan", "Built with Textualize framework"]
        assert detect_plan_domain(lines) == "tui-rich"

    def test_web_api_fastapi(self):
        lines = ["# Plan", "Add FastAPI endpoint"]
        assert detect_plan_domain(lines) == "web-api"

    def test_web_api_flask(self):
        lines = ["# Plan", "Flask REST endpoint"]
        assert detect_plan_domain(lines) == "web-api"

    def test_cli_detection(self):
        lines = ["# Plan", "Add CLI support with Typer"]
        assert detect_plan_domain(lines) == "cli"

    def test_generic_fallback(self):
        lines = ["# Plan", "Some generic content"]
        assert detect_plan_domain(lines) == "generic"

    def test_tui_precedence_over_cli(self):
        lines = ["# Plan", "Rich CLI tool for terminal"]
        assert detect_plan_domain(lines) == "tui-rich"

    def test_empty_plan(self):
        assert detect_plan_domain([]) == "generic"

    def test_no_false_positive_interest(self):
        """'interest' should not match 'rest'."""
        lines = ["# Plan", "User interest in the project"]
        assert detect_plan_domain(lines) == "generic"

    def test_no_false_positive_clickhouse(self):
        """'clickhouse' should not match 'click'."""
        lines = ["# Plan", "Using ClickHouse for analytics"]
        assert detect_plan_domain(lines) == "generic"

    def test_no_false_positive_rich_adjective(self):
        """'rich' as adjective should not trigger tui-rich (bug #10)."""
        lines = ["# Plan", "Provide rich error messages to the user"]
        assert detect_plan_domain(lines) == "generic"

    def test_rich_library_detection(self):
        """'Rich' as library name with terminal context should match tui-rich."""
        lines = ["# Plan", "Use Rich for terminal output"]
        assert detect_plan_domain(lines) == "tui-rich"

    def test_enrich_not_rich(self):
        """'enrich' should not match Rich library."""
        lines = ["# Plan", "Enrich the data model"]
        assert detect_plan_domain(lines) == "generic"
