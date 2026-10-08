"""SQS-triggered reply Lambda with partial batch failures."""

from __future__ import annotations

import json
import logging
from typing import Any, Mapping

from app.comment_log import apply_decision, new_record, utc_now, write_record
from app.config import Config
from app.graph_api import reply_to_comment
from app.judge.combiner import combine
from app.problem_store import ProblemNotFound, get_problem
from app.reply.writer import write_reply
from app.secrets import get_secrets, require_keys


LOGGER = logging.getLogger(__name__)


def _write_best_effort(record: dict[str, Any], config: Config, client: Any) -> None:
    try:
        write_record(record, bucket=config.comment_log_bucket, client=client)
    except Exception:
        LOGGER.exception("comment record write failed: comment_id=%s", record["comment_id"])


def process_message(
    body: Mapping[str, Any], config: Config, credentials: Mapping[str, str],
    *, s3_client: Any,
) -> None:
    """Process one queue message, recording either outcome when possible."""
    comment = body.get("comment")
    if not isinstance(comment, dict):
        raise ValueError("SQS message lacks comment object")
    comment_id = str(comment.get("id") or "")
    if not comment_id:
        raise ValueError("SQS comment lacks id")
    received = body.get("webhook_received_at") or utc_now()
    record = new_record(comment, body.get("entry_time"), str(received), config)
    media_id = record["media_id"]
    try:
        try:
            problem = get_problem(config.assets_bucket, config.problems_prefix, media_id, client=s3_client)
        except ProblemNotFound:
            LOGGER.info("problem snapshot absent: comment_id=%s media_id=%s", comment_id, media_id)
            record["errors"].append("problem_not_found")
            return
        record = new_record(comment, body.get("entry_time"), str(received), config, problem)
        result = combine(
            comment_id, record["text"], problem, config, credentials,
            media_id=media_id,
        )
        judged_at = utc_now()
        reply = write_reply(
            result, comment_id, record["text"], problem,
            variant=config.reply_variant,
            openai_api_key=credentials["openai_api_key"], model=config.luna_model,
            anthropic_api_key=credentials.get("anthropic_api_key", ""),
            haiku_effort=config.haiku_effort,
        )
        apply_decision(record, result, reply, judged_at=judged_at)
        if reply.text:
            # This is the sole 200-character truncation boundary.
            sent_text = reply.text[:200]
            record["reply"]["text"] = sent_text
            record["reply"]["reply_id"] = reply_to_comment(
                comment_id, sent_text, credentials["ig_access_token"],
                base_url=config.graph_api_base,
            )
            record["times"]["replied_at"] = utc_now()
    except Exception as exc:
        record["errors"].append(f"processing: {type(exc).__name__}: {exc}")
        raise
    finally:
        _write_best_effort(record, config, s3_client)


def lambda_handler(event: Mapping[str, Any], context: Any) -> dict[str, Any]:
    """Return SQS ReportBatchItemFailures for only failed message IDs."""
    config = Config.from_env()
    config.require("secret_arn", "assets_bucket", "comment_log_bucket")
    credentials = get_secrets(config.secret_arn)
    require_keys(
        credentials, "ig_access_token", "ig_user_id", "openai_api_key", "typesafe_api_key",
    )
    import boto3

    s3_client = boto3.client("s3")
    failures = []
    for message in event.get("Records", []):
        message_id = message.get("messageId", "")
        try:
            body = json.loads(message["body"])
            if not isinstance(body, dict):
                raise ValueError("SQS body must be an object")
            process_message(body, config, credentials, s3_client=s3_client)
        except Exception:
            LOGGER.exception("reply processing failed: message_id=%s", message_id)
            failures.append({"itemIdentifier": message_id})
    return {"batchItemFailures": failures}
