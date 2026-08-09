"""Repository functions for published posts eligible for insights."""

from __future__ import annotations

import datetime
from typing import Any

from .models import Post


def fetch_collectible_posts(
    cursor: Any,
    *,
    set_id: int,
    sns_account_id: int,
    now: datetime.datetime,
    media_lookback_days: int,
) -> list[Post]:
    """Fetch recent successful posts in chronological order."""
    media_cutoff = now - datetime.timedelta(days=media_lookback_days)
    story_cutoff = now - datetime.timedelta(hours=24)
    cursor.execute(
        "SELECT id, media_type, platform_post_id, posted_at FROM posts "
        "WHERE set_id = %s AND sns_account_id = %s "
        "AND status = 'success' AND platform_post_id IS NOT NULL "
        "AND posted_at IS NOT NULL "
        "AND ( (media_type IN ('feed_image', 'reel') AND posted_at >= %s) "
        "OR (media_type = 'story' AND posted_at >= %s) ) "
        "ORDER BY posted_at ASC, id ASC",
        (set_id, sns_account_id, media_cutoff, story_cutoff),
    )
    return [Post(row[0], row[1], str(row[2]), row[3]) for row in cursor.fetchall()]
