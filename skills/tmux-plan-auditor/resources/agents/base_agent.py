"""Base agent class with common functionality."""

from __future__ import annotations

import json
import os
import re
import sys
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

from resources.rules.loader import load_rules, find_project_rules_file, Rule


_TUI_PATTERNS = [
    re.compile(r"\bRich\b"),
    re.compile(r"\btextual\b", re.IGNORECASE),
    re.compile(r"\btextualize\b", re.IGNORECASE),
]
_WEB_PATTERNS = [
    re.compile(r"\bfastapi\b", re.IGNORECASE),
    re.compile(r"\bflask\b", re.IGNORECASE),
    re.compile(r"\bexpress\.?js\b", re.IGNORECASE),
    re.compile(r"\bendpoint\b", re.IGNORECASE),
]
_CLI_PATTERNS = [
    re.compile(r"\bcli\b", re.IGNORECASE),
    re.compile(r"\bterminal\b", re.IGNORECASE),
    re.compile(r"\btyper\b", re.IGNORECASE),
    re.compile(r"\bclick\b", re.IGNORECASE),
]


def detect_plan_domain(lines: list[str]) -> str:
    """Detect plan domain from content keywords using word boundaries."""
    text = "\n".join(lines)
    text_lower = text.lower()

    # TUI patterns need mixed-case text (\bRich\b must match capital R)
    if any(p.search(text) for p in _TUI_PATTERNS):
        return "tui-rich"
    if any(p.search(text_lower) for p in _WEB_PATTERNS):
        return "web-api"
    if any(p.search(text_lower) for p in _CLI_PATTERNS):
        return "cli"
    return "generic"


VALID_DOMAINS = frozenset({"tui-rich", "web-api", "cli", "generic"})


def validate_domain(domain: str | None) -> str:
    """Validate domain value, fallback to auto-detect if invalid."""
    if domain and domain in VALID_DOMAINS:
        return domain
    return "generic"


@dataclass
class Evidence:
    """Evidence for a finding."""

    file: str
    line: int
    snippet: str


@dataclass
class Finding:
    """A single finding from an agent."""

    severity: str
    title: str
    evidence: Evidence
    risk: str
    recommendation: str
    agent: str | None = None
    confidence: float = 1.0


# Severity ordering constant (reused across modules)
SEVERITY_ORDER = {"Alta": 0, "Media": 1, "Baja": 2}

_PROPOSAL_PATTERNS = [
    re.compile(r"añadir\b|agregar\b|implementar\b|incluir\b|crear\b", re.IGNORECASE),
    re.compile(r"\bwill\b|\bshall\b|\bplan\b|\bpropuesta\b", re.IGNORECASE),
]


class BaseAgent(ABC):
    """Base class for plan auditing agents."""

    name: str = "base"

    def __init__(self, plan_path: str):
        raw_plan_path = Path(plan_path).expanduser()
        project_root = os.getenv("AUDITOR_PROJECT_ROOT")

        if raw_plan_path.is_absolute():
            resolved_plan_path = raw_plan_path.resolve()
        elif project_root:
            resolved_plan_path = (Path(project_root) / raw_plan_path).resolve()
        else:
            resolved_plan_path = raw_plan_path.resolve()

        self.plan_path = str(resolved_plan_path)
        self.lines: list[str] = []
        self.findings: list[Finding] = []
        self.plan_domain: str | None = None
        self.start_time: float = 0
        self.status: str = "pending"
        self.error: str | None = None

        workflow = os.getenv("AUDITOR_WORKFLOW", "feature")
        project_rules_file = find_project_rules_file(project_root)
        self.rules: list[Rule] = load_rules(self.name, project_rules_file, workflow)

    def load_plan(self) -> None:
        """Load plan file into memory."""
        path = Path(self.plan_path)
        if not path.exists():
            raise FileNotFoundError(f"Plan not found: {self.plan_path}")
        try:
            self.lines = path.read_text(encoding="utf-8").splitlines()
        except UnicodeDecodeError:
            raise ValueError(f"Plan file is not valid UTF-8: {self.plan_path}")

    def run(self) -> dict[str, Any]:
        """Execute the agent and return structured output."""
        self.start_time = time.time()
        try:
            self.load_plan()
            if self.plan_domain is None:
                env_domain = os.getenv("AUDITOR_PLAN_DOMAIN")
                self.plan_domain = (
                    env_domain if env_domain else detect_plan_domain(self.lines)
                )
            self.analyze()
            self.status = "completed"
        except Exception as e:
            self.status = "failed"
            self.error = str(e)
            self.findings.append(
                Finding(
                    severity="Media",
                    title=f"Agent {self.name} failed",
                    evidence=Evidence(file=self.plan_path, line=0, snippet=str(e)),
                    risk="analysis incomplete",
                    recommendation="Check agent implementation and plan format",
                    agent=self.name,
                )
            )

        duration_ms = int((time.time() - self.start_time) * 1000)
        return self.to_dict(duration_ms)

    @abstractmethod
    def analyze(self) -> None:
        """Analyze the plan and populate findings. Must be implemented by subclasses."""
        raise NotImplementedError("Subclasses must implement analyze()")

    def apply_rules(self, rules: list[Rule] | None = None) -> None:
        """Apply detection rules to plan lines with context awareness."""
        rules = rules or self.rules

        for i, line in enumerate(self.lines, start=1):
            is_proposal = any(p.search(line) for p in _PROPOSAL_PATTERNS)

            for rule in rules:
                if (
                    self.plan_domain
                    and self.plan_domain != "generic"
                    and rule.applies_to is not None
                    and self.plan_domain not in rule.applies_to
                ):
                    continue

                if rule.matches(line, flags=re.IGNORECASE):
                    # Default confidence
                    confidence = 0.9

                    # If this is a proposal context and the rule indicates a potential issue,
                    # we lower the confidence or discard it if explicitly marked as proposal-safe.
                    if is_proposal:
                        if rule.is_proposal:
                            # Rule itself is looking for a proposal (positive signal)
                            confidence = 1.0
                        else:
                            # Rule is looking for a deficiency, but line is proposing a fix!
                            # We lower confidence significantly.
                            confidence = 0.2

                    self.findings.append(
                        Finding(
                            severity=rule.severity,
                            title=rule.title,
                            evidence=Evidence(
                                file=self.plan_path, line=i, snippet=line.strip()
                            ),
                            risk=rule.risk,
                            recommendation=rule.recommendation,
                            agent=self.name,
                            confidence=confidence,
                        )
                    )

        # Filter out low-confidence findings
        self.findings = [f for f in self.findings if f.confidence > 0.3]

    def add_default_finding(self, title: str, risk: str, recommendation: str) -> None:
        """Add a default finding when no rules match."""
        self.findings.append(
            Finding(
                severity="Baja",
                title=title,
                evidence=Evidence(file=self.plan_path, line=1, snippet="No matches"),
                risk=risk,
                recommendation=recommendation,
                agent=self.name,
            )
        )

    def to_dict(self, duration_ms: int) -> dict[str, Any]:
        """Convert agent output to dictionary."""
        return {
            "agent": self.name,
            "generated_at": datetime.now().isoformat(),
            "status": self.status,
            "duration_ms": duration_ms,
            "error": self.error,
            "findings": [
                {
                    "severity": f.severity,
                    "title": f.title,
                    "evidence": {
                        "file": f.evidence.file,
                        "line": f.evidence.line,
                        "snippet": f.evidence.snippet,
                    },
                    "risk": f.risk,
                    "recommendation": f.recommendation,
                    "agent": f.agent,
                    "confidence": f.confidence,
                }
                for f in self.findings
            ],
        }

    def write_output(self, json_path: str, txt_path: str) -> None:
        """Write output to JSON and TXT files."""
        result = self.run()

        Path(json_path).write_text(
            json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8"
        )

        txt_lines = [f"# Agent {self.name.title()}"]
        for f in self.findings:
            ev = f.evidence
            txt_lines.append(f"- [{f.severity}] {f.title} ({ev.file}:{ev.line})")

        Path(txt_path).write_text("\n".join(txt_lines), encoding="utf-8")


def run_agent(
    agent_class: type[BaseAgent], plan_path: str, json_path: str, txt_path: str
) -> None:
    """Convenience function to run an agent from CLI."""
    agent = agent_class(plan_path)
    agent.write_output(json_path, txt_path)


def run_agent_cli(agent_class: type[BaseAgent]) -> None:
    """CLI entry point helper - handles argument parsing and runs agent.

    Usage in agent __main__:
        if __name__ == "__main__":
            run_agent_cli(MyAgent)
    """
    if len(sys.argv) != 4:
        print(f"Usage: {sys.argv[0]} <plan_path> <json_output> <txt_output>")
        sys.exit(1)
    run_agent(agent_class, sys.argv[1], sys.argv[2], sys.argv[3])


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print(f"Usage: {sys.argv[0]} <plan_path> <json_output> <txt_output>")
        sys.exit(1)

    # This module is abstract, subclasses should implement their own __main__
    print("Error: Use a specific agent module, not base_agent")
    sys.exit(1)
