"""Instagram insights metric request catalog."""

from __future__ import annotations

from dataclasses import dataclass


# follows_and_unfollows の集計は最大 48 時間遅れる（前日分は未集計のことがある）。
FOLLOWS_BACKFILL_MIN_AGE_DAYS = 2
# 2026-10-14 に 09-17（27 日前）まで取得できることを確認。要求数を抑えるため 30 日まで。
FOLLOWS_BACKFILL_LOOKBACK_DAYS = 30


@dataclass(frozen=True)
class MetricRequest:
    """One Graph API insights request group."""

    metrics: tuple[str, ...]
    metric_type: str | None = None
    breakdown: str | None = None


MEDIA_METRIC_REQUESTS: dict[str, tuple[MetricRequest, ...]] = {
    "reel": (
        MetricRequest(
            (
                "views",
                "reach",
                "likes",
                "comments",
                "saved",
                "shares",
                "total_interactions",
                # follows / profile_visits はリールでは非対応。16-11 の疎通確認
                # （2026-08-10、v25.0）で実 API が 400 を返すことを確認したため
                # 定数から外した（自動縮退のプローブ 1 往復を省く）。
                "ig_reels_video_view_total_time",
                "ig_reels_avg_watch_time",
                "reels_skip_rate",
                "reposts",
            )
        ),
    ),
    "feed_image": (
        MetricRequest(
            (
                "views",
                "reach",
                "likes",
                "comments",
                "saved",
                "shares",
                "total_interactions",
                "follows",
                "profile_visits",
            )
        ),
        MetricRequest(("profile_activity",), breakdown="action_type"),
    ),
    "story": (
        MetricRequest(
            (
                "views",
                "reach",
                "replies",
                "shares",
                "total_interactions",
                "follows",
                "profile_visits",
            )
        ),
        MetricRequest(
            ("navigation",), breakdown="story_navigation_action_type"
        ),
    ),
}

FOLLOWS_AND_UNFOLLOWS_REQUEST = MetricRequest(
    ("follows_and_unfollows",),
    metric_type="total_value",
    breakdown="follow_type",
)


ACCOUNT_METRIC_REQUESTS: tuple[MetricRequest, ...] = (
    MetricRequest(
        (
            "views",
            "reach",
            "accounts_engaged",
            "total_interactions",
            "likes",
            "comments",
            "saves",
            "shares",
            "replies",
            "profile_links_taps",
        ),
        metric_type="total_value",
    ),
    FOLLOWS_AND_UNFOLLOWS_REQUEST,
)

# Removed metric names must not be reintroduced: impressions, plays,
# video_views, clips_replays_count, ig_reels_aggregated_all_plays_count,
# engagement, profile_views, website_clicks.
