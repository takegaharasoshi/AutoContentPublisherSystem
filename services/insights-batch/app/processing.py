"""Account-level insights collection and partial-failure aggregation."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
import datetime
import logging
from typing import Any
import urllib.request

from acps_shared import get_secret_string
from acps_shared.instagram import (
    GRAPH_API_VERSION,
    InstagramInsightsUnavailable,
    InstagramObjectUnavailable,
    InstagramRateLimited,
    RateLimitGuard,
)
from acps_shared.sns_secrets import build_sns_secret_name, parse_sns_secret

from .account_insights import (
    fetch_latest_metric_date,
    insert_account_insights,
    resolve_target_dates,
)
from .clock import now_utc
from .insights_api import (
    fetch_account_insights,
    fetch_followers_count,
    fetch_media_insights,
)
from .models import SnsAccount
from .post_insights import fetch_collected_post_ids, insert_post_insights
from .posts import fetch_collectible_posts


logger = logging.getLogger(__name__)
MAX_CONSECUTIVE_RATE_LIMIT_FAILURES = 3


@dataclass(frozen=True)
class InsightsCollectionResult:
    """Result of collecting insights for all active accounts."""

    records_inserted: int
    failure_count: int
    accounts_processed: int


def _rollback_safely(connection: Any) -> None:
    """Roll back uncommitted work without masking the collection failure."""
    rollback = getattr(connection, "rollback", None)
    if callable(rollback):
        try:
            rollback()
        except Exception:
            logger.exception("インサイト収集処理のロールバックに失敗")


def process_accounts(
    cursor: Any,
    connection: Any,
    *,
    set_id: int,
    accounts: list[SnsAccount],
    env_name: str,
    set_code: str,
    scheduled_at: datetime.datetime,
    media_lookback_days: int,
    secrets_client: Any | None = None,
    urlopen: Any = urllib.request.urlopen,
    current_time: datetime.datetime | None = None,
    guard_factory: Callable[[], RateLimitGuard] = RateLimitGuard,
) -> InsightsCollectionResult:
    """Collect account and media insights with independent failure handling."""
    records_inserted = 0
    failure_count = 0
    unsupported: dict[str, set[str]] = {}
    collection_time = current_time if current_time is not None else now_utc()
    closed_date = collection_time.date() - datetime.timedelta(days=1)

    for account in accounts:
        guard = guard_factory()
        consecutive_rate_limits = 0
        stop_account = False

        try:
            secret_name = build_sns_secret_name(
                env_name,
                set_code,
                account.platform,
                account.account_code,
            )
            credentials = parse_sns_secret(
                get_secret_string(secret_name, client=secrets_client)
            )
        except Exception as exc:
            failure_count += 1
            logger.error(
                "SNS credential retrieval failed: sns_account_id=%s error_type=%s",
                account.id,
                type(exc).__name__,
            )
            continue

        try:
            latest_date = fetch_latest_metric_date(cursor, account.id)
            target_dates = resolve_target_dates(
                latest_date,
                collection_time.date(),
            )
        except Exception as exc:
            failure_count += 1
            logger.error(
                "Account insights date resolution failed: sns_account_id=%s "
                "error_type=%s",
                account.id,
                type(exc).__name__,
            )
            _rollback_safely(connection)
            target_dates = []

        for metric_date in target_dates:
            try:
                metrics = fetch_account_insights(
                    credentials.ig_user_id,
                    credentials.access_token,
                    metric_date,
                    guard=guard,
                    unsupported=unsupported,
                    urlopen=urlopen,
                )
                followers_count = (
                    fetch_followers_count(
                        credentials.ig_user_id,
                        credentials.access_token,
                        guard=guard,
                        urlopen=urlopen,
                    )
                    if metric_date == closed_date
                    else None
                )
                inserted = insert_account_insights(
                    cursor,
                    set_id=set_id,
                    sns_account_id=account.id,
                    metric_date=metric_date,
                    metrics=metrics,
                    followers_count=followers_count,
                    collected_at=now_utc(),
                    api_version=GRAPH_API_VERSION,
                )
                connection.commit()
                records_inserted += int(inserted)
                consecutive_rate_limits = 0
            except Exception as exc:
                failure_count += 1
                _rollback_safely(connection)
                if isinstance(exc, InstagramRateLimited):
                    consecutive_rate_limits += 1
                else:
                    consecutive_rate_limits = 0
                logger.warning(
                    "Account daily insights collection failed: "
                    "sns_account_id=%s metric_date=%s error_type=%s",
                    account.id,
                    metric_date,
                    type(exc).__name__,
                )
                if consecutive_rate_limits >= MAX_CONSECUTIVE_RATE_LIMIT_FAILURES:
                    stop_account = True
                    logger.error(
                        "Stopping account after three consecutive rate-limit "
                        "failures: sns_account_id=%s",
                        account.id,
                    )
                    break

        if stop_account:
            continue

        try:
            posts = fetch_collectible_posts(
                cursor,
                set_id=set_id,
                sns_account_id=account.id,
                now=collection_time,
                media_lookback_days=media_lookback_days,
            )
            collected_post_ids = fetch_collected_post_ids(
                cursor,
                set_id=set_id,
                scheduled_at=scheduled_at,
            )
        except Exception as exc:
            failure_count += 1
            logger.error(
                "Collectible post lookup failed: sns_account_id=%s error_type=%s",
                account.id,
                type(exc).__name__,
            )
            _rollback_safely(connection)
            continue

        attempted_media = 0
        successful_media = 0
        unavailable_media = 0
        for post in posts:
            if post.id in collected_post_ids:
                logger.info(
                    "Post insights already collected; skipping: post_id=%s",
                    post.id,
                )
                continue
            attempted_media += 1
            try:
                metrics = fetch_media_insights(
                    post.platform_post_id,
                    credentials.access_token,
                    post.media_type,
                    guard=guard,
                    unsupported=unsupported,
                    urlopen=urlopen,
                )
                inserted = insert_post_insights(
                    cursor,
                    set_id=set_id,
                    post_id=post.id,
                    scheduled_at=scheduled_at,
                    collected_at=now_utc(),
                    metrics=metrics,
                    api_version=GRAPH_API_VERSION,
                )
                connection.commit()
                records_inserted += int(inserted)
                successful_media += 1
                consecutive_rate_limits = 0
            except InstagramObjectUnavailable:
                unavailable_media += 1
                consecutive_rate_limits = 0
                _rollback_safely(connection)
                logger.warning(
                    "Instagram media object unavailable; skipping: post_id=%s",
                    post.id,
                )
            except InstagramInsightsUnavailable:
                # Meta withholds metrics below its viewer privacy threshold.
                # Permanent for that media and unrelated to our configuration,
                # so skipping keeps low-reach stories from alarming every run.
                consecutive_rate_limits = 0
                _rollback_safely(connection)
                logger.warning(
                    "Insights withheld below Instagram's viewer threshold; "
                    "skipping: post_id=%s media_type=%s",
                    post.id,
                    post.media_type,
                )
            except Exception as exc:
                failure_count += 1
                _rollback_safely(connection)
                if isinstance(exc, InstagramRateLimited):
                    consecutive_rate_limits += 1
                else:
                    consecutive_rate_limits = 0
                logger.warning(
                    "Post insights collection failed: post_id=%s error_type=%s "
                    "code=%s subcode=%s message=%s",
                    post.id,
                    type(exc).__name__,
                    getattr(exc, "code", None),
                    getattr(exc, "subcode", None),
                    getattr(exc, "message", str(exc)),
                )
                if consecutive_rate_limits >= MAX_CONSECUTIVE_RATE_LIMIT_FAILURES:
                    stop_account = True
                    logger.error(
                        "Stopping account after three consecutive rate-limit "
                        "failures: sns_account_id=%s",
                        account.id,
                    )
                    break

        if (
            attempted_media > 0
            and successful_media == 0
            and unavailable_media == attempted_media
        ):
            failure_count += 1
            logger.error(
                "All media objects were unavailable; instagram_manage_insights "
                "permission may be missing: sns_account_id=%s",
                account.id,
            )

    return InsightsCollectionResult(
        records_inserted=records_inserted,
        failure_count=failure_count,
        accounts_processed=len(accounts),
    )
