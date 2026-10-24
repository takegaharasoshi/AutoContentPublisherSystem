"""Configuration, controls, and S3 document persistence without AWS calls."""

from __future__ import annotations

import io
import json
from copy import deepcopy
from types import SimpleNamespace
from unittest.mock import Mock

import pytest
from botocore.exceptions import ClientError

from app import secrets, snapshot_store, state_store, switch
from app.config import Config


def s3_error(code: str) -> ClientError:
    return ClientError({"Error": {"Code": code}}, "GetObject")


def test_config_defaults_and_explicit_values() -> None:
    config = Config.from_env({})
    assert config.graph_api_base == "https://graph.instagram.com/v25.0"
    assert config.judge_model == "claude-haiku-5-5" and config.judge_effort == "high"
    overridden = Config.from_env({"STATE_PREFIX": "custom/", "JUDGE_MODEL": "model", "JUDGE_EFFORT": "max"})
    assert overridden.state_prefix == "custom/" and overridden.judge_model == "model"
    with pytest.raises(ValueError, match="missing configuration"):
        config.require("secret_arn", "assets_bucket")


@pytest.mark.parametrize("key,value", [
    ("PROBLEMS_PREFIX", "/absolute/"), ("STATE_PREFIX", "no-slash"),
    ("STATE_PREFIX", ""), ("PARAM_PREFIX", "relative/"),
    ("PARAM_PREFIX", "/no-slash"), ("JUDGE_EFFORT", "unsupported"),
    ("JUDGE_MODEL", ""), ("GRAPH_API_BASE", ""),
])
def test_bad_configuration_is_rejected(key, value) -> None:
    with pytest.raises(ValueError):
        Config.from_env({key: value})


@pytest.mark.parametrize("value", [
    "2026-10-24", "2026-10-24T00:00:00", "2026-10-24T09:00:00+09:00",
    "2026-13-01T00:00:00Z", "not-a-date", " 2026-10-24T00:00:00Z", 123,
])
def test_switch_rejects_non_utc_or_malformed_timestamps(value) -> None:
    client = Mock()
    client.get_parameter.side_effect = [
        {"Parameter": {"Value": "on"}}, {"Parameter": {"Value": value}},
    ]
    with pytest.raises(ValueError):
        switch.read_switch("/params/", client=client)


@pytest.mark.parametrize("value,expected", [("on", True), ("off", False)])
def test_switch_uses_individual_get_parameter_calls(value, expected) -> None:
    client = Mock()
    client.get_parameter.side_effect = [
        {"Parameter": {"Value": value}}, {"Parameter": {"Value": "2026-10-24T00:00:00Z"}},
    ]
    result = switch.read_switch("/p/", client=client)
    assert result.enabled is expected and result.value == value
    assert [call.kwargs["Name"] for call in client.get_parameter.call_args_list] == [
        "/p/reply-enabled", "/p/reply-not-before",
    ]


def test_bad_or_unreadable_switch_is_never_defaulted_to_on() -> None:
    client = Mock()
    client.get_parameter.return_value = {"Parameter": {"Value": "ON"}}
    with pytest.raises(ValueError):
        switch.read_switch("/p/", client=client)
    client.get_parameter.side_effect = s3_error("AccessDenied")
    with pytest.raises(ClientError):
        switch.read_switch("/p/", client=client)


def test_missing_s3_state_has_only_initial_values() -> None:
    client = Mock()
    client.get_object.side_effect = s3_error("NoSuchKey")
    assert state_store.get_media_counts("b", "s/", client=client) == {"media": {}}
    assert state_store.get_judged("b", "s/", "m", client=client) == {
        "media_id": "m", "first_correct_replied": False, "comments": {},
    }
    assert snapshot_store.get_snapshot("b", "p/", "m", client=client) is None


@pytest.mark.parametrize("code", ["AccessDenied", "SlowDown", "InternalError"])
def test_s3_errors_are_not_absence(code) -> None:
    client = Mock()
    client.get_object.side_effect = s3_error(code)
    with pytest.raises(ClientError):
        snapshot_store.get_snapshot("b", "p/", "m", client=client)


@pytest.mark.parametrize("raw", [b"broken-json", b"[]", b"null"])
def test_corrupt_documents_do_not_reset_state(raw) -> None:
    client = Mock()
    client.get_object.return_value = {"Body": io.BytesIO(raw)}
    with pytest.raises(ValueError):
        state_store.get_media_counts("b", "s/", client=client)


def test_state_and_snapshot_keys_content_and_roundtrip(snapshot) -> None:
    client = Mock()
    counts = {"media": {"m1": {"comments_count": 4, "checked_at": "now"}}, "updated_at": "now"}
    state_store.put_media_counts("b", "s/", counts, client=client)
    written = client.put_object.call_args.kwargs
    assert written["Key"] == "s/media-counts.json" and written["ContentType"] == "application/json"
    client.get_object.return_value = {"Body": io.BytesIO(written["Body"])}
    assert state_store.get_media_counts("b", "s/", client=client) == counts
    state = {"media_id": "m1", "first_correct_replied": True,
             "comments": {"c": {"verdict": "correct", "reason": "核心が一致"}}}
    state_store.put_judged("b", "s/", "m1", state, client=client)
    assert client.put_object.call_args.kwargs["Key"] == "s/judged/m1.json"
    client.get_object.return_value = {"Body": io.BytesIO(client.put_object.call_args.kwargs["Body"])}
    assert state_store.get_judged("b", "s/", "m1", client=client) == state
    client.get_object.return_value = {"Body": io.BytesIO(json.dumps(snapshot).encode())}
    assert snapshot_store.get_snapshot("b", "p/", "m1", client=client) == snapshot
    assert client.get_object.call_args.kwargs == {"Bucket": "b", "Key": "p/m1.json"}


@pytest.mark.parametrize("data,method", [
    ({"media": []}, "counts"), ({"media": {"m": {"comments_count": True}}}, "counts"),
    ({"media_id": "wrong", "comments": {}, "first_correct_replied": False}, "judged"),
    ({"media_id": "m", "comments": [], "first_correct_replied": False}, "judged"),
])
def test_malformed_state_is_an_error(data, method) -> None:
    client = Mock()
    client.get_object.return_value = {"Body": io.BytesIO(json.dumps(data).encode())}
    with pytest.raises(ValueError):
        if method == "counts":
            state_store.get_media_counts("b", "s/", client=client)
        else:
            state_store.get_judged("b", "s/", "m", client=client)


def test_other_snapshot_kind_is_absent_but_broken_quiz_is_an_error(snapshot) -> None:
    client = Mock()
    for data, error in [(dict(snapshot, kind="umigame"), False),
                        (dict(snapshot, media_id="wrong"), True),
                        (dict(snapshot, answer_text=""), True)]:
        client.get_object.return_value = {"Body": io.BytesIO(json.dumps(data).encode())}
        if error:
            with pytest.raises(ValueError):
                snapshot_store.get_snapshot("b", "p/", "m1", client=client)
        else:
            assert snapshot_store.get_snapshot("b", "p/", "m1", client=client) is None


@pytest.mark.parametrize("as_text", [False, True])
def test_answer_snapshot_extracts_json_content_fields_and_normalizes_utc(as_text) -> None:
    fields = {"explanation": "解説", "hint": "ヒント", "other": "捨てる"}
    answer = {"media_id": "m", "posted_at": "2026-10-24 01:02:03", "question_text": "問題",
              "answer_text": "答え", "content_fields": json.dumps(fields) if as_text else fields}
    original = deepcopy(answer)
    snapshot = snapshot_store.snapshot_from_answer(answer)
    assert snapshot["explanation"] == "解説" and snapshot["hint"] == "ヒント"
    assert snapshot["kind"] == "quiz" and snapshot["source"] == "backfill"
    assert snapshot["posted_at"] == "2026-10-24T01:02:03Z"
    assert "other" not in snapshot and answer == original


def test_secrets_are_read_again_after_rotation_and_never_return_non_strings(monkeypatch) -> None:
    client = Mock()
    client.get_secret_value.side_effect = [
        {"SecretString": '{"ig_access_token":"old","count":1}'},
        {"SecretBinary": b'{"ig_access_token":"new"}'},
    ]
    monkeypatch.setattr("boto3.client", lambda service: client)
    assert secrets.get_secrets("arn") == {"ig_access_token": "old"}
    assert secrets.get_secrets("arn") == {"ig_access_token": "new"}
    with pytest.raises(ValueError, match="missing secret fields"):
        secrets.require_keys({"key": "  "}, "key")
    with pytest.raises(ValueError, match="SECRET_ARN"):
        secrets.get_secrets("")
