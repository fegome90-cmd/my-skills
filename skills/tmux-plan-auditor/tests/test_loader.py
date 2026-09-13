"""Tests for rule loading and merging."""

import pytest

from resources.rules.loader import Rule, parse_rules_from_dict, _rule_id, load_yaml_file
from pathlib import Path


class TestRuleParsing:
    def test_parse_basic_rule(self):
        data = {
            "rules": [
                {
                    "pattern": r"\btest\b",
                    "severity": "Alta",
                    "title": "Test rule",
                    "risk": "test risk",
                    "recommendation": "fix it",
                }
            ]
        }
        rules = parse_rules_from_dict(data)
        assert len(rules) == 1
        assert rules[0].pattern == r"\btest\b"
        assert rules[0].applies_to is None

    def test_parse_with_applies_to(self):
        data = {
            "rules": [
                {
                    "pattern": r"\bstatus\b",
                    "severity": "Media",
                    "title": "HTTP status",
                    "risk": "risk",
                    "recommendation": "fix",
                    "applies_to": ["web-api"],
                }
            ]
        }
        rules = parse_rules_from_dict(data)
        assert rules[0].applies_to == ["web-api"]

    def test_rule_id_stability(self):
        r1 = Rule(
            pattern=r"\btest\b",
            severity="Alta",
            title="Test",
            risk="r",
            recommendation="fix",
        )
        r2 = Rule(
            pattern=r"\btest\b",
            severity="Alta",
            title="Test",
            risk="r",
            recommendation="fix",
        )
        assert _rule_id(r1) == _rule_id(r2)

    def test_rule_matches(self):
        rule = Rule(
            pattern=r"\btest\b",
            severity="Alta",
            title="Test",
            risk="r",
            recommendation="fix",
        )
        assert rule.matches("this is a test case")
        assert not rule.matches("testing 123")


class TestRuleMatchesFlags:
    """Bug #7: Rule.matches() must respect per-call flags."""

    def test_flags_respected_on_subsequent_calls(self):
        rule = Rule(
            pattern="test",
            severity="Alta",
            title="Flags test",
            risk="r",
            recommendation="fix",
        )
        import re

        # First call WITH IGNORECASE
        assert rule.matches("TEST", flags=re.IGNORECASE) is True

        # Second call WITHOUT IGNORECASE – must not be cached
        assert rule.matches("TEST", flags=0) is False

    def test_flags_cached_with_same_flags(self):
        rule = Rule(
            pattern="test",
            severity="Alta",
            title="Cache test",
            risk="r",
            recommendation="fix",
        )
        import re

        assert rule.matches("test", flags=re.IGNORECASE) is True
        assert rule.matches("TEST", flags=re.IGNORECASE) is True


class TestFallbackYamlParser:
    """Bug #6: Fallback parser must handle namespaced YAML files."""

    def test_fallback_parses_default_yaml(self, skill_dir):
        import resources.rules.loader as L

        L.HAS_YAML = False
        L._rules_cache.clear()
        try:
            default_path = skill_dir / "resources" / "rules" / "default.yaml"
            data = L.load_yaml_file(default_path)
            assert "logic" in data
            assert "code_quality" in data
            assert "silent_failure" in data
            assert "testing_static" in data
        finally:
            L.HAS_YAML = True

    def test_fallback_loads_all_rules(self, skill_dir):
        import resources.rules.loader as L

        L.HAS_YAML = False
        L._rules_cache.clear()
        try:
            from resources.rules.loader import load_rules

            rules = load_rules("silent_failure")
            assert len(rules) == 3
            # Check applies_to survived
            applies = [r for r in rules if r.applies_to is not None]
            assert len(applies) > 0
        finally:
            L.HAS_YAML = True

    def test_fallback_workflow_yaml(self, skill_dir):
        import resources.rules.loader as L

        L.HAS_YAML = False
        L._rules_cache.clear()
        try:
            refactor_path = skill_dir / "resources" / "rules" / "refactor.yaml"
            data = L.load_yaml_file(refactor_path)
            assert "code_quality" in data
            assert "testing_static" in data
        finally:
            L.HAS_YAML = True
