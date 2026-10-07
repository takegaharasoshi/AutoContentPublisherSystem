"""Webhook and SQS handler behavior with no network access."""

from __future__ import annotations

import hashlib
import hmac
import io
import json
import sys
from dataclasses import asdict
from types import SimpleNamespace
from unittest.mock import Mock

import pytest

from app import graph_api, problem_store, reply_handler, webhook_handler
from app.config import Config
from app.judge.combiner import Combined
from app.judge.contract import Judgement, ProblemInvalid
from app.reply.writer import Reply


def _webhook_event(body: bytes, secret: str = "secret", *, method: str = "POST") -> dict:
    signature = hmac.new(secret.encode(), body, hashlib.sha256).hexdigest()
    return {
        "requestContext": {"http": {"method": method}},
        "headers": {"x-hub-signature-256": f"sha256={signature}"},
        "body": body.decode("utf-8"),
    }


def _install_boto3(monkeypatch, *, sqs=None, s3=None) -> None:
    clients = {"sqs": sqs, "s3": s3}
    monkeypatch.setitem(sys.modules, "boto3", SimpleNamespace(client=lambda name: clients[name]))


def test_signature_checks_exact_prefix_and_digest() -> None:
    body = b"hello"
    signature = hmac.new(b"key", body, hashlib.sha256).hexdigest()
    assert webhook_handler.is_valid_signature(f"sha256={signature}", body, "key")
    assert not webhook_handler.is_valid_signature(f"sha256={signature}", body + b"x", "key")
    assert not webhook_handler.is_valid_signature(signature, body, "key")


def test_get_verification(monkeypatch) -> None:
    monkeypatch.setenv("SECRET_ARN", "test-secret")
    monkeypatch.setattr(webhook_handler, "get_secrets", lambda arn: {"verify_token": "v"})
    event = {"requestContext": {"http": {"method": "GET"}},
             "queryStringParameters": {"hub.mode": "subscribe", "hub.verify_token": "v", "hub.challenge": "123"}}
    assert webhook_handler.lambda_handler(event, None)["body"] == "123"
    event["queryStringParameters"]["hub.verify_token"] = "bad"
    assert webhook_handler.lambda_handler(event, None)["statusCode"] == 403


def test_webhook_skips_self_and_enqueues_fifo_params(monkeypatch) -> None:
    monkeypatch.setenv("SECRET_ARN", "test-secret")
    monkeypatch.setenv("QUEUE_URL", "queue-url")
    monkeypatch.setattr(webhook_handler, "get_secrets", lambda arn: {"app_secret": "secret", "ig_user_id": "self"})
    sqs = Mock()
    _install_boto3(monkeypatch, sqs=sqs)
    payload = {"entry": [{"time": 123, "changes": [
        {"field": "comments", "value": {"id": "1", "from": {"id": "self"}, "media": {"id": "m"}}},
        {"field": "comments", "value": {"id": "2", "from": {"id": "other"}, "media": {"id": "m"}, "text": "hi"}},
        {"field": "comments", "value": {"from": {"id": "other"}}},
    ]}]}
    event = _webhook_event(json.dumps(payload).encode())
    assert webhook_handler.lambda_handler(event, None)["statusCode"] == 200
    sqs.send_message.assert_called_once()
    sent = sqs.send_message.call_args.kwargs
    assert (sent["QueueUrl"], sent["MessageGroupId"], sent["MessageDeduplicationId"]) == ("queue-url", "m", "2")
    message = json.loads(sent["MessageBody"])
    assert message["entry_time"] == 123
    assert message["webhook_received_at"].endswith("Z")
    assert message["comment"]["id"] == "2"


def test_webhook_enqueue_failure_500_and_bad_json_200(monkeypatch) -> None:
    monkeypatch.setenv("SECRET_ARN", "test-secret")
    monkeypatch.setenv("QUEUE_URL", "queue-url")
    monkeypatch.setattr(webhook_handler, "get_secrets", lambda arn: {"app_secret": "secret", "ig_user_id": "self"})
    sqs = Mock()
    sqs.send_message.side_effect = RuntimeError("queue failed")
    _install_boto3(monkeypatch, sqs=sqs)
    payload = {"entry": [{"changes": [{"field": "comments", "value": {"id": "1"}}]}]}
    assert webhook_handler.lambda_handler(_webhook_event(json.dumps(payload).encode()), None)["statusCode"] == 500
    assert webhook_handler.lambda_handler(_webhook_event(b"not-json"), None)["statusCode"] == 200
    invalid = _webhook_event(b"{}")
    invalid["headers"] = {"X-Hub-Signature-256": "sha256=wrong"}
    assert webhook_handler.lambda_handler(invalid, None)["statusCode"] == 401


def test_problem_404_and_invalid_snapshot(problem) -> None:
    class Missing(Exception):
        response = {"Error": {"Code": "NoSuchKey"}}

    client = Mock()
    client.get_object.side_effect = Missing()
    with pytest.raises(problem_store.ProblemNotFound):
        problem_store.get_problem("bucket", "prefix/", "media-1", client=client)
    client.get_object.side_effect = None
    raw = {**asdict(problem), "core_points": None}
    client.get_object.return_value = {"Body": io.BytesIO(json.dumps(raw).encode())}
    with pytest.raises(ProblemInvalid):
        problem_store.get_problem("bucket", "prefix/", "media-1", client=client)


def _message() -> dict:
    return {"comment": {"id": "comment-1", "text": "質問", "from": {"id": "user"},
                        "media": {"id": "media-1"}},
            "entry_time": 1700000000, "webhook_received_at": "2026-09-30T01:00:00Z"}


def _credentials() -> dict:
    return {"ig_access_token": "token", "ig_user_id": "self",
            "openai_api_key": "openai", "typesafe_api_key": "jev"}


def test_reply_missing_snapshot_logs_and_succeeds(monkeypatch) -> None:
    monkeypatch.setattr(reply_handler, "get_problem", Mock(side_effect=problem_store.ProblemNotFound("media-1")))
    write = Mock()
    monkeypatch.setattr(reply_handler, "write_record", write)
    reply_handler.process_message(
        _message(), Config(assets_bucket="bucket", comment_log_bucket="bucket"),
        _credentials(), s3_client=Mock(),
    )
    assert write.call_args.args[0]["errors"] == ["problem_not_found"]
    assert write.call_args.args[0]["reply"]["text"] is None


def test_graph_failure_is_partial_failure_and_log_failure_does_not_stop_reply(monkeypatch, problem) -> None:
    monkeypatch.setenv("SECRET_ARN", "test-secret")
    monkeypatch.setenv("ASSETS_BUCKET", "bucket")
    monkeypatch.setenv("REPLY_VARIANT", "2b")
    monkeypatch.setattr(reply_handler, "get_secrets", lambda arn: _credentials())
    monkeypatch.setattr(reply_handler, "get_problem", lambda *args, **kwargs: problem)
    combined = Combined(Judgement("luna", "q_yesno", "yes"), None,
                        "q_yesno", "yes", None, "luna", None)
    monkeypatch.setattr(reply_handler, "combine", lambda *args, **kwargs: combined)
    monkeypatch.setattr(reply_handler, "write_reply", lambda *args, **kwargs: Reply("はい！", "template", False))
    graph = Mock(side_effect=[RuntimeError("graph failed"), "reply-1"])
    monkeypatch.setattr(reply_handler, "reply_to_comment", graph)
    records = []

    def write(record, **kwargs):
        records.append(json.loads(json.dumps(record)))
        raise RuntimeError("S3 write failed")

    monkeypatch.setattr(reply_handler, "write_record", write)
    _install_boto3(monkeypatch, s3=Mock())
    event = {"Records": [
        {"messageId": "a", "body": json.dumps(_message())},
        {"messageId": "b", "body": json.dumps(_message())},
    ]}
    assert reply_handler.lambda_handler(event, None) == {"batchItemFailures": [{"itemIdentifier": "a"}]}
    assert len(records) == 2
    assert "graph failed" in records[0]["errors"][-1]
    assert records[1]["reply"]["reply_id"] == "reply-1"


def test_graph_api_truncates_only_at_send_boundary(monkeypatch) -> None:
    payloads = []

    def transport(req, **kwargs):
        from urllib.parse import parse_qs

        payloads.append(parse_qs(req.data.decode("utf-8")))
        return b'{"id":"reply-1"}'

    monkeypatch.setattr(graph_api, "post_with_retry", transport)
    long_text = "あ" * 210
    assert graph_api.reply_to_comment("comment-1", long_text, "fake") == "reply-1"
    assert payloads[0]["message"] == [long_text[:200]]
