"""Tests for handoff builder validation."""

import pytest

from resources.handoff_builder import HandoffBuilder


@pytest.fixture
def builder():
    return HandoffBuilder(
        run_dir="/tmp/test",
        run_id="test-1",
        session_name="test",
        plan_path="/tmp/plan.md",
        plan_domain="generic",
    )


class TestPayloadValidation:
    def test_valid_payload_passes(self, builder):
        data = {
            "agent": "logic",
            "status": "completed",
            "findings": [],
            "duration_ms": 100,
        }
        result = builder._validate_agent_payload(data, "logic")
        assert result["status"] == "completed"

    def test_missing_keys_normalized(self, builder):
        data = {"agent": "logic"}
        result = builder._validate_agent_payload(data, "logic")
        assert result["status"] == "invalid"
        assert "Missing keys" in result["error"]

    def test_findings_wrong_type_fixed(self, builder):
        data = {
            "agent": "logic",
            "status": "completed",
            "findings": "not a list",
        }
        result = builder._validate_agent_payload(data, "logic")
        assert result["findings"] == []
