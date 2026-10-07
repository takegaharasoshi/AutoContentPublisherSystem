"""Build schema-v1 comment records and write them to S3 or a local directory."""

from __future__ import annotations

import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping

from app.config import Config
from app.judge.combiner import Combined
from app.judge.contract import Problem
from app.reply.writer import Reply


PROMPTS_DIR = Path(__file__).resolve().parent / "prompts"


def prompt_version() -> str:
    """Hash the complete set of bundled prompt file names and contents."""
    digest = hashlib.sha256()
    for path in sorted(PROMPTS_DIR.glob("*.txt")):
        digest.update(path.name.encode("utf-8"))
        digest.update(b"\0")
        digest.update(path.read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()[:12]


PROMPT_VERSION = prompt_version()


def utc_now() -> str:
    """Return current UTC time in ISO 8601 with Z suffix."""
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def normalize_time(value: Any) -> str | None:
    """Normalize a Meta epoch timestamp or ISO 8601 string to UTC."""
    if value is None or value == "":
        return None
    try:
        if isinstance(value, (int, float)) or (isinstance(value, str) and value.isdecimal()):
            seconds = float(value)
            if seconds > 10**12:
                seconds /= 1000
            moment = datetime.fromtimestamp(seconds, timezone.utc)
        elif isinstance(value, str):
            moment = datetime.fromisoformat(value.replace("Z", "+00:00"))
            if moment.tzinfo is None:
                moment = moment.replace(tzinfo=timezone.utc)
            moment = moment.astimezone(timezone.utc)
        else:
            return None
    except (ValueError, OverflowError, OSError):
        return None
    return moment.isoformat(timespec="seconds").replace("+00:00", "Z")


def new_record(
    comment: Mapping[str, Any], entry_time: Any, received_at: str,
    config: Config, problem: Problem | None = None,
) -> dict[str, Any]:
    """Build a record from an allowlist, deliberately excluding username."""
    sender = comment.get("from") if isinstance(comment.get("from"), Mapping) else {}
    media = comment.get("media") if isinstance(comment.get("media"), Mapping) else {}
    media_id = str(media.get("id") or comment.get("media_id") or "")
    fact_hash = None
    if problem is not None:
        content = json.dumps(
            [problem.content_key, list(problem.fact_sheet)],
            ensure_ascii=False, separators=(",", ":"),
        )
        fact_hash = hashlib.sha256(content.encode("utf-8")).hexdigest()[:12]
    return {
        "schema_version": 1,
        "comment_id": str(comment.get("id") or ""),
        "parent_id": str(comment["parent_id"]) if comment.get("parent_id") is not None else None,
        "media_id": media_id,
        "set_code": problem.set_code if problem else config.set_code,
        "content_key": problem.content_key if problem else None,
        "problem_schema_version": problem.schema_version if problem else None,
        "fact_sheet_hash": fact_hash,
        "commenter_id": str(sender["id"]) if sender.get("id") is not None else None,
        "text": str(comment.get("text") or ""),
        "times": {
            "comment_created_at": normalize_time(entry_time) or normalize_time(comment.get("timestamp")),
            "webhook_received_at": normalize_time(received_at) or received_at,
            "judged_at": None, "replied_at": None,
        },
        "config": {
            "judge_mode": config.judge_mode,
            "shadow": config.shadow,
            "consensus": config.consensus,
            "reply_variant": config.reply_variant,
            "luna_model": config.luna_model,
            "prompt_version": PROMPT_VERSION,
        },
        "judgements": {"luna": None, "jev": None,
                       **({"decisions": None} if config.judge_mode == "decisions" else {})},
        "shadow_mismatch": None,
        "final": {"kind": None, "answer": None, "decision": None},
        "reply": {
            "text": None, "source": "no_reply", "reply_id": None,
            "over_80": False, "guard": None,
        },
        "errors": [],
    }


def apply_decision(
    record: dict[str, Any], combined: Combined, reply: Reply, *, judged_at: str | None = None,
) -> None:
    """Fill judge, final, and writer fields before Graph delivery."""
    record["judgements"] = {
        "luna": combined.luna.as_log() if combined.luna else None,
        "jev": combined.jev.as_log() if combined.jev else None,
    }
    if combined.decisions is not None:
        record["judgements"]["decisions"] = combined.decisions.as_log()
    record["shadow_mismatch"] = combined.mismatch
    record["final"] = combined.final_log()
    record["times"]["judged_at"] = judged_at or utc_now()
    record["reply"].update({"text": reply.text, "source": reply.source,
                            "over_80": reply.over_80, "guard": reply.guard})
    record["errors"].extend(combined.errors)
    if reply.error:
        record["errors"].append(f"writer: {reply.error}")


def record_key(record: Mapping[str, Any]) -> str:
    """Derive the stable S3 key from receive time and set code."""
    received = record["times"]["webhook_received_at"]
    date = (normalize_time(received) or utc_now())[:10]
    set_code = str(record["set_code"])
    comment_id = str(record["comment_id"])
    if not re.fullmatch(r"[A-Za-z0-9_-]+", set_code) or not re.fullmatch(r"[A-Za-z0-9_-]+", comment_id):
        raise ValueError("set_code or comment_id has unsafe path characters")
    return f"comment-log/{set_code}/dt={date}/{comment_id}.json"


def write_record(
    record: Mapping[str, Any], *, bucket: str | None = None,
    directory: Path | None = None, client: Any = None,
) -> str:
    """Write one record to S3 or local storage using the same JSON encoder."""
    if bool(bucket) == bool(directory):
        raise ValueError("provide exactly one of bucket or directory")
    key = record_key(record)
    body = json.dumps(record, ensure_ascii=False, indent=2, sort_keys=True).encode("utf-8")
    if directory is not None:
        target = directory / key
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(body)
        return str(target)
    if client is None:
        import boto3

        client = boto3.client("s3")
    client.put_object(Bucket=bucket, Key=key, Body=body, ContentType="application/json; charset=utf-8")
    return f"s3://{bucket}/{key}"
