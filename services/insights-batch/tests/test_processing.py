"""Tests for partial-failure insights account processing."""

from __future__ import annotations

import datetime
from unittest.mock import Mock

from acps_shared.instagram import (
    InstagramInsightsUnavailable,
    InstagramObjectUnavailable,
    InstagramRateLimited,
)

from app.models import Post, SnsAccount
from app import processing
from app.insights_api import MetricsRequestUnsupported


NOW = datetime.datetime(2026, 8, 10, 9)
SCHEDULED = datetime.datetime(2026, 8, 10, 9)
ACCOUNT = SnsAccount(7, "instagram", "main", "Main")


class Connection:
    """Connection double tracking transaction boundaries."""

    def __init__(self) -> None:
        self.commits = 0
        self.rollbacks = 0

    def commit(self) -> None:
        self.commits += 1

    def rollback(self) -> None:
        self.rollbacks += 1


def _patch_base(monkeypatch, posts: list[Post], collected: set[int] | None = None):
    monkeypatch.setattr(
        processing,
        "get_secret_string",
        lambda name, client=None: '{"access_token":"token","ig_user_id":"user"}',
    )
    monkeypatch.setattr(processing, "fetch_latest_metric_date", lambda *args: NOW.date())
    monkeypatch.setattr(processing, "resolve_target_dates", lambda *args, **kwargs: [])
    monkeypatch.setattr(processing, "fetch_collectible_posts", lambda *args, **kwargs: posts)
    monkeypatch.setattr(
        processing,
        "fetch_collected_post_ids",
        lambda *args, **kwargs: set() if collected is None else collected,
    )
    monkeypatch.setattr(processing, "insert_post_insights", lambda *args, **kwargs: True)


def _run(connection: Connection):
    return processing.process_accounts(
        object(),
        connection,
        set_id=1,
        accounts=[ACCOUNT],
        env_name="prod",
        set_code="set-a",
        scheduled_at=SCHEDULED,
        media_lookback_days=14,
        current_time=NOW,
    )


def test_partial_media_failure_continues(monkeypatch) -> None:
    """A failed post is counted while later posts are still collected."""
    posts = [
        Post(1, "reel", "media-1", NOW),
        Post(2, "reel", "media-2", NOW),
    ]
    _patch_base(monkeypatch, posts)
    calls = 0

    def fetch(*args, **kwargs):
        nonlocal calls
        calls += 1
        if calls == 1:
            raise RuntimeError("one post failed")
        return {"reach": 1}

    monkeypatch.setattr(processing, "fetch_media_insights", fetch)
    result = _run(Connection())
    assert calls == 2
    assert result.records_inserted == 1
    assert result.failure_count == 1


def test_object_unavailable_skip_is_not_failure_when_another_succeeds(monkeypatch) -> None:
    """A deleted media object is a warning skip rather than a failure."""
    posts = [Post(1, "story", "missing", NOW), Post(2, "story", "ok", NOW)]
    _patch_base(monkeypatch, posts)

    def fetch(media_id, *args, **kwargs):
        if media_id == "missing":
            raise InstagramObjectUnavailable("does not exist", status=400)
        return {"views": 1}

    monkeypatch.setattr(processing, "fetch_media_insights", fetch)
    result = _run(Connection())
    assert result.records_inserted == 1
    assert result.failure_count == 0


def test_insights_below_viewer_threshold_is_skipped_not_failed(monkeypatch) -> None:
    """Meta's viewer-threshold refusal skips the media without a failure.

    Low-reach stories hit this on every run, so counting it as a failure would
    make the batch alarm twice a day indefinitely (16-11 の疎通確認で判明)。
    """
    posts = [Post(1, "story", "quiet", NOW), Post(2, "reel", "ok", NOW)]
    _patch_base(monkeypatch, posts)

    def fetch(media_id, *args, **kwargs):
        if media_id == "quiet":
            raise InstagramInsightsUnavailable(
                "(#10) Not enough viewers for the media to show insights",
                status=400,
                code=10,
            )
        return {"views": 1}

    monkeypatch.setattr(processing, "fetch_media_insights", fetch)
    result = _run(Connection())
    assert result.records_inserted == 1
    assert result.failure_count == 0


def test_all_insights_below_threshold_does_not_trip_permission_guard(
    monkeypatch,
) -> None:
    """The all-unavailable permission guard ignores viewer-threshold skips.

    The API answered with a media-specific refusal, which proves the token and
    permission are fine — unlike an object that cannot be loaded at all.
    """
    _patch_base(monkeypatch, [Post(1, "story", "quiet", NOW)])
    monkeypatch.setattr(
        processing,
        "fetch_media_insights",
        lambda *args, **kwargs: (_ for _ in ()).throw(
            InstagramInsightsUnavailable("Not enough viewers", status=400, code=10)
        ),
    )
    result = _run(Connection())
    assert result.failure_count == 0


def test_all_objects_unavailable_guard_is_failure(monkeypatch) -> None:
    """All-unavailable media collection triggers the permission safety guard."""
    _patch_base(monkeypatch, [Post(1, "reel", "missing", NOW)])
    monkeypatch.setattr(
        processing,
        "fetch_media_insights",
        lambda *args, **kwargs: (_ for _ in ()).throw(
            InstagramObjectUnavailable("cannot be loaded", status=400)
        ),
    )
    result = _run(Connection())
    assert result.failure_count == 1


def test_three_consecutive_rate_limits_stop_account(monkeypatch) -> None:
    """A fourth media call is suppressed after three terminal rate limits."""
    posts = [Post(index, "reel", str(index), NOW) for index in range(1, 5)]
    _patch_base(monkeypatch, posts)
    calls = 0

    def fetch(*args, **kwargs):
        nonlocal calls
        calls += 1
        raise InstagramRateLimited("busy", status=429)

    monkeypatch.setattr(processing, "fetch_media_insights", fetch)
    result = _run(Connection())
    assert calls == 3
    assert result.failure_count == 3


def test_previously_collected_posts_skip_api_calls(monkeypatch) -> None:
    """Run-level idempotency is checked before making a Graph API request."""
    _patch_base(monkeypatch, [Post(1, "reel", "media", NOW)], {1})
    fetch = lambda *args, **kwargs: (_ for _ in ()).throw(AssertionError("called"))
    monkeypatch.setattr(processing, "fetch_media_insights", fetch)
    result = _run(Connection())
    assert result.records_inserted == 0
    assert result.failure_count == 0


def test_unsupported_media_metrics_fail_without_insert(monkeypatch) -> None:
    """No post snapshot is written when every metric request is unsupported."""
    _patch_base(monkeypatch, [Post(1, "reel", "media", NOW)])
    monkeypatch.setattr(
        processing,
        "fetch_media_insights",
        lambda *args, **kwargs: (_ for _ in ()).throw(
            MetricsRequestUnsupported("target=reel unsupported=views")
        ),
    )
    insert = Mock()
    monkeypatch.setattr(processing, "insert_post_insights", insert)
    result = _run(Connection())
    assert result.failure_count == 1
    assert result.records_inserted == 0
    insert.assert_not_called()


def test_account_daily_rows_commit_individually_and_latest_has_followers(monkeypatch) -> None:
    """Daily backfill is ascending, committed per row, and only the last gets balance."""
    _patch_base(monkeypatch, [])
    dates = [datetime.date(2026, 8, 8), datetime.date(2026, 8, 9)]
    monkeypatch.setattr(processing, "resolve_target_dates", lambda *args, **kwargs: dates)
    monkeypatch.setattr(processing, "fetch_account_insights", lambda *args, **kwargs: {})
    follower = []
    monkeypatch.setattr(
        processing,
        "fetch_followers_count",
        lambda *args, **kwargs: follower.append(True) or 42,
    )
    inserted_followers = []

    def insert(*args, **kwargs):
        inserted_followers.append(kwargs["followers_count"])
        return True

    monkeypatch.setattr(processing, "insert_account_insights", insert)
    connection = Connection()
    result = _run(connection)
    assert inserted_followers == [None, 42]
    assert follower == [True]
    assert connection.commits == 2
    assert result.records_inserted == 2


def test_account_object_unavailable_is_failure(monkeypatch) -> None:
    """An unreadable account object fails loudly instead of being skipped."""
    _patch_base(monkeypatch, [])
    monkeypatch.setattr(
        processing,
        "resolve_target_dates",
        lambda *args, **kwargs: [datetime.date(2026, 8, 9)],
    )
    monkeypatch.setattr(
        processing,
        "fetch_account_insights",
        lambda *args, **kwargs: (_ for _ in ()).throw(
            InstagramObjectUnavailable("cannot be loaded", status=400)
        ),
    )
    insert = Mock()
    monkeypatch.setattr(processing, "insert_account_insights", insert)
    result = _run(Connection())
    assert result.failure_count == 1
    assert result.records_inserted == 0
    insert.assert_not_called()


def test_credential_failure_counts_one_account_failure(monkeypatch) -> None:
    """A malformed Secret skips the account without exposing its value."""
    monkeypatch.setattr(
        processing,
        "get_secret_string",
        lambda *args, **kwargs: (_ for _ in ()).throw(RuntimeError("secret")),
    )
    result = _run(Connection())
    assert result == processing.InsightsCollectionResult(0, 1, 1)
