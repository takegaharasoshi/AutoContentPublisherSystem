"""Scheduled token refresh retains other Secret fields and skips empty tokens."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from unittest.mock import Mock

import pytest

from app import token_refresh_handler


def test_refresh_preserves_secret_and_stores_expiration(monkeypatch, caplog) -> None:
    client = Mock()
    original = {"ig_access_token": "old-private", "ig_user_id": "own-id",
                "anthropic_api_key": "private-api-key", "unknown": {"number": 42}}
    client.get_secret_value.return_value = {"SecretString": json.dumps(original)}
    seen = []

    def refresh(token, **kwargs):
        seen.append((token, kwargs))
        return {"access_token": "new-private", "expires_in": 3600}

    monkeypatch.setattr(token_refresh_handler.graph_api, "refresh_token", refresh)
    now = datetime(2026, 10, 24, 1, 2, 3, tzinfo=timezone.utc)
    result = token_refresh_handler.refresh_token("arn", client=client, now=lambda: now)
    assert result == {"token_expires_at": "2026-10-24T02:02:03Z", "expires_in": 3600}
    assert seen == [("old-private", {"base_url": "https://graph.instagram.com"})]
    written = json.loads(client.put_secret_value.call_args.kwargs["SecretString"])
    assert written == {**original, "ig_access_token": "new-private",
                       "token_expires_at": "2026-10-24T02:02:03Z"}
    assert all(value not in caplog.text for value in ("old-private", "new-private", "private-api-key"))


@pytest.mark.parametrize("old", [None, "", "   "])
def test_unset_token_exits_normally_without_graph_or_write(monkeypatch, old) -> None:
    client = Mock()
    data = {} if old is None else {"ig_access_token": old}
    client.get_secret_value.return_value = {"SecretString": json.dumps(data)}
    graph = Mock(side_effect=AssertionError("must not call Graph"))
    monkeypatch.setattr(token_refresh_handler.graph_api, "refresh_token", graph)
    assert token_refresh_handler.refresh_token("arn", client=client) == {"skipped": "token_not_set"}
    assert not graph.called and not client.put_secret_value.called


@pytest.mark.parametrize("payload", [
    {}, {"access_token": "new"}, {"access_token": "", "expires_in": 10},
    {"access_token": "new", "expires_in": 0}, {"access_token": "new", "expires_in": True},
])
def test_invalid_refresh_never_writes_secret(monkeypatch, payload) -> None:
    client = Mock()
    client.get_secret_value.return_value = {"SecretString": '{"ig_access_token":"old"}'}
    monkeypatch.setattr(token_refresh_handler.graph_api, "refresh_token", lambda *a, **k: payload)
    with pytest.raises(RuntimeError):
        token_refresh_handler.refresh_token("arn", client=client)
    client.put_secret_value.assert_not_called()


def test_bad_secret_and_write_failure_propagate(monkeypatch) -> None:
    client = Mock()
    client.get_secret_value.return_value = {"SecretString": '{"ig_access_token":123}'}
    with pytest.raises(ValueError):
        token_refresh_handler.refresh_token("arn", client=client)
    client.get_secret_value.return_value = {"SecretString": '{"ig_access_token":"old"}'}
    client.put_secret_value.side_effect = OSError("write failed")
    monkeypatch.setattr(token_refresh_handler.graph_api, "refresh_token",
                        lambda *a, **k: {"access_token": "new", "expires_in": 60})
    with pytest.raises(OSError, match="write failed"):
        token_refresh_handler.refresh_token("arn", client=client)


def test_handler_only_requires_secret_arn_and_retains_refresh_base_override(monkeypatch) -> None:
    monkeypatch.delenv("SECRET_ARN", raising=False)
    with pytest.raises(ValueError, match="SECRET_ARN"):
        token_refresh_handler.lambda_handler({}, None)
    monkeypatch.setenv("SECRET_ARN", "arn")
    monkeypatch.setenv("REFRESH_API_BASE", "https://example.invalid")
    refresh = Mock(return_value={"skipped": "token_not_set"})
    monkeypatch.setattr(token_refresh_handler, "refresh_token", refresh)
    assert token_refresh_handler.lambda_handler({}, None) == {"skipped": "token_not_set"}
    refresh.assert_called_once_with("arn", "https://example.invalid")
