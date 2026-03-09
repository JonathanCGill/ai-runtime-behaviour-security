"""Tests for the Circuit Breaker."""

from airs.runtime.circuit_breaker import CircuitBreaker, CircuitBreakerConfig, CircuitState


class TestCircuitBreaker:
    def test_starts_closed(self):
        cb = CircuitBreaker()
        assert cb.state == CircuitState.CLOSED

    def test_allows_requests_when_closed(self):
        cb = CircuitBreaker()
        assert cb.allow_request()

    def test_trips_after_threshold(self):
        cb = CircuitBreaker(config=CircuitBreakerConfig(failure_threshold=3))
        cb.record_failure("test")
        cb.record_failure("test")
        cb.record_failure("test")
        assert cb.state == CircuitState.OPEN

    def test_blocks_when_open(self):
        cb = CircuitBreaker(config=CircuitBreakerConfig(failure_threshold=2))
        cb.record_failure("test")
        cb.record_failure("test")
        assert not cb.allow_request()

    def test_manual_trip(self):
        cb = CircuitBreaker()
        cb.trip("emergency")
        assert cb.state == CircuitState.OPEN
        assert not cb.allow_request()

    def test_manual_reset(self):
        cb = CircuitBreaker()
        cb.trip("test")
        cb.reset()
        assert cb.state == CircuitState.CLOSED
        assert cb.allow_request()

    def test_state_change_callback(self):
        transitions = []
        cb = CircuitBreaker(
            config=CircuitBreakerConfig(failure_threshold=2),
            on_state_change=lambda old, new: transitions.append((old, new)),
        )
        cb.record_failure("test")
        cb.record_failure("test")
        assert len(transitions) == 1
        assert transitions[0] == (CircuitState.CLOSED, CircuitState.OPEN)

    def test_stats(self):
        cb = CircuitBreaker()
        cb.record_success()
        cb.record_failure("test")
        stats = cb.stats()
        assert stats["total_events"] == 2
        assert stats["failures"] == 1
        assert stats["state"] == "closed"

    def test_success_doesnt_trip(self):
        cb = CircuitBreaker(config=CircuitBreakerConfig(failure_threshold=3))
        cb.record_success()
        cb.record_success()
        cb.record_failure("test")
        cb.record_success()
        assert cb.state == CircuitState.CLOSED
