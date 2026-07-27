"""Tests for the GPT quiz multi-cut generator."""

from __future__ import annotations

import datetime
import json
from pathlib import Path
from unittest.mock import Mock

import pytest

from app.generators import GeneratorContext
from app.generators import gpt_quiz_multicut as quiz
from app.models import PromptConfig


def _parameters(
    *,
    slots: list[dict] | None = None,
    max_regenerations: int = 3,
) -> str:
    """Build quiz parameters."""
    return json.dumps(
        {
            "llm_model": "test-model",
            "slots": slots
            or [
                {
                    "from_jst_hour": 4,
                    "quiz_type": "L1",
                    "difficulty": "light",
                },
                {
                    "from_jst_hour": 11,
                    "quiz_type": "L3",
                    "difficulty": "standard",
                },
                {
                    "from_jst_hour": 17,
                    "quiz_type": "L1",
                    "difficulty": "deep",
                },
            ],
            "max_regenerations": max_regenerations,
        }
    )


def _base_fields(**updates) -> dict:
    """Build valid common structured fields."""
    fields = {
        "hook": "ひらめける？",
        "question": "日本にある信号機の数を推定してください。",
        "answer": "約20万基（目安）",
        "explanation": "交差点数を人口と道路密度から見積もります。",
        "coach_comment": "推定ルートが大切！",
        "tags": ["脳トレ", "推定", "クイズ"],
        "summary": "日本の信号機の数を人口から推定",
    }
    fields.update(updates)
    return fields


def _values_after(command: list[str], option: str) -> list[str]:
    """Return every command value immediately following an option."""
    return [
        command[index + 1]
        for index, value in enumerate(command[:-1])
        if value == option
    ]


def _truth_spec() -> dict:
    """Return a uniquely solvable truth-teller specification."""
    return {
        "kind": "truth_tellers",
        "people": ["A", "B"],
        "statements": [
            {
                "speaker": "A",
                "predicate": "same_type",
                "left": "A",
                "right": "B",
            },
            {
                "speaker": "B",
                "predicate": "is_honest",
                "subject": "A",
            },
        ],
    }


def test_resolve_slot_uses_jst_boundaries_and_wraps_early_hours() -> None:
    """Boundary hours select that slot; earlier hours use the previous night."""
    _, slots, _ = quiz._parse_parameters(_parameters())

    # 02:00 UTC is 11:00 JST.
    selected = quiz.resolve_slot(
        datetime.datetime(2026, 7, 27, 2, tzinfo=datetime.timezone.utc),
        slots,
    )
    assert selected["quiz_type"] == "L3"

    # 18:00 UTC is 03:00 JST on the next day, before the first 04:00 slot.
    wrapped = quiz.resolve_slot(
        datetime.datetime(2026, 7, 27, 18, tzinfo=datetime.timezone.utc),
        slots,
    )
    assert wrapped["difficulty"] == "deep"


@pytest.mark.parametrize(
    "parameters, message",
    [
        ({}, "slots"),
        ({"slots": []}, "slots"),
        (
            {
                "slots": [
                    {"from_jst_hour": 24, "quiz_type": "L1"}
                ]
            },
            "from_jst_hour",
        ),
        (
            {
                "slots": [
                    {"from_jst_hour": 4, "quiz_type": "L2"}
                ]
            },
            "quiz_type",
        ),
    ],
)
def test_invalid_slots_fail_loudly(parameters: dict, message: str) -> None:
    """Missing and invalid slot configuration is a runtime error."""
    with pytest.raises(RuntimeError, match=message):
        quiz._parse_parameters(json.dumps(parameters))


@pytest.mark.parametrize(
    "updates, message",
    [
        ({"hook": ""}, "hook"),
        ({"question": "問" * 91}, "question"),
        ({"tags": ["a", "b"]}, "tags"),
        ({"answer": "20万基です"}, "L3 answer"),
    ],
)
def test_programmatic_field_validation_rejects_invalid_content(
    updates: dict,
    message: str,
) -> None:
    """Required fields, length limits, tags, and L3 format are enforced."""
    with pytest.raises(quiz.QuizValidationError, match=message):
        quiz.validate_content_fields(_base_fields(**updates), "L3")


def test_truth_teller_unique_solution_passes() -> None:
    """The truth-teller solver returns its sole canonical assignment."""
    solution = quiz.solve_machine_spec(_truth_spec())
    assert solution == {"A": "honest", "B": "honest"}


def test_truth_teller_multiple_solutions_fail() -> None:
    """An underconstrained testimony puzzle is rejected."""
    spec = {
        "kind": "truth_tellers",
        "people": ["A", "B"],
        "statements": [
            {
                "speaker": "A",
                "predicate": "is_honest",
                "subject": "B",
            }
        ],
    }
    with pytest.raises(quiz.QuizValidationError, match="exactly one"):
        quiz.solve_machine_spec(spec)


def test_truth_teller_contradiction_and_unknown_vocabulary_fail() -> None:
    """Contradictions and predicates outside the closed DSL are rejected."""
    contradiction = {
        "kind": "truth_tellers",
        "people": ["A"],
        "statements": [
            {
                "speaker": "A",
                "predicate": "is_liar",
                "subject": "A",
            }
        ],
    }
    with pytest.raises(quiz.QuizValidationError, match="exactly one"):
        quiz.solve_machine_spec(contradiction)

    unknown = _truth_spec()
    unknown["statements"][0]["predicate"] = "implies"
    with pytest.raises(quiz.QuizValidationError, match="unknown"):
        quiz.solve_machine_spec(unknown)


def test_ordering_unique_solution_passes() -> None:
    """Finite ordering constraints are exhaustively solved."""
    spec = {
        "kind": "ordering",
        "items": ["A", "B", "C"],
        "constraints": [
            {"op": "position", "item": "A", "position": 1},
            {"op": "position", "item": "B", "position": 2},
        ],
    }
    assert quiz.solve_machine_spec(spec) == ["A", "B", "C"]


@pytest.mark.parametrize(
    "constraints, message",
    [
        ([{"op": "before", "left": "A", "right": "B"}], "exactly one"),
        (
            [
                {"op": "position", "item": "A", "position": 1},
                {"op": "position", "item": "A", "position": 2},
            ],
            "exactly one",
        ),
        ([{"op": "around", "left": "A", "right": "B"}], "unknown"),
    ],
)
def test_ordering_ambiguous_contradictory_and_unknown_constraints_fail(
    constraints: list[dict],
    message: str,
) -> None:
    """All non-unique and unknown ordering specifications are rejected."""
    spec = {
        "kind": "ordering",
        "items": ["A", "B", "C"],
        "constraints": constraints,
    }
    with pytest.raises(quiz.QuizValidationError, match=message):
        quiz.solve_machine_spec(spec)


def test_matching_unique_solution_and_machine_answer_mismatch() -> None:
    """Matching is enumerable and generated canonical answers are compared."""
    spec = {
        "kind": "matching",
        "items": ["A", "B"],
        "values": ["red", "blue"],
        "constraints": [{"op": "match", "item": "A", "value": "red"}],
    }
    assert quiz.solve_machine_spec(spec) == {"A": "red", "B": "blue"}
    fields = _base_fields(
        answer="Aは赤、Bは青",
        machine_spec=spec,
        machine_answer={"A": "blue", "B": "red"},
    )
    with pytest.raises(quiz.QuizValidationError, match="does not match"):
        quiz.validate_content_fields(fields, "L1")


def test_duplicate_normalization_and_jaccard_threshold() -> None:
    """NFKC, whitespace, and punctuation do not hide duplicate wording."""
    assert quiz.normalize_for_duplicate("Ａ、 B！\n") == "AB"
    assert quiz.bigram_jaccard("東京 の人口？", "東京の人口") == 1.0

    left = "abcdef"
    right = "abcxef"
    score = quiz.bigram_jaccard(left, right)
    assert score < quiz.DUPLICATE_JACCARD_THRESHOLD
    assert quiz._is_duplicate(left, [left])
    assert not quiz._is_duplicate(left, [right])


class GenerateCursor:
    """Route generator SQL to deterministic fake rows."""

    def __init__(self) -> None:
        """Initialize SQL history and active result set."""
        self.calls: list[tuple[str, tuple]] = []
        self.current = ""

    def execute(self, sql: str, params: tuple) -> None:
        """Record a statement and select the matching fake result."""
        self.calls.append((sql, params))
        self.current = sql

    def fetchone(self):
        """Return single-row query results."""
        if "SELECT set_code" in self.current:
            return ("quiz-set",)
        if "asset_type = 'bgm'" in self.current:
            return (77, "audio/quiz-set/bgm/track.m4a")
        raise AssertionError(f"Unexpected fetchone for {self.current}")

    def fetchall(self):
        """Return multi-row query results."""
        if "asset_type = 'se'" in self.current:
            return (
                (81, "audio/quiz-set/se/countdown_tick.m4a"),
                (82, "audio/quiz-set/se/answer_chime.m4a"),
            )
        if "SELECT summary" in self.current:
            return (("過去の要旨",),)
        if "SELECT question_text" in self.current:
            return (("別の問題です",),)
        raise AssertionError(f"Unexpected fetchall for {self.current}")


def _context(
    cursor: GenerateCursor,
    *,
    max_regenerations: int = 3,
) -> GeneratorContext:
    """Create a generator context selecting the 11:00 JST L3 slot."""
    return GeneratorContext(
        prompt_config=PromptConfig(
            5,
            9,
            "身近な日本をテーマにする",
            None,
            _parameters(max_regenerations=max_regenerations),
        ),
        cursor=cursor,
        s3_client=Mock(),
        s3_bucket="bucket",
        scheduled_at=datetime.datetime(
            2026, 7, 27, 2, tzinfo=datetime.timezone.utc
        ),
        generation_run_id=123,
    )


def _patch_generate_dependencies(
    monkeypatch: pytest.MonkeyPatch,
    fields: dict,
) -> None:
    """Patch fonts, coach images, OpenAI, layout, and ffmpeg."""
    monkeypatch.setattr(
        quiz,
        "_load_fonts",
        lambda: {"regular": Path("regular"), "bold": Path("bold")},
    )
    monkeypatch.setattr(
        quiz,
        "_load_coach_assets",
        lambda context, set_code: {
            name: Mock() for name in quiz.COACH_FILENAMES
        },
    )
    monkeypatch.setattr(quiz, "get_object", lambda *args, **kwargs: b"audio")
    monkeypatch.setattr(quiz.openai_image, "load_api_key", lambda: "key")
    monkeypatch.setattr(
        quiz.openai_image, "build_client", lambda key: object()
    )
    monkeypatch.setattr(
        quiz, "_request_quiz_fields", lambda *args: fields.copy()
    )
    monkeypatch.setattr(
        quiz, "_independent_validation", lambda *args: True
    )
    monkeypatch.setattr(
        quiz,
        "_render_cards",
        lambda *args: ([b"card"] * 8, [b"cut1", b"cut2", b"cut3", b"cut4"]),
    )
    monkeypatch.setattr(quiz, "_build_video", lambda *args: b"video")
    monkeypatch.setattr(
        quiz,
        "now_utc",
        lambda: datetime.datetime(2026, 7, 27, 3, 4, 5),
    )


def test_generate_checks_fixed_assets_before_openai(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A missing startup asset prevents any LLM client construction."""
    cursor = GenerateCursor()
    build_client = Mock()
    monkeypatch.setattr(
        quiz,
        "_load_fonts",
        Mock(side_effect=RuntimeError("Required quiz font is missing")),
    )
    monkeypatch.setattr(quiz.openai_image, "build_client", build_client)

    with pytest.raises(RuntimeError, match="font is missing"):
        quiz.generate(_context(cursor))

    build_client.assert_not_called()
    assert cursor.calls == []


def test_generate_happy_path_stages_history_and_rotates_only_bgm(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Happy path inserts quiz history and returns final/intermediate media."""
    cursor = GenerateCursor()
    fields = _base_fields()
    _patch_generate_dependencies(monkeypatch, fields)

    result = quiz.generate(_context(cursor))

    insert_call = next(
        call for call in cursor.calls if call[0].startswith("INSERT INTO quiz_items")
    )
    assert insert_call[1][:7] == (
        9,
        123,
        "L3",
        "standard",
        fields["summary"],
        fields["question"],
        fields["answer"],
    )
    assert json.loads(insert_call[1][7]) == fields
    updates = [
        call for call in cursor.calls if call[0].startswith("UPDATE audio_assets")
    ]
    assert updates == [
        (
            "UPDATE audio_assets SET last_used_at = %s WHERE id = %s",
            (datetime.datetime(2026, 7, 27, 3, 4, 5), 77),
        )
    ]
    assert result.media[0].content == b"video"
    assert result.media[0].audio_asset_id == 77
    assert result.media[0].duration_seconds == 20
    assert [item.suffix for item in result.intermediates] == [
        "_cut1",
        "_cut2",
        "_cut3",
        "_cut4",
    ]
    assert all(item.file_format == "png" for item in result.intermediates)


def test_generate_exhausts_regeneration_limit(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Initial generation plus configured regenerations eventually fail."""
    cursor = GenerateCursor()
    _patch_generate_dependencies(
        monkeypatch,
        _base_fields(question="問" * 91),
    )
    request = Mock(return_value=_base_fields(question="問" * 91))
    monkeypatch.setattr(quiz, "_request_quiz_fields", request)

    with pytest.raises(RuntimeError, match="exhausted"):
        quiz.generate(_context(cursor, max_regenerations=2))

    assert request.call_count == 3
    assert not any(
        sql.startswith("INSERT INTO quiz_items") for sql, _ in cursor.calls
    )


def test_build_video_uses_hard_cuts_and_timed_normalization_free_mix(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Eight sequential encodes precede copy-concat and timed audio mixing."""
    calls: list[tuple[list[str], dict]] = []
    observed_filelist = {}

    def run(command, **kwargs):
        calls.append((command, kwargs))
        if "concat" in command:
            filelist_path = Path(command[command.index("-i") + 1])
            observed_filelist["content"] = filelist_path.read_text()
        Path(command[-1]).write_bytes(b"mp4")

    monkeypatch.setattr(quiz.subprocess, "run", run)
    monkeypatch.setattr(quiz, "FFMPEG_BINARY", "test-ffmpeg")

    result = quiz._build_video(
        [b"png"] * 8,
        b"bgm",
        b"tick",
        b"chime",
    )

    assert result == b"mp4"
    assert len(calls) == 9
    segment_calls = calls[:8]
    for index, ((command, kwargs), duration) in enumerate(
        zip(segment_calls, quiz.CUT_DURATIONS)
    ):
        assert Path(command[-1]).name == f"segment-{index}.mp4"
        assert command[command.index("-c:v") + 1] == "libx264"
        assert command[command.index("-crf") + 1] == "20"
        assert command[command.index("-preset") + 1] == "medium"
        assert _values_after(command, "-t") == [str(duration), str(duration)]
        filter_complex = command[command.index("-filter_complex") + 1]
        assert "scale=2160:3840" in filter_complex
        assert "zoompan=z='1.0+0.04*on/" in filter_complex
        assert "format=yuv420p" in filter_complex
        assert kwargs == {
            "check": True,
            "capture_output": True,
            "timeout": 600,
        }

    command, kwargs = calls[-1]
    assert command[command.index("-f") + 1] == "concat"
    assert command[command.index("-safe") + 1] == "0"
    assert command[command.index("-c:v") + 1] == "copy"
    assert command[command.index("-stream_loop") + 1] == "-1"
    assert observed_filelist["content"].count("file '") == 8
    filter_complex = command[command.index("-filter_complex") + 1]
    assert "adelay=10000|10000" in filter_complex
    assert "adelay=15000|15000" in filter_complex
    assert "normalize=0" in filter_complex
    assert command[command.index("-c:a") + 1] == "aac"
    assert command[command.index("-t", command.index("-c:a")) + 1] == "20"
    assert kwargs == {
        "check": True,
        "capture_output": True,
        "timeout": 600,
    }
