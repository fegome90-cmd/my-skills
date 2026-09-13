"""Build handoff.json v2 from agent outputs."""

from __future__ import annotations

import hashlib
import json
import os
import sys
import time
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any

from resources.agents.base_agent import SEVERITY_ORDER


@dataclass
class AgentStatus:
    """Status of an agent execution."""

    name: str
    status: str = "pending"
    duration_ms: int = 0
    error: str | None = None


@dataclass
class HandoffBuilder:
    """Builds handoff.json v2 from agent outputs."""

    run_dir: str
    run_id: str
    session_name: str
    plan_path: str
    plan_domain: str = "generic"
    agent_names: list[str] = field(
        default_factory=lambda: [
            "logic",
            "code_quality",
            "silent_failure",
            "testing_static",
        ]
    )
    start_time: float = field(default_factory=time.time)

    def get_agent_json_path(self, agent: str) -> str:
        """Get path to agent JSON output."""
        return os.path.join(self.run_dir, f"agent-{agent.replace('_', '-')}.json")

    def load_agent_output(self, agent: str) -> tuple[dict[str, Any], AgentStatus]:
        """Load agent output from JSON file."""
        json_path = self.get_agent_json_path(agent)

        if not os.path.exists(json_path):
            return {}, AgentStatus(name=agent, status="missing")

        try:
            data = json.loads(Path(json_path).read_text(encoding="utf-8"))
            data = self._validate_agent_payload(data, agent)
            status = AgentStatus(
                name=agent,
                status=data.get("status", "completed"),
                duration_ms=data.get("duration_ms", 0),
                error=data.get("error"),
            )
            return data, status
        except json.JSONDecodeError as e:
            return {}, AgentStatus(name=agent, status="invalid", error=str(e))

    def _validate_agent_payload(self, data: dict, agent_name: str) -> dict:
        """Validate and normalize an agent's JSON output."""
        required_keys = {"agent", "status", "findings"}
        missing = required_keys - set(data.keys())
        if missing:
            return {
                "agent": agent_name,
                "status": "invalid",
                "findings": [],
                "error": f"Missing keys: {missing}",
                "duration_ms": 0,
            }

        if not isinstance(data.get("findings"), list):
            data["findings"] = []

        return data

    def collect_findings(
        self, agents_data: dict[str, dict], agent_statuses: list[AgentStatus]
    ) -> list[dict]:
        """Collect and sort findings from all agents, including synthetic findings for failures."""
        all_findings = []

        # Add synthetic findings for failed agents
        for status in agent_statuses:
            if status.status != "completed":
                all_findings.append(
                    {
                        "severity": "Alta",
                        "title": f"Auditoría incompleta: Agente {status.name} ({status.status})",
                        "evidence": {
                            "file": "runtime",
                            "line": 0,
                            "snippet": status.error or "No output generated",
                        },
                        "risk": "Fase de revisión no completada, riesgos potenciales no detectados.",
                        "recommendation": "Verificar logs de la sesión tmux y re-ejecutar si es necesario.",
                        "agent": status.name,
                        "confidence": 1.0,
                    }
                )

        for agent_name, data in agents_data.items():
            for item in data.get("findings", []):
                finding = dict(item)
                finding["agent"] = agent_name
                all_findings.append(finding)

        # Sort by severity
        all_findings.sort(
            key=lambda x: SEVERITY_ORDER.get(x.get("severity", "Baja"), 9)
        )

        return all_findings

    def build_raw_patches(
        self, findings: list[dict], max_patches: int = 10
    ) -> list[dict]:
        """Build raw patch candidates from findings."""
        patches = []
        for idx, f in enumerate(findings[:max_patches], start=1):
            patches.append(
                {
                    "id": f"patch-{idx}",
                    "priority": f.get("severity", "Baja"),
                    "source_agent": f.get("agent"),
                    "change_summary": f.get("recommendation"),
                    "risk_if_not_applied": f.get("risk"),
                    "status": "proposed",
                    "requires_user_confirmation": True,
                    "user_decision": "deferred",
                    "user_notes": "",
                }
            )
        return patches

    def deduplicate_patches(self, raw_patches: list[dict]) -> list[dict]:
        """Deduplicate patches by (priority, change_summary, risk)."""
        dedup_map: dict[tuple, dict] = {}

        for p in raw_patches:
            key = (
                p.get("priority"),
                p.get("change_summary"),
                p.get("risk_if_not_applied"),
            )

            if key not in dedup_map:
                stable_id = hashlib.sha256(
                    f"{key[0]}:{key[1]}:{key[2]}".encode()
                ).hexdigest()[:8]
                dedup_map[key] = {
                    "id": f"patch-{stable_id}",
                    "priority": p.get("priority"),
                    "change_summary": p.get("change_summary"),
                    "risk_if_not_applied": p.get("risk_if_not_applied"),
                    "source_agents": [p.get("source_agent")],
                    "status": "proposed",
                    "requires_user_confirmation": True,
                    "user_decision": "deferred",
                    "user_notes": "",
                }
            else:
                src = p.get("source_agent")
                if src and src not in dedup_map[key]["source_agents"]:
                    dedup_map[key]["source_agents"].append(src)

        # Sort by severity
        deduped = list(dedup_map.values())
        deduped.sort(key=lambda x: SEVERITY_ORDER.get(x.get("priority", "Baja"), 9))

        return deduped

    def build_confirmation_template(self, deduped_patches: list[dict]) -> dict:
        """Build patch confirmation template."""
        return {
            "run_id": self.run_id,
            "decisions": [
                {
                    "patch_id": p["id"],
                    "user_decision": "deferred",
                    "user_notes": "",
                    "approved_by": "",
                    "approved_at": "",
                }
                for p in deduped_patches
            ],
        }

    def build_execution_summary(
        self,
        agent_statuses: list[AgentStatus],
        findings: list[dict],
        session_cleaned_up: bool = False,
    ) -> dict:
        """Build execution summary with overall confidence."""
        max_duration = max((s.duration_ms for s in agent_statuses), default=0)
        completed = sum(1 for s in agent_statuses if s.status == "completed")
        failed = sum(1 for s in agent_statuses if s.status == "failed")
        timeout = sum(1 for s in agent_statuses if s.status == "timeout")
        missing = sum(1 for s in agent_statuses if s.status == "missing")
        invalid = sum(1 for s in agent_statuses if s.status == "invalid")

        # Use median instead of mean to avoid skew from many low-confidence findings
        confidences = sorted(f.get("confidence", 1.0) for f in findings)
        n = len(confidences)
        if n == 0:
            median_confidence = 1.0
        elif n % 2 == 0:
            median_confidence = (confidences[n // 2 - 1] + confidences[n // 2]) / 2
        else:
            median_confidence = confidences[n // 2]

        return {
            "total_duration_ms": max_duration,
            "agents_completed": completed,
            "agents_failed": failed + timeout,
            "agents_timeout": timeout,
            "agents_missing": missing,
            "agents_invalid": invalid,
            "session_cleaned_up": session_cleaned_up,
            "overall_confidence": round(median_confidence, 2),
        }

    def build(
        self, session_cleaned_up: bool = False
    ) -> tuple[dict[str, Any], dict[str, Any]]:
        """Build complete handoff.json v2."""
        agents_data: dict[str, dict] = {}
        agent_statuses: list[AgentStatus] = []
        agent_outputs: dict[str, str] = {}

        for agent in self.agent_names:
            data, status = self.load_agent_output(agent)
            agents_data[agent] = data
            agent_statuses.append(status)
            agent_outputs[agent] = self.get_agent_json_path(agent)

        findings = self.collect_findings(agents_data, agent_statuses)
        raw_patches = self.build_raw_patches(findings)
        deduped_patches = self.deduplicate_patches(raw_patches)
        confirmation_template = self.build_confirmation_template(deduped_patches)
        execution_summary = self.build_execution_summary(
            agent_statuses, findings, session_cleaned_up
        )

        handoff = {
            "schema_version": "2.0",
            "handoff_version": "2.0",
            "generated_at": datetime.now().isoformat(),
            "run_id": self.run_id,
            "session_name": self.session_name,
            "plan_path": self.plan_path,
            "plan_domain": self.plan_domain,
            "agent_outputs": agent_outputs,
            "findings": findings,
            "raw_patch_candidates": raw_patches,
            "deduplicated_patch_candidates": deduped_patches,
            "decision_rules": {
                "allowed_user_decisions": ["approved", "rejected", "deferred"],
                "default": "deferred",
                "requires_user_confirmation": True,
            },
            "execution_summary": execution_summary,
            "next_step_for_parent_agent": (
                "Presentar deduplicated_patch_candidates al usuario, "
                "capturar user_decision por patch y aplicar solo approved."
            ),
        }

        return handoff, confirmation_template

    def write_outputs(self, session_cleaned_up: bool = False) -> None:
        """Write handoff.json and confirmation template."""
        handoff, confirmation_template = self.build(session_cleaned_up)

        handoff_path = Path(self.run_dir) / "handoff.json"
        confirmation_path = Path(self.run_dir) / "patch-confirmation-template.json"

        handoff_path.write_text(
            json.dumps(handoff, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        confirmation_path.write_text(
            json.dumps(confirmation_template, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

        print(f"Wrote: {handoff_path}")
        print(f"Wrote: {confirmation_path}")


def main() -> None:
    """CLI entry point."""
    if len(sys.argv) < 5:
        print(
            "Usage: handoff_builder.py <run_dir> <run_id> <session_name> <plan_path> [session_cleaned_up]"
        )
        sys.exit(1)

    run_dir = sys.argv[1]
    run_id = sys.argv[2]
    session_name = sys.argv[3]
    plan_path = sys.argv[4]
    session_cleaned_up = sys.argv[5].lower() == "true" if len(sys.argv) > 5 else False
    plan_domain = sys.argv[6] if len(sys.argv) > 6 else "generic"

    builder = HandoffBuilder(
        run_dir=run_dir,
        run_id=run_id,
        session_name=session_name,
        plan_path=plan_path,
        plan_domain=plan_domain,
    )
    builder.write_outputs(session_cleaned_up)


if __name__ == "__main__":
    main()
