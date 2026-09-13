#!/usr/bin/env python3
"""
txn_manager.py - Transaction State Marker & Crash Recovery Manager
Tracks states: INIT -> PRECOMMIT -> SKILL_SWAPPED -> REGISTRY_SWAPPED -> COMPLETE
Provides lock acquisition, startup crash recovery, and TOCTOU consistency guards.

Compliant with python-patterns, python-production, and atomic state journal standards.
"""

from __future__ import annotations
import sys
import os
import json
import hashlib
import shutil
import subprocess
import argparse
import time
from pathlib import Path
from typing import Any, Dict, Optional

STATE_FILE = "txn_state.json"
MANIFEST_SCRIPT_NAME = "generate_manifest.sh"
DEFAULT_LOCK_DIR = ".atl/.promotion.lock"

EXIT_RECOVERY_FAILED = 8
STATE_ROLLED_BACK = "ROLLED_BACK"
STATE_RECOVERY_FAILED = "RECOVERY_FAILED"

def sha256_file(filepath: str | Path) -> str:
    path = Path(filepath)
    if not path.is_file():
        return ""
    h = hashlib.sha256()
    with path.open("rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()

def run_manifest_script(target_dir: Path, output_file: Path) -> str:
    script_path = Path(__file__).parent / MANIFEST_SCRIPT_NAME
    if not script_path.exists():
        raise FileNotFoundError(f"Manifest generator script not found at '{script_path}'")
    
    subprocess.run(
        [str(script_path), str(target_dir), str(output_file)],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=60
    )
    return sha256_file(output_file)

def acquire_lock(lock_path: str | Path = DEFAULT_LOCK_DIR, timeout_seconds: int = 10) -> None:
    l_path = Path(lock_path)
    start_time = time.time()
    while True:
        try:
            l_path.mkdir(parents=True, exist_ok=False)
            print(f"Acquired exclusive promotion lock at: {l_path}")
            return
        except FileExistsError:
            if time.time() - start_time > timeout_seconds:
                print(f"LOCK_CONTENTION: Timeout waiting for lock '{l_path}' after {timeout_seconds}s", file=sys.stderr)
                sys.exit(5)
            time.sleep(0.2)

def release_lock(lock_path: str | Path = DEFAULT_LOCK_DIR) -> None:
    l_path = Path(lock_path)
    if l_path.exists():
        try:
            l_path.rmdir()
            print(f"Released exclusive promotion lock at: {l_path}")
        except OSError:
            shutil.rmtree(l_path, ignore_errors=True)

def save_state_atomic(staging_path: Path, data: Dict[str, Any]) -> None:
    state_file = staging_path / STATE_FILE
    temp_file = state_file.with_suffix(".tmp")
    temp_file.write_text(json.dumps(data, indent=2), encoding="utf-8")
    temp_file.replace(state_file)

def load_state(staging_path: Path) -> Dict[str, Any]:
    state_file = staging_path / STATE_FILE
    if not state_file.is_file():
        print(f"Error: No active transaction state file in '{staging_path}'", file=sys.stderr)
        sys.exit(1)
    try:
        return json.loads(state_file.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        print(f"CRITICAL: Corrupted transaction state file '{state_file}': {e}", file=sys.stderr)
        sys.exit(1)

def init_txn(
    staging_dir: str | Path,
    skill_name: str,
    live_registry_path: str | Path,
    live_skill_path: str | Path
) -> None:
    staging = Path(staging_dir)
    base_dir = staging / "base"
    backup_dir = staging / "backup"
    
    base_dir.mkdir(parents=True, exist_ok=True)
    backup_dir.mkdir(parents=True, exist_ok=True)

    live_reg = Path(live_registry_path)
    live_skill = Path(live_skill_path)

    # 1. Freeze snapshot BEFORE overlay compilation
    live_registry_backup = base_dir / "live-registry.md"
    if live_reg.is_file():
        shutil.copy2(live_reg, live_registry_backup)
        reg_sha = sha256_file(live_registry_backup)
    else:
        live_registry_backup.write_text("# Skill Registry\n\n## Compact Rules\n\n", encoding="utf-8")
        reg_sha = sha256_file(live_registry_backup)

    skill_sha = ""
    if live_skill.is_dir():
        base_skill_backup = base_dir / "live-skill"
        if base_skill_backup.exists():
            shutil.rmtree(base_skill_backup)
        shutil.copytree(live_skill, base_skill_backup, symlinks=True)
        manifest_out = base_dir / "SKILL_MANIFEST"
        skill_sha = run_manifest_script(base_skill_backup, manifest_out)

    txn_data: Dict[str, Any] = {
        "run_id": staging.name,
        "skill_name": skill_name,
        "state": "INIT",
        "live_registry_path": str(live_reg.resolve()),
        "live_skill_path": str(live_skill.resolve()) if live_skill.exists() else "",
        "base_registry_sha256": reg_sha,
        "base_skill_tree_digest": skill_sha,
        "timestamp": live_registry_backup.stat().st_mtime
    }

    save_state_atomic(staging, txn_data)
    print(f"Initialized transaction '{txn_data['run_id']}' with state INIT")

def set_state(staging_dir: str | Path, new_state: str) -> None:
    staging = Path(staging_dir)
    txn_data = load_state(staging)
    txn_data["state"] = new_state
    save_state_atomic(staging, txn_data)
    print(f"Transaction '{txn_data['run_id']}' transitioned to {new_state}")

def check_toctou(staging_dir: str | Path) -> None:
    staging = Path(staging_dir)
    txn_data = load_state(staging)

    current_reg_sha = sha256_file(txn_data["live_registry_path"])
    if current_reg_sha != txn_data["base_registry_sha256"]:
        print(f"CONFLICT_BASE_CHANGED: Live registry SHA ({current_reg_sha}) drifted from base ({txn_data['base_registry_sha256']})", file=sys.stderr)
        sys.exit(2)

    live_skill_str = txn_data.get("live_skill_path")
    if live_skill_str and Path(live_skill_str).is_dir():
        temp_manifest = staging / "temp_manifest"
        current_skill_sha = run_manifest_script(Path(live_skill_str), temp_manifest)
        if current_skill_sha != txn_data["base_skill_tree_digest"]:
            print(f"CONFLICT_BASE_CHANGED: Live skill tree digest ({current_skill_sha}) drifted from base ({txn_data['base_skill_tree_digest']})", file=sys.stderr)
            sys.exit(3)

    print("TOCTOU Guard: Base integrity verified.")

def _restore_registry_component(
    staging: Path, txn: Dict[str, Any], expected_digest: str
) -> Dict[str, Any]:
    """Restores the live registry and verifies restored bytes against the frozen baseline.

    Source precedence: backup/live-registry.md first; if absent, base/live-registry.md
    (frozen by init_txn). Readback digest MUST equal the baseline digest or recovery fails.
    """
    live_reg_str = txn.get("live_registry_path")
    if not live_reg_str or expected_digest == "":
        return {"component": "registry", "status": "N/A", "reason": "no live registry recorded in transaction"}

    live_reg = Path(live_reg_str)
    sources = [staging / "backup" / "live-registry.md", staging / "base" / "live-registry.md"]
    source_used = next((s for s in sources if s.is_file()), None)

    if source_used is None:
        return {
            "component": "registry",
            "status": "FAILED",
            "reason": "no valid restore source found (backup/live-registry.md and base/live-registry.md both missing)",
            "expected_sha256": expected_digest,
        }

    live_reg.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source_used, live_reg)

    got_digest = sha256_file(live_reg)
    if got_digest != expected_digest:
        return {
            "component": "registry",
            "status": "FAILED",
            "reason": f"readback mismatch after restore from {source_used.name}/",
            "source": str(source_used),
            "expected_sha256": expected_digest,
            "got_sha256": got_digest,
        }
    return {
        "component": "registry",
        "status": "RESTORED",
        "source": str(source_used),
        "sha256_verified": got_digest,
    }


def _restore_skill_component(
    staging: Path, txn: Dict[str, Any], expected_digest: str
) -> Dict[str, Any]:
    """Restores the live skill tree and verifies its manifest digest against the frozen baseline.

    Source precedence: backup/live-skill first; if absent, base/live-skill (frozen by init_txn).
    """
    live_skill_str = txn.get("live_skill_path")
    if not live_skill_str:
        return {"component": "skill", "status": "N/A", "reason": "no live skill recorded in transaction"}
    if expected_digest == "":
        return {"component": "skill", "status": "N/A", "reason": "transaction froze no skill baseline"}

    live_skill = Path(live_skill_str)
    sources = [staging / "backup" / "live-skill", staging / "base" / "live-skill"]
    source_used = next((s for s in sources if s.is_dir()), None)

    if source_used is None:
        return {
            "component": "skill",
            "status": "FAILED",
            "reason": "no valid restore source found (backup/live-skill and base/live-skill both missing)",
            "expected_tree_digest": expected_digest,
        }

    if live_skill.exists():
        shutil.rmtree(live_skill)
    shutil.copytree(source_used, live_skill, symlinks=True)

    temp_manifest = staging / "temp_manifest_recovery"
    try:
        got_digest = run_manifest_script(live_skill, temp_manifest)
    finally:
        if temp_manifest.exists():
            temp_manifest.unlink()

    if got_digest != expected_digest:
        return {
            "component": "skill",
            "status": "FAILED",
            "reason": f"manifest readback mismatch after restore from {source_used.name}/",
            "source": str(source_used),
            "expected_tree_digest": expected_digest,
            "got_tree_digest": got_digest,
        }
    return {
        "component": "skill",
        "status": "RESTORED",
        "source": str(source_used),
        "tree_digest_verified": got_digest,
    }


def recover(staging_dir: str | Path) -> None:
    """Crash recovery that only claims success when bytes are verifiably restored.

    Order per contract:
      1. backup/live-* when present (valid restore source).
      2. If missing, base/live-* frozen by init_txn.
      3. Readback + exact digest comparison against the frozen baseline
         (base_registry_sha256 / base_skill_tree_digest in txn_state.json).
    Any missing source, copy failure, or digest mismatch => RECOVERY_FAILED,
    INTERVENTION_REQUIRED=true in state journal, exit code 8. Silent success is impossible.
    """
    staging = Path(staging_dir)
    state_file = staging / STATE_FILE
    if not state_file.is_file():
        print("No transaction found. Clean state.")
        return

    txn = load_state(staging)
    state = txn.get("state", "INIT")

    if state == "COMPLETE":
        print("Previous transaction was cleanly completed.")
        return
    if state in ["INIT", "PRECOMMIT"]:
        print(f"Transaction '{txn['run_id']}' stopped in {state}: no atomic swap performed, nothing to roll back.")
        return

    # Only SKILL_SWAPPED / REGISTRY_SWAPPED reach a compensating rollback.
    print(f"CRASH DETECTED in state {state}. Initiating verified compensating rollback...")

    components = [
        _restore_registry_component(staging, txn, txn.get("base_registry_sha256", "")),
        _restore_skill_component(staging, txn, txn.get("base_skill_tree_digest", "")),
    ]
    failed_components = [c for c in components if c["status"] == "FAILED"]

    txn["recovery"] = {
        "from_state": state,
        "components": components,
        "intervention_required": bool(failed_components),
    }

    if failed_components:
        txn["state"] = STATE_RECOVERY_FAILED
        save_state_atomic(staging, txn)
        for c in failed_components:
            print(f"RECOVERY_FAILED component={c['component']}: {c['reason']}", file=sys.stderr)
        print("INTERVENTION_REQUIRED: manual inspection of staging/live state required.", file=sys.stderr)
        sys.exit(EXIT_RECOVERY_FAILED)

    txn["state"] = STATE_ROLLED_BACK
    save_state_atomic(staging, txn)
    for c in components:
        print(f"Restored {c['component']} from {c['source']} (digest verified).")
    print("Recovery complete. Baseline bytes verified via exact digest readback.")

def main() -> None:
    parser = argparse.ArgumentParser(description="Transaction State Marker & Crash Recovery Manager")
    subparsers = parser.add_subparsers(dest="command", required=True)

    init_p = subparsers.add_parser("init")
    init_p.add_argument("staging_dir", help="Path to staging directory")
    init_p.add_argument("skill_name", help="Name of candidate skill")
    init_p.add_argument("live_registry_path", help="Path to live skill registry")
    init_p.add_argument("live_skill_path", help="Path to live skill directory")

    state_p = subparsers.add_parser("state")
    state_p.add_argument("staging_dir", help="Path to staging directory")
    state_p.add_argument("new_state", choices=["INIT", "PRECOMMIT", "SKILL_SWAPPED", "REGISTRY_SWAPPED", "COMPLETE", "ROLLED_BACK"], help="New transaction state")

    toctou_p = subparsers.add_parser("check_toctou")
    toctou_p.add_argument("staging_dir", help="Path to staging directory")

    lock_p = subparsers.add_parser("lock")
    lock_p.add_argument("--path", default=DEFAULT_LOCK_DIR, help="Lock directory path")
    lock_p.add_argument("--timeout", type=int, default=10, help="Lock timeout in seconds")

    unlock_p = subparsers.add_parser("unlock")
    unlock_p.add_argument("--path", default=DEFAULT_LOCK_DIR, help="Lock directory path")

    rec_p = subparsers.add_parser("recover")
    rec_p.add_argument("staging_dir", help="Path to staging directory")

    args = parser.parse_args()
    if args.command == "init":
        init_txn(args.staging_dir, args.skill_name, args.live_registry_path, args.live_skill_path)
    elif args.command == "state":
        set_state(args.staging_dir, args.new_state)
    elif args.command == "check_toctou":
        check_toctou(args.staging_dir)
    elif args.command == "lock":
        acquire_lock(args.path, args.timeout)
    elif args.command == "unlock":
        release_lock(args.path)
    elif args.command == "recover":
        recover(args.staging_dir)

if __name__ == "__main__":
    main()
