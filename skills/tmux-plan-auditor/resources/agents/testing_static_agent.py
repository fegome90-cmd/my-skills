"""Testing static agent - analyzes testing requirements and runs static checks."""

from __future__ import annotations

import json
import os
import re
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .base_agent import BaseAgent, Finding, Evidence


@dataclass
class CommandResult:
    """Result of a command execution."""

    command: str
    exit_code: int | None = None
    ok: bool = False
    stdout_tail: str | None = None
    stderr_tail: str | None = None
    error: str | None = None


def _detect_static_commands(project_root: str) -> tuple[list[list[str]], str | None]:
    """Detect static commands from project files.

    Returns (commands, error_message).
    """
    root = Path(project_root)
    commands = []

    pkg = root / "package.json"
    if pkg.exists():
        try:
            data = json.loads(pkg.read_text())
            scripts = data.get("scripts", {})
            # Detect package manager
            if (root / "bun.lockb").exists():
                pm = "bun"
            elif (root / "yarn.lock").exists():
                pm = "yarn"
            elif (root / "pnpm-lock.yaml").exists():
                pm = "pnpm"
            elif (root / "package-lock.json").exists():
                pm = "npm"
            else:
                # No lock file — cannot determine which PM the project uses
                return [], None
            for cmd_name in ("lint", "typecheck:app", "typecheck"):
                if cmd_name in scripts:
                    commands.append([pm, "run", cmd_name])
        except (json.JSONDecodeError, KeyError) as e:
            return [], f"Invalid package.json: {e}"

    pyproject = root / "pyproject.toml"
    if pyproject.exists():
        content = pyproject.read_text()
        has_pytest = bool(
            re.search(r"\[tool\.pytest", content)
            or re.search(r"\[tool\.hatch\.envs\.test", content)
            or re.search(r"pytest\s*=", content)
        )
        if has_pytest:
            commands.append(["pytest", "--co", "-q"])
        if "[tool.mypy" in content:
            commands.append(["mypy", "."])

    return commands, None


class TestingStaticAgent(BaseAgent):
    """Agent that analyzes testing requirements and runs static checks."""

    name = "testing_static"

    def __init__(self, plan_path: str):
        super().__init__(plan_path)
        self.commands: list[CommandResult] = []

    def analyze(self) -> None:
        """Apply testing rules and run static commands."""
        self.apply_rules()

        project_root = os.getenv("AUDITOR_PROJECT_ROOT", str(Path.cwd()))
        detected, error = _detect_static_commands(project_root)

        if error:
            self.findings.append(
                Finding(
                    severity="Baja",
                    title="No se pudo parsear package.json",
                    evidence=Evidence(file="runtime", line=0, snippet=error),
                    risk="sin señal de calidad estática (Node)",
                    recommendation="Verificar que package.json sea JSON válido.",
                    agent=self.name,
                )
            )
            return

        if not detected:
            self.findings.append(
                Finding(
                    severity="Baja",
                    title="No se detectó stack de proyecto",
                    evidence=Evidence(
                        file="runtime",
                        line=0,
                        snippet="Sin package.json ni pyproject.toml",
                    ),
                    risk="sin señal de calidad estática",
                    recommendation="Verificar que AUDITOR_PROJECT_ROOT apunte al directorio correcto.",
                    agent=self.name,
                )
            )
            return

        for cmd in detected:
            result = CommandResult(command=" ".join(cmd))
            try:
                proc = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    timeout=180,
                    cwd=project_root,
                )
                result.exit_code = proc.returncode
                result.ok = proc.returncode == 0
                result.stdout_tail = "\n".join(proc.stdout.splitlines()[-20:])
                result.stderr_tail = "\n".join(proc.stderr.splitlines()[-20:])
            except subprocess.TimeoutExpired:
                result.ok = False
                result.error = "Command timed out after 180s"
            except FileNotFoundError:
                result.ok = False
                result.error = f"Command not found: {cmd[0]}"
            except Exception as e:
                result.ok = False
                result.error = str(e)

            self.commands.append(result)

            if not result.ok:
                severity = (
                    "Baja" if "Script not found" in (result.error or "") else "Media"
                )
                self.findings.append(
                    Finding(
                        severity=severity,
                        title=f"Falla en {result.command}",
                        evidence=Evidence(
                            file="runtime",
                            line=0,
                            snippet=result.error or f"exit_code={result.exit_code}",
                        ),
                        risk="quality gate inestable",
                        recommendation="Corregir errores o verificar configuración.",
                        agent=self.name,
                    )
                )

    def to_dict(self, duration_ms: int) -> dict[str, Any]:
        """Convert agent output to dictionary with commands."""
        result = super().to_dict(duration_ms)
        result["commands"] = [
            {
                "command": c.command,
                "exit_code": c.exit_code,
                "ok": c.ok,
                "stdout_tail": c.stdout_tail,
                "stderr_tail": c.stderr_tail,
                "error": c.error,
            }
            for c in self.commands
        ]
        return result


if __name__ == "__main__":
    from .base_agent import run_agent_cli

    run_agent_cli(TestingStaticAgent)
