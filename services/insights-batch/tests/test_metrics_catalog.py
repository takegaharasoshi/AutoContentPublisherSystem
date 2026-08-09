"""Tests for the fixed Instagram metric request catalog."""

from app.metrics_catalog import ACCOUNT_METRIC_REQUESTS, MEDIA_METRIC_REQUESTS


def test_metric_groups_keep_request_wide_options_separate() -> None:
    """Breakdown and metric type options are attached to whole request groups."""
    assert MEDIA_METRIC_REQUESTS["feed_image"][1].breakdown == "action_type"
    assert MEDIA_METRIC_REQUESTS["story"][1].breakdown == (
        "story_navigation_action_type"
    )
    assert ACCOUNT_METRIC_REQUESTS[0].metric_type == "total_value"
    assert ACCOUNT_METRIC_REQUESTS[1].breakdown == "follow_type"


def test_removed_metric_names_are_absent() -> None:
    """Deprecated Graph API names do not return to any request group."""
    removed = {
        "impressions",
        "plays",
        "video_views",
        "clips_replays_count",
        "ig_reels_aggregated_all_plays_count",
        "engagement",
        "profile_views",
        "website_clicks",
    }
    all_metrics = {
        metric
        for requests in (*MEDIA_METRIC_REQUESTS.values(), ACCOUNT_METRIC_REQUESTS)
        for request in requests
        for metric in request.metrics
    }
    assert all_metrics.isdisjoint(removed)
