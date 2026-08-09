"""Repository functions for post insights snapshots."""

from __future__ import annotations

import datetime
import json
from typing import Any


def fetch_collected_post_ids(
    cursor: Any,
    *,
    set_id: int,
    scheduled_at: datetime.datetime,
) -> set[int]:
    """Fetch post IDs already snapshotted by this scheduled run."""
    cursor.execute(
        "SELECT post_id FROM post_insights WHERE set_id = %s AND scheduled_at = %s",
        (set_id, scheduled_at),
    )
    return {row[0] for row in cursor.fetchall()}


def insert_post_insights(
    cursor: Any,
    *,
    set_id: int,
    post_id: int,
    scheduled_at: datetime.datetime,
    collected_at: datetime.datetime,
    metrics: dict[str, Any],
    api_version: str,
) -> bool:
    """Insert one idempotent post insights snapshot."""
    affected = cursor.execute(
        "INSERT IGNORE INTO post_insights "
        "(set_id, post_id, scheduled_at, collected_at, metrics, api_version) "
        "VALUES (%s, %s, %s, %s, %s, %s)",
        (
            set_id,
            post_id,
            scheduled_at,
            collected_at,
            json.dumps(metrics, ensure_ascii=False),
            api_version,
        ),
    )
    return affected == 1
