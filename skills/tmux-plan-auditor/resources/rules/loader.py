"""Load and merge detection rules from YAML files."""

from __future__ import annotations

import hashlib

try:
    import yaml  # type: ignore[import-untyped]

    HAS_YAML = True
except ImportError:
    HAS_YAML = False

import os
import re
import threading
import warnings
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

_rules_cache: dict[str, list[Rule]] = {}
_rules_cache_lock = threading.Lock()


@dataclass
class Rule:
    """A detection rule for an agent."""

    pattern: str
    severity: str
    title: str
    risk: str
    recommendation: str
    is_proposal: bool = False
    applies_to: list[str] | None = None
    _compiled: re.Pattern | None = field(default=None, repr=False, init=False)

    _compiled_flags: int | None = field(default=None, repr=False, init=False)

    def matches(self, text: str, flags: int = 0) -> bool:
        """Check if this rule matches the given text.

        The regex is lazily compiled and cached.  If *flags* differs from
        the previously cached compilation, the regex is recompiled.
        """
        if self._compiled is None or self._compiled_flags != flags:
            object.__setattr__(self, "_compiled", re.compile(self.pattern, flags))
            object.__setattr__(self, "_compiled_flags", flags)
        return self._compiled.search(text) is not None


def parse_rules_from_dict(data: dict[str, Any]) -> list[Rule]:
    """Parse rules from a dictionary."""
    rules = []
    for rule_data in data.get("rules", []):
        rules.append(
            Rule(
                pattern=rule_data.get("pattern", ""),
                severity=rule_data.get("severity", "Baja"),
                title=rule_data.get("title", ""),
                risk=rule_data.get("risk", ""),
                recommendation=rule_data.get("recommendation", ""),
                is_proposal=rule_data.get("is_proposal", False),
                applies_to=rule_data.get("applies_to"),
            )
        )
    return rules


def load_yaml_file(path: Path) -> dict[str, Any]:
    """Load a YAML file.  Uses PyYAML when available; falls back to a
    built-in parser that handles the agent-namespaced format used by
    default.yaml and workflow .yaml files."""
    if HAS_YAML:
        return yaml.safe_load(path.read_text(encoding="utf-8")) or {}

    # --- Fallback parser (no PyYAML) ---
    content = path.read_text(encoding="utf-8")
    result: dict[str, Any] = {}
    current_section: str | None = None
    current_rule: dict[str, Any] = {}

    def _flush_rule() -> None:
        nonlocal current_rule
        if current_rule and current_section:
            result.setdefault(current_section, {"rules": []})
            result[current_section].setdefault("rules", []).append(current_rule)
            current_rule = {}

    for raw_line in content.splitlines():
        stripped = raw_line.strip()

        if not stripped or stripped.startswith("#"):
            continue

        # Top-level namespace (agent name) – no leading dash, colon present,
        # and NOT indented in the raw line.
        if (
            not raw_line[0].isspace()
            and not stripped.startswith("-")
            and ":" in stripped
        ):
            _flush_rule()
            current_section = stripped.split(":", 1)[0].strip()
            result[current_section] = result.get(current_section, {"rules": []})
            continue

        # "rules:" key inside a namespace – skip the marker
        if stripped == "rules:":
            continue

        # List item beginning: "- pattern: ..."
        if stripped.startswith("- pattern:"):
            _flush_rule()
            current_rule = {
                "pattern": stripped.split(":", 1)[1].strip().strip("'\"")
            }
        elif current_rule:
            if stripped.startswith("severity:"):
                current_rule["severity"] = (
                    stripped.split(":", 1)[1].strip().strip("'\"")
                )
            elif stripped.startswith("title:"):
                current_rule["title"] = stripped.split(":", 1)[1].strip().strip("'\"")
            elif stripped.startswith("risk:"):
                current_rule["risk"] = stripped.split(":", 1)[1].strip().strip("'\"")
            elif stripped.startswith("recommendation:"):
                current_rule["recommendation"] = (
                    stripped.split(":", 1)[1].strip().strip("'\"")
                )
            elif stripped.startswith("is_proposal:"):
                current_rule["is_proposal"] = (
                    stripped.split(":", 1)[1].strip().lower() == "true"
                )
            elif stripped.startswith("applies_to:"):
                raw_val = stripped.split(":", 1)[1].strip()
                if raw_val.startswith("[") and raw_val.endswith("]"):
                    current_rule["applies_to"] = [
                        s.strip().strip("'\"")
                        for s in raw_val[1:-1].split(",")
                    ]
                else:
                    current_rule["applies_to"] = [raw_val.strip("'\"")]

    _flush_rule()
    return result


def load_rules(
    agent_name: str, project_rules_path: Path | None = None, workflow: str | None = None
) -> list[Rule]:
    """Load rules for an agent, merging default, workflow, and project overrides.

    Results are cached by (agent_name, project_rules_path, workflow) key.
    """
    cache_key = f"{agent_name}:{project_rules_path}:{workflow}"
    with _rules_cache_lock:
        if cache_key in _rules_cache:
            return _rules_cache[cache_key]

        # Default rules path
        skill_dir = Path(__file__).parent.parent
        default_rules_path = skill_dir / "rules" / "default.yaml"

        # Load default rules
        default_rules: list[Rule] = []
        if default_rules_path.exists():
            default_data = load_yaml_file(default_rules_path)
            agent_data = (
                default_data.get(agent_name, {})
                if agent_name in default_data
                else default_data
            )
            default_rules = parse_rules_from_dict(agent_data)

        # Load workflow-specific rules if provided
        workflow_rules: list[Rule] = []
        if workflow and workflow != "feature":
            workflow_rules_path = skill_dir / "rules" / f"{workflow}.yaml"
            if workflow_rules_path.exists():
                workflow_data = load_yaml_file(workflow_rules_path)
                agent_wf_data = (
                    workflow_data.get(agent_name, {})
                    if agent_name in workflow_data
                    else workflow_data
                )
                workflow_rules = parse_rules_from_dict(agent_wf_data)

        # Load project-specific rules if provided
        project_rules: list[Rule] = []
        if project_rules_path and project_rules_path.exists():
            project_data = load_yaml_file(project_rules_path)
            agent_pj_data = (
                project_data.get(agent_name, {})
                if agent_name in project_data
                else project_data
            )
            project_rules = parse_rules_from_dict(agent_pj_data)

        # Merge rules in order: default < workflow < project
        merged_base = merge_rules(default_rules, workflow_rules, agent_name)
        result = merge_rules(merged_base, project_rules, agent_name)
        _rules_cache[cache_key] = result
        return result


def _rule_id(rule: Rule) -> str:
    """Generate a stable ID for a rule based on pattern + title."""
    key = f"{rule.pattern}:{rule.title}"
    return hashlib.sha256(key.encode()).hexdigest()[:8]


def merge_rules(
    base_rules: list[Rule], override_rules: list[Rule], agent_name: str
) -> list[Rule]:
    """Merge base and override rules for a specific agent.

    Override rules override base rules with the same stable ID.
    Warns if an override replaces a rule with different content.
    """
    merged: dict[str, Rule] = {_rule_id(r): r for r in base_rules}

    for rule in override_rules:
        rid = _rule_id(rule)
        if rid in merged:
            existing = merged[rid]
            if (
                existing.severity != rule.severity
                or existing.recommendation != rule.recommendation
            ):
                warnings.warn(
                    f"Rule '{rule.title}' overridden for agent '{agent_name}': "
                    f"severity {existing.severity}→{rule.severity}"
                )
        merged[rid] = rule

    return list(merged.values())


def find_project_rules_file(project_root: str | None = None) -> Path | None:
    """Find project-specific rules file.

    Search from project_root (if given) or AUDITOR_PROJECT_ROOT env var.
    Falls back to None (use default rules only).
    """
    root_str = project_root or os.getenv("AUDITOR_PROJECT_ROOT")
    if not root_str:
        return None

    root = Path(root_str)
    candidate = root / ".pi" / "auditor-rules.yaml"
    if candidate.exists():
        return candidate
    return None
