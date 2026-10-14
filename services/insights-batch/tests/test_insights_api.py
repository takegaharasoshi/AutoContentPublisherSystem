"""Tests for Instagram insights request normalization and fallback."""

from __future__ import annotations

import datetime
import json
from urllib.parse import parse_qs, urlsplit

import pytest

from acps_shared.instagram import InstagramInvalidMetric

from app import insights_api
from app.metrics_catalog import MetricRequest


class Guard:
    """Guard double that immediately runs its request."""

    def call(self, request):
        return request()


class Response:
    """Minimal JSON HTTP response."""

    status = 200
    headers = {}

    def __init__(self, payload) -> None:
        self.payload = payload

    def read(self):
        return json.dumps(self.payload).encode()

    def close(self):
        pass


def test_collect_metrics_normalizes_all_response_shapes() -> None:
    """Values, series, total values, breakdowns, and API names are preserved."""
    payload = {
        "data": [
            {"name": "single", "values": [{"value": 1, "end_time": "a"}]},
            {
                "name": "series",
                "values": [
                    {"value": 2, "end_time": "a"},
                    {"value": 3, "end_time": "b"},
                ],
            },
            {"name": "total", "total_value": {"value": 4}},
            {
                "name": "split",
                "total_value": {"breakdowns": [{"dimension_keys": ["x"]}]},
            },
        ]
    }
    result = insights_api.collect_metrics(
        "1",
        "token",
        MetricRequest(("single", "series", "total", "split")),
        guard=Guard(),
        urlopen=lambda *args, **kwargs: Response(payload),
    )
    assert result == {
        "single": 1,
        "series": [
            {"end_time": "a", "value": 2},
            {"end_time": "b", "value": 3},
        ],
        "total": 4,
        "split": {"breakdowns": [{"dimension_keys": ["x"]}]},
    }


def test_collect_metrics_empty_data_is_normal() -> None:
    """An empty data list produces no zero-filled metrics."""
    assert insights_api.collect_metrics(
        "1",
        "token",
        MetricRequest(("reach",)),
        guard=Guard(),
        urlopen=lambda *args, **kwargs: Response({"data": []}),
    ) == {}


def test_all_invalid_metrics_raise_unsupported(monkeypatch) -> None:
    """A target with no successful metric request fails loudly."""
    monkeypatch.setitem(
        insights_api.MEDIA_METRIC_REQUESTS,
        "reel",
        (MetricRequest(("bad-a", "bad-b")),),
    )

    def collect(*args, **kwargs):
        raise InstagramInvalidMetric("invalid metric", status=400, code=100)

    monkeypatch.setattr(insights_api, "collect_metrics", collect)
    with pytest.raises(insights_api.MetricsRequestUnsupported) as caught:
        insights_api.fetch_media_insights(
            "1", "token", "reel", guard=Guard(), unsupported={}
        )
    assert "target=reel" in str(caught.value)
    assert "bad-a,bad-b" in str(caught.value)


def test_successful_empty_data_returns_empty_metrics(monkeypatch) -> None:
    """A successful response with no data remains a normal empty result."""
    monkeypatch.setitem(
        insights_api.MEDIA_METRIC_REQUESTS,
        "reel",
        (MetricRequest(("reach",)),),
    )
    assert insights_api.fetch_media_insights(
        "1",
        "token",
        "reel",
        guard=Guard(),
        unsupported={},
        urlopen=lambda *args, **kwargs: Response({"data": []}),
    ) == {}


def test_all_invalid_account_metrics_raise_unsupported(monkeypatch) -> None:
    """Account collection also fails when every request group is unsupported."""
    monkeypatch.setattr(
        insights_api,
        "ACCOUNT_METRIC_REQUESTS",
        (MetricRequest(("bad-account",), metric_type="total_value"),),
    )

    def collect(*args, **kwargs):
        raise InstagramInvalidMetric("invalid metric", status=400, code=100)

    monkeypatch.setattr(insights_api, "collect_metrics", collect)
    with pytest.raises(insights_api.MetricsRequestUnsupported) as caught:
        insights_api.fetch_account_insights(
            "user",
            "token",
            datetime.date(2026, 8, 9),
            guard=Guard(),
            unsupported={},
        )
    assert "target=account" in str(caught.value)
    assert "bad-account" in str(caught.value)


def test_invalid_metric_fallback_and_cache(monkeypatch) -> None:
    """A failed group is probed once and cached failures are then excluded."""
    monkeypatch.setitem(
        insights_api.MEDIA_METRIC_REQUESTS,
        "reel",
        (MetricRequest(("good", "bad")),),
    )
    calls: list[tuple[str, ...]] = []

    def collect(object_id, token, request, **kwargs):
        calls.append(request.metrics)
        if "bad" in request.metrics:
            raise InstagramInvalidMetric("bad metric", status=400, code=100)
        return {"good": 1}

    monkeypatch.setattr(insights_api, "collect_metrics", collect)
    unsupported: dict[str, set[str]] = {}
    assert insights_api.fetch_media_insights(
        "1", "token", "reel", guard=Guard(), unsupported=unsupported
    ) == {"good": 1}
    assert unsupported == {"reel": {"bad"}}
    assert insights_api.fetch_media_insights(
        "2", "token", "reel", guard=Guard(), unsupported=unsupported
    ) == {"good": 1}
    assert calls == [("good", "bad"), ("good",), ("bad",), ("good",)]


def test_account_insights_uses_exact_utc_day(monkeypatch) -> None:
    """Account calls pass day period and adjacent UTC epoch boundaries."""
    monkeypatch.setattr(
        insights_api,
        "ACCOUNT_METRIC_REQUESTS",
        (MetricRequest(("reach",), metric_type="total_value"),),
    )
    captured = {}

    def collect(object_id, token, request, **kwargs):
        captured.update(kwargs["extra_params"])
        return {"reach": 1}

    monkeypatch.setattr(insights_api, "collect_metrics", collect)
    result = insights_api.fetch_account_insights(
        "user",
        "token",
        datetime.date(2026, 8, 9),
        guard=Guard(),
        unsupported={},
    )
    start = datetime.datetime(2026, 8, 9, tzinfo=datetime.UTC)
    assert result == {"reach": 1}
    assert captured == {
        "period": "day",
        "since": str(int(start.timestamp())),
        "until": str(int((start + datetime.timedelta(days=1)).timestamp())),
    }


def test_follows_api_preserves_delayed_and_ready_breakdown_shapes() -> None:
    """The previous UTC day can be empty while older dates return both values."""
    closed_date = datetime.date(2026, 10, 13)
    ready_date = closed_date - datetime.timedelta(days=2)
    captured: list[dict[str, list[str]]] = []

    def urlopen(request, *, timeout):
        params = parse_qs(urlsplit(request.full_url).query)
        captured.append(params)
        requested_date = datetime.datetime.fromtimestamp(
            int(params["since"][0]), tz=datetime.UTC
        ).date()
        breakdown = {"dimension_keys": ["follow_type"]}
        if requested_date == ready_date:
            breakdown["results"] = [
                {"dimension_values": ["FOLLOWER"], "value": 3},
                {"dimension_values": ["NON_FOLLOWER"], "value": 2},
            ]
        return Response(
            {
                "data": [
                    {
                        "name": "follows_and_unfollows",
                        "period": "day",
                        "total_value": {"breakdowns": [breakdown]},
                    }
                ]
            }
        )

    delayed = insights_api.fetch_follows_and_unfollows(
        "user",
        "token",
        closed_date,
        guard=Guard(),
        unsupported={},
        urlopen=urlopen,
    )
    ready = insights_api.fetch_follows_and_unfollows(
        "user",
        "token",
        ready_date,
        guard=Guard(),
        unsupported={},
        urlopen=urlopen,
    )

    assert delayed == {"breakdowns": [{"dimension_keys": ["follow_type"]}]}
    assert not insights_api.has_breakdown_results(delayed)
    assert ready == {
        "breakdowns": [
            {
                "dimension_keys": ["follow_type"],
                "results": [
                    {"dimension_values": ["FOLLOWER"], "value": 3},
                    {"dimension_values": ["NON_FOLLOWER"], "value": 2},
                ],
            }
        ]
    }
    assert insights_api.has_breakdown_results(ready)
    assert [params["period"] for params in captured] == [["day"], ["day"]]
    assert [params["metric_type"] for params in captured] == [
        ["total_value"],
        ["total_value"],
    ]
    assert [params["breakdown"] for params in captured] == [
        ["follow_type"],
        ["follow_type"],
    ]
    assert [
        datetime.datetime.fromtimestamp(int(params["since"][0]), tz=datetime.UTC).date()
        for params in captured
    ] == [closed_date, ready_date]
    assert [
        datetime.datetime.fromtimestamp(int(params["until"][0]), tz=datetime.UTC).date()
        for params in captured
    ] == [
        closed_date + datetime.timedelta(days=1),
        ready_date + datetime.timedelta(days=1),
    ]


def test_has_breakdown_results_requires_nonempty_results_list() -> None:
    """Only a nonempty results array signals that Meta has finished aggregating."""
    assert not insights_api.has_breakdown_results(None)
    assert not insights_api.has_breakdown_results({"breakdowns": []})
    assert not insights_api.has_breakdown_results(
        {"breakdowns": [{"dimension_keys": ["follow_type"], "results": []}]}
    )
    assert not insights_api.has_breakdown_results(
        {"breakdowns": [{"dimension_keys": ["follow_type"]}]}
    )
    assert insights_api.has_breakdown_results(
        {"breakdowns": [{"results": [{"value": 0}]}]}
    )


def test_fetch_followers_count_is_best_effort(monkeypatch) -> None:
    """Follower lookup returns None rather than failing collection."""
    class FailingGuard:
        def call(self, request):
            raise RuntimeError("no access")

    assert insights_api.fetch_followers_count(
        "user", "token", guard=FailingGuard()
    ) is None
