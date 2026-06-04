"""
Unit tests for the error-handling and resilience layer:
  - Retry with exponential backoff
  - Fallback chains
  - Circuit breaker
"""

import pytest
import time
from unittest.mock import MagicMock, patch

from agent.error_handler import retry_with_backoff, random_failure
from agent.fallback_chains import execute_with_fallbacks, FALLBACK_CHAINS
from agent.circuit_breaker import CircuitBreaker


class TestRetryWithBackoff:
    def test_succeeds_on_first_attempt(self):
        call_count = 0

        @retry_with_backoff(retries=3, base_delay=0.01)
        def flaky():
            nonlocal call_count
            call_count += 1
            return "ok"

        result = flaky()
        assert result == "ok"
        assert call_count == 1

    def test_retries_on_failure_and_returns_error_dict(self):
        call_count = 0

        @retry_with_backoff(retries=3, base_delay=0.001)
        def always_fail():
            nonlocal call_count
            call_count += 1
            raise ValueError("boom")

        result = always_fail()
        assert call_count == 3
        assert isinstance(result, dict)
        assert "error" in result

    def test_succeeds_after_transient_failures(self):
        call_count = 0

        @retry_with_backoff(retries=3, base_delay=0.001)
        def flaky_then_ok():
            nonlocal call_count
            call_count += 1
            if call_count < 3:
                raise ConnectionError("transient")
            return "recovered"

        result = flaky_then_ok()
        assert result == "recovered"
        assert call_count == 3


class TestRandomFailure:
    def test_always_fails_with_rate_1(self):
        @random_failure(failure_rate=1.0)
        def tool():
            return "should not reach"

        with pytest.raises(Exception):
            tool()

    def test_never_fails_with_rate_0(self):
        @random_failure(failure_rate=0.0)
        def tool():
            return "success"

        assert tool() == "success"


class TestFallbackChains:
    def test_all_primary_tools_have_fallbacks(self):
        primary_tools = [
            "financial_data_api", "sec_filing_search", "earnings_transcript",
            "web_search", "peer_comparison", "calculation_engine",
            "news_sentiment", "company_profile", "fact_checker",
        ]
        for tool in primary_tools:
            assert tool in FALLBACK_CHAINS, f"No fallback chain for '{tool}'"
            assert len(FALLBACK_CHAINS[tool]) >= 2, (
                f"Tool '{tool}' needs at least 2 fallback options, "
                f"got {len(FALLBACK_CHAINS[tool])}"
            )

    def test_execute_with_fallbacks_succeeds(self):
        mock_fn = MagicMock(return_value={"data": "mock"})
        mock_fn.__name__ = "mock_fn"
        with patch.dict(
            "agent.fallback_chains.FALLBACK_CHAINS",
            {"mock_tool": [mock_fn]}
        ):
            result = execute_with_fallbacks("mock_tool", "AAPL")
        assert result["success"] is True
        assert result["tool_used"] == "mock_fn"

    def test_execute_with_fallbacks_returns_failure_when_all_fail(self):
        def fail(_):
            raise RuntimeError("always fails")

        with patch.dict(
            "agent.fallback_chains.FALLBACK_CHAINS",
            {"bad_tool": [fail, fail]}
        ):
            result = execute_with_fallbacks("bad_tool", "AAPL")
        assert result["success"] is False
        assert "error" in result

    def test_execute_unknown_tool_returns_failure(self):
        result = execute_with_fallbacks("nonexistent_tool_xyz", "AAPL")
        assert result["success"] is False


class TestCircuitBreaker:
    def test_closed_state_allows_calls(self):
        breaker = CircuitBreaker(failure_threshold=3, recovery_timeout=10)
        result = breaker.call(lambda: "ok")
        assert result == "ok"

    def test_opens_after_threshold_failures(self):
        breaker = CircuitBreaker(failure_threshold=2, recovery_timeout=60)

        def fail():
            raise Exception("boom")

        breaker.call(fail)
        breaker.call(fail)
        assert breaker.state == "OPEN"

    def test_open_circuit_returns_error_dict(self):
        breaker = CircuitBreaker(failure_threshold=1, recovery_timeout=60)

        def fail():
            raise Exception("boom")

        breaker.call(fail)
        result = breaker.call(lambda: "should not run")
        assert isinstance(result, dict)
        assert "error" in result

    def test_half_open_after_recovery_timeout(self):
        breaker = CircuitBreaker(failure_threshold=1, recovery_timeout=0)

        def fail():
            raise Exception("boom")

        breaker.call(fail)
        assert breaker.state == "OPEN"
        time.sleep(0.05)
        assert breaker.allow_request() is True

    def test_records_success_resets_count(self):
        breaker = CircuitBreaker(failure_threshold=3, recovery_timeout=10)
        breaker.record_failure()
        breaker.record_success()
        assert breaker.failure_count == 0
        assert breaker.state == "CLOSED"
