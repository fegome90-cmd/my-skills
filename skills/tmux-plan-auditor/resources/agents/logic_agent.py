"""Logic agent - detects logical issues in plans."""

from __future__ import annotations

from .base_agent import BaseAgent


class LogicAgent(BaseAgent):
    """Agent that analyzes logical consistency and completeness of plans."""

    name = "logic"

    def analyze(self) -> None:
        """Apply logic rules to the plan."""
        self.apply_rules()

        if not self.findings:
            self.add_default_finding(
                title="Sin red flags lógicas por heurística",
                risk="pueden existir casos no detectados automáticamente",
                recommendation="Hacer revisión manual de contradicciones entre fases y criterios.",
            )


if __name__ == "__main__":
    from .base_agent import run_agent_cli

    run_agent_cli(LogicAgent)
