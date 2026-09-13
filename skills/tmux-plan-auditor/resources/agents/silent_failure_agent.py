"""Silent failure agent - detects potential silent failure risks in plans."""

from __future__ import annotations

from .base_agent import BaseAgent, Finding, Evidence


class SilentFailureAgent(BaseAgent):
    """Agent that analyzes potential silent failure risks in plans."""

    name = "silent_failure"

    def analyze(self) -> None:
        """Apply silent failure rules with context awareness from base agent."""
        self.apply_rules()

        if not self.findings:
            self._add_domain_default_finding()

    def _add_domain_default_finding(self) -> None:
        domain = self.plan_domain or "generic"

        recommendations = {
            "web-api": "Agregar sección de semántica de error HTTP y observabilidad mínima.",
            "cli": "Agregar manejo de errores visible en terminal (exit codes, stderr, Rich diagnostics).",
            "tui-rich": "Agregar manejo de errores visible en terminal (exit codes, stderr, Rich diagnostics).",
            "generic": "Agregar sección de manejo de errores y observabilidad mínima.",
        }

        risks = {
            "web-api": "riesgos de errores silenciosos no cubiertos en API",
            "cli": "errores podrían no ser visibles para el usuario de terminal",
            "tui-rich": "errores podrían no ser visibles en la interfaz TUI",
            "generic": "riesgos de errores silenciosos no cubiertos",
        }

        self.findings.append(
            Finding(
                severity="Baja",
                title="Sin sección explícita de silent failures",
                evidence=Evidence(file=self.plan_path, line=1, snippet="No matches"),
                risk=risks.get(domain, risks["generic"]),
                recommendation=recommendations.get(domain, recommendations["generic"]),
                agent=self.name,
            )
        )


if __name__ == "__main__":
    from .base_agent import run_agent_cli

    run_agent_cli(SilentFailureAgent)
