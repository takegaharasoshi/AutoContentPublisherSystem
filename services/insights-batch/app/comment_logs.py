"""Import comment log records from S3 into Aurora."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime, timedelta, timezone
import json
import logging
from typing import Any, Iterable, Mapping


logger = logging.getLogger(__name__)

_SELECT_BATCH_SIZE = 500
_INSERT_SQL = """INSERT IGNORE INTO umigame_comment_logs (
    comment_id, set_id, parent_id, media_id, content_key,
    problem_schema_version, fact_sheet_hash, commenter_id, comment_text,
    comment_created_at, webhook_received_at, judged_at, replied_at,
    judge_mode, reply_variant, prompt_version, final_kind, final_decision,
    reply_text, reply_source, reply_id, error_count, record_json, s3_key,
    imported_at
) VALUES (
    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
)"""


@dataclass(frozen=True)
class CommentLogImportResult:
    """Counts for one S3 comment log import run."""

    listed: int
    fetched: int
    inserted: int
    skipped_invalid: int
    deleted_expired: int


def _as_utc(moment: datetime) -> datetime:
    """Return a datetime as aware UTC, treating naive input as UTC."""
    if moment.tzinfo is None:
        return moment.replace(tzinfo=timezone.utc)
    return moment.astimezone(timezone.utc)


def _naive_utc(moment: datetime) -> datetime:
    """Convert an aware or naive datetime to naive UTC for MySQL DATETIME."""
    return _as_utc(moment).replace(tzinfo=None)


def _parse_iso_datetime(value: Any) -> datetime:
    """Parse an ISO 8601 timestamp and return naive UTC."""
    if not isinstance(value, str) or not value:
        raise ValueError("timestamp must be a non-empty ISO 8601 string")
    normalized = value[:-1] + "+00:00" if value.endswith("Z") else value
    parsed = datetime.fromisoformat(normalized)
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc).replace(tzinfo=None)


def _without_usernames(value: Any) -> Any:
    """Return a JSON-compatible deep copy without username keys."""
    if isinstance(value, dict):
        return {
            key: _without_usernames(item)
            for key, item in value.items()
            if key != "username"
        }
    if isinstance(value, list):
        return [_without_usernames(item) for item in value]
    return value


def _chunks(values: list[str], size: int) -> Iterable[list[str]]:
    for start in range(0, len(values), size):
        yield values[start : start + size]


def _row_value(row: Any, key: str) -> Any:
    """Read a selected column from tuple and mapping cursor rows."""
    if isinstance(row, Mapping):
        return row[key]
    return row[0]


def _existing_comment_ids(cursor: Any, comment_ids: list[str]) -> set[str]:
    """Return IDs already stored, querying in bounded batches."""
    existing: set[str] = set()
    for batch in _chunks(list(dict.fromkeys(comment_ids)), _SELECT_BATCH_SIZE):
        placeholders = ", ".join(["%s"] * len(batch))
        cursor.execute(
            "SELECT comment_id FROM umigame_comment_logs "
            f"WHERE comment_id IN ({placeholders})",
            tuple(batch),
        )
        existing.update(str(_row_value(row, "comment_id")) for row in cursor.fetchall())
    return existing


def _list_json_keys(
    s3_client: Any, *, bucket: str, prefix: str
) -> list[str]:
    """List all JSON object keys under a prefix, following S3 continuation tokens."""
    keys: list[str] = []
    continuation_token: str | None = None
    while True:
        request: dict[str, Any] = {"Bucket": bucket, "Prefix": prefix}
        if continuation_token is not None:
            request["ContinuationToken"] = continuation_token
        response = s3_client.list_objects_v2(**request)
        for item in response.get("Contents", []):
            key = item.get("Key")
            if isinstance(key, str) and key.endswith(".json"):
                keys.append(key)
        if not response.get("IsTruncated", False):
            break
        next_token = response.get("NextContinuationToken")
        if not next_token:
            raise RuntimeError("S3 list_objects_v2 omitted its continuation token")
        continuation_token = next_token
    return keys


def _read_body(response: Any) -> Any:
    body = response["Body"]
    return body.read() if hasattr(body, "read") else body


def _validated_record(record: Any, *, comment_id: str, set_code: str) -> dict[str, Any]:
    """Validate required schema-v1 fields and remove usernames."""
    if not isinstance(record, dict):
        raise ValueError("record must be an object")
    if type(record.get("schema_version")) is not int or record["schema_version"] != 1:
        raise ValueError("unsupported schema version")
    if record.get("comment_id") != comment_id:
        raise ValueError("comment ID does not match object key")
    if record.get("set_code") != set_code:
        raise ValueError("set code does not match import target")
    if not isinstance(record.get("text"), str):
        raise ValueError("comment text must be a string")
    times = record.get("times")
    if not isinstance(times, dict):
        raise ValueError("times must be an object")
    _parse_iso_datetime(times.get("webhook_received_at"))
    return _without_usernames(record)


def _optional_time(times: Mapping[str, Any], name: str) -> datetime | None:
    value = times.get(name)
    if value is None or value == "":
        return None
    return _parse_iso_datetime(value)


def _mapping(value: Any) -> Mapping[str, Any]:
    return value if isinstance(value, dict) else {}


def _insert_values(
    record: dict[str, Any], *, set_id: int, s3_key: str, imported_at: datetime
) -> tuple[Any, ...]:
    times = _mapping(record.get("times"))
    config = _mapping(record.get("config"))
    final = _mapping(record.get("final"))
    reply = _mapping(record.get("reply"))
    errors = record.get("errors")
    error_count = len(errors) if isinstance(errors, list) else 0
    return (
        record["comment_id"],
        set_id,
        record.get("parent_id"),
        record.get("media_id"),
        record.get("content_key"),
        record.get("problem_schema_version"),
        record.get("fact_sheet_hash"),
        record.get("commenter_id"),
        record["text"],
        _optional_time(times, "comment_created_at"),
        _parse_iso_datetime(times["webhook_received_at"]),
        _optional_time(times, "judged_at"),
        _optional_time(times, "replied_at"),
        config.get("judge_mode"),
        config.get("reply_variant"),
        config.get("prompt_version"),
        final.get("kind"),
        final.get("decision"),
        reply.get("text"),
        reply.get("source"),
        reply.get("reply_id"),
        error_count,
        json.dumps(record, ensure_ascii=False),
        s3_key,
        imported_at,
    )


def import_comment_logs(
    cursor: Any,
    connection: Any,
    *,
    set_id: int,
    set_code: str,
    bucket: str,
    now: datetime,
    lookback_days: int,
    retention_days: int,
    s3_client: Any,
) -> CommentLogImportResult:
    """Import recent S3 comment records and delete expired rows.

    Retention is measured from ``webhook_received_at`` (the acquisition time)
    so that rows are kept at most ``retention_days`` after receipt, matching
    the privacy policy.
    """
    now_utc = _as_utc(now)
    imported_at = now_utc.replace(tzinfo=None)
    cutoff = (now_utc - timedelta(days=retention_days)).replace(tzinfo=None)
    first_date: date = (now_utc.date() - timedelta(days=lookback_days))

    keys: list[str] = []
    for offset in range(lookback_days + 1):
        current_date = first_date + timedelta(days=offset)
        prefix = f"comment-log/{set_code}/dt={current_date.isoformat()}/"
        keys.extend(_list_json_keys(s3_client, bucket=bucket, prefix=prefix))

    comment_ids = [key.rsplit("/", 1)[-1][:-5] for key in keys]
    existing_ids = _existing_comment_ids(cursor, comment_ids)
    fetched = 0
    inserted = 0
    skipped_invalid = 0
    for key, comment_id in zip(keys, comment_ids):
        if comment_id in existing_ids:
            continue
        response = s3_client.get_object(Bucket=bucket, Key=key)
        fetched += 1
        raw = _read_body(response)
        try:
            if isinstance(raw, bytes):
                raw = raw.decode("utf-8")
            record = _validated_record(
                json.loads(raw), comment_id=comment_id, set_code=set_code
            )
            values = _insert_values(
                record, set_id=set_id, s3_key=key, imported_at=imported_at
            )
        except (UnicodeDecodeError, json.JSONDecodeError, ValueError, TypeError, KeyError):
            logger.warning("Skipping invalid comment log record: key=%s", key)
            skipped_invalid += 1
            continue
        cursor.execute(_INSERT_SQL, values)
        inserted += int(cursor.rowcount or 0)

    connection.commit()
    cursor.execute(
        "DELETE FROM umigame_comment_logs "
        "WHERE set_id = %s AND webhook_received_at < %s",
        (set_id, cutoff),
    )
    deleted_expired = int(cursor.rowcount or 0)
    connection.commit()
    return CommentLogImportResult(
        listed=len(keys),
        fetched=fetched,
        inserted=inserted,
        skipped_invalid=skipped_invalid,
        deleted_expired=deleted_expired,
    )
