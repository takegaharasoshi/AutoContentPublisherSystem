"""Write the comment reply problem snapshot after a reel is published."""

from __future__ import annotations

import datetime
import json
from typing import Any

from acps_shared.s3 import put_object

from .clock import now_utc
from .umigame_items import fetch_umigame_item


CONTENT_TYPE = "application/json; charset=utf-8"


def _posted_at_utc(posted_at: datetime.datetime) -> str:
    """Format the exact posts.posted_at value as an ISO 8601 UTC timestamp."""
    if posted_at.tzinfo is None:
        posted_at = posted_at.replace(tzinfo=datetime.UTC)
    return posted_at.astimezone(datetime.UTC).isoformat().replace("+00:00", "Z")


def write_problem_snapshot(
    cursor: Any,
    connection: Any,
    *,
    set_id: int,
    set_code: str,
    generation_run_id: int,
    media_id: str,
    posted_at: datetime.datetime,
    s3_bucket: str,
    s3_client: Any,
) -> bool:
    """Upload one snapshot and commit its key, if this run has an umigame item.

    The caller commits the successful post before invoking this function and
    rolls back this function's transaction if it raises.
    """
    item = fetch_umigame_item(cursor, generation_run_id)
    if item is None:
        return False

    cursor.execute(
        "SELECT prompt_text FROM prompt_configs "
        "WHERE set_id = %s AND is_active = 1 ORDER BY id LIMIT 1",
        (set_id,),
    )
    prompt_row = cursor.fetchone()
    if (
        prompt_row is None
        or not isinstance(prompt_row[0], str)
        or not prompt_row[0].strip()
    ):
        raise RuntimeError(
            f"Active prompt_configs.prompt_text is missing: set_id={set_id}"
        )

    key = f"assets/{set_code}/problems/{media_id}.json"
    snapshot = {
        "schema_version": 1,
        "set_code": set_code,
        "media_id": media_id,
        "content_key": item.content_key,
        "posted_at": _posted_at_utc(posted_at),
        "problem_text": item.problem_text,
        "truth": item.truth,
        "fact_sheet": item.fact_sheet,
        "rule_text": item.rule_text,
        "master_rules": prompt_row[0],
    }
    put_object(
        s3_bucket,
        key,
        json.dumps(snapshot, ensure_ascii=False).encode("utf-8"),
        content_type=CONTENT_TYPE,
        client=s3_client,
    )
    cursor.execute(
        "UPDATE umigame_items SET snapshot_s3_key = %s, "
        "snapshot_written_at = %s WHERE id = %s",
        (key, now_utc(), item.id),
    )
    connection.commit()
    return True
