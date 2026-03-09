"""Tests for the PACE resilience controller."""

import pytest

from airs.core.models import PACEState
from airs.runtime.pace import PACEController, PACETransition


class TestPACEController:
    def test_starts_at_primary(self):
        pace = PACEController()
        assert pace.state == PACEState.PRIMARY

    def test_escalate_one_level(self):
        pace = PACEController()
        new = pace.escalate("test failure")
        assert new == PACEState.ALTERNATE
        assert pace.state == PACEState.ALTERNATE

    def test_escalate_to_emergency(self):
        pace = PACEController()
        pace.escalate("failure 1")
        pace.escalate("failure 2")
        pace.escalate("failure 3")
        assert pace.state == PACEState.EMERGENCY

    def test_cannot_escalate_past_emergency(self):
        pace = PACEController()
        pace.emergency("breach")
        result = pace.escalate("more")
        assert result == PACEState.EMERGENCY

    def test_emergency_jumps_directly(self):
        pace = PACEController()
        pace.emergency("confirmed breach")
        assert pace.state == PACEState.EMERGENCY

    def test_recovery_requires_authorization(self):
        pace = PACEController()
        pace.escalate("test")
        with pytest.raises(ValueError, match="authorized_by"):
            pace.recover()

    def test_recovery_steps_down(self):
        pace = PACEController()
        pace.emergency("test")
        pace.recover(authorized_by="admin@test.com")
        assert pace.state == PACEState.CONTINGENCY
        pace.recover(authorized_by="admin@test.com")
        assert pace.state == PACEState.ALTERNATE
        pace.recover(authorized_by="admin@test.com")
        assert pace.state == PACEState.PRIMARY

    def test_full_recovery(self):
        pace = PACEController()
        pace.emergency("test")
        pace.full_recovery(authorized_by="admin@test.com")
        assert pace.state == PACEState.PRIMARY

    def test_history_recorded(self):
        pace = PACEController()
        pace.escalate("issue 1")
        pace.escalate("issue 2")
        assert len(pace.history) == 2
        assert pace.history[0].from_state == PACEState.PRIMARY
        assert pace.history[0].to_state == PACEState.ALTERNATE

    def test_transition_callback(self):
        transitions: list[PACETransition] = []
        pace = PACEController(on_transition=transitions.append)
        pace.escalate("test")
        assert len(transitions) == 1
        assert transitions[0].reason == "test"

    def test_policy_changes_with_state(self):
        pace = PACEController()
        assert pace.current_policy()["human_approval_required"] is False

        pace.escalate("test")
        pace.escalate("test")  # contingency
        assert pace.requires_human_approval()

    def test_judge_sampling_at_primary(self):
        pace = PACEController()
        policy = pace.current_policy()
        assert policy["judge_mode"] == "sampling"
        assert policy["judge_sample_rate"] == 0.05

    def test_judge_all_at_alternate(self):
        pace = PACEController()
        pace.escalate("test")
        policy = pace.current_policy()
        assert policy["judge_mode"] == "all"
