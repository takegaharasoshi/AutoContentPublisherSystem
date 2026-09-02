"""Tests for the stock-backed quiz multi-cut generator."""

from __future__ import annotations

import datetime
from io import BytesIO
import json
from pathlib import Path
from unittest.mock import Mock

from PIL import Image
import pytest

from app.generators import GeneratorContext
from app.generators import gpt_quiz_multicut as quiz
from app.models import PromptConfig


def _slot(
    hour: int = 11,
    quiz_type: str = "L3",
    difficulty: str = "standard",
    slot_code: str = "noon",
    slot_label: str = "昼の推定",
    slot_hook: str = "30秒で解けたら天才",
    **extra: object,
) -> dict[str, object]:
    return {
        "from_jst_hour": hour,
        "quiz_type": quiz_type,
        "difficulty": difficulty,
        "slot_code": slot_code,
        "slot_label": slot_label,
        "slot_hook": slot_hook,
        **extra,
    }


def _parameters(slots: list[dict[str, object]] | None = None) -> str:
    return json.dumps(
        {
            "slots": slots
            or [
                _slot(4, "L1", "light", "morning", "朝のクイズ"),
                _slot(),
                _slot(17, "L1", "deep", "night", "夜のクイズ"),
            ],
            "max_regenerations": "ignored",
            "llm_model": {"also": "ignored"},
        }
    )


def _fields(**updates: object) -> dict[str, object]:
    fields: dict[str, object] = {
        "hook": "推定できる？",
        "hint": "一人あたりから考えよう",
        "question": "日本にある信号機の数を推定してください。",
        "answer": "約20万基（目安）",
        "explanation": "前提から順に分解して概算します。",
        "coach_comment": "推定ルートが大切！",
        "tags": ["脳トレ", "推定", "クイズ"],
        "summary": "日本の信号機数を推定",
        "illustration_scene": "文字のない明るい街角の風景",
    }
    fields.update(updates)
    return fields


def _stock_row(
    *,
    stock_id: int = 91,
    fields: dict[str, object] | None = None,
    last_used_at: datetime.datetime | None = None,
) -> tuple[object, ...]:
    return (
        stock_id,
        "日本にある信号機の数を推定してください。",
        "約20万基（目安）",
        json.dumps(fields or _fields(), ensure_ascii=False),
        last_used_at,
    )


class Cursor:
    """Cursor fake for the generator's fixed query sequence."""

    def __init__(
        self,
        *,
        stock_row: tuple[object, ...] | None = None,
        bgm_row: tuple[object, ...] | None = (77, "audio/quiz/bgm.m4a"),
    ) -> None:
        self.stock_row = _stock_row() if stock_row is None else stock_row
        self.bgm_row = bgm_row
        self.calls: list[tuple[str, tuple[object, ...]]] = []
        self.current = ""

    def execute(self, sql: str, params: tuple[object, ...]) -> None:
        self.calls.append((sql, params))
        self.current = sql

    def fetchone(self) -> tuple[object, ...] | None:
        if "SELECT set_code" in self.current:
            return ("quiz",)
        if "asset_type = 'bgm'" in self.current:
            return self.bgm_row
        if "FROM quiz_stock_items" in self.current:
            return self.stock_row
        raise AssertionError(f"Unexpected fetchone: {self.current}")

    def fetchall(self) -> tuple[tuple[object, ...], ...]:
        if "asset_type = 'se'" in self.current:
            return (
                (81, "audio/quiz/se/countdown_tick.m4a"),
                (82, "audio/quiz/se/answer_chime.m4a"),
            )
        raise AssertionError(f"Unexpected fetchall: {self.current}")


def _context(cursor: Cursor) -> GeneratorContext:
    return GeneratorContext(
        prompt_config=PromptConfig(5, 9, "unused", None, _parameters()),
        cursor=cursor,
        s3_client=Mock(),
        s3_bucket="bucket",
        scheduled_at=datetime.datetime(
            2026, 8, 7, 2, tzinfo=datetime.timezone.utc
        ),
        generation_run_id=123,
    )


def _patch_generate_dependencies(monkeypatch: pytest.MonkeyPatch) -> Mock:
    monkeypatch.setattr(
        quiz,
        "_load_fonts",
        lambda: {"regular": Path("regular"), "bold": Path("bold")},
    )
    monkeypatch.setattr(
        quiz,
        "_load_coach_assets",
        lambda context, set_code: {
            pose: Mock(name=pose) for pose in quiz.COACH_FILENAMES
        },
    )
    monkeypatch.setattr(quiz, "get_object", lambda *args, **kwargs: b"audio")
    monkeypatch.setattr(quiz.openai_image, "load_api_key", lambda: "key")
    monkeypatch.setattr(quiz.openai_image, "build_client", lambda key: object())
    illustration = Mock(return_value=b"illustration")
    monkeypatch.setattr(quiz.openai_image, "request_illustration", illustration)
    monkeypatch.setattr(
        quiz,
        "_render_cards",
        lambda *args: ([b"card"] * 7, [b"cut1", b"cut2", b"cut3"]),
    )
    monkeypatch.setattr(quiz, "_build_video", lambda *args: b"video")
    monkeypatch.setattr(
        quiz,
        "now_utc",
        lambda: datetime.datetime(2026, 8, 7, 3, 4, 5),
    )
    return illustration


def test_parameters_allow_missing_or_ignored_tone_and_llm_settings() -> None:
    slots = quiz._parse_parameters(_parameters([_slot(tone_hint="ignored")]))
    assert slots == [_slot()]


def test_parameters_reject_unknown_quiz_type() -> None:
    with pytest.raises(RuntimeError, match="unknown quiz_type"):
        quiz._parse_parameters(_parameters([_slot(quiz_type="L2")]))


def test_parameters_reject_unknown_slot_palette() -> None:
    with pytest.raises(RuntimeError, match="unknown slot_code"):
        quiz._parse_parameters(_parameters([_slot(slot_code="dawn")]))


def test_parameters_reject_missing_slot_hook() -> None:
    slot = _slot()
    del slot["slot_hook"]
    with pytest.raises(
        RuntimeError,
        match="slots entry is missing required fields: slot_hook",
    ):
        quiz._parse_parameters(_parameters([slot]))


def test_resolve_slot_keeps_jst_boundaries_and_early_wrap() -> None:
    slots = quiz._parse_parameters(_parameters())
    noon = quiz.resolve_slot(
        datetime.datetime(2026, 8, 7, 2, tzinfo=datetime.timezone.utc),
        slots,
    )
    night = quiz.resolve_slot(
        datetime.datetime(2026, 8, 7, 18, tzinfo=datetime.timezone.utc),
        slots,
    )
    assert noon["slot_code"] == "noon"
    assert night["slot_code"] == "night"
    assert "tone_hint" not in noon


def test_fetch_stock_item_uses_lru_query_and_returns_parsed_fields() -> None:
    cursor = Cursor()
    item = quiz._fetch_stock_item(cursor, 9, "L3", "standard")
    query, params = cursor.calls[0]
    assert "last_used_at" in query
    assert "ORDER BY last_used_at ASC, id ASC LIMIT 1" in query
    assert params == (9, "L3", "standard")
    assert item["id"] == 91
    assert item["content_fields"]["hint"] == "一人あたりから考えよう"


def test_fetch_stock_item_fails_when_no_active_stock() -> None:
    cursor = Cursor(stock_row=())
    cursor.stock_row = None
    with pytest.raises(RuntimeError, match="No active quiz stock item"):
        quiz._fetch_stock_item(cursor, 9, "L3", "standard")


def test_fetch_stock_item_warns_when_reusing_stock(
    caplog: pytest.LogCaptureFixture,
) -> None:
    cursor = Cursor(
        stock_row=_stock_row(
            stock_id=44,
            last_used_at=datetime.datetime(2026, 8, 1, 0, 0),
        )
    )
    with caplog.at_level("WARNING"):
        quiz._fetch_stock_item(cursor, 9, "L3", "standard")
    assert "stock_id=44" in caplog.text
    assert "quiz_type=L3" in caplog.text
    assert "difficulty=standard" in caplog.text


def test_l3_explanation_allows_240_characters_only_for_l3() -> None:
    assert quiz.validate_content_fields(
        _fields(explanation="説" * 240), "L3"
    )["explanation"] == "説" * 240
    with pytest.raises(RuntimeError, match="240"):
        quiz.validate_content_fields(_fields(explanation="説" * 241), "L3")
    with pytest.raises(RuntimeError, match="80"):
        quiz.validate_content_fields(_fields(explanation="説" * 81), "L1")


@pytest.mark.parametrize(
    "updates, message",
    [
        ({"hint": ""}, "hint"),
        ({"tags": ["a", "b"]}, "exactly three"),
        ({"tags": ["a", "b", "c" * 11]}, "exactly three"),
        ({"question": "問" * 91}, "question"),
    ],
)
def test_stock_content_field_validation_fails_loudly(
    updates: dict[str, object], message: str
) -> None:
    with pytest.raises(RuntimeError, match=message):
        quiz.validate_content_fields(_fields(**updates), "L3")


def test_timeline_has_seven_cards_and_sixteen_seconds() -> None:
    assert quiz.CUT_DURATIONS == (8, 1, 1, 1, 1, 1, 3)
    assert len(quiz.CUT_DURATIONS) == 7
    assert sum(quiz.CUT_DURATIONS) == quiz.OUTPUT_DURATION_SECONDS == 16


def test_render_cards_assigns_coaches_and_bubble_text(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    coaches = {pose: object() for pose in quiz.COACH_FILENAMES}
    calls: list[tuple[object, str, int | None]] = []

    def render(*args, countdown=None, **kwargs):
        del kwargs
        coach = args[1]
        bubble = args[2]
        calls.append((coach, bubble, countdown))
        stamp = f"{bubble}:{countdown}".encode()
        return quiz._CardLayers(b"base", b"layer", stamp), 500

    monkeypatch.setattr(quiz, "_decode_illustration", lambda content: object())
    monkeypatch.setattr(quiz, "_trim_coaches", lambda values: values)
    monkeypatch.setattr(quiz, "_render_card", render)
    timeline, cuts = quiz._render_cards(
        _fields(),
        "noon",
        "昼の推定",
        "30秒で解けたら天才",
        b"illustration",
        coaches,
        {"regular": Path("regular"), "bold": Path("bold")},
    )

    actual = calls[1:]
    assert [entry[0] for entry in actual] == [
        coaches["hook"],
        *([coaches["question"]] * 5),
        coaches["answer"],
    ]
    assert [entry[1] for entry in actual] == [
        quiz.INTRO_BUBBLE_TEXT,
        *(["一人あたりから考えよう"] * 5),
        quiz.GUIDANCE_BUBBLE_TEXT,
    ]
    assert [entry[2] for entry in actual[1:6]] == [5, 4, 3, 2, 1]
    assert len(timeline) == 7
    assert cuts == [
        timeline[0].composite,
        timeline[1].composite,
        timeline[6].composite,
    ]


def test_segment_output_filter_resets_timestamp_without_zoom() -> None:
    assert quiz._segment_output_filter("comp", "v") == (
        "[comp]format=yuv420p,setpts=PTS-STARTPTS[v]"
    )


def test_build_video_uses_new_audio_timing_and_fade(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    commands: list[list[str]] = []

    def run(command: list[str], **kwargs: object) -> None:
        del kwargs
        commands.append(command)
        Path(command[-1]).write_bytes(b"mp4")

    monkeypatch.setattr(quiz.subprocess, "run", run)
    cards = [quiz._CardLayers(b"base", b"layer", b"comp")] * 7
    result = quiz._build_video(cards, b"bgm", b"tick", b"chime")
    assert result == b"mp4"
    assert len(commands) == 8
    final = commands[-1]
    filters = final[final.index("-filter_complex") + 1]
    assert "afade=t=out:st=15:d=1" in filters
    assert "adelay=8000|8000" in filters
    assert "adelay=13000|13000" in filters
    assert "amix=inputs=3:duration=longest:normalize=0" in filters
    assert final[final.index("-t") + 1] == "16"
    assert final[final.index("-c:v") + 1] == "copy"
    assert final[final.index("-c:a") + 1] == "aac"


def test_build_video_bounces_coach_layer_on_bubble_changes(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    commands: list[list[str]] = []

    def run(command: list[str], **kwargs: object) -> None:
        del kwargs
        commands.append(command)
        Path(command[-1]).write_bytes(b"mp4")

    monkeypatch.setattr(quiz.subprocess, "run", run)
    cards = [quiz._CardLayers(b"base", b"layer", b"comp")] * 7
    quiz._build_video(cards, b"bgm", b"tick", b"chime")
    segment_filters = [
        command[command.index("-filter_complex") + 1]
        for command in commands[:7]
    ]
    for index, filters in enumerate(segment_filters):
        amplitude = quiz.CUT_BOUNCE_AMPLITUDES[index]
        assert "overlay=x=0" in filters
        if amplitude:
            assert f"y='-{amplitude}*exp(" in filters
        else:
            assert "y=0" in filters


def test_large_bounces_align_with_existing_sound_effects() -> None:
    large = [
        index
        for index, amplitude in enumerate(quiz.CUT_BOUNCE_AMPLITUDES)
        if amplitude == quiz.BOUNCE_LARGE_AMPLITUDE_PIXELS
    ]
    assert large == [1, 6]
    assert sum(quiz.CUT_DURATIONS[:1]) * 1000 == quiz.TICK_DELAY_MILLISECONDS
    assert sum(quiz.CUT_DURATIONS[:6]) * 1000 == quiz.CHIME_DELAY_MILLISECONDS


def test_generate_consumes_stock_and_stages_snapshot(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    cursor = Cursor()
    illustration = _patch_generate_dependencies(monkeypatch)
    result = quiz.generate(_context(cursor))

    stock_select_index = next(
        index
        for index, (sql, _) in enumerate(cursor.calls)
        if "FROM quiz_stock_items" in sql
    )
    bgm_select_index = next(
        index
        for index, (sql, _) in enumerate(cursor.calls)
        if "asset_type = 'bgm'" in sql
    )
    assert bgm_select_index < stock_select_index
    illustration.assert_called_once()
    assert (
        "文字・数字は情景で明示的に指定されたものだけを、指定どおりの字形で正確に描く。"
        in illustration.call_args.args[1]
    )
    assert (
        "情景で指定されていない文字・数字・記号は一切描画しない"
        in illustration.call_args.args[1]
    )
    assert "tone_hint" not in illustration.call_args.args[1]

    insert = next(
        call for call in cursor.calls if call[0].startswith("INSERT INTO quiz_items")
    )
    assert "stock_item_id" in insert[0]
    assert insert[1][:6] == (9, 123, 91, "L3", "standard", "日本の信号機数を推定")
    assert json.loads(insert[1][-1]) == _fields()

    stock_update = next(
        call
        for call in cursor.calls
        if call[0].startswith("UPDATE quiz_stock_items")
    )
    assert "use_count = use_count + 1" in stock_update[0]
    assert stock_update[1] == (datetime.datetime(2026, 8, 7, 3, 4, 5), 91)
    bgm_update = next(
        call for call in cursor.calls if call[0].startswith("UPDATE audio_assets")
    )
    assert bgm_update[1] == (datetime.datetime(2026, 8, 7, 3, 4, 5), 77)

    assert result.media[0].duration_seconds == 16
    assert [item.suffix for item in result.intermediates] == [
        "_cut1",
        "_cut2",
        "_cut3",
        "_illustration",
    ]


def test_generate_fails_before_stock_and_images_when_font_is_missing(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    cursor = Cursor()
    build_client = Mock()
    monkeypatch.setattr(
        quiz,
        "_load_fonts",
        Mock(side_effect=RuntimeError("font missing")),
    )
    monkeypatch.setattr(quiz.openai_image, "build_client", build_client)
    with pytest.raises(RuntimeError, match="font missing"):
        quiz.generate(_context(cursor))
    assert not cursor.calls
    build_client.assert_not_called()


def test_decode_coach_requires_rgba_png() -> None:
    rgb = Image.new("RGB", (10, 10), "white")
    output = BytesIO()
    rgb.save(output, format="PNG")
    with pytest.raises(RuntimeError, match="RGBA PNG"):
        quiz._decode_coach_png(output.getvalue(), "coach.png")
