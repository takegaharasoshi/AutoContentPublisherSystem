"""Tests for the scheduled Instagram token refresh handler."""

from __future__ import annotations

import io
import json
import logging
from datetime import datetime, timezone
from urllib import error, parse

import pytest

from app import secrets
from app import token_refresh_handler


SECRET_ARN = "arn:aws:secretsmanager:ap-northeast-1:123456789012:secret:test"
OLD_TOKEN = "old-token+/with-sensitive-value"
FIXED_NOW = datetime(2026, 10, 11, 1, 2, 3, tzinfo=timezone.utc)


class FakeSecretsManager:
    """Keep the Secrets Manager read and write calls for assertions."""

    def __init__(self, secret: dict, put_error: Exception | None = None) -> None:
        self.secret = secret
        self.put_error = put_error
        self.put_calls: list[dict] = []

    def get_secret_value(self, **kwargs: str) -> dict[str, str]:
        assert kwargs == {"SecretId": SECRET_ARN}
        return {"SecretString": json.dumps(self.secret, ensure_ascii=False)}

    def put_secret_value(self, **kwargs: str) -> dict[str, str]:
        self.put_calls.append(kwargs)
        if self.put_error:
            raise self.put_error
        return {}


class FakeResponse:
    """Provide the context manager interface used by urllib responses."""

    def __init__(self, payload: dict) -> None:
        self.body = json.dumps(payload).encode("utf-8")

    def __enter__(self) -> FakeResponse:
        return self

    def __exit__(self, *_args: object) -> None:
        return None

    def read(self) -> bytes:
        return self.body


def make_secret(**overrides: object) -> dict:
    secret = {
        "ig_access_token": OLD_TOKEN,
        "app_secret": "app-secret",
        "verify_token": "verify-token",
        "unknown_object": {"enabled": True, "count": 3},
        "unknown_number": 42,
    }
    secret.update(overrides)
    return secret


def test_refresh_token_updates_only_token_fields_and_logs_safe_result(
    monkeypatch: pytest.MonkeyPatch, caplog: pytest.LogCaptureFixture,
) -> None:
    secret = make_secret()
    client = FakeSecretsManager(secret)
    requests: list[tuple[str, float]] = []

    def fake_urlopen(req, *, timeout: float) -> FakeResponse:
        requests.append((req.full_url, timeout))
        return FakeResponse({"access_token": "new-token", "expires_in": 3600})

    cache_before = dict(secrets._cache)
    monkeypatch.setattr(token_refresh_handler.request, "urlopen", fake_urlopen)
    caplog.set_level(logging.INFO, logger=token_refresh_handler.__name__)

    result = token_refresh_handler.refresh_token(
        SECRET_ARN, client=client, now=lambda: FIXED_NOW,
    )

    expected_expiry = "2026-10-11T02:02:03Z"
    assert result == {"token_expires_at": expected_expiry, "expires_in": 3600}
    assert len(requests) == 1
    url, timeout = requests[0]
    assert parse.urlparse(url).path == "/refresh_access_token"
    assert parse.parse_qs(parse.urlparse(url).query) == {
        "grant_type": ["ig_refresh_token"],
        "access_token": [OLD_TOKEN],
    }
    assert timeout == 30
    assert len(client.put_calls) == 1
    put_call = client.put_calls[0]
    assert put_call["SecretId"] == SECRET_ARN
    stored_secret = json.loads(put_call["SecretString"])
    assert stored_secret == {
        **secret,
        "ig_access_token": "new-token",
        "token_expires_at": expected_expiry,
    }
    assert stored_secret["unknown_object"] == {"enabled": True, "count": 3}
    assert stored_secret["unknown_number"] == 42
    assert secrets._cache == cache_before
    assert expected_expiry in caplog.text
    assert "expires_in=3600" in caplog.text
    assert OLD_TOKEN not in caplog.text


@pytest.mark.parametrize(
    ("status", "expected_calls"),
    [(400, 1), (500, 3)],
)
def test_api_http_errors_are_sanitized_and_do_not_write_secret(
    monkeypatch: pytest.MonkeyPatch,
    caplog: pytest.LogCaptureFixture,
    status: int,
    expected_calls: int,
) -> None:
    client = FakeSecretsManager(make_secret())
    calls = 0
    def fake_urlopen(req, *, timeout: float) -> FakeResponse:
        nonlocal calls
        calls += 1
        body = json.dumps({
            "error": {
                "message": f"Refresh rejected for {OLD_TOKEN}; URL={req.full_url}",
                "type": "OAuthException",
            },
        }).encode("utf-8")
        raise error.HTTPError(req.full_url, status, "failure", None, io.BytesIO(body))

    monkeypatch.setattr(token_refresh_handler.request, "urlopen", fake_urlopen)
    monkeypatch.setattr(token_refresh_handler.time, "sleep", lambda _seconds: None)
    caplog.set_level(logging.ERROR, logger=token_refresh_handler.__name__)

    with pytest.raises(RuntimeError) as raised:
        token_refresh_handler.refresh_token(
            SECRET_ARN, client=client, now=lambda: FIXED_NOW,
        )

    assert calls == expected_calls
    assert client.put_calls == []
    assert str(raised.value) == "Token refresh API request failed"
    assert OLD_TOKEN not in str(raised.value)
    assert OLD_TOKEN not in caplog.text
    assert f"status={status}" in caplog.text
    if status == 400:
        assert "OAuthException" in caplog.text
    assert "https://graph.instagram.com/refresh_access_token" not in caplog.text


@pytest.mark.parametrize(
    "payload",
    [
        {"expires_in": 3600},
        {"access_token": "new-token"},
        {"access_token": "new-token", "expires_in": 0},
        {"access_token": "new-token", "expires_in": True},
    ],
)
def test_invalid_api_response_does_not_write_secret(
    monkeypatch: pytest.MonkeyPatch, payload: dict,
) -> None:
    client = FakeSecretsManager(make_secret())
    calls = 0

    def fake_urlopen(_req, *, timeout: float) -> FakeResponse:
        nonlocal calls
        calls += 1
        return FakeResponse(payload)

    monkeypatch.setattr(token_refresh_handler.request, "urlopen", fake_urlopen)

    with pytest.raises(RuntimeError):
        token_refresh_handler.refresh_token(
            SECRET_ARN, client=client, now=lambda: FIXED_NOW,
        )

    assert calls == 1
    assert client.put_calls == []


@pytest.mark.parametrize("token", [None, "", "  "])
def test_missing_or_empty_old_token_skips_without_api_call(
    monkeypatch: pytest.MonkeyPatch, token: object,
) -> None:
    secret = make_secret()
    if token is None:
        secret.pop("ig_access_token")
    else:
        secret["ig_access_token"] = token
    client = FakeSecretsManager(secret)

    def unexpected_urlopen(*_args, **_kwargs):
        raise AssertionError("API must not be called without an access token")

    monkeypatch.setattr(token_refresh_handler.request, "urlopen", unexpected_urlopen)

    result = token_refresh_handler.refresh_token(SECRET_ARN, client=client)

    assert result == {"skipped": "token_not_set"}
    assert client.put_calls == []


def test_non_string_old_token_fails_before_api_call(monkeypatch: pytest.MonkeyPatch) -> None:
    secret = make_secret()
    secret["ig_access_token"] = 123
    client = FakeSecretsManager(secret)

    def unexpected_urlopen(*_args, **_kwargs):
        raise AssertionError("API must not be called with a malformed access token")

    monkeypatch.setattr(token_refresh_handler.request, "urlopen", unexpected_urlopen)

    with pytest.raises(ValueError, match="ig_access_token must be a string"):
        token_refresh_handler.refresh_token(SECRET_ARN, client=client)

    assert client.put_calls == []


def test_secret_write_failure_propagates_after_successful_api_call(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    put_error = OSError("secret write failed")
    client = FakeSecretsManager(make_secret(), put_error=put_error)
    monkeypatch.setattr(
        token_refresh_handler.request,
        "urlopen",
        lambda _req, *, timeout: FakeResponse({
            "access_token": "new-token", "expires_in": 3600,
        }),
    )

    with pytest.raises(OSError, match="secret write failed") as raised:
        token_refresh_handler.refresh_token(
            SECRET_ARN, client=client, now=lambda: FIXED_NOW,
        )

    assert raised.value is put_error
    assert len(client.put_calls) == 1


def test_lambda_handler_requires_secret_arn(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("SECRET_ARN", raising=False)

    with pytest.raises(ValueError, match="SECRET_ARN is required"):
        token_refresh_handler.lambda_handler({}, None)
