"""Code quality agent - detects code smells and quality issues in plans."""

from __future__ import annotations

from .base_agent import BaseAgent


class CodeQualityAgent(BaseAgent):
    """Agent that analyzes code quality implications in plans."""

    name = "code_quality"

    def analyze(self) -> None:
        """Apply code quality rules to the plan."""
        self.apply_rules()

        if not self.findings:
            self.add_default_finding(
                title="Sin smells claros en plan (heurística)",
                risk="smells pueden emerger al implementar",
                recommendation="Mantener cambios atómicos y medir complejidad por PR.",
            )


if __name__ == "__main__":
    from .base_agent import run_agent_cli

    run_agent_cli(CodeQualityAgent)
