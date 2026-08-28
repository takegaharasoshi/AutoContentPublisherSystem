"""umigame-comment-webhook Lambda ハンドラのテスト。"""

import base64
import hashlib
import hmac
import importlib
import json
import sys
from pathlib import Path
from unittest.mock import Mock

import pytest


LAMBDA_DIR = Path(__file__).parents[1] / "lambda"
sys.path.insert(0, str(LAMBDA_DIR))


@pytest.fixture
def handler(monkeypatch):
    monkeypatch.setenv("SECRET_ARN", "arn:aws:secretsmanager:ap-northeast-1:123456789012:secret:test")
    monkeypatch.setenv("GRAPH_API_BASE", "https://graph.instagram.com/v23.0")
    sys.modules.pop("handler", None)
    module = importlib.import_module("handler")
    module._secrets_cache = {
        "verify_token": "verify-token",
        "app_secret": "app-secret",
        "ig_access_token": "access-token",
        "ig_user_id": "our-instagram-user",
        "openai_api_key": "",
    }
    return module


def event_with_signature(body, secret="app-secret", base64_encoded=False):
    raw_body = json.dumps(body, ensure_ascii=False).encode("utf-8")
    signature = hmac.new(secret.encode(), raw_body, hashlib.sha256).hexdigest()
    return {
        "requestContext": {"http": {"method": "POST"}},
        "headers": {"X-Hub-Signature-256": f"sha256={signature}"},
        "body": base64.b64encode(raw_body).decode() if base64_encoded else raw_body.decode(),
        "isBase64Encoded": base64_encoded,
    }


def comments_payload(sender_id="another-user", comment_id="comment-123", text="これは関係ありますか？"):
    return {
        "entry": [
            {
                "changes": [
                    {
                        "field": "comments",
                        "value": {
                            "id": comment_id,
                            "text": text,
                            "from": {"id": sender_id, "username": "tester"},
                            "media": {"id": "media-456"},
                        },
                    }
                ]
            }
        ]
    }


def test_get_verification_returns_challenge(handler):
    result = handler.lambda_handler(
        {
            "requestContext": {"http": {"method": "GET"}},
            "queryStringParameters": {
                "hub.mode": "subscribe",
                "hub.verify_token": "verify-token",
                "hub.challenge": "challenge-value",
            },
        },
        None,
    )

    assert result == {
        "statusCode": 200,
        "headers": {"Content-Type": "text/plain"},
        "body": "challenge-value",
    }


def test_get_verification_rejects_wrong_token(handler):
    result = handler.lambda_handler(
        {
            "requestContext": {"http": {"method": "GET"}},
            "queryStringParameters": {
                "hub.mode": "subscribe",
                "hub.verify_token": "wrong-token",
                "hub.challenge": "challenge-value",
            },
        },
        None,
    )

    assert result["statusCode"] == 403


def test_post_accepts_valid_base64_signature(handler, monkeypatch):
    reply = Mock(return_value="{\"id\": \"reply-1\"}")
    monkeypatch.setattr(handler, "reply_to_comment", reply)

    result = handler.lambda_handler(event_with_signature(comments_payload(), base64_encoded=True), None)

    assert result["statusCode"] == 200
    reply.assert_called_once()


def test_post_rejects_invalid_signature(handler, monkeypatch):
    reply = Mock()
    monkeypatch.setattr(handler, "reply_to_comment", reply)
    event = event_with_signature(comments_payload())
    event["headers"]["X-Hub-Signature-256"] = "sha256=invalid"

    result = handler.lambda_handler(event, None)

    assert result["statusCode"] == 403
    reply.assert_not_called()


def test_own_comment_is_skipped(handler, monkeypatch):
    reply = Mock()
    monkeypatch.setattr(handler, "reply_to_comment", reply)

    result = handler.lambda_handler(event_with_signature(comments_payload(sender_id="our-instagram-user")), None)

    assert result["statusCode"] == 200
    reply.assert_not_called()


def test_normal_comment_posts_reply_to_graph_api(handler, monkeypatch):
    post_form = Mock(return_value="{\"id\": \"reply-1\"}")
    monkeypatch.setattr(handler, "post_form", post_form)

    result = handler.lambda_handler(event_with_signature(comments_payload()), None)

    assert result["statusCode"] == 200
    post_form.assert_called_once_with(
        "https://graph.instagram.com/v23.0/comment-123/replies",
        {"message": handler.FALLBACK_REPLY, "access_token": "access-token"},
    )


def test_empty_openai_api_key_uses_fallback_reply(handler):
    assert handler.generate_reply("ヒントはありますか？", "") == handler.FALLBACK_REPLY
