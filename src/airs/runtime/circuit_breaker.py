"""Circuit Breaker — the emergency stop for AI systems.

When controls fail, the circuit breaker fires. All AI traffic stops.
A non-AI fallback takes over. This is the last line of defense.

States:
  CLOSED  → Normal operation, AI traffic flows
  OPEN    → AI traffic blocked, fallback active
  HALF    → Testing recovery, limited AI traffic allowed
"""

from __future__ import annotations

import logging
import threading
import time
from collections import deque
from enum import Enum
from typing import Any, Callable

from pydantic import BaseModel

logger = logging.getLogger(__name__)


class CircuitState(str, Enum):
    CLOSED = "closed"    # Normal — AI active
    OPEN = "open"        # Tripped — fallback active
    HALF_OPEN = "half_open"  # Recovery test — limited traffic


class CircuitBreakerConfig(BaseModel):
    """Configuration for the circuit breaker."""

    failure_threshold: int = 5           # failures before tripping
    window_seconds: float = 60.0         # sliding window for failure count
    recovery_timeout: float = 300.0      # seconds before attempting recovery
    half_open_max_requests: int = 3      # test requests during half-open
    block_rate_threshold: float = 0.20   # trip if >20% of requests blocked


class CircuitBreaker:
    """Circuit breaker for AI systems.

    Monitors guardrail block rates and explicit failures.
    Trips to OPEN (fallback mode) when thresholds are exceeded.
    Automatically tests recovery after timeout.

    Usage:
        breaker = CircuitBreaker()

        if breaker.allow_request():
            response = call_ai_model(input)
            breaker.record_success()
        else:
            response = fallback_response()

        # Or record a failure:
        breaker.record_failure("guardrail_block")
    """

    def __init__(
        self,
        config: CircuitBreakerConfig | None = None,
        on_state_change: Callable[[CircuitState, CircuitState], None] | None = None,
        fallback: Callable[..., Any] | None = None,
    ) -> None:
        self._config = config or CircuitBreakerConfig()
        self._on_state_change = on_state_change
        self._fallback = fallback

        self._state = CircuitState.CLOSED
        self._lock = threading.Lock()

        # Sliding window of (timestamp, is_failure) tuples
        self._events: deque[tuple[float, bool]] = deque()
        self._last_failure_time: float = 0.0
        self._half_open_successes: int = 0

    @property
    def state(self) -> CircuitState:
        with self._lock:
            self._check_recovery()
            return self._state

    def allow_request(self) -> bool:
        """Check if a request should be allowed through."""
        with self._lock:
            self._check_recovery()

            if self._state == CircuitState.CLOSED:
                return True
            elif self._state == CircuitState.HALF_OPEN:
                return self._half_open_successes < self._config.half_open_max_requests
            else:
                return False

    def record_success(self) -> None:
        """Record a successful AI request."""
        with self._lock:
            now = time.monotonic()
            self._events.append((now, False))
            self._trim_window(now)

            if self._state == CircuitState.HALF_OPEN:
                self._half_open_successes += 1
                if self._half_open_successes >= self._config.half_open_max_requests:
                    self._transition(CircuitState.CLOSED)
                    self._half_open_successes = 0

    def record_failure(self, reason: str = "") -> None:
        """Record a failed or blocked AI request."""
        with self._lock:
            now = time.monotonic()
            self._events.append((now, True))
            self._last_failure_time = now
            self._trim_window(now)

            if self._state == CircuitState.HALF_OPEN:
                # Any failure during half-open → back to open
                self._transition(CircuitState.OPEN)
                self._half_open_successes = 0
                logger.warning("Circuit breaker re-opened during recovery test: %s", reason)
                return

            # Check if we should trip
            failures = sum(1 for _, is_fail in self._events if is_fail)
            total = len(self._events)

            should_trip = (
                failures >= self._config.failure_threshold
                or (
                    total >= 10
                    and failures / total > self._config.block_rate_threshold
                )
            )

            if should_trip and self._state == CircuitState.CLOSED:
                self._transition(CircuitState.OPEN)
                logger.warning(
                    "Circuit breaker TRIPPED: %d failures in %d requests. Reason: %s",
                    failures, total, reason,
                )

    def trip(self, reason: str = "manual") -> None:
        """Manually trip the circuit breaker (emergency stop)."""
        with self._lock:
            if self._state != CircuitState.OPEN:
                self._transition(CircuitState.OPEN)
                self._last_failure_time = time.monotonic()
                logger.warning("Circuit breaker manually tripped: %s", reason)

    def reset(self) -> None:
        """Manually reset the circuit breaker."""
        with self._lock:
            self._transition(CircuitState.CLOSED)
            self._events.clear()
            self._half_open_successes = 0
            logger.info("Circuit breaker manually reset")

    def get_fallback(self) -> Callable[..., Any] | None:
        return self._fallback

    def stats(self) -> dict[str, Any]:
        """Return current circuit breaker statistics."""
        with self._lock:
            now = time.monotonic()
            self._trim_window(now)
            failures = sum(1 for _, is_fail in self._events if is_fail)
            total = len(self._events)
            return {
                "state": self._state.value,
                "total_events": total,
                "failures": failures,
                "failure_rate": failures / total if total > 0 else 0.0,
                "threshold": self._config.failure_threshold,
                "block_rate_threshold": self._config.block_rate_threshold,
            }

    def _check_recovery(self) -> None:
        """Transition from OPEN → HALF_OPEN after recovery timeout."""
        if self._state == CircuitState.OPEN:
            elapsed = time.monotonic() - self._last_failure_time
            if elapsed >= self._config.recovery_timeout:
                self._transition(CircuitState.HALF_OPEN)
                self._half_open_successes = 0
                logger.info("Circuit breaker entering recovery test (half-open)")

    def _transition(self, new_state: CircuitState) -> None:
        old_state = self._state
        self._state = new_state
        if self._on_state_change and old_state != new_state:
            self._on_state_change(old_state, new_state)

    def _trim_window(self, now: float) -> None:
        cutoff = now - self._config.window_seconds
        while self._events and self._events[0][0] < cutoff:
            self._events.popleft()
