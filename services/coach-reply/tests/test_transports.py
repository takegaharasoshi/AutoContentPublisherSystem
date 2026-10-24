"""urllib and Anthropic transport behavior using local response stubs only."""

from __future__ import annotations

import io
import json
from urllib import error, request

import pytest

from app import anthropic_util, http_util


class Response(io.BytesIO):
    def __init__(self, payload) -> None:
        super().__init__(json.dumps(payload).encode("utf-8"))


@pytest.mark.parametrize("status,retries,calls", [(429, 2, 3), (503, 2, 3), (400, 2, 1)])
def test_http_retries_only_rate_limits_and_server_errors(monkeypatch, status, retries, calls) -> None:
    attempts, sleeps = [], []

    def failing(req, **kwargs):
        attempts.append(req)
        raise error.HTTPError(req.full_url, status, "failed", None, io.BytesIO(b"{}"))

    monkeypatch.setattr(request, "urlopen", failing)
    monkeypatch.setattr(http_util.time, "sleep", sleeps.append)
    with pytest.raises(error.HTTPError):
        http_util.post_with_retry(request.Request("https://example.invalid", data=b"{}"), retries=retries)
    assert len(attempts) == calls
    assert sleeps == ([2.0, 4.0] if calls == 3 else [])


def test_http_success_and_non_object_json(monkeypatch) -> None:
    monkeypatch.setattr(request, "urlopen", lambda *a, **k: Response({"ok": True}))
    assert http_util.post_json_with_retry(request.Request("https://example.invalid")) == {"ok": True}
    monkeypatch.setattr(request, "urlopen", lambda *a, **k: Response([]))
    with pytest.raises(ValueError):
        http_util.post_json_with_retry(request.Request("https://example.invalid"))


def test_anthropic_posts_configured_model_and_ignores_thinking(monkeypatch) -> None:
    seen = []

    def respond(req, **kwargs):
        seen.append((req, kwargs))
        return Response({"content": [{"type": "thinking", "thinking": "hidden"},
                                     {"type": "text", "text": '{"results":[]}' }],
                         "stop_reason": "end_turn", "usage": {"input_tokens": 3, "output_tokens": 2}})

    monkeypatch.setattr(request, "urlopen", respond)
    data, debug = anthropic_util.request_json(
        "system", "user", {"type": "object", "properties": {}}, api_key="key",
        model="configured", effort="high", max_tokens=123, timeout=12,
    )
    assert data == {"results": []} and debug["input_tokens"] == 3
    req, kwargs = seen[0]
    body = json.loads(req.data)
    assert req.full_url == anthropic_util.MESSAGES_URL and req.get_method() == "POST"
    assert body["model"] == "configured" and body["output_config"]["effort"] == "high"
    assert body["max_tokens"] == 123 and body["stream"] is False
    assert body["output_config"]["format"]["schema"]["additionalProperties"] is False
    assert kwargs["timeout"] == 12 and debug["model"] == "configured"


@pytest.mark.parametrize("response,expected", [
    ({"stop_reason": "refusal", "stop_details": {"category": "safety"}}, anthropic_util.AnthropicRefusalError),
    ({"stop_reason": "max_tokens"}, anthropic_util.AnthropicError),
    ({"content": []}, anthropic_util.AnthropicError),
    ({"content": [{"type": "text", "text": "not-json"}]}, anthropic_util.AnthropicError),
    ({"content": [{"type": "text", "text": "[]"}]}, anthropic_util.AnthropicError),
])
def test_anthropic_failures_propagate_as_judgment_failures(monkeypatch, response, expected) -> None:
    monkeypatch.setattr(request, "urlopen", lambda *a, **k: Response(response))
    with pytest.raises(expected):
        anthropic_util.request_json("s", "u", {}, api_key="key", effort="high", max_tokens=20)


def test_schema_adaptation_does_not_mutate_original() -> None:
    schema = {"type": "object", "properties": {"reason": {"type": "string", "maxLength": 40}}}
    adapted = anthropic_util.adapt_schema(schema)
    assert adapted["additionalProperties"] is False
    assert "maxLength" not in adapted["properties"]["reason"]
    assert schema["properties"]["reason"]["maxLength"] == 40
