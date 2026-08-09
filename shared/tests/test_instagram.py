"""Tests for the shared Instagram Graph API HTTP layer."""

from __future__ import annotations

from email.message import Message
import io
import json
import urllib.error

import pytest

from acps_shared import instagram


class FakeResponse:
    """Small urlopen response double."""

    def __init__(self, payload: object, headers: dict[str, str] | None = None) -> None:
        self.body = json.dumps(payload).encode()
        self.headers = headers or {}
        self.status = 200
        self.closed = False

    def read(self) -> bytes:
        return self.body

    def close(self) -> None:
        self.closed = True


def _http_error(status: int, payload: object, headers: dict[str, str] | None = None):
    message = Message()
    for key, value in (headers or {}).items():
        message[key] = value
    return urllib.error.HTTPError(
        "https://example.invalid",
        status,
        "failed",
        message,
        io.BytesIO(json.dumps(payload).encode()),
    )


def test_get_json_normalizes_headers_and_parses_both_usage_forms() -> None:
    """X-App-Usage accepts observed key variants without a fixed schema."""
    usages = [
        {"call_count": 10, "total_cputime": 20, "total_time": 30},
        {"call_volume": 40, "cpu_time": 50},
    ]
    for usage in usages:
        response = instagram.get_json(
            "/1",
            {"fields": "id", "unused": None},
            urlopen=lambda *args, usage=usage, **kwargs: FakeResponse(
                {"id": "1"}, {"X-App-Usage": json.dumps(usage)}
            ),
        )
        assert response.app_usage == usage
        assert "x-app-usage" in response.headers


@pytest.mark.parametrize(
    ("status", "payload", "expected"),
    [
        (429, {"error": {"message": "busy"}}, instagram.InstagramRateLimited),
        (400, {"error": {"code": 4, "message": "busy"}}, instagram.InstagramRateLimited),
        (
            400,
            {"error": {"code": 100, "error_subcode": 33, "message": "bad"}},
            instagram.InstagramObjectUnavailable,
        ),
        (
            400,
            {"error": {"code": 100, "message": "Invalid metric"}},
            instagram.InstagramInvalidMetric,
        ),
    ],
)
def test_get_json_classifies_graph_errors(status, payload, expected) -> None:
    """HTTP and Graph fields select the stable exception hierarchy."""
    with pytest.raises(expected) as caught:
        instagram.get_json(
            "/1",
            {"access_token": "secret-token"},
            urlopen=lambda *args, **kwargs: (_ for _ in ()).throw(
                _http_error(status, payload)
            ),
        )
    assert "secret-token" not in str(caught.value)
    assert "secret-token" not in repr(caught.value.response)


def test_get_json_wraps_transport_and_invalid_json() -> None:
    """Network and JSON decoding failures use InstagramTransportError."""
    with pytest.raises(instagram.InstagramTransportError):
        instagram.get_json(
            "/1",
            {},
            urlopen=lambda *args, **kwargs: (_ for _ in ()).throw(
                urllib.error.URLError("offline")
            ),
        )
    bad_response = FakeResponse({})
    bad_response.body = b"not-json"
    with pytest.raises(instagram.InstagramTransportError):
        instagram.get_json("/1", {}, urlopen=lambda *args, **kwargs: bad_response)


def test_rate_limit_guard_retries_with_backoff(monkeypatch) -> None:
    """Retryable failures sleep three times before a fourth success."""
    sleeps: list[float] = []
    attempts = 0
    monkeypatch.setattr(instagram.random, "uniform", lambda low, high: 1.0)

    def request() -> instagram.GraphResponse:
        nonlocal attempts
        attempts += 1
        if attempts < 4:
            raise instagram.InstagramRateLimited("busy", status=429)
        return instagram.GraphResponse({}, {}, None)

    result = instagram.RateLimitGuard(sleep=sleeps.append).call(request)
    assert result.payload == {}
    assert attempts == 4
    assert sleeps == [5.0, 15.0, 45.0]


def test_rate_limit_guard_uses_proactive_and_business_usage_delays() -> None:
    """High prior usage and business regain estimates take precedence."""
    sleeps: list[float] = []
    guard = instagram.RateLimitGuard(sleep=sleeps.append)
    guard.call(
        lambda: instagram.GraphResponse(
            {}, {}, {"call_volume": 91, "cpu_time": 3}
        )
    )
    attempts = 0

    def request() -> instagram.GraphResponse:
        nonlocal attempts
        attempts += 1
        if attempts == 1:
            raise instagram.InstagramRateLimited(
                "busy",
                headers={
                    "x-business-use-case-usage": json.dumps(
                        {"1": [{"estimated_time_to_regain_access": 9}]}
                    )
                },
            )
        return instagram.GraphResponse({}, {}, None)

    guard.call(request)
    assert sleeps == [60.0, 300.0]


def test_rate_limit_guard_reraises_after_attempt_limit() -> None:
    """The final retryable exception is preserved when attempts are exhausted."""
    sleeps: list[float] = []
    error = instagram.InstagramTransportError("offline")
    with pytest.raises(instagram.InstagramTransportError) as caught:
        instagram.RateLimitGuard(sleep=sleeps.append, max_attempts=2).call(
            lambda: (_ for _ in ()).throw(error)
        )
    assert caught.value is error
    assert len(sleeps) == 1
