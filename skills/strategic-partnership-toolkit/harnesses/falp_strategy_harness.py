#!/usr/bin/env python3
"""
FALP Strategic Analysis Harness

Gatekeeper script for strategic analysis runs.

It does not "think" for the agent. It forces structure:
- Creates a run folder.
- Creates required phase artifacts.
- Requires every phase to be marked STATUS: COMPLETE.
- Requires source ledger, audit, and claim verification before final delivery.
- Blocks final artifact creation if the run is incomplete.

Usage:

    python falp_strategy_harness.py init --input richard_email.md --out runs/richard_falp
    python falp_strategy_harness.py validate --run runs/richard_falp
    python falp_strategy_harness.py final --run runs/richard_falp

Optional:

    python falp_strategy_harness.py status --run runs/richard_falp
    python falp_strategy_harness.py reset --run runs/richard_falp --phase 03

"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Dict, Tuple


PHASES: List[Dict[str, object]] = [
    {
        "id": "00",
        "filename": "00_INPUT.md",
        "title": "Input",
        "required_for_validate": True,
        "requires_complete_status": False,
    },
    {
        "id": "01",
        "filename": "01_SOURCE_EVIDENCE_LEDGER.md",
        "title": "Source Evidence Ledger",
        "required_for_validate": True,
        "requires_complete_status": True,
    },
    {
        "id": "02",
        "filename": "02_STRATEGIC_SITUATION_ASSESSMENT.md",
        "title": "Strategic Situation Assessment",
        "required_for_validate": True,
        "requires_complete_status": True,
    },
    {
        "id": "03",
        "filename": "03_STAKEHOLDER_POWER_MAP.md",
        "title": "Stakeholder Power Map",
        "required_for_validate": True,
        "requires_complete_status": True,
    },
    {
        "id": "04",
        "filename": "04_PILOT_READINESS_MAP.md",
        "title": "Pilot Readiness Map",
        "required_for_validate": True,
        "requires_complete_status": True,
    },
    {
        "id": "05",
        "filename": "05_RISK_GOVERNANCE_REVIEW.md",
        "title": "Risk Governance Review",
        "required_for_validate": True,
        "requires_complete_status": True,
    },
    {
        "id": "06",
        "filename": "06_CONFERENCE_READINESS_MAP.md",
        "title": "Conference Readiness Map",
        "required_for_validate": True,
        "requires_complete_status": True,
    },
    {
        "id": "07",
        "filename": "07_DECISION_MEMO.md",
        "title": "Decision Memo",
        "required_for_validate": True,
        "requires_complete_status": True,
    },
    {
        "id": "08",
        "filename": "08_CROSS_SKILL_AUDIT.md",
        "title": "Cross-Skill Audit",
        "required_for_validate": True,
        "requires_complete_status": True,
    },
    {
        "id": "09",
        "filename": "09_CLAIM_VERIFICATION.md",
        "title": "Claim Verification",
        "required_for_validate": True,
        "requires_complete_status": True,
    },
]

FINAL_FILE = "10_FINAL_DELIVERABLE.md"
STATUS_FILE = "HARNESS_STATUS.json"
RUNBOOK_FILE = "RUNBOOK.md"
MANIFEST_FILE = "MANIFEST.json"


@dataclass
class GateResult:
    gate: str
    passed: bool
    detail: str


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def has_complete_status(text: str) -> bool:
    return bool(re.search(r"(?im)^STATUS:\s*COMPLETE\s*$", text))


def meaningful_body(text: str) -> bool:
    stripped = text.strip()
    if len(stripped) < 350:
        return False
    todo_count = len(re.findall(r"\bTODO\b|\[fill\]|\[complete\]|\[replace\]", stripped, flags=re.I))
    return todo_count == 0


def template_for_phase(filename: str, title: str) -> str:
    common_header = f"""# {title}

STATUS: TODO

Run created by falp_strategy_harness.py.

Do not mark STATUS: COMPLETE until the section is fully answered and checked against sources.

---

"""

    templates: Dict[str, str] = {
        "01_SOURCE_EVIDENCE_LEDGER.md": common_header + """## Source ledger

## Source Lock Gate

- Verbatim quote captured: TODO
- IS about / IS NOT about frame completed: TODO
- Conflation check: PASS / FAIL

## Actor Separation Checkpoint

| Entity | Nature | Status | Authority | Key risk |
|---|---|---|---|---|
| TODO | TODO | TODO | TODO | TODO |

| ID | Claim or input | Source class | Source detail | Confidence | Used for | Limitation |
|---|---|---|---|---|---|---|
| S1 | TODO | Primary/Public/Internal/Inference/Unknown | TODO | High/Medium/Low | TODO | TODO |

## Required source classes

- Primary source:
- Public verification source:
- Internal interpretation:
- Agent inference:
- Unknown / evidence gap:

## Source comparison pre-check

| Potential final claim | Source IDs | Fully supported? | Adjustment needed |
|---|---|---|---|
| TODO | TODO | Yes/Partially/No | TODO |
""",
        "02_STRATEGIC_SITUATION_ASSESSMENT.md": common_header + """## Veredicto

TODO

## Qué está explícito

TODO

## Qué está implícito

| Inference | Confidence | Source basis | Risk if wrong |
|---|---|---|---|
| TODO | High/Medium/Low | TODO | TODO |

## Actores e incentivos

| Actor | Likely interest | What they need | Risk if ignored |
|---|---|---|---|
| TODO | TODO | TODO | TODO |

## Reloj estratégico

TODO

## Riesgos principales

TODO

## Opciones

### Conservative

TODO

### Focused fast

TODO

### Ambitious

TODO

## Recomendación

TODO

## Frase útil para responder

TODO
""",
        "03_STAKEHOLDER_POWER_MAP.md": common_header + """## Veredicto político

TODO

## Mapa de actores

| Stakeholder | Role | Power | Interest | Alignment | Main concern | Best message | Ask |
|---|---|---|---|---|---|---|---|
| TODO | TODO | High/Medium/Low | High/Medium/Low | Ally/Neutral/Unknown/Risk/Blocker | TODO | TODO | TODO |

## Riesgos de manejo

TODO

## Secuencia recomendada

TODO

## Mensajes por actor

TODO

## Próximo movimiento

TODO
""",
        "04_PILOT_READINESS_MAP.md": common_header + """## Veredicto

TODO

## Pregunta piloto

TODO

## Tipo de piloto

TODO

## Alcance mínimo

TODO

## Criterios de inclusión/exclusión

### Inclusión

TODO

### Exclusión

TODO

## Flujo operativo mínimo

TODO

## Gobernanza mínima

| Area | Owner role | Responsibility | Blocking risk |
|---|---|---|---|
| Clinical | TODO | TODO | TODO |
| Operational | TODO | TODO | TODO |
| Technical | TODO | TODO | TODO |
| Ethics/Data | TODO | TODO | TODO |
| Partner | TODO | TODO | TODO |

## Métricas

| Metric | Why it matters | How to collect | Minimum acceptable signal |
|---|---|---|---|
| TODO | TODO | TODO | TODO |

## Evidencia presentable

TODO

## Límites de claims

TODO

## Próximos 7–14 días

TODO
""",
        "05_RISK_GOVERNANCE_REVIEW.md": common_header + """## Veredicto de riesgo

Low / Moderate / High / Not enough information

## Etapa real del proyecto

TODO

## Datos involucrados

| Data type | Sensitivity | Who accesses | Storage/transfer concern | Required control |
|---|---|---|---|---|
| TODO | Low/Moderate/High | TODO | TODO | TODO |

## Riesgos priorizados

| Risk | Probability | Severity | Exposure | Mitigation | Stop condition |
|---|---|---|---|---|---|
| TODO | Low/Medium/High | Low/Medium/High | Low/Medium/High | TODO | TODO |

## Autoridades necesarias

| Authority | Why needed | Before what action |
|---|---|---|
| TODO | TODO | TODO |

## Lo permitido ahora

TODO

## Lo no permitido todavía

TODO

## Próximo control mínimo

TODO
""",
        "06_CONFERENCE_READINESS_MAP.md": common_header + """## Veredicto

Conference-ready / Near-ready / Not ready / Event unconfirmed

## Evento y ambigüedad

TODO

## Objetivo de presentación

TODO

## Evidencia mínima requerida

| Evidence | Needed for | Current status | Owner | Deadline |
|---|---|---|---|---|
| TODO | TODO | TODO | TODO | TODO |

## Artifacts

| Artifact | Purpose | Owner | Status | Deadline |
|---|---|---|---|---|
| TODO | TODO | TODO | TODO | TODO |

## Claims ladder

### Safe now

TODO

### Safe after data

TODO

### Hypothesis only

TODO

### Do not say

TODO

## Backward plan

TODO

## Próximo correo o reunión

TODO
""",
        "07_DECISION_MEMO.md": common_header + """## Title

TODO

## Decision required

TODO

## Recommendation

TODO

## Why now

TODO

## Context

TODO

## Options

| Option | Description | Pros | Cons | Risk level |
|---|---|---|---|---|
| Defer | TODO | TODO | TODO | Low/Moderate/High |
| Narrow pilot | TODO | TODO | TODO | Low/Moderate/High |
| Broader initiative | TODO | TODO | TODO | Low/Moderate/High |

## Recommended scope

TODO

## Governance and approvals

TODO

## Risks and mitigations

| Risk | Mitigation | Owner |
|---|---|---|
| TODO | TODO | TODO |

## Decision ask

TODO

## Next 14 days

TODO
""",
        "08_CROSS_SKILL_AUDIT.md": common_header + """## Audit result

Choose one:

- Pass
- Pass with limitations
- Fail — preliminary only

## Skill coverage audit

| Required skill | Completed? | Missing output | Fix required |
|---|---|---|---|
| strategic-situation-assessment | TODO | TODO | TODO |
| stakeholder-power-map | TODO | TODO | TODO |
| pilot-readiness-map | TODO | TODO | TODO |
| risk-governance-review | TODO | TODO | TODO |
| conference-readiness-map | TODO | TODO | TODO |
| decision-memo-writer | TODO | TODO | TODO |

## Source discipline audit

TODO

## Strategic coherence audit

TODO

## Stakeholder audit

TODO

## Pilot audit

TODO

## Risk/governance audit

TODO

## Conference-readiness audit

TODO

## Decision memo audit

TODO

## Red flags found

TODO

## Residual limitations

TODO
""",
        "09_CLAIM_VERIFICATION.md": common_header + """## Final claim verification table

| Claim | Support | Source IDs | Confidence | Action |
|---|---|---|---|---|
| TODO | Direct/Partial/Inference/Unsupported | S1 | High/Medium/Low | Keep/Weaken/Reframe as hypothesis/Remove/Verify before use |

## Unsupported claims removed or revised

TODO

## Claims reframed as hypothesis

TODO

## Claims requiring verification before external use

TODO
""",
    }

    return templates.get(filename, common_header + "TODO\n")


def runbook_template() -> str:
    return """# FALP Strategic Analysis Runbook

This run must follow the complete harness sequence.

## Required order

1. Capture context discovery in 00_INPUT.md (profiles, prior notes, hidden actors)
2. Fill 01_SOURCE_EVIDENCE_LEDGER.md including Source Lock Gate and Actor Separation
3. Fill 02_STRATEGIC_SITUATION_ASSESSMENT.md
4. Fill 03_STAKEHOLDER_POWER_MAP.md
5. Fill 04_PILOT_READINESS_MAP.md
6. Fill 05_RISK_GOVERNANCE_REVIEW.md
7. Fill 06_CONFERENCE_READINESS_MAP.md
8. Fill 07_DECISION_MEMO.md
9. Record grill corrections / limitations in 08_CROSS_SKILL_AUDIT.md
10. Fill 09_CLAIM_VERIFICATION.md
11. Run validation:
    python falp_strategy_harness.py validate --run <RUN_DIR>
12. Only if validation passes, create the final deliverable:
    python falp_strategy_harness.py final --run <RUN_DIR>

## Completion rule

A phase is not complete until:

- STATUS: COMPLETE appears at the top.
- TODO placeholders are removed.
- The content is specific to the case.
- Claims are tied back to the source ledger where relevant.

## Fail-closed rule

If governance, consent, conference details, source support, or ownership is missing,
the run can pass only as:

    Pass with limitations

If the missing item blocks decision-making, mark audit as:

    Fail — preliminary only

## Final deliverable rule

Do not manually create 10_FINAL_DELIVERABLE.md before validation.

"""


def final_template() -> str:
    return """# Final Strategic Deliverable

STATUS: TODO

This file was created only after harness validation passed.

Before marking complete, verify that every major claim appears in 09_CLAIM_VERIFICATION.md.

---

## 1. Executive verdict

TODO

## 2. Strategic interpretation

TODO

## 3. Recommended next move

TODO

## 4. Minimal viable pilot path

TODO

## 5. Governance and ethics requirements

TODO

## 6. Stakeholder engagement sequence

TODO

## 7. Conference-readiness path

TODO

## 8. Decision memo summary

TODO

## 9. Claims safe to say now

TODO

## 10. Claims not safe to say yet

TODO

## 11. Open questions

TODO

## 12. Next 14 days

TODO

## 13. Source and assumption notes

TODO

## 14. Residual risks

TODO
"""


def init_run(input_path: Path, out_dir: Path, mode: str) -> None:
    """Initialize a new strategic analysis run with all phase templates."""
    if not input_path.exists():
        raise SystemExit(f"Input file not found: {input_path}")

    out_dir.mkdir(parents=True, exist_ok=True)

    # Copy input into run folder.
    input_target = out_dir / "00_INPUT.md"
    input_text = input_path.read_text(encoding="utf-8")
    write_text(
        input_target,
        "# Input\n\n"
        f"Source file: `{input_path}`\n\n"
        "## Context Discovery\n\n"
        "- Existing profiles/wiki/org-chart notes: TODO\n"
        "- Prior analysis or meeting notes: TODO\n"
        "- Hidden actors not visible in primary source: TODO\n\n"
        "---\n\n"
        f"{input_text.strip()}\n",
    )

    # Create phase templates (skip input, already created).
    for phase in PHASES:
        if phase["filename"] == "00_INPUT.md":
            continue
        target = out_dir / phase["filename"]
        if not target.exists():
            write_text(target, template_for_phase(phase["filename"], phase["title"]))

    # Write manifest.
    manifest: Dict[str, object] = {
        "created_at": utc_now(),
        "input_file": str(input_path),
        "mode": mode,
        "required_phases": [p["filename"] for p in PHASES],
        "final_file": FINAL_FILE,
        "policy": "final deliverable blocked until validate passes",
    }
    write_text(out_dir / MANIFEST_FILE, json.dumps(manifest, indent=2, ensure_ascii=False))
    write_text(out_dir / RUNBOOK_FILE, runbook_template())

    print(f"Initialized run: {out_dir}")
    print(f"Next: fill phase files, then run: python {Path(__file__).name} validate --run {out_dir}")


def validate_run(run_dir: Path, write_status_file: bool = True) -> Tuple[bool, List[GateResult]]:
    """Validate all phases. Returns (passed, gates)."""
    gates: List[GateResult] = []
    if not run_dir.exists():
        return False, [GateResult("run_dir_exists", False, f"Run directory not found: {run_dir}")]

    # Required file existence and completion checks.
    for phase in PHASES:
        if not phase["required_for_validate"]:
            continue

        path = run_dir / phase["filename"]
        exists = path.exists()
        gates.append(GateResult(f"{phase['filename']}:exists", exists, "exists" if exists else "missing"))
        if not exists:
            continue

        text = read_text(path)

        if phase["requires_complete_status"]:
            complete = has_complete_status(text)
            gates.append(
                GateResult(
                    f"{phase['filename']}:status_complete",
                    complete,
                    "STATUS: COMPLETE found" if complete else "missing STATUS: COMPLETE",
                )
            )

        body_ok = meaningful_body(text)
        gates.append(
            GateResult(
                f"{phase['filename']}:meaningful_body",
                body_ok,
                "no placeholders and enough content" if body_ok else "too short or still contains TODO/placeholders",
            )
        )

    # Specific source ledger checks.
    ledger = read_text(run_dir / "01_SOURCE_EVIDENCE_LEDGER.md")
    if ledger:
        has_source_ids = bool(re.search(r"\bS\d+\b", ledger))
        gates.append(
            GateResult("source_ledger:has_source_ids", has_source_ids, "source IDs present" if has_source_ids else "no source IDs found")
        )

        source_classes = ["Primary", "Public", "Internal", "Inference", "Unknown"]
        class_count = sum(1 for c in source_classes if re.search(rf"\b{re.escape(c)}\b", ledger, flags=re.I))
        gates.append(
            GateResult(
                "source_ledger:source_classes_present",
                class_count >= 3,
                f"{class_count}/5 source class labels found",
            )
        )

    # Audit result gate.
    audit = read_text(run_dir / "08_CROSS_SKILL_AUDIT.md")
    if audit:
        audit_pass = bool(re.search(r"(?im)^\s*[-*]?\s*Pass(?:\s+with\s+limitations)?\s*$", audit))
        audit_fail = bool(re.search(r"(?i)Fail\s+—?\s*preliminary\s+only", audit))
        gates.append(
            GateResult(
                "audit:result_not_fail",
                audit_pass and not audit_fail,
                "audit is Pass or Pass with limitations" if audit_pass and not audit_fail else "audit missing pass result or marked fail",
            )
        )

    # Claim verification action gate.
    claims = read_text(run_dir / "09_CLAIM_VERIFICATION.md")
    if claims:
        has_actions = any(action in claims for action in ["Keep", "Weaken", "Reframe as hypothesis", "Remove", "Verify before use"])
        gates.append(
            GateResult(
                "claim_verification:has_actions",
                has_actions,
                "claim actions present" if has_actions else "claim actions missing",
            )
        )

    passed = all(g.passed for g in gates)

    if write_status_file:
        status: Dict[str, object] = {
            "validated_at": utc_now(),
            "passed": passed,
            "gates": [g.__dict__ for g in gates],
        }
        write_text(run_dir / STATUS_FILE, json.dumps(status, indent=2, ensure_ascii=False))

    return passed, gates


def print_status(gates: List[GateResult]) -> None:
    width = max(len(g.gate) for g in gates) if gates else 10
    for g in gates:
        mark = "PASS" if g.passed else "FAIL"
        print(f"{mark:4} {g.gate:<{width}} {g.detail}")


def status_run(run_dir: Path) -> None:
    passed, gates = validate_run(run_dir, write_status_file=True)
    print_status(gates)
    print()
    print("HARNESS:", "PASS" if passed else "FAIL")


def reset_phase(run_dir: Path, phase_id: str) -> None:
    """Reset a specific phase back to TODO status."""
    phase_match = [p for p in PHASES if p["id"] == phase_id]
    if not phase_match:
        raise SystemExit(f"Unknown phase ID: {phase_id}. Valid: {', '.join(p['id'] for p in PHASES)}")

    phase = phase_match[0]
    path = run_dir / phase["filename"]
    if not path.exists():
        raise SystemExit(f"Phase file not found: {path}")

    write_text(path, template_for_phase(phase["filename"], phase["title"]))
    print(f"Reset phase {phase_id} ({phase['title']}): {path}")


def final_run(run_dir: Path) -> None:
    passed, gates = validate_run(run_dir, write_status_file=True)
    if not passed:
        print_status(gates)
        raise SystemExit("\nBlocked: validation failed. Fix phase artifacts before creating final deliverable.")

    final_path = run_dir / FINAL_FILE
    if final_path.exists():
        print(f"Final deliverable already exists: {final_path}")
        return

    write_text(final_path, final_template())
    print(f"Created final deliverable template: {final_path}")
    print("Fill it, then mark STATUS: COMPLETE only after checking 09_CLAIM_VERIFICATION.md.")


def main(argv: List[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="FALP Strategic Analysis Harness")
    sub = parser.add_subparsers(dest="command", required=True)

    p_init = sub.add_parser("init", help="Initialize a strategic analysis run")
    p_init.add_argument("--input", required=True, type=Path, help="Input markdown/text file")
    p_init.add_argument("--out", required=True, type=Path, help="Run output directory")
    p_init.add_argument("--mode", default="full-strategic-report", help="Output mode label (metadata only)")

    p_validate = sub.add_parser("validate", help="Validate a run")
    p_validate.add_argument("--run", required=True, type=Path, help="Run directory")

    p_status = sub.add_parser("status", help="Print run status")
    p_status.add_argument("--run", required=True, type=Path, help="Run directory")

    p_final = sub.add_parser("final", help="Create final deliverable template if validation passes")
    p_final.add_argument("--run", required=True, type=Path, help="Run directory")

    p_reset = sub.add_parser("reset", help="Reset a specific phase back to TODO")
    p_reset.add_argument("--run", required=True, type=Path, help="Run directory")
    p_reset.add_argument("--phase", required=True, help="Phase ID to reset (e.g. 03)")

    args = parser.parse_args(argv)

    if args.command == "init":
        init_run(args.input, args.out, args.mode)
    elif args.command == "validate":
        passed, gates = validate_run(args.run)
        print_status(gates)
        return 0 if passed else 2
    elif args.command == "status":
        status_run(args.run)
    elif args.command == "final":
        final_run(args.run)
    elif args.command == "reset":
        reset_phase(args.run, args.phase)
    else:
        parser.print_help()
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
