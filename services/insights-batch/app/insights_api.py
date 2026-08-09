"""Instagram insights requests and response normalization."""

from __future__ import annotations

import datetime
import logging
from typing import Any
import urllib.request

from acps_shared.instagram import (
    InstagramInvalidMetric,
    RateLimitGuard,
    get_json,
)

from .metrics_catalog import (
    ACCOUNT_METRIC_REQUESTS,
    MEDIA_METRIC_REQUESTS,
    MetricRequest,
)


logger = logging.getLogger(__name__)


class MetricsRequestUnsupported(Exception):
    """Raised when no metrics request can be executed successfully."""


def _normalize_metric(element: dict[str, Any]) -> Any:
    """Normalize one insights response element without renaming it."""
    total_value = element.get("total_value")
    if isinstance(total_value, dict):
        if "breakdowns" in total_value:
            return {"breakdowns": total_value["breakdowns"]}
        if "value" in total_value:
            return total_value["value"]

    values = element.get("values")
    if not isinstance(values, list) or not values:
        return None
    if len(values) == 1 and isinstance(values[0], dict):
        return values[0].get("value")
    return [
        {"end_time": value.get("end_time"), "value": value.get("value")}
        for value in values
        if isinstance(value, dict)
    ]


def collect_metrics(
    object_id: str,
    access_token: str,
    request: MetricRequest,
    *,
    guard: RateLimitGuard,
    urlopen: Any = urllib.request.urlopen,
    extra_params: dict[str, str] | None = None,
) -> dict[str, Any]:
    """Collect and normalize one insights metric request group."""
    params = {
        "metric": ",".join(request.metrics),
        "access_token": access_token,
    }
    if request.metric_type is not None:
        params["metric_type"] = request.metric_type
    if request.breakdown is not None:
        params["breakdown"] = request.breakdown
    if extra_params:
        params.update(extra_params)
    response = guard.call(
        lambda: get_json(
            f"/{object_id}/insights",
            params,
            urlopen=urlopen,
        )
    )
    data = response.payload.get("data")
    if not isinstance(data, list):
        return {}
    normalized: dict[str, Any] = {}
    for element in data:
        if not isinstance(element, dict) or not isinstance(element.get("name"), str):
            continue
        normalized[element["name"]] = _normalize_metric(element)
    return normalized


def _collect_with_fallback(
    object_id: str,
    access_token: str,
    request: MetricRequest,
    *,
    cache_key: str,
    guard: RateLimitGuard,
    unsupported: dict[str, set[str]],
    urlopen: Any,
    extra_params: dict[str, str] | None = None,
) -> tuple[dict[str, Any], bool]:
    """Collect a group, probing individual metrics after an invalid group."""
    known_unsupported = unsupported.setdefault(cache_key, set())
    remaining = tuple(
        metric for metric in request.metrics if metric not in known_unsupported
    )
    if not remaining:
        return {}, False
    filtered_request = MetricRequest(
        remaining,
        metric_type=request.metric_type,
        breakdown=request.breakdown,
    )
    try:
        return (
            collect_metrics(
                object_id,
                access_token,
                filtered_request,
                guard=guard,
                urlopen=urlopen,
                extra_params=extra_params,
            ),
            True,
        )
    except InstagramInvalidMetric:
        if len(remaining) == 1:
            metric = remaining[0]
            if metric not in known_unsupported:
                known_unsupported.add(metric)
                logger.warning(
                    "Unsupported Instagram insights metric: target=%s metric=%s",
                    cache_key,
                    metric,
                )
            return {}, False

    collected: dict[str, Any] = {}
    executed_ok = False
    for metric in remaining:
        single_request = MetricRequest(
            (metric,),
            metric_type=request.metric_type,
            breakdown=request.breakdown,
        )
        try:
            metric_values = collect_metrics(
                object_id,
                access_token,
                single_request,
                guard=guard,
                urlopen=urlopen,
                extra_params=extra_params,
            )
            executed_ok = True
            collected.update(metric_values)
        except InstagramInvalidMetric:
            if metric not in known_unsupported:
                known_unsupported.add(metric)
                logger.warning(
                    "Unsupported Instagram insights metric: target=%s metric=%s",
                    cache_key,
                    metric,
                )
    return collected, executed_ok


def _unsupported_error(
    cache_key: str, unsupported: set[str]
) -> MetricsRequestUnsupported:
    """Build a diagnostic error for a target with no executable metrics."""
    metric_names = ",".join(sorted(unsupported))
    return MetricsRequestUnsupported(
        "No Instagram insights metrics request succeeded: "
        f"target={cache_key} unsupported={metric_names}"
    )


def fetch_media_insights(
    media_id: str,
    access_token: str,
    media_type: str,
    *,
    guard: RateLimitGuard,
    unsupported: dict[str, set[str]],
    urlopen: Any = urllib.request.urlopen,
) -> dict[str, Any]:
    """Collect all supported metrics for one media object."""
    try:
        requests = MEDIA_METRIC_REQUESTS[media_type]
    except KeyError:
        raise ValueError(f"Unsupported media type: {media_type}") from None
    metrics: dict[str, Any] = {}
    any_executed_ok = False
    for request in requests:
        collected, executed_ok = _collect_with_fallback(
            media_id,
            access_token,
            request,
            cache_key=media_type,
            guard=guard,
            unsupported=unsupported,
            urlopen=urlopen,
        )
        metrics.update(collected)
        any_executed_ok = any_executed_ok or executed_ok
    if not any_executed_ok:
        raise _unsupported_error(media_type, unsupported.get(media_type, set()))
    return metrics


def fetch_account_insights(
    ig_user_id: str,
    access_token: str,
    metric_date: datetime.date,
    *,
    guard: RateLimitGuard,
    unsupported: dict[str, set[str]],
    urlopen: Any = urllib.request.urlopen,
) -> dict[str, Any]:
    """Collect account metrics for exactly one closed UTC day."""
    day_start = datetime.datetime.combine(
        metric_date, datetime.time.min, tzinfo=datetime.UTC
    )
    day_end = day_start + datetime.timedelta(days=1)
    extra_params = {
        "period": "day",
        "since": str(int(day_start.timestamp())),
        "until": str(int(day_end.timestamp())),
    }
    metrics: dict[str, Any] = {}
    any_executed_ok = False
    for request in ACCOUNT_METRIC_REQUESTS:
        collected, executed_ok = _collect_with_fallback(
            ig_user_id,
            access_token,
            request,
            cache_key="account",
            guard=guard,
            unsupported=unsupported,
            urlopen=urlopen,
            extra_params=extra_params,
        )
        metrics.update(collected)
        any_executed_ok = any_executed_ok or executed_ok
    if not any_executed_ok:
        raise _unsupported_error("account", unsupported.get("account", set()))
    return metrics


def fetch_followers_count(
    ig_user_id: str,
    access_token: str,
    *,
    guard: RateLimitGuard,
    urlopen: Any = urllib.request.urlopen,
) -> int | None:
    """Fetch the current follower count, returning None on any failure."""
    try:
        response = guard.call(
            lambda: get_json(
                f"/{ig_user_id}",
                {"fields": "followers_count", "access_token": access_token},
                urlopen=urlopen,
            )
        )
        value = response.payload.get("followers_count")
        if isinstance(value, int) and not isinstance(value, bool):
            return value
        logger.warning("Instagram followers_count was unavailable in the response")
    except Exception as exc:
        logger.warning(
            "Instagram followers_count request failed: error_type=%s",
            type(exc).__name__,
        )
    return None
