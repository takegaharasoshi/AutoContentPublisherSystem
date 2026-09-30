"""Function URL ingress: verify Meta signatures and enqueue comment events."""

from __future__ import annotations

import base64
import hashlib
import hmac
import json
import logging
from datetime import datetime, timezone
from typing import Any, Mapping

from app.config import Config
from app.secrets import get_secrets, require_keys


LOGGER = logging.getLogger(__name__)


def response(status: int, body: str) -> dict[str, Any]:
    """Return a Lambda Function URL response."""
    return {"statusCode": status, "headers": {"Content-Type": "text/plain"}, "body": body}


def get_raw_body(event: Mapping[str, Any]) -> bytes:
    """Return the exact payload bytes covered by Meta's signature."""
    body = event.get("body") or ""
    if not isinstance(body, str):
        raise ValueError("body must be text")
    if event.get("isBase64Encoded"):
        return base64.b64decode(body, validate=True)
    return body.encode("utf-8")


def get_header(headers: Mapping[str, Any] | None, name: str) -> str:
    """Read a case insensitive header."""
    return next((str(value) for key, value in (headers or {}).items()
                 if key.lower() == name.lower()), "")


def is_valid_signature(signature: str, raw_body: bytes, app_secret: str) -> bool:
    """Check the exact sha256= HMAC header with constant time comparison."""
    if not signature.startswith("sha256="):
        return False
    expected = hmac.new(app_secret.encode("utf-8"), raw_body, hashlib.sha256).hexdigest()
    return hmac.compare_digest(signature[7:], expected)


def enqueue_comments(
    payload: Mapping[str, Any], ig_user_id: str, queue_url: str, client: Any,
    received_at: str,
) -> bool:
    """Enqueue every valid comment; report any failure for Meta redelivery."""
    failed = False
    entries = payload.get("entry", [])
    for entry in entries if isinstance(entries, list) else []:
        if not isinstance(entry, Mapping):
            continue
        changes = entry.get("changes", [])
        for change in changes if isinstance(changes, list) else []:
            if not isinstance(change, Mapping) or change.get("field") != "comments":
                continue
            value = change.get("value")
            if not isinstance(value, Mapping):
                continue
            comment_id = value.get("id")
            author = value.get("from") if isinstance(value.get("from"), Mapping) else {}
            if not comment_id or str(author.get("id", "")) == ig_user_id:
                continue
            media = value.get("media") if isinstance(value.get("media"), Mapping) else {}
            media_id = str(media.get("id") or value.get("media_id") or "unknown")
            message = {
                "comment": dict(value), "entry_time": entry.get("time"),
                "webhook_received_at": received_at,
            }
            try:
                client.send_message(
                    QueueUrl=queue_url,
                    MessageGroupId=media_id,
                    MessageDeduplicationId=str(comment_id),
                    MessageBody=json.dumps(message, ensure_ascii=False),
                )
            except Exception:
                LOGGER.exception("SQS enqueue failed: comment_id=%s", comment_id)
                failed = True
    return failed


def lambda_handler(event: Mapping[str, Any], context: Any) -> dict[str, Any]:
    """Handle GET verification and POST comment delivery."""
    config = Config.from_env()
    config.require("secret_arn")
    credentials = get_secrets(config.secret_arn)
    method = event.get("requestContext", {}).get("http", {}).get("method")
    if method == "GET":
        require_keys(credentials, "verify_token")
        query = event.get("queryStringParameters") or {}
        if (query.get("hub.mode") == "subscribe"
                and hmac.compare_digest(str(query.get("hub.verify_token", "")), credentials["verify_token"])):
            return response(200, str(query.get("hub.challenge", "")))
        return response(403, "Forbidden")
    if method != "POST":
        return response(405, "Method Not Allowed")
    require_keys(credentials, "app_secret", "ig_user_id")
    try:
        raw_body = get_raw_body(event)
    except (ValueError, TypeError) as exc:
        LOGGER.warning("Webhook body invalid: %s", exc)
        return response(401, "Unauthorized")
    signature = get_header(event.get("headers"), "X-Hub-Signature-256")
    if not is_valid_signature(signature, raw_body, credentials["app_secret"]):
        LOGGER.warning("Webhook signature invalid")
        return response(401, "Unauthorized")
    try:
        payload = json.loads(raw_body)
    except (UnicodeDecodeError, json.JSONDecodeError):
        LOGGER.warning("Webhook JSON invalid")
        return response(200, "OK")
    if not isinstance(payload, dict):
        LOGGER.warning("Webhook JSON is not an object")
        return response(200, "OK")
    config.require("queue_url")
    import boto3

    failed = enqueue_comments(
        payload, credentials["ig_user_id"], config.queue_url, boto3.client("sqs"),
        datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z"),
    )
    return response(500 if failed else 200, "Retry" if failed else "OK")
