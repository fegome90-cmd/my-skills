"""Pydantic models for handoff validation (optional).

Note: Agents use dataclasses from base_agent.py for performance.
These Pydantic models are for optional validation of the final handoff output.
"""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any, Literal

from pydantic import BaseModel, Field


class Severity(str, Enum):
    """Finding severity levels."""

    ALTA = "Alta"
    MEDIA = "Media"
    BAJA = "Baja"


class PatchCandidate(BaseModel):
    """A patch candidate for user approval."""

    id: str
    priority: Severity
    change_summary: str
    risk_if_not_applied: str
    source_agents: list[str] = Field(default_factory=list)
    status: Literal["proposed", "approved", "rejected", "applied"] = "proposed"
    requires_user_confirmation: bool = True
    user_decision: Literal["approved", "rejected", "deferred"] = "deferred"
    user_notes: str = ""


class DecisionRules(BaseModel):
    """Rules for user decisions."""

    allowed_user_decisions: list[Literal["approved", "rejected", "deferred"]] = [
        "approved",
        "rejected",
        "deferred",
    ]
    default: Literal["approved", "rejected", "deferred"] = "deferred"
    requires_user_confirmation: bool = True


class ExecutionSummary(BaseModel):
    """Summary of execution for handoff v2."""

    total_duration_ms: int
    agents_completed: int
    agents_failed: int
    agents_timeout: int = 0
    agents_missing: int = 0
    agents_invalid: int = 0
    session_cleaned_up: bool
    overall_confidence: float | None = None


class HandoffV2(BaseModel):
    """Handoff JSON v2 schema."""

    schema_version: Literal["2.0"] = "2.0"
    handoff_version: Literal["2.0"] = "2.0"
    generated_at: str = Field(default_factory=lambda: datetime.now().isoformat())
    run_id: str
    session_name: str
    plan_path: str
    agent_outputs: dict[str, str]
    findings: list[dict[str, Any]] = Field(default_factory=list)
    raw_patch_candidates: list[dict[str, Any]] = Field(default_factory=list)
    deduplicated_patch_candidates: list[PatchCandidate] = Field(default_factory=list)
    decision_rules: DecisionRules = Field(default_factory=DecisionRules)
    execution_summary: ExecutionSummary | None = None
    next_step_for_parent_agent: str = (
        "Presentar deduplicated_patch_candidates al usuario, capturar user_decision por patch y aplicar solo approved."
    )


def validate_handoff(data: dict[str, Any]) -> HandoffV2:
    """Validate and parse handoff JSON."""
    return HandoffV2.model_validate(data)
