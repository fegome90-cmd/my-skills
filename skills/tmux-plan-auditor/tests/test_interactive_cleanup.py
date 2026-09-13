"""Tests for interactive session cleanup and absence readback in tmux-plan-auditor."""

from pathlib import Path
import re
import pytest

from resources.handoff_builder import HandoffBuilder


def test_script_invokes_kill_session_and_verifies_absence():
    """Verify that run_tmux_plan_audit.sh invokes kill-session and checks absence before unsetting trap and passing CLEANUP_FLAG."""
    script_path = Path(__file__).resolve().parent.parent / "scripts" / "run_tmux_plan_audit.sh"
    content = script_path.read_text(encoding="utf-8")

    # Locate the auto-cleanup section after wait_for_agents
    wait_pos = content.find("wait_for_agents")
    assert wait_pos != -1, "wait_for_agents not found"
    post_wait_section = content[wait_pos:]

    # In the post-wait auto-cleanup section, tmux kill-session must be invoked
    assert 'tmux kill-session -t "$SESSION_TARGET"' in post_wait_section, (
        "Post-wait auto-cleanup must invoke tmux kill-session"
    )

    # Absence must be verified in post-wait section before unsetting trap
    assert 'tmux has-session -t "$SESSION_TARGET"' in post_wait_section, (
        "Post-wait auto-cleanup must verify absence via tmux has-session"
    )

    kill_idx = post_wait_section.find('tmux kill-session -t "$SESSION_TARGET"')
    has_idx = post_wait_section.find('tmux has-session -t "$SESSION_TARGET"')
    trap_unset_idx = post_wait_section.find('trap - EXIT INT TERM')
    builder_idx = post_wait_section.find('handoff_builder.py')

    assert kill_idx != -1 and has_idx != -1 and trap_unset_idx != -1 and builder_idx != -1
    # kill must occur before has-session check
    assert kill_idx < has_idx, "kill-session must occur before absence check"
    # absence check must occur before handoff builder call so verified flag is recorded
    assert has_idx < builder_idx, "absence check must occur before handoff_builder call"
    # trap unset must occur after kill
    assert kill_idx < trap_unset_idx, "trap unset must occur after kill-session"


def test_handoff_builder_records_session_cleanup_flag():
    """Verify handoff builder accurately sets session_cleaned_up in execution summary."""
    builder = HandoffBuilder(
        run_dir="/tmp/test_cleanup_run",
        run_id="test-cleanup-1",
        session_name="plan-audit-test",
        plan_path="/tmp/plan.md",
    )

    handoff_true, _ = builder.build(session_cleaned_up=True)
    assert handoff_true["execution_summary"]["session_cleaned_up"] is True

    handoff_false, _ = builder.build(session_cleaned_up=False)
    assert handoff_false["execution_summary"]["session_cleaned_up"] is False
