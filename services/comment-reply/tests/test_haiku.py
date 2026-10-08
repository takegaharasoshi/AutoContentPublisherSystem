"""Offline Haiku judge/writer requests, fallback telemetry and shared prompts."""

from __future__ import annotations

import io
import json
from copy import deepcopy
from dataclasses import replace
from unittest.mock import Mock
from urllib.error import HTTPError, URLError

import pytest

from app import anthropic_util, comment_log, http_util
from app.config import Config
from app.judge import haiku, luna
from app.judge.combiner import Combined, combine
from app.judge.contract import Judgement
from app.reply import leak_guard, templates, writer


class _Response:
    def __init__(self, body: dict) -> None:
        self.body = json.dumps(body, ensure_ascii=False).encode("utf-8")

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False

    def read(self) -> bytes:
        return self.body


def _decision(**changes) -> dict:
    return {"kind": "q_yesno", "answer": "yes", "reply": "はい！", "reason": "確定事実",
            "bare_term": None, **changes}


def _body(data: dict | None = None, **changes) -> dict:
    return {
        "content": [{"type": "thinking", "thinking": ""},
                    {"type": "text", "text": json.dumps(data or _decision(), ensure_ascii=False)}],
        "stop_reason": "end_turn",
        "usage": {"input_tokens": 100, "output_tokens": 200,
                  "cache_creation_input_tokens": 40, "cache_read_input_tokens": 60},
        **changes,
    }


def _combined(kind: str = "q_yesno", answer: str | None = "yes", **changes) -> Combined:
    return Combined(None, None, kind, answer, None, "haiku", None, **changes)


def _mock_http(monkeypatch, body: dict) -> Mock:
    post = Mock(side_effect=lambda req, timeout: _Response(body))
    monkeypatch.setattr(http_util.request, "urlopen", post)
    return post


def _assert_request(req, effort: str, max_tokens: int, system: str, text: str, schema: dict) -> None:
    assert req.full_url == anthropic_util.MESSAGES_URL
    assert req.get_method() == "POST"
    headers = {key.lower(): value for key, value in req.header_items()}
    assert headers == {"x-api-key": "fake-anthropic", "anthropic-version": "2023-06-01",
                       "content-type": "application/json"}
    payload = json.loads(req.data)
    assert payload == {
        "model": "claude-haiku-5-5", "max_tokens": max_tokens, "stream": False,
        "system": [{"type": "text", "text": system, "cache_control": {"type": "ephemeral"}}],
        "messages": [{"role": "user", "content": text}],
        "output_config": {"effort": effort, "format": {"type": "json_schema", "schema": schema}},
    }
    assert not {"thinking", "temperature", "top_p", "top_k", "prefill", "fallbacks"} & payload.keys()


def test_judge_text_blocks_request_and_usage(monkeypatch, problem) -> None:
    output = json.dumps(_decision(), ensure_ascii=False)
    body = _body(content=[{"type": "thinking", "thinking": "ignore invalid JSON"},
                          {"type": "text", "text": output[:20]},
                          {"type": "text", "text": output[20:]}])
    post = _mock_http(monkeypatch, body)
    result = haiku.judge("c", "病院に行った？", problem, api_key="fake-anthropic")
    assert (result.method, result.kind, result.answer) == ("haiku", "q_yesno", "yes")
    assert result.reply_draft == "はい！" and result.reason == "確定事実"
    assert result.debug["usage"] == body["usage"]
    assert result.debug["prompt_tokens"] == 200 and result.debug["completion_tokens"] == 200
    assert result.debug["latency_s"] >= 0 and result.debug["stop_reason"] == "end_turn"
    assert "thinking" not in result.debug
    _assert_request(post.call_args.args[0], "max", 16000,
                    luna.build_prompt(problem), "病院に行った？", luna._schema())


def test_judge_uses_luna_bare_term_postprocessing(monkeypatch, problem) -> None:
    _mock_http(monkeypatch, _body(_decision(
        kind="guess_correct", answer=None, bare_term="違う表記",
    )))
    result = haiku.judge("c", "【レントゲン？】", problem, api_key="fake-anthropic")
    assert (result.kind, result.answer, result.bare_term) == ("q_open", None, "レントゲン")


def test_schema_constraints_are_removed_only_from_anthropic_copy() -> None:
    schema = {
        "type": "object", "additionalProperties": True,
        "properties": {
            "format": {"type": "string", "minLength": 2, "maxLength": 10, "pattern": ".+"},
            "nested": {"anyOf": [{"type": "object", "properties": {
                "value": {"type": "string", "format": "email"},
            }}, {"type": "null"}]},
        },
    }
    original = deepcopy(schema)
    converted = anthropic_util.adapt_schema(schema)
    assert schema == original
    assert converted["additionalProperties"] is False
    assert converted["properties"]["format"] == {"type": "string"}
    nested = converted["properties"]["nested"]["anyOf"][0]
    assert nested["additionalProperties"] is False
    assert nested["properties"]["value"] == {"type": "string"}


@pytest.mark.parametrize("category", ["cyber", "bio", "frontier_llm", "general_harms", None])
def test_judge_refusal_category_retained(monkeypatch, problem, category) -> None:
    _mock_http(monkeypatch, _body(content=[], stop_reason="refusal",
                                  stop_details={"category": category}))
    with pytest.raises(anthropic_util.AnthropicRefusalError) as caught:
        haiku.judge("c", "質問", problem, api_key="fake-anthropic")
    assert caught.value.category == category
    assert caught.value.debug["refusal_category"] == category
    assert caught.value.debug["usage"]["output_tokens"] == 200
    assert caught.value.debug["latency_s"] >= 0


@pytest.mark.parametrize("changes,reason", [
    ({"stop_reason": "max_tokens"}, "max_tokens"),
    ({"content": []}, "missing_text"),
    ({"content": [{"type": "thinking", "thinking": ""}]}, "missing_text"),
    ({"content": [{"type": "text", "text": ""}]}, "empty_text"),
    ({"content": [{"type": "text", "text": " \n "}]}, "empty_text"),
    ({"content": [{"type": "text", "text": None}]}, "invalid_text"),
    ({"content": [{"type": "text", "text": "not JSON"}]}, "invalid_json"),
])
def test_judge_invalid_output_retains_usage(monkeypatch, problem, changes, reason) -> None:
    _mock_http(monkeypatch, _body(**changes))
    with pytest.raises(anthropic_util.AnthropicError) as caught:
        haiku.judge("c", "質問", problem, api_key="fake-anthropic")
    assert not isinstance(caught.value, anthropic_util.AnthropicRefusalError)
    assert caught.value.debug["error_reason"] == reason
    assert caught.value.debug["input_tokens"] == 100
    assert caught.value.debug["latency_s"] >= 0


@pytest.mark.parametrize("data", [
    _decision(answer="maybe"), _decision(reply=1), _decision(bare_term=1),
    _decision(kind="greeting", answer="yes"),
])
def test_judge_rejects_same_invalid_fields_as_luna(monkeypatch, problem, data) -> None:
    _mock_http(monkeypatch, _body(data))
    with pytest.raises(anthropic_util.AnthropicError) as caught:
        haiku.judge("c", "質問", problem, api_key="fake-anthropic")
    assert caught.value.debug["error_reason"] == "invalid_judgement"


@pytest.mark.parametrize("status", [429, 500, 529])
def test_judge_retries_three_times_with_exponential_backoff(monkeypatch, problem, status) -> None:
    calls = []

    def post(req, timeout):
        calls.append(req)
        if len(calls) <= 3:
            raise HTTPError(req.full_url, status, "retry", {}, io.BytesIO())
        return _Response(_body())

    monkeypatch.setattr(http_util.request, "urlopen", post)
    sleep = Mock()
    monkeypatch.setattr(http_util.time, "sleep", sleep)
    assert haiku.judge("c", "質問", problem, api_key="fake-anthropic").answer == "yes"
    assert len(calls) == 4
    assert [call.args[0] for call in sleep.call_args_list] == [5, 10, 20]


def test_judge_transport_failure_is_logged_without_retrying_client_errors(monkeypatch, problem) -> None:
    post = Mock(side_effect=HTTPError(anthropic_util.MESSAGES_URL, 400, "bad", {}, io.BytesIO()))
    monkeypatch.setattr(http_util.request, "urlopen", post)
    with pytest.raises(anthropic_util.AnthropicError) as caught:
        haiku.judge("c", "質問", problem, api_key="fake-anthropic")
    assert post.call_count == 1 and caught.value.debug["error_reason"] == "request_failed"


def test_combiner_success_skips_luna_and_jev(monkeypatch, problem) -> None:
    post = _mock_http(monkeypatch, _body())
    blocked = Mock(side_effect=AssertionError("Haiku succeeded"))
    result = combine(
        "c", "質問", problem, Config(judge_mode="haiku"),
        {"anthropic_api_key": "fake-anthropic"}, luna_call=blocked, jev_call=blocked,
        decisions_call=blocked,
    )
    assert result.decision == "haiku" and result.haiku.method == "haiku"
    assert result.luna is None and result.jev is None and result.decisions is None
    blocked.assert_not_called()
    assert post.call_count == 1


def test_combiner_refusal_rejudges_with_luna_and_logs_both(monkeypatch, problem) -> None:
    calls = []

    def post(req, timeout):
        calls.append(req.full_url)
        if req.full_url == anthropic_util.MESSAGES_URL:
            return _Response(_body(stop_reason="refusal", stop_details={"category": "cyber"}))
        assert req.full_url == luna.OPENAI_CHAT_COMPLETIONS_URL
        return _Response({"choices": [{"finish_reason": "stop", "message": {
            "content": json.dumps(_decision()),
        }}], "usage": {"prompt_tokens": 300, "completion_tokens": 10,
                       "prompt_tokens_details": {"cached_tokens": 200}}})

    monkeypatch.setattr(http_util.request, "urlopen", post)
    result = combine("c", "質問", problem, Config(judge_mode="haiku"), {
        "anthropic_api_key": "fake-anthropic", "openai_api_key": "fake-openai",
    })
    assert calls == [anthropic_util.MESSAGES_URL, luna.OPENAI_CHAT_COMPLETIONS_URL]
    assert result.decision == "haiku_fallback_luna" and result.answer == "yes"
    assert result.haiku.error and result.haiku.debug["refusal_category"] == "cyber"
    assert result.luna.debug["cached_tokens"] == 200
    record = comment_log.new_record({"id": "c", "text": "質問"}, None, "now", Config(), problem)
    comment_log.apply_decision(record, result, writer.Reply("はい！", "template", False))
    assert record["judgements"]["haiku"]["debug"]["stop_reason"] == "refusal"
    assert record["final"]["decision"] == "haiku_fallback_luna"


@pytest.mark.parametrize("variant,luna_variant,effort,max_tokens", [
    ("1b-haiku", "1b", "max", 16000), ("1d-haiku", "1d-luna", "low", 4000),
])
def test_writer_normal_request_and_shared_prompt(
    monkeypatch, problem, variant, luna_variant, effort, max_tokens,
) -> None:
    post = _mock_http(monkeypatch, _body({"reply": "はい！"}))
    combined = _combined()
    reply = writer.write_reply(combined, "c", "質問", problem,
                               variant=variant, anthropic_api_key="fake-anthropic")
    assert reply.text == "はい！" and reply.source == "llm" and reply.error is None
    system, slot = writer.build_prompt(combined, "c", problem, variant=luna_variant)
    assert reply.debug["slot"] == slot and reply.debug["model"] == anthropic_util.MODEL
    assert reply.debug["cache_read_input_tokens"] == 60
    _assert_request(post.call_args.args[0], effort, max_tokens, system, "質問", writer.reply_schema())


@pytest.mark.parametrize("variant", ["1b-haiku", "1d-haiku"])
@pytest.mark.parametrize("changes,reason", [
    ({"stop_reason": "refusal", "stop_details": {"category": "general_harms"}}, "refusal"),
    ({"stop_reason": "max_tokens"}, "max_tokens"),
    ({"content": []}, "missing_text"),
    ({"content": [{"type": "text", "text": ""}]}, "empty_text"),
    ({"content": [{"type": "text", "text": '{"reply":3}'}]}, "invalid_reply"),
    ({"content": [{"type": "text", "text": '{"reply":""}'}]}, "empty_reply"),
])
def test_writer_failures_return_template_with_telemetry(monkeypatch, problem, variant, changes, reason) -> None:
    _mock_http(monkeypatch, _body({"reply": "はい！"}, **changes))
    reply = writer.write_reply(_combined(), "c", "質問", problem,
                               variant=variant, anthropic_api_key="fake-anthropic")
    assert reply.source == "fallback_template" and reply.text.startswith("はい！")
    assert reply.error and reply.debug["error_reason"] == reason
    assert reply.debug["usage"]["output_tokens"] == 200
    if reason == "refusal":
        assert reply.debug["refusal_category"] == "general_harms"


@pytest.mark.parametrize("variant", ["1b-haiku", "1d-haiku"])
def test_writer_transport_failure_and_missing_key_fall_back(monkeypatch, problem, variant) -> None:
    post = Mock(side_effect=URLError("offline"))
    monkeypatch.setattr(http_util.request, "urlopen", post)
    reply = writer.write_reply(_combined(), "c", "質問", problem,
                               variant=variant, anthropic_api_key="fake-anthropic")
    assert reply.source == "fallback_template" and reply.debug["latency_s"] >= 0
    missing = writer.write_reply(_combined(), "c", "質問", problem, variant=variant)
    assert missing.source == "fallback_template" and "anthropic_api_key is empty" in missing.error
    assert post.call_count == 1


@pytest.mark.parametrize("variant", ["1b-haiku", "1d-haiku"])
def test_writer_yesno_and_leak_guards_are_shared(monkeypatch, problem, variant) -> None:
    _mock_http(monkeypatch, _body({"reply": "いいえ。"}))
    bad = writer.write_reply(_combined(), "c", "質問", problem,
                             variant=variant, anthropic_api_key="fake-anthropic")
    assert bad.source == "fallback_template" and bad.debug["output_tokens"] == 200
    _mock_http(monkeypatch, _body({"reply": "はい！レントゲンだよ"}))
    guarded_problem = replace(problem, content_key=leak_guard.load_leak_words()["U01"].content_key)
    reply = writer.write_reply(_combined(), "c", "質問", guarded_problem,
                               variant=variant, anthropic_api_key="fake-anthropic")
    assert reply.source == "leak_guard" and reply.text == "はい！"
    assert reply.guard["words"] == ["レントゲン"] and reply.debug["model"] == anthropic_util.MODEL


def test_writer_correct_truth_and_forced_templates(monkeypatch, problem) -> None:
    post = _mock_http(monkeypatch, _body({"reply": "正解！真相を説明するよ"}))
    result = _combined("guess_correct", None)
    truth_reply = writer.write_reply(result, "c", "推理", problem,
                                     variant="1b-haiku", anthropic_api_key="fake-anthropic")
    assert truth_reply.source == "llm" and truth_reply.text.startswith("正解！")
    fixed = writer.write_reply(result, "c", "推理", problem, variant="1d-haiku")
    assert fixed.source == "template" and fixed.text == templates.CORRECT_PREFIX + problem.reveal_text
    for variant in ("1b-haiku", "1d-haiku"):
        assert writer.write_reply(_combined("spam", None), "c", "宣伝", problem,
                                  variant=variant).source == "no_reply"
        assert writer.write_reply(_combined("troll", None), "c", "荒らし", problem,
                                  variant=variant).source == "template"
    assert post.call_count == 1


def test_luna_writer_records_cached_tokens_without_changing_request(monkeypatch, problem) -> None:
    post = _mock_http(monkeypatch, {
        "choices": [{"finish_reason": "stop", "message": {"content": '{"reply":"はい！"}'}}],
        "usage": {"prompt_tokens": 300, "completion_tokens": 10,
                  "prompt_tokens_details": {"cached_tokens": 200}},
    })
    reply = writer.write_reply(_combined(), "c", "質問", problem,
                               variant="1d-luna", openai_api_key="fake")
    assert reply.debug["cached_tokens"] == 200 and reply.source == "llm"
    payload = json.loads(post.call_args.args[0].data)
    assert payload["model"] == "gpt-6-luna" and payload["reasoning_effort"] == "low"
    assert not {"cache_control", "temperature"} & payload.keys()


@pytest.mark.parametrize("finish,content,reason", [
    ("length", "", "max_tokens"), ("stop", "", "empty_text"), ("stop", None, "missing_text"),
])
def test_luna_failed_calls_retain_usage_for_probe(monkeypatch, problem, finish, content, reason) -> None:
    _mock_http(monkeypatch, {
        "choices": [{"finish_reason": finish, "message": {"content": content}}],
        "usage": {"prompt_tokens": 300, "completion_tokens": 10,
                  "prompt_tokens_details": {"cached_tokens": 200}},
    })
    with pytest.raises((ValueError, TypeError)) as caught:
        luna.judge("c", "質問", problem, api_key="fake")
    assert caught.value.debug["error_reason"] == reason
    assert caught.value.debug["cached_tokens"] == 200
    reply = writer.write_reply(_combined(), "c", "質問", problem,
                               variant="1d-luna", openai_api_key="fake")
    assert reply.source == "fallback_template" and reply.debug["error_reason"] == reason
