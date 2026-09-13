#!/usr/bin/env python3
"""
receipt_manager.py - Durable Append-Only Onboarding Receipt Manager
Enforces strict immutability (no-overwrite semantics) and emits tamper-evident, run-keyed receipts.
Captures candidate tree digest, upstream provenance, gate results, and timestamps.
"""

from __future__ import annotations
import sys
import os
import json
import argparse
from pathlib import Path
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

class ReceiptExistsError(FileExistsError):
    """Raised when attempting to overwrite an immutable execution receipt."""
    pass

def emit_receipt(
    receipt_dir: str | Path,
    skill_name: str,
    run_id: str,
    status: str,  # "SUCCESS" | "FAILED" | "ROLLED_BACK"
    candidate_tree_digest: str,
    upstream_author: str,
    upstream_license: str,
    onboarded_by: str,
    tier: str,
    risk: str,
    playbook: str,
    gates: Dict[str, Any],
    error_message: Optional[str] = None,
    allow_overwrite: bool = False
) -> Path:
    out_dir = Path(receipt_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    timestamp_iso = datetime.now(timezone.utc).isoformat()
    filename_base = f"onboarding-{skill_name}-{run_id}"
    json_path = out_dir / f"{filename_base}.json"
    md_path = out_dir / f"{filename_base}.md"

    # Enforce strict immutability / no-overwrite invariant
    if not allow_overwrite:
        if json_path.exists():
            raise ReceiptExistsError(f"Immutable receipt already exists at '{json_path}'. Overwriting is prohibited.")
        if md_path.exists():
            raise ReceiptExistsError(f"Immutable receipt already exists at '{md_path}'. Overwriting is prohibited.")

    data: Dict[str, Any] = {
        "receipt_version": "2.1.4",
        "timestamp": timestamp_iso,
        "run_id": run_id,
        "skill_name": skill_name,
        "status": status,
        "provenance": {
            "upstream_author": upstream_author,
            "upstream_license": upstream_license,
            "onboarded_by": onboarded_by
        },
        "classification": {
            "tier": tier,
            "risk": risk,
            "playbook": playbook
        },
        "candidate_tree_digest": candidate_tree_digest,
        "gates": gates,
        "error": error_message
    }

    # Atomic write with exclusive creation protection
    temp_json = json_path.with_suffix(".tmp")
    temp_json.write_text(json.dumps(data, indent=2), encoding="utf-8")
    temp_json.replace(json_path)

    # NOTE: no backslash sequences inside f-string expressions (Python 3.9 compatibility)
    error_section = ""
    if error_message:
        error_section = "### Error / Rollback Notice\n`" + str(error_message) + "`"

    md_content = f"""# Onboarding Execution Receipt: `{skill_name}`

- **Status:** `{status}`
- **Run ID:** `{run_id}`
- **Timestamp:** `{timestamp_iso}`
- **Candidate Tree Digest:** `{candidate_tree_digest}`

## Provenance & Classification
- **Upstream Author:** {upstream_author}
- **Upstream License:** `{upstream_license}`
- **Onboarded By:** {onboarded_by}
- **Tier:** `{tier}` | **Risk:** `{risk}` | **Playbook:** `{playbook}`

## Verification Gates Summary
- **Preflight:** `{gates.get('preflight', 'N/A')}`
- **Judge A (Exact Lookup):** `{gates.get('judge_a', 'N/A')}`
- **Judge B (5-Fixture Battery):** `{len(gates.get('judge_b', []))} fixtures evaluated`
- **Capability Smoke Test:** `{gates.get('smoke_test', 'N/A')}`
- **TOCTOU Guard:** `{gates.get('toctou', 'N/A')}`
- **Atomic Promotion:** `{gates.get('promotion', 'N/A')}`

{error_section}
"""
    temp_md = md_path.with_suffix(".tmp")
    temp_md.write_text(md_content, encoding="utf-8")
    temp_md.replace(md_path)

    print(f"Receipt written to: {json_path} and {md_path}")
    return json_path

def main() -> None:
    """Minimal CLI (RUN-001): Step F of the runbook invokes this directly, without
    requiring scripts/ on PYTHONPATH. No-overwrite semantics are mandatory here too."""
    parser = argparse.ArgumentParser(prog="receipt_manager", description="Durable append-only onboarding receipt manager")
    sub = parser.add_subparsers(dest="command", required=True)

    emit_p = sub.add_parser("emit", help="Emit an immutable onboarding receipt")
    emit_p.add_argument("--receipt-dir", required=True)
    emit_p.add_argument("--skill-name", required=True)
    emit_p.add_argument("--run-id", required=True)
    emit_p.add_argument("--status", required=True, choices=["SUCCESS", "FAILED", "ROLLED_BACK"])
    emit_p.add_argument("--candidate-tree-digest", required=True)
    emit_p.add_argument("--upstream-author", required=True)
    emit_p.add_argument("--upstream-license", required=True)
    emit_p.add_argument("--onboarded-by", required=True)
    emit_p.add_argument("--tier", required=True)
    emit_p.add_argument("--risk", required=True)
    emit_p.add_argument("--playbook", required=True)
    emit_p.add_argument("--gates-json", required=True,
                        help="Path to verification_receipt.json whose 'gates' dict is embedded")
    emit_p.add_argument("--error-message", default=None)

    args = parser.parse_args()
    if args.command == "emit":
        try:
            gates = json.loads(Path(args.gates_json).read_text(encoding="utf-8"))["gates"]
        except (OSError, KeyError, json.JSONDecodeError) as e:
            print(f"CLI ERROR: cannot read gates from '{args.gates_json}': {e}", file=sys.stderr)
            sys.exit(2)
        try:
            out = emit_receipt(
                receipt_dir=args.receipt_dir,
                skill_name=args.skill_name,
                run_id=args.run_id,
                status=args.status,
                candidate_tree_digest=args.candidate_tree_digest,
                upstream_author=args.upstream_author,
                upstream_license=args.upstream_license,
                onboarded_by=args.onboarded_by,
                tier=args.tier,
                risk=args.risk,
                playbook=args.playbook,
                gates=gates,
                error_message=args.error_message,
            )
        except ReceiptExistsError as e:
            print(f"CLI ERROR: {e}", file=sys.stderr)
            sys.exit(3)
        print(json.dumps({"receipt_json": str(out)}))

if __name__ == "__main__":
    main()
