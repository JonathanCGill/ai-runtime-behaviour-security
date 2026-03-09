"""PACE Resilience Controller — structured degradation for AI systems.

PACE defines four operational states with clear transition triggers:

  PRIMARY     → All controls active, normal operation
  ALTERNATE   → One control degraded, backup active, scope tightened
  CONTINGENCY → Multiple controls degraded, human-in-the-loop for all
  EMERGENCY   → Confirmed compromise, circuit breaker fires, full stop

Transitions are one-directional during an incident (P→A→C→E).
Recovery requires explicit human authorization (E→C→A→P).
"""

from __future__ import annotations

import logging
import time
from typing import Any, Callable

from pydantic import BaseModel, Field

from airs.core.models import PACEState

logger = logging.getLogger(__name__)


class PACETransition(BaseModel):
    """Record of a PACE state transition."""

    from_state: PACEState
    to_state: PACEState
    reason: str
    timestamp: float = Field(default_factory=time.time)
    authorized_by: str = "system"  # "system" for automatic, user ID for manual


class PACEPolicy(BaseModel):
    """Policy governing PACE state behavior."""

    # What changes at each level
    primary: dict[str, Any] = Field(default_factory=lambda: {
        "judge_mode": "sampling",       # sample % of requests
        "judge_sample_rate": 0.05,      # 5% sampling
        "human_approval_required": False,
        "max_autonomy": "full",
    })
    alternate: dict[str, Any] = Field(default_factory=lambda: {
        "judge_mode": "all",            # judge every request
        "judge_sample_rate": 1.0,
        "human_approval_required": False,
        "max_autonomy": "reduced",      # no new tool access
    })
    contingency: dict[str, Any] = Field(default_factory=lambda: {
        "judge_mode": "all",
        "judge_sample_rate": 1.0,
        "human_approval_required": True,  # human approves all
        "max_autonomy": "minimal",       # read-only
    })
    emergency: dict[str, Any] = Field(default_factory=lambda: {
        "judge_mode": "disabled",       # AI is off
        "judge_sample_rate": 0.0,
        "human_approval_required": True,
        "max_autonomy": "none",         # circuit breaker active
    })


class PACEController:
    """Manages PACE state transitions and enforces degradation policy.

    Usage:
        pace = PACEController()

        # Automatic escalation on failures
        pace.escalate("Judge service timeout")

        # Check current policy
        policy = pace.current_policy()
        if policy["human_approval_required"]:
            await queue_for_human_review(request)

        # Manual recovery (requires authorization)
        pace.recover(authorized_by="admin@company.com")
    """

    # Degradation order
    _ORDER = [PACEState.PRIMARY, PACEState.ALTERNATE, PACEState.CONTINGENCY, PACEState.EMERGENCY]

    def __init__(
        self,
        policy: PACEPolicy | None = None,
        on_transition: Callable[[PACETransition], None] | None = None,
    ) -> None:
        self._policy = policy or PACEPolicy()
        self._on_transition = on_transition
        self._state = PACEState.PRIMARY
        self._history: list[PACETransition] = []

    @property
    def state(self) -> PACEState:
        return self._state

    @property
    def history(self) -> list[PACETransition]:
        return list(self._history)

    def current_policy(self) -> dict[str, Any]:
        """Return the active policy for the current PACE state."""
        policies = {
            PACEState.PRIMARY: self._policy.primary,
            PACEState.ALTERNATE: self._policy.alternate,
            PACEState.CONTINGENCY: self._policy.contingency,
            PACEState.EMERGENCY: self._policy.emergency,
        }
        return dict(policies[self._state])

    def escalate(self, reason: str = "") -> PACEState:
        """Move one level toward EMERGENCY.

        P → A → C → E. Cannot go past EMERGENCY.
        """
        idx = self._ORDER.index(self._state)
        if idx >= len(self._ORDER) - 1:
            logger.warning("Already at EMERGENCY — cannot escalate further")
            return self._state

        new_state = self._ORDER[idx + 1]
        self._transition(new_state, reason, authorized_by="system")
        return new_state

    def emergency(self, reason: str = "") -> None:
        """Jump directly to EMERGENCY state (e.g., confirmed breach)."""
        if self._state != PACEState.EMERGENCY:
            self._transition(PACEState.EMERGENCY, reason or "Emergency triggered", "system")

    def recover(self, authorized_by: str = "", reason: str = "") -> PACEState:
        """Move one level toward PRIMARY. Requires human authorization.

        E → C → A → P.
        """
        if not authorized_by:
            raise ValueError("Recovery requires authorized_by (human identifier)")

        idx = self._ORDER.index(self._state)
        if idx <= 0:
            logger.info("Already at PRIMARY — fully recovered")
            return self._state

        new_state = self._ORDER[idx - 1]
        self._transition(
            new_state,
            reason or "Recovery authorized",
            authorized_by=authorized_by,
        )
        return new_state

    def full_recovery(self, authorized_by: str = "") -> None:
        """Return to PRIMARY state. Requires authorization."""
        if not authorized_by:
            raise ValueError("Full recovery requires authorized_by (human identifier)")
        if self._state != PACEState.PRIMARY:
            self._transition(
                PACEState.PRIMARY,
                "Full recovery authorized",
                authorized_by=authorized_by,
            )

    def should_judge(self) -> bool:
        """Whether the judge should evaluate this request given current PACE state."""
        policy = self.current_policy()
        mode = policy.get("judge_mode", "sampling")
        if mode == "disabled":
            return False
        if mode == "all":
            return True
        # sampling mode
        import random
        rate = policy.get("judge_sample_rate", 0.05)
        return random.random() < rate

    def requires_human_approval(self) -> bool:
        return self.current_policy().get("human_approval_required", False)

    def _transition(self, new_state: PACEState, reason: str, authorized_by: str) -> None:
        transition = PACETransition(
            from_state=self._state,
            to_state=new_state,
            reason=reason,
            authorized_by=authorized_by,
        )
        old = self._state
        self._state = new_state
        self._history.append(transition)

        logger.info(
            "PACE %s → %s (reason: %s, by: %s)",
            old.value, new_state.value, reason, authorized_by,
        )

        if self._on_transition:
            self._on_transition(transition)
