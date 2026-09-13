"""Regression tests for skill-onboarding: ONB-001, ONB-002, ONB-003."""

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path
import pytest

SCRIPTS_DIR = Path(__file__).resolve().parent.parent / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

import txn_manager


def test_candidate_missing_skill_md_fails_preflight(tmp_path):
    """ONB-001: verify_candidate.py must fail non-zero if candidate_dir/SKILL.md is missing."""
    candidate_dir = tmp_path / "candidate"
    candidate_dir.mkdir()
    # Notice: SKILL.md is NOT created in candidate_dir

    overlay_path = tmp_path / "overlay.md"
    overlay_path.write_text("### test-skill\nTest description for test-skill.", encoding="utf-8")

    fixtures_path = tmp_path / "fixtures.json"
    fixtures_data = {
        "fixtures": [
            {"query": "test skill query one", "expected_result": "SHOULD_TRIGGER", "type": "SHOULD_TRIGGER"},
            {"query": "completely unrelated query", "expected_result": "MUST_NOT_TRIGGER", "type": "MUST_NOT"},
            {"query": "another unrelated query", "expected_result": "MUST_NOT_TRIGGER", "type": "MUST_NOT"},
        ]
    }
    fixtures_path.write_text(json.dumps(fixtures_data), encoding="utf-8")

    receipt_out = tmp_path / "receipt.json"

    # Invoke verify_candidate.py
    proc = subprocess.run(
        [
            sys.executable,
            str(SCRIPTS_DIR / "verify_candidate.py"),
            str(candidate_dir),
            str(overlay_path),
            str(fixtures_path),
            "test-skill",
            "read-only",
            str(receipt_out),
        ],
        capture_output=True,
        text=True,
    )

    assert proc.returncode != 0, "Verifier must fail non-zero when candidate SKILL.md is missing"
    assert "SKILL.md missing" in proc.stderr or "PREFLIGHT FAIL" in proc.stderr


def test_toctou_detects_existence_drift(tmp_path):
    """ONB-002: check_toctou must detect if skill did not exist at init but was created before commit."""
    staging_dir = tmp_path / "staging"
    live_reg = tmp_path / "live-registry.md"
    live_reg.write_text("# Registry\n", encoding="utf-8")
    live_skill = tmp_path / "skills" / "drift-skill"
    # Skill does NOT exist at init
    assert not live_skill.exists()

    txn_manager.init_txn(
        staging_dir=staging_dir,
        skill_name="drift-skill",
        live_registry_path=live_reg,
        live_skill_path=live_skill,
    )

    # State file must record initial existence
    state = txn_manager.load_state(staging_dir)
    assert "skill_existed_initially" in state
    assert state["skill_existed_initially"] is False

    # Simulate drift: someone created the skill in between
    live_skill.mkdir(parents=True)
    (live_skill / "SKILL.md").write_text("# Sneaky Skill\n", encoding="utf-8")

    # check_toctou must fail with exit code 3 or error
    with pytest.raises(SystemExit) as exc_info:
        txn_manager.check_toctou(staging_dir)
    assert exc_info.value.code == 3


def test_recover_restores_live_skill_when_crashed_during_precommit(tmp_path):
    """ONB-003: recover() must restore live-skill if crash occurred in PRECOMMIT after moving live-skill to backup."""
    staging_dir = tmp_path / "staging"
    live_reg = tmp_path / "live-registry.md"
    live_reg.write_text("# Registry\n", encoding="utf-8")
    live_skill = tmp_path / "skills" / "live-skill"
    live_skill.mkdir(parents=True)
    original_skill_content = "# Original Live Skill Content\n"
    (live_skill / "SKILL.md").write_text(original_skill_content, encoding="utf-8")

    txn_manager.init_txn(
        staging_dir=staging_dir,
        skill_name="live-skill",
        live_registry_path=live_reg,
        live_skill_path=live_skill,
    )

    # Simulate Step B & C in runbook: transition to PRECOMMIT, move live skill to backup
    txn_manager.set_state(staging_dir, "PRECOMMIT")
    backup_dir = staging_dir / "backup"
    backup_dir.mkdir(parents=True, exist_ok=True)
    shutil.move(str(live_skill), str(backup_dir / "live-skill"))

    # Live skill is now gone from disk!
    assert not live_skill.exists()

    # Now simulate crash recovery
    txn_manager.recover(staging_dir)

    # Live skill must be restored on disk and match original content
    assert live_skill.exists(), "Live skill must be restored on disk after crash in PRECOMMIT"
    assert (live_skill / "SKILL.md").read_text(encoding="utf-8") == original_skill_content
