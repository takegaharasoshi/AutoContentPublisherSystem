"""Repository and date-window helpers for account insights."""

from __future__ import annotations

import datetime
import json
from typing import Any


def fetch_latest_metric_date(
    cursor: Any, sns_account_id: int
) -> datetime.date | None:
    """Return the latest stored UTC metric date for an account."""
    cursor.execute(
        "SELECT MAX(metric_date) FROM account_insights_daily "
        "WHERE sns_account_id = %s",
        (sns_account_id,),
    )
    row = cursor.fetchone()
    return row[0] if row is not None else None


def resolve_target_dates(
    latest_date: datetime.date | None,
    today_utc: datetime.date,
    *,
    retention_days: int = 90,
) -> list[datetime.date]:
    """Resolve missing closed UTC dates in ascending order."""
    if retention_days < 1:
        raise ValueError("retention_days must be at least 1")
    end = today_utc - datetime.timedelta(days=1)
    retention_start = end - datetime.timedelta(days=retention_days - 1)
    start = (
        latest_date + datetime.timedelta(days=1)
        if latest_date is not None
        else retention_start
    )
    start = max(start, retention_start)
    if start > end:
        return []
    return [
        start + datetime.timedelta(days=offset)
        for offset in range((end - start).days + 1)
    ]


def insert_account_insights(
    cursor: Any,
    *,
    set_id: int,
    sns_account_id: int,
    metric_date: datetime.date,
    metrics: dict[str, Any],
    followers_count: int | None,
    collected_at: datetime.datetime,
    api_version: str,
) -> bool:
    """Insert one idempotent account daily insights row."""
    affected = cursor.execute(
        "INSERT IGNORE INTO account_insights_daily "
        "(set_id, sns_account_id, metric_date, metrics, followers_count, "
        "collected_at, api_version) VALUES (%s, %s, %s, %s, %s, %s, %s)",
        (
            set_id,
            sns_account_id,
            metric_date,
            json.dumps(metrics, ensure_ascii=False),
            followers_count,
            collected_at,
            api_version,
        ),
    )
    return affected == 1
