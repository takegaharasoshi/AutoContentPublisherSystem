"""Tests for the runtime-only prebuilt ranking video generator."""

from __future__ import annotations

import datetime
import json
from unittest.mock import Mock

import pytest

from app.generators import GeneratorContext
from app.generators import ranking_prebuilt as ranking
from app.models import PromptConfig


def _parameters(*, include_night: bool = False) -> str:
    slots = [
        {"from_jst_hour": 0, "slot_code": "day", "duration_seconds": 20},
    ]
    if include_night:
        slots.append(
            {"from_jst_hour": 18, "slot_code": "night", "duration_seconds": 30}
        )
    return json.dumps({"slots": slots})


def _content_fields(**updates: object) -> dict[str, object]:
    fields: dict[str, object] = {
        "hook": "あなたの県は何位？",
        "trivia": "地域ごとに違いがあります。",
        "source_display": "総務省統計をもとに作成",
        "result_list": "1位 A県\n2位 B県\n3位 C県\n4位 D県\n5位 E県",
        "value_prefix": None,
    }
    fields.update(updates)
    return fields


def _ranking_data(**updates: object) -> dict[str, object]:
    data: dict[str, object] = {
        "entries": [
            {"rank": rank, "pref_code": rank, "value": rank * 10}
            for rank in range(1, 6)
        ]
    }
    data.update(updates)
    return data


def _stock_row(
    *,
    fields: dict[str, object] | None = None,
    ranking_data: dict[str, object] | None = None,
    title: object = "住みたい都道府県ランキング",
    format_name: object = "top5-map",
    audio_asset_id: int | None = 77,
    last_used_at: datetime.datetime | None = None,
    video_s3_key: object = "assets/ranking/prebuilt/001_20s.mp4",
) -> tuple[object, ...]:
    return (
        91,
        format_name,
        title,
        json.dumps(fields or _content_fields(), ensure_ascii=False),
        json.dumps(ranking_data or _ranking_data(), ensure_ascii=False),
        video_s3_key,
        audio_asset_id,
        last_used_at,
    )


class Cursor:
    """Cursor fake for the prebuilt ranking generator's query sequence."""

    def __init__(
        self,
        *,
        stock_row: tuple[object, ...] | None = None,
        unbuilt_count: int = 0,
    ) -> None:
        self.stock_row = _stock_row() if stock_row is None else stock_row
        self.unbuilt_count = unbuilt_count
        self.calls: list[tuple[str, tuple[object, ...]]] = []
        self.current = ""

    def execute(self, sql: str, params: tuple[object, ...]) -> None:
        self.calls.append((sql, params))
        self.current = sql

    def fetchone(self) -> tuple[object, ...] | None:
        if "COUNT(*)" in self.current:
            return (self.unbuilt_count,)
        if "FROM ranking_stock_items" in self.current:
            return self.stock_row
        raise AssertionError(f"Unexpected fetchone: {self.current}")


def _context(
    cursor: Cursor,
    *,
    scheduled_at: datetime.datetime = datetime.datetime(
        2026, 8, 7, tzinfo=datetime.timezone.utc
    ),
    parameters: str | None = None,
) -> GeneratorContext:
    return GeneratorContext(
        prompt_config=PromptConfig(5, 9, "unused", None, parameters or _parameters()),
        cursor=cursor,
        s3_client=Mock(),
        s3_bucket="bucket",
        scheduled_at=scheduled_at,
        generation_run_id=123,
    )


@pytest.mark.parametrize(
    ("duration_seconds", "key_column", "video_key"),
    [
        (20, "video_s3_key_20s", "assets/ranking/prebuilt/001_20s.mp4"),
        (30, "video_s3_key_30s", "assets/ranking/prebuilt/001_30s.mp4"),
    ],
)
def test_generate_fetches_selected_duration_and_stages_history_and_lru(
    monkeypatch: pytest.MonkeyPatch,
    duration_seconds: int,
    key_column: str,
    video_key: str,
) -> None:
    cursor = Cursor(stock_row=_stock_row(video_s3_key=video_key))
    get_object = Mock(return_value=b"prebuilt-mp4")
    monkeypatch.setattr(ranking, "get_object", get_object)
    used_at = datetime.datetime(2026, 8, 7, 3, 4, 5)
    monkeypatch.setattr(ranking, "now_utc", lambda: used_at)
    parameters = json.dumps(
        {
            "slots": [
                {
                    "from_jst_hour": 0,
                    "slot_code": "any",
                    "duration_seconds": duration_seconds,
                }
            ]
        }
    )

    context = _context(cursor, parameters=parameters)
    result = ranking.generate(context)

    assert result.media[0].content == b"prebuilt-mp4"
    assert result.media[0].file_format == "mp4"
    assert result.media[0].width == 1080
    assert result.media[0].height == 1920
    assert result.media[0].duration_seconds == duration_seconds
    assert result.media[0].audio_asset_id == 77
    assert result.intermediates == []
    assert key_column in cursor.calls[0][0]
    get_object.assert_called_once_with("bucket", video_key, client=context.s3_client)
    queries = [call[0] for call in cursor.calls]
    assert "INSERT INTO ranking_items" in queries[2]
    assert "use_count = use_count + 1" in queries[3]
    assert cursor.calls[3][1] == (used_at, 91)
    assert cursor.calls[2][1][6] == duration_seconds
    assert cursor.calls[2][1][7] == 91


def _slot_parameters(**updates: object) -> str:
    slot: dict[str, object] = {
        "from_jst_hour": 0,
        "slot_code": "x",
        "duration_seconds": 20,
    }
    slot.update(updates)
    for name, value in list(slot.items()):
        if value is None:
            del slot[name]
    return json.dumps({"slots": [slot]})


@pytest.mark.parametrize(
    "parameters, message",
    [
        ("{}", "parameters.slots"),
        (
            _slot_parameters(duration_seconds=25),
            "duration_seconds must be 20 or 30",
        ),
        (
            _slot_parameters(duration_seconds="20"),
            "duration_seconds must be an integer",
        ),
        (_slot_parameters(duration_seconds=None), "duration_seconds"),
        (_slot_parameters(from_jst_hour=24), "from_jst_hour"),
    ],
)
def test_parse_parameters_rejects_invalid_slots(parameters: str, message: str) -> None:
    with pytest.raises(RuntimeError, match=message):
        ranking._parse_parameters(parameters)


@pytest.mark.parametrize(
    ("scheduled_at", "expected_duration", "key_column"),
    [
        (
            datetime.datetime(2026, 8, 7, 3, tzinfo=datetime.timezone.utc),
            20,
            "video_s3_key_20s",
        ),
        (
            datetime.datetime(2026, 8, 7, 10, tzinfo=datetime.timezone.utc),
            30,
            "video_s3_key_30s",
        ),
    ],
)
def test_generate_resolves_jst_slot_duration(
    monkeypatch: pytest.MonkeyPatch,
    scheduled_at: datetime.datetime,
    expected_duration: int,
    key_column: str,
) -> None:
    cursor = Cursor(stock_row=_stock_row(video_s3_key="selected.mp4"))
    monkeypatch.setattr(ranking, "get_object", lambda *args, **kwargs: b"video")
    result = ranking.generate(
        _context(
            cursor,
            scheduled_at=scheduled_at,
            parameters=_parameters(include_night=True),
        )
    )

    assert key_column in cursor.calls[0][0]
    assert result.media[0].duration_seconds == expected_duration


def test_generate_fails_when_no_built_stock_exists() -> None:
    cursor = Cursor()
    cursor.stock_row = None
    with pytest.raises(RuntimeError, match="set_id=9 duration_seconds=20"):
        ranking.generate(_context(cursor))


def test_generate_warns_for_unbuilt_and_reused_stock(
    monkeypatch: pytest.MonkeyPatch,
    caplog: pytest.LogCaptureFixture,
) -> None:
    cursor = Cursor(
        stock_row=_stock_row(last_used_at=datetime.datetime(2026, 8, 1)),
        unbuilt_count=2,
    )
    monkeypatch.setattr(ranking, "get_object", lambda *args, **kwargs: b"video")

    ranking.generate(_context(cursor))

    assert "being reused" in caplog.text
    assert "remain unbuilt" in caplog.text


@pytest.mark.parametrize(
    "stock_row, message",
    [
        (_stock_row(title=""), "ranking_stock_items.title is required"),
        (
            _stock_row(fields=_content_fields(hook="")),
            "content_fields.hook is required",
        ),
        (
            _stock_row(
                ranking_data=_ranking_data(
                    entries=[{"rank": rank} for rank in range(1, 5)]
                )
            ),
            "exactly five",
        ),
        (
            _stock_row(ranking_data=_ranking_data(entries=[{"rank": 1}] * 5)),
            "ranks 1 through 5",
        ),
        (_stock_row(audio_asset_id=None), "video_audio_asset_id is required"),
    ],
)
def test_generate_rejects_invalid_stock_fields(
    stock_row: tuple[object, ...],
    message: str,
) -> None:
    with pytest.raises(RuntimeError, match=message):
        ranking.generate(_context(Cursor(stock_row=stock_row)))
