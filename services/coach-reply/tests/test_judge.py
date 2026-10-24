"""Structured judgment contracts, isolation and batch failure handling."""

from __future__ import annotations

import json

import pytest

from app import judge
from app.config import Config


def result(cid: str, **overrides) -> dict:
    return {"id": cid, "verdict": "correct", "confidence": "high", "reason": "答えが一致", **overrides}


def test_judge_batches_at_twenty_and_never_sends_usernames(monkeypatch, snapshot) -> None:
    requests = []

    def request_json(system, text, schema, **kwargs):
        data = json.loads(text)
        requests.append((system, data, schema, kwargs))
        return {"results": [result(c["id"]) for c in data["comments"]]}, {}

    monkeypatch.setattr(judge.anthropic_util, "request_json", request_json)
    comments = [{"id": str(i), "text": "フライパンかな？👏", "username": "private-name"} for i in range(45)]
    results = judge.judge_comments(dict(snapshot, private_field="discard"), comments,
                                   config=Config(judge_model="custom", judge_effort="max"), api_key="key")
    assert len(results) == 45
    assert [len(req[1]["comments"]) for req in requests] == [20, 20, 5]
    for system, data, schema, kwargs in requests:
        assert set(data["snapshot"]) == {"question_text", "answer_text", "explanation", "hint"}
        assert data["snapshot"]["explanation"] == snapshot["explanation"]
        assert all(set(c) == {"id", "text"} for c in data["comments"])
        assert "private-name" not in json.dumps(data)
        assert kwargs["model"] == "custom" and kwargs["effort"] == "max"
        assert kwargs["api_key"] == "key" and schema == judge.SCHEMA
        assert "最悪の失敗" in system and "複数の候補" in system


@pytest.mark.parametrize("raw", [{}, {"results": {}}, [], {"results": [], "extra": True}])
def test_bad_top_level_output_fails_whole_batch(monkeypatch, snapshot, raw) -> None:
    monkeypatch.setattr(judge.anthropic_util, "request_json", lambda *a, **k: (raw, {}))
    assert judge.judge_comments(snapshot, [{"id": "c", "text": "answer"}], api_key="key") == {}


@pytest.mark.parametrize("bad", [
    {"id": "bad", "verdict": "correct", "confidence": "high"},
    result("bad", verdict="unknown"), result("bad", verdict=[]),
    result("bad", confidence="medium"), result("bad", confidence=None),
    result("bad", reason=None), result("bad", reason=""), result("bad", extra=True),
    result("foreign"), {"id": ["bad"]}, "invalid row",
])
def test_bad_missing_and_foreign_ids_do_not_poison_valid_peers(monkeypatch, snapshot, bad) -> None:
    monkeypatch.setattr(judge.anthropic_util, "request_json", lambda *a, **k: (
        {"results": [result("good"), bad]}, {},
    ))
    results = judge.judge_comments(snapshot, [
        {"id": "good", "text": "yes"}, {"id": "bad", "text": "bad"}, {"id": "missing", "text": "none"},
    ], api_key="key")
    assert results == {"good": {"verdict": "correct", "confidence": "high", "reason": "答えが一致"}}


def test_duplicate_output_id_is_a_failure_even_when_both_rows_agree(monkeypatch, snapshot) -> None:
    monkeypatch.setattr(judge.anthropic_util, "request_json", lambda *a, **k: (
        {"results": [result("duplicate"), result("duplicate"), result("valid", verdict="alt")]}, {},
    ))
    results = judge.judge_comments(snapshot, [
        {"id": "duplicate", "text": "x"}, {"id": "valid", "text": "y"},
    ], api_key="key")
    assert set(results) == {"valid"} and results["valid"]["verdict"] == "alt"


def test_api_error_loses_only_its_batch_and_does_not_log_request_details(monkeypatch, snapshot, caplog) -> None:
    count = 0

    def request_json(*args, **kwargs):
        nonlocal count
        count += 1
        if count == 1:
            raise RuntimeError("secret-api-key and private-comment")
        return {"results": [result("20")]}, {}

    monkeypatch.setattr(judge.anthropic_util, "request_json", request_json)
    results = judge.judge_comments(snapshot, [{"id": str(i), "text": "x"} for i in range(21)], api_key="key")
    assert set(results) == {"20"} and count == 2
    assert "secret-api-key" not in caplog.text and "private-comment" not in caplog.text


def test_empty_input_needs_no_credentials_and_default_call_can_load_secret(monkeypatch, snapshot) -> None:
    assert judge.judge_comments(snapshot, []) == {}
    monkeypatch.setenv("SECRET_ARN", "arn")
    monkeypatch.setattr(judge.secrets, "get_secrets", lambda arn: {"anthropic_api_key": "test-key"})
    seen = []

    def request_json(*args, **kwargs):
        seen.append(kwargs["api_key"])
        return {"results": [result("c")]}, {}

    monkeypatch.setattr(judge.anthropic_util, "request_json", request_json)
    assert "c" in judge.judge_comments(snapshot, [{"id": "c", "text": "answer"}])
    assert seen == ["test-key"]
