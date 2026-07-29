"""GPT quiz multi-cut video generator.

The L1 machine specification is a closed JSON DSL.  It never evaluates source
code and accepts only these forms:

* ``{"kind": "truth_tellers", "people": [...], "statements": [...]}``
  where every statement has ``speaker`` and one of the predicates
  ``is_honest``, ``is_liar``, ``same_type``, or ``different_type``.
  Unary predicates use ``subject``; binary predicates use ``left``/``right``.
  The canonical answer is ``{person: "honest"|"liar"}``.
* ``{"kind": "ordering", "items": [...], "constraints": [...]}`` with
  ``position``, ``not_position``, ``before``, ``after``, ``adjacent``, or
  ``not_adjacent`` constraints.  Positions are one-based.  The canonical
  answer is the ordered item list.
* ``{"kind": "matching", "items": [...], "values": [...],
  "constraints": [...]}`` with ``match`` or ``not_match`` constraints.
  The canonical answer is ``{item: value}``.

All assignments/permutations are exhaustively enumerated.  Unknown fields in a
constraint vocabulary, invalid references, more than five elements, no
solution, and multiple solutions are validation failures.
"""

from __future__ import annotations

import datetime
from io import BytesIO
import itertools
import json
import logging
import math
from pathlib import Path
import re
import subprocess
import tempfile
import unicodedata
from typing import Any

from PIL import Image, ImageDraw, ImageFont, ImageOps

from acps_shared.s3 import get_object

from ..clock import now_utc
from . import openai_image
from .contracts import (
    GeneratorContext,
    GeneratorResult,
    IntermediateOutput,
    MediaOutput,
)


logger = logging.getLogger(__name__)

DEFAULT_LLM_MODEL = "gpt-5.6-terra"
DEFAULT_MAX_REGENERATIONS = 3
QUIZ_TYPES = {"L1", "L3"}
JST = datetime.timezone(datetime.timedelta(hours=9))

FIELD_LIMITS = {
    "hook": 20,
    "question": 90,
    "answer": 30,
    "explanation": 80,
    "coach_comment": 30,
    "summary": 100,
    "illustration_scene": 200,
}
TAG_COUNT = 3
TAG_MAX_LENGTH = 10
L3_ANSWER_PATTERN = re.compile(
    r"^約\s*[0-9０-９][0-9０-９,，.．]*"
    r"(?:[^\s（）0-9０-９]+)?\s*（目安）$"
)
SUMMARY_HISTORY_LIMIT = 30
QUESTION_HISTORY_LIMIT = 120
DUPLICATE_JACCARD_THRESHOLD = 0.55

OUTPUT_WIDTH = 1080
OUTPUT_HEIGHT = 1920
OUTPUT_FPS = 30
OUTPUT_DURATION_SECONDS = 20
OUTPUT_CRF = 20
FFMPEG_BINARY = "ffmpeg"
FFMPEG_TIMEOUT_SECONDS = 600
ZOOM_START = 1.0
ZOOM_END = 1.04
SUPERSAMPLE_FACTOR = 2
SAFE_BOX_MARGIN = 8
INSTAGRAM_RIGHT_RESERVED_RATIO = 0.12
INSTAGRAM_BOTTOM_RESERVED_RATIO = 0.15

HOOK_DURATION_SECONDS = 3
QUESTION_DURATION_SECONDS = 7
THINK_DURATION_SECONDS = 1
ANSWER_DURATION_SECONDS = 5
CUT_DURATIONS = (
    HOOK_DURATION_SECONDS,
    QUESTION_DURATION_SECONDS,
    THINK_DURATION_SECONDS,
    THINK_DURATION_SECONDS,
    THINK_DURATION_SECONDS,
    THINK_DURATION_SECONDS,
    THINK_DURATION_SECONDS,
    ANSWER_DURATION_SECONDS,
)

BGM_VOLUME = 1.0
TICK_VOLUME = 10 ** (-6 / 20)
CHIME_VOLUME = 10 ** (-3 / 20)
TICK_DELAY_MILLISECONDS = 10_000
CHIME_DELAY_MILLISECONDS = 15_000

SLOT_PALETTES = {
    "morning": {
        "background": "#F3EEE3",
        "card": "#FBF8F1",
        "text": "#1B2A4A",
        "muted_text": "#56688A",
        "accent": "#F4B942",
        "decoration": "#E4DCC9",
    },
    "noon": {
        "background": "#E9F1F8",
        "card": "#FBFDFF",
        "text": "#1B2A4A",
        "muted_text": "#56688A",
        "accent": "#E39B0C",
        "decoration": "#D3E2EF",
    },
    "night": {
        "background": "#0A1226",
        "card": "#111E3C",
        "text": "#F7F7F2",
        "muted_text": "#9FB0CC",
        "accent": "#F4B942",
        "decoration": "#1B2C50",
    },
}
SLOT_TIME_MOODS = {
    "morning": "朝の柔らかい光",
    "noon": "昼の明るい光",
    "night": "夜の落ち着いた照明",
}
ANSWER_ILLUSTRATION_OVERLAY_OPACITY = 0.55
HEADING_FONT_SIZE = 88
THINK_COUNT_FONT_SIZE = 140
QUESTION_FONT_SIZE = 56
SUPPLEMENT_FONT_SIZE = 40
MIN_BODY_FONT_SIZE = 30
LINE_START_PROHIBITED = "、。，．,.)）]］｝」』】〉》!！?？:：;；ー〜…‥・%％℃"
LINE_END_PROHIBITED = "（(「『【〈《[［｛"
CARD_PADDING = 64
COACH_BOX = (300, 430)

FONT_FILENAMES = {
    "regular": "NotoSansJP-Regular.otf",
    "bold": "NotoSansJP-Bold.otf",
}
COACH_FILENAMES = {
    "hook": "coach_hook.png",
    "question": "coach_question.png",
    "think": "coach_think.png",
    "answer": "coach_answer.png",
}
SE_FILENAMES = ("countdown_tick.m4a", "answer_chime.m4a")

GENERATION_INSTRUCTIONS = """
次の条件に従い、縦型ショート動画用のクイズを JSON オブジェクトだけで返す。
必須フィールド:
- hook: 20文字以内
- question: 90文字以内
- answer: 30文字以内
- explanation: 80文字以内
- coach_comment: 30文字以内
- tags: 10文字以内をちょうど3個
- summary: 100文字以内
- illustration_scene: 200文字以内。動画背景用の情景描写とし、文字・数字・
  記号・答えの内容は含めない
型は {quiz_type}、難度は {difficulty}。
口調の方向性は「{tone_hint}」。hook と coach_comment の口調へ反映する。
L1 の場合は machine_spec と machine_answer も必須。machine_spec は指定された
閉じた DSL の truth_tellers / ordering / matching のいずれかだけを使い、
全列挙で唯一解になる問題を作る。machine_answer は DSL の正準形にする。
machine_spec はトップレベルに "kind" フィールド（truth_tellers / ordering /
matching のいずれか）を持つ 1 個のフラットなオブジェクトにする。
例: {{"kind": "matching", "items": [...], "values": [...],
"constraints": [...]}}。kind 名をキーにした入れ子（{{"matching": ...}} 等）
は不可。machine_answer の正準形は、truth_tellers なら人物名から
"honest"/"liar" への辞書、ordering なら並び順どおりの配列そのもの
（"order" 等のキーで包まない）、matching なら item から value への辞書
（ペアの配列にしない）。
truth_tellers は people と statements を持ち、statement は speaker と
predicate を持つ。predicate は is_honest/is_liar（subject を指定）または
same_type/different_type（left/right を指定）だけを使う。
ordering は items と constraints を持ち、constraint の op は
position/not_position（item/position）または before/after/adjacent/
not_adjacent（left/right）だけを使う。position は1始まり。
matching は同数の items/values と constraints を持ち、constraint の op は
match/not_match（item/value）だけを使う。要素・人物は最大5件。
L3 の場合、answer は必ず「約<数値と単位>（目安）」とし、explanation に
推定ルートを含め、断定表現を避ける。
既存問題の言い換え、固有名詞への中傷、医療・法律・投資助言、差別、暴力、
性的内容、政治的扇動、危険行為は除外する。
"""

L1_VALIDATION_INSTRUCTIONS = """
あなたは独立した論理パズル解答者です。提示された問題文だけを解き、
JSON で {"machine_answer": ...} を返してください。正準形は、正直者・
嘘つきなら人物から honest/liar への辞書、順序なら配列、対応なら辞書です。
生成側の答えは提示されていません。
"""

L3_VALIDATION_INSTRUCTIONS = """
あなたは独立したフェルミ推定の検証者です。問題文を独立に推定し、JSON で
{"estimated_value": 数値, "route_valid": true|false} を返してください。
estimated_value は単位換算後の正の数値、route_valid は問題が妥当な推定
ルートを持つ場合だけ true にしてください。生成側の答えは提示されていません。
"""


class QuizValidationError(ValueError):
    """Raised when generated quiz content fails deterministic validation."""


def _parse_parameters(raw: str | None) -> tuple[str, list[dict[str, Any]], int]:
    """Parse and validate the three supported prompt parameters."""
    try:
        parameters = json.loads(raw or "{}")
    except (TypeError, json.JSONDecodeError) as exc:
        raise RuntimeError("parameters must be a JSON object") from exc
    if not isinstance(parameters, dict):
        raise RuntimeError("parameters must be a JSON object")

    slots = parameters.get("slots")
    if not isinstance(slots, list) or not slots:
        raise RuntimeError("parameters.slots is required and must not be empty")
    validated_slots: list[dict[str, Any]] = []
    for slot in slots:
        if not isinstance(slot, dict):
            raise RuntimeError("each slots entry must be an object")
        required_fields = {
            "from_jst_hour",
            "quiz_type",
            "difficulty",
            "slot_code",
            "tone_hint",
            "slot_label",
        }
        missing = required_fields - set(slot)
        if missing:
            raise RuntimeError(
                "slots entry is missing required fields: "
                + ", ".join(sorted(missing))
            )
        hour = slot.get("from_jst_hour")
        quiz_type = slot.get("quiz_type")
        if isinstance(hour, bool) or not isinstance(hour, int) or not 0 <= hour <= 23:
            raise RuntimeError("from_jst_hour must be an integer from 0 to 23")
        for field in required_fields - {"from_jst_hour"}:
            value = slot.get(field)
            if not isinstance(value, str) or not value.strip():
                raise RuntimeError(f"{field} must be a non-empty string")
        if quiz_type not in QUIZ_TYPES:
            raise RuntimeError("quiz_type must be L1 or L3")
        slot_code = slot["slot_code"].strip()
        if slot_code not in SLOT_PALETTES:
            raise RuntimeError(f"unknown slot_code: {slot_code}")
        validated_slots.append(
            {
                "from_jst_hour": hour,
                "quiz_type": quiz_type.strip(),
                "difficulty": slot["difficulty"].strip(),
                "slot_code": slot_code,
                "tone_hint": slot["tone_hint"].strip(),
                "slot_label": slot["slot_label"].strip(),
            }
        )

    max_regenerations = parameters.get(
        "max_regenerations", DEFAULT_MAX_REGENERATIONS
    )
    if (
        isinstance(max_regenerations, bool)
        or not isinstance(max_regenerations, int)
        or max_regenerations < 0
    ):
        raise RuntimeError("max_regenerations must be a non-negative integer")
    llm_model = parameters.get("llm_model", DEFAULT_LLM_MODEL)
    if not isinstance(llm_model, str) or not llm_model:
        raise RuntimeError("llm_model must be a non-empty string")
    return llm_model, validated_slots, max_regenerations


def resolve_slot(
    scheduled_at: datetime.datetime,
    slots: list[dict[str, Any]],
) -> dict[str, Any]:
    """Resolve the deterministic JST slot, including early-morning wrap."""
    if not slots:
        raise RuntimeError("slots must not be empty")
    if scheduled_at.tzinfo is None:
        scheduled_at = scheduled_at.replace(tzinfo=datetime.timezone.utc)
    jst_hour = scheduled_at.astimezone(JST).hour
    ordered = sorted(slots, key=lambda item: item["from_jst_hour"])
    eligible = [
        slot for slot in ordered if slot["from_jst_hour"] <= jst_hour
    ]
    return eligible[-1] if eligible else ordered[-1]


def _font_directory() -> Path:
    """Return the deployment-stable font directory."""
    return Path(__file__).resolve().parents[2] / "fonts"


def _load_fonts() -> dict[str, Path]:
    """Fail loudly before LLM work when a required font is missing."""
    font_dir = _font_directory()
    paths = {
        name: font_dir / filename for name, filename in FONT_FILENAMES.items()
    }
    missing = [str(path) for path in paths.values() if not path.is_file()]
    if missing:
        raise RuntimeError(f"Required quiz font is missing: {', '.join(missing)}")
    return paths


def _fetch_set_code(context: GeneratorContext) -> str:
    """Fetch the set code needed by fixed S3 asset conventions."""
    context.cursor.execute(
        "SELECT set_code FROM batch_sets WHERE id = %s",
        (context.prompt_config.set_id,),
    )
    row = context.cursor.fetchone()
    if row is None:
        raise RuntimeError(
            f"batch_sets row not found: set_id={context.prompt_config.set_id}"
        )
    return str(row[0])


def _decode_coach_png(content: bytes, key: str) -> Image.Image:
    """Decode and validate one RGBA character asset."""
    try:
        with Image.open(BytesIO(content)) as image:
            image.load()
            if image.format != "PNG" or image.mode != "RGBA":
                raise RuntimeError(f"Coach asset must be an RGBA PNG: {key}")
            return image.copy()
    except RuntimeError:
        raise
    except Exception as exc:
        raise RuntimeError(f"Invalid coach PNG: {key}") from exc


def _load_coach_assets(
    context: GeneratorContext,
    set_code: str,
) -> dict[str, Image.Image]:
    """Load all fixed coach pose assets from S3."""
    result: dict[str, Image.Image] = {}
    for pose, filename in COACH_FILENAMES.items():
        key = f"assets/{set_code}/{filename}"
        content = get_object(
            context.s3_bucket,
            key,
            client=context.s3_client,
        )
        result[pose] = _decode_coach_png(content, key)
    return result


def _load_audio_assets(
    context: GeneratorContext,
    set_code: str,
    slot_code: str,
) -> tuple[int, bytes, bytes, bytes]:
    """Load mandatory SE assets and the least-recently-used BGM."""
    context.cursor.execute(
        "SELECT id, s3_key FROM audio_assets "
        "WHERE set_id = %s AND asset_type = 'se' AND is_active = 1",
        (context.prompt_config.set_id,),
    )
    se_rows = context.cursor.fetchall()
    expected = {
        filename: f"audio/{set_code}/se/{filename}"
        for filename in SE_FILENAMES
    }
    available = {str(row[1]): int(row[0]) for row in se_rows}
    missing = [key for key in expected.values() if key not in available]
    if missing:
        raise RuntimeError(
            f"Required quiz sound effect is missing: {', '.join(missing)}"
        )
    tick = get_object(
        context.s3_bucket,
        expected["countdown_tick.m4a"],
        client=context.s3_client,
    )
    chime = get_object(
        context.s3_bucket,
        expected["answer_chime.m4a"],
        client=context.s3_client,
    )

    context.cursor.execute(
        "SELECT id, s3_key FROM audio_assets "
        "WHERE set_id = %s AND asset_type = 'bgm' AND is_active = 1 "
        "AND (time_slot = %s OR time_slot IS NULL) "
        "ORDER BY last_used_at ASC, id ASC LIMIT 1",
        (context.prompt_config.set_id, slot_code),
    )
    bgm_row = context.cursor.fetchone()
    if bgm_row is None:
        raise RuntimeError(
            "No active quiz BGM for "
            f"set_id={context.prompt_config.set_id} slot_code={slot_code}"
        )
    bgm_id, bgm_key = int(bgm_row[0]), str(bgm_row[1])
    bgm = get_object(
        context.s3_bucket,
        bgm_key,
        client=context.s3_client,
    )
    return bgm_id, bgm, tick, chime


def _fetch_history(
    context: GeneratorContext,
    quiz_type: str,
) -> tuple[list[str], list[str]]:
    """Fetch summary exclusions and full questions for duplicate checks."""
    params = (context.prompt_config.set_id, quiz_type)
    context.cursor.execute(
        "SELECT summary FROM quiz_items "
        "WHERE set_id = %s AND quiz_type = %s "
        "ORDER BY created_at DESC LIMIT 30",
        params,
    )
    summaries = [str(row[0]) for row in context.cursor.fetchall()]
    context.cursor.execute(
        "SELECT question_text FROM quiz_items "
        "WHERE set_id = %s AND quiz_type = %s "
        "ORDER BY created_at DESC LIMIT 120",
        params,
    )
    questions = [str(row[0]) for row in context.cursor.fetchall()]
    return summaries, questions


def _build_generation_prompt(
    base_prompt: str,
    quiz_type: str,
    difficulty: str,
    tone_hint: str,
    excluded_summaries: list[str],
    attempt: int,
) -> str:
    """Combine the DB theme with code-owned generation rules."""
    exclusions = (
        "\n".join(f"- {summary}" for summary in excluded_summaries)
        if excluded_summaries
        else "（なし）"
    )
    return (
        f"テーマ・世界観:\n{base_prompt}\n\n"
        + GENERATION_INSTRUCTIONS.format(
            quiz_type=quiz_type,
            difficulty=difficulty,
            tone_hint=tone_hint,
        )
        + "\nL1 DSL はこのモジュール仕様どおりのキー名を使う。"
        + f"\n直近要旨（重複禁止）:\n{exclusions}"
        + f"\n生成試行番号: {attempt + 1}"
    )


def _response_text(response: Any) -> str:
    """Extract text from an OpenAI Responses API result."""
    output_text = getattr(response, "output_text", None)
    if isinstance(output_text, str) and output_text:
        return output_text
    try:
        return str(response.output[0].content[0].text)
    except (AttributeError, IndexError, TypeError) as exc:
        raise RuntimeError("OpenAI text response did not contain output text") from exc


def _request_json(client: Any, model: str, prompt: str) -> dict[str, Any]:
    """Request one JSON object from the OpenAI text API."""
    response = client.responses.create(
        model=model,
        input=prompt,
        text={"format": {"type": "json_object"}},
    )
    parsed = json.loads(_response_text(response))
    if not isinstance(parsed, dict):
        raise QuizValidationError("LLM response must be a JSON object")
    return parsed


def _request_quiz_fields(
    client: Any,
    model: str,
    prompt: str,
) -> dict[str, Any]:
    """Generate structured quiz fields."""
    return _request_json(client, model, prompt)


def _validate_object_keys(
    value: dict[str, Any],
    required: set[str],
    allowed: set[str],
) -> None:
    """Reject missing and unknown DSL keys."""
    if not isinstance(value, dict):
        # LLM が入れ子のリストを返すことがある。ここで弾かないと set() が
        # TypeError（unhashable type）を投げ、再生成理由が読み取りにくくなる。
        raise QuizValidationError("DSL node must be an object")
    if set(value) - allowed:
        raise QuizValidationError("unknown DSL vocabulary")
    if not required <= set(value):
        raise QuizValidationError("missing DSL field")


def _validate_names(values: Any, label: str) -> list[str]:
    """Validate a unique one-to-five element string list."""
    if (
        not isinstance(values, list)
        or not 1 <= len(values) <= 5
        or any(not isinstance(item, str) or not item for item in values)
        or len(set(values)) != len(values)
    ):
        raise QuizValidationError(f"invalid {label}")
    return values


def _solve_truth_tellers(spec: dict[str, Any]) -> dict[str, str]:
    """Exhaustively solve the truth-teller DSL."""
    _validate_object_keys(
        spec,
        {"kind", "people", "statements"},
        {"kind", "people", "statements"},
    )
    people = _validate_names(spec["people"], "people")
    statements = spec["statements"]
    if not isinstance(statements, list) or not statements:
        raise QuizValidationError("statements must be a non-empty list")

    def statement_value(statement: dict[str, Any], assignment: dict[str, bool]) -> bool:
        predicate = statement.get("predicate")
        speaker = statement.get("speaker")
        if speaker not in people:
            raise QuizValidationError("unknown speaker")
        if predicate in {"is_honest", "is_liar"}:
            _validate_object_keys(
                statement,
                {"speaker", "predicate", "subject"},
                {"speaker", "predicate", "subject"},
            )
            subject = statement["subject"]
            if subject not in people:
                raise QuizValidationError("unknown statement subject")
            return (
                assignment[subject]
                if predicate == "is_honest"
                else not assignment[subject]
            )
        if predicate in {"same_type", "different_type"}:
            _validate_object_keys(
                statement,
                {"speaker", "predicate", "left", "right"},
                {"speaker", "predicate", "left", "right"},
            )
            left, right = statement["left"], statement["right"]
            if left not in people or right not in people:
                raise QuizValidationError("unknown statement subject")
            same = assignment[left] == assignment[right]
            return same if predicate == "same_type" else not same
        raise QuizValidationError("unknown DSL vocabulary")

    validation_assignment = {person: False for person in people}
    for statement in statements:
        if not isinstance(statement, dict):
            raise QuizValidationError("statement must be an object")
        statement_value(statement, validation_assignment)

    solutions: list[dict[str, str]] = []
    for values in itertools.product((False, True), repeat=len(people)):
        assignment = dict(zip(people, values))
        if all(
            assignment[statement["speaker"]]
            == statement_value(statement, assignment)
            for statement in statements
        ):
            solutions.append(
                {
                    person: "honest" if assignment[person] else "liar"
                    for person in people
                }
            )
    return _require_unique_solution(solutions)


def _constraint_matches_order(
    constraint: dict[str, Any],
    positions: dict[str, int],
    items: list[str],
) -> bool:
    """Evaluate one closed-vocabulary ordering constraint."""
    op = constraint.get("op")
    if op in {"position", "not_position"}:
        _validate_object_keys(
            constraint,
            {"op", "item", "position"},
            {"op", "item", "position"},
        )
        item, position = constraint["item"], constraint["position"]
        if (
            item not in items
            or isinstance(position, bool)
            or not isinstance(position, int)
        ):
            raise QuizValidationError("invalid position constraint")
        if not 1 <= position <= len(items):
            raise QuizValidationError("position is outside the permutation")
        matches = positions[item] == position
        return matches if op == "position" else not matches
    if op in {"before", "after", "adjacent", "not_adjacent"}:
        _validate_object_keys(
            constraint,
            {"op", "left", "right"},
            {"op", "left", "right"},
        )
        left, right = constraint["left"], constraint["right"]
        if left not in items or right not in items or left == right:
            raise QuizValidationError("invalid ordering reference")
        if op == "before":
            return positions[left] < positions[right]
        if op == "after":
            return positions[left] > positions[right]
        adjacent = abs(positions[left] - positions[right]) == 1
        return adjacent if op == "adjacent" else not adjacent
    raise QuizValidationError("unknown DSL vocabulary")


def _solve_ordering(spec: dict[str, Any]) -> list[str]:
    """Exhaustively solve the ordering DSL."""
    _validate_object_keys(
        spec,
        {"kind", "items", "constraints"},
        {"kind", "items", "constraints"},
    )
    items = _validate_names(spec["items"], "items")
    constraints = spec["constraints"]
    if not isinstance(constraints, list) or not constraints:
        raise QuizValidationError("constraints must be a non-empty list")
    if any(not isinstance(item, dict) for item in constraints):
        raise QuizValidationError("constraint must be an object")
    solutions: list[list[str]] = []
    for permutation in itertools.permutations(items):
        positions = {
            item: index + 1 for index, item in enumerate(permutation)
        }
        if all(
            _constraint_matches_order(constraint, positions, items)
            for constraint in constraints
        ):
            solutions.append(list(permutation))
    return _require_unique_solution(solutions)


def _solve_matching(spec: dict[str, Any]) -> dict[str, str]:
    """Exhaustively solve the finite matching DSL."""
    _validate_object_keys(
        spec,
        {"kind", "items", "values", "constraints"},
        {"kind", "items", "values", "constraints"},
    )
    items = _validate_names(spec["items"], "items")
    values = _validate_names(spec["values"], "values")
    if len(items) != len(values):
        raise QuizValidationError("items and values must have equal length")
    constraints = spec["constraints"]
    if not isinstance(constraints, list) or not constraints:
        raise QuizValidationError("constraints must be a non-empty list")
    for constraint in constraints:
        if not isinstance(constraint, dict):
            raise QuizValidationError("constraint must be an object")
        _validate_object_keys(
            constraint,
            {"op", "item", "value"},
            {"op", "item", "value"},
        )
        if constraint["op"] not in {"match", "not_match"}:
            raise QuizValidationError("unknown DSL vocabulary")
        if constraint["item"] not in items or constraint["value"] not in values:
            raise QuizValidationError("invalid matching reference")
    solutions: list[dict[str, str]] = []
    for permutation in itertools.permutations(values):
        assignment = dict(zip(items, permutation))
        if all(
            (assignment[item["item"]] == item["value"])
            == (item["op"] == "match")
            for item in constraints
        ):
            solutions.append(assignment)
    return _require_unique_solution(solutions)


def _require_unique_solution(solutions: list[Any]) -> Any:
    """Return a unique solution or reject contradiction/ambiguity."""
    if len(solutions) != 1:
        raise QuizValidationError(
            "machine_spec must have exactly one solution"
        )
    return solutions[0]


def solve_machine_spec(spec: Any) -> Any:
    """Validate and solve one closed L1 machine specification."""
    if not isinstance(spec, dict):
        raise QuizValidationError("machine_spec must be an object")
    kind = spec.get("kind")
    if kind == "truth_tellers":
        return _solve_truth_tellers(spec)
    if kind == "ordering":
        return _solve_ordering(spec)
    if kind == "matching":
        return _solve_matching(spec)
    raise QuizValidationError("unknown DSL vocabulary")


def validate_content_fields(fields: Any, quiz_type: str) -> Any | None:
    """Run deterministic field and L1 machine checks.

    Returns:
        The canonical L1 solution, or ``None`` for L3.

    Raises:
        QuizValidationError: If any deterministic requirement is violated.
    """
    if not isinstance(fields, dict):
        raise QuizValidationError("quiz content must be an object")
    for name, limit in FIELD_LIMITS.items():
        value = fields.get(name)
        if not isinstance(value, str) or not value:
            raise QuizValidationError(f"{name} is required")
        if name == "illustration_scene":
            value = value.strip()
            if not value:
                raise QuizValidationError(f"{name} is required")
            fields[name] = value
        if len(value) > limit:
            raise QuizValidationError(f"{name} exceeds {limit} characters")
    tags = fields.get("tags")
    if (
        not isinstance(tags, list)
        or len(tags) != TAG_COUNT
        or any(
            not isinstance(tag, str)
            or not tag
            or len(tag) > TAG_MAX_LENGTH
            for tag in tags
        )
    ):
        raise QuizValidationError("tags must contain three strings of <=10 chars")

    if quiz_type == "L3":
        if not L3_ANSWER_PATTERN.fullmatch(fields["answer"]):
            raise QuizValidationError("L3 answer must use 約...（目安）")
        return None
    if quiz_type != "L1":
        raise QuizValidationError("unsupported quiz type")
    if "machine_spec" not in fields or "machine_answer" not in fields:
        raise QuizValidationError("L1 machine fields are required")
    solution = solve_machine_spec(fields["machine_spec"])
    if solution != fields["machine_answer"]:
        raise QuizValidationError("machine_answer does not match unique solution")
    return solution


def normalize_for_duplicate(value: str) -> str:
    """NFKC-normalize and remove whitespace and Unicode punctuation."""
    normalized = unicodedata.normalize("NFKC", value)
    return "".join(
        char
        for char in normalized
        if not char.isspace()
        and not unicodedata.category(char).startswith("P")
    )


def bigram_jaccard(left: str, right: str) -> float:
    """Calculate character-bigram Jaccard similarity."""
    left_normalized = normalize_for_duplicate(left)
    right_normalized = normalize_for_duplicate(right)
    if left_normalized == right_normalized:
        return 1.0
    left_bigrams = {
        left_normalized[index : index + 2]
        for index in range(max(1, len(left_normalized) - 1))
        if left_normalized
    }
    right_bigrams = {
        right_normalized[index : index + 2]
        for index in range(max(1, len(right_normalized) - 1))
        if right_normalized
    }
    union = left_bigrams | right_bigrams
    return len(left_bigrams & right_bigrams) / len(union) if union else 0.0


def _is_duplicate(question: str, recent_questions: list[str]) -> bool:
    """Return whether any recent question reaches the rejection threshold."""
    return any(
        bigram_jaccard(question, previous) >= DUPLICATE_JACCARD_THRESHOLD
        for previous in recent_questions
    )


def _extract_l3_number(answer: str) -> float:
    """Extract a comparable numeric magnitude from a Japanese range answer."""
    normalized = unicodedata.normalize("NFKC", answer)
    match = re.search(r"([0-9][0-9,.]*)\s*(万|億|兆)?", normalized)
    if match is None:
        raise QuizValidationError("L3 answer has no numeric value")
    value = float(match.group(1).replace(",", ""))
    multiplier = {"万": 1e4, "億": 1e8, "兆": 1e12}.get(
        match.group(2), 1.0
    )
    value *= multiplier
    if not math.isfinite(value) or value <= 0:
        raise QuizValidationError("L3 answer must be positive")
    return value


def _independent_validation(
    client: Any,
    model: str,
    fields: dict[str, Any],
    quiz_type: str,
    canonical_solution: Any | None,
) -> bool:
    """Run answer-blind independent LLM validation."""
    if quiz_type == "L1":
        validation = _request_json(
            client,
            model,
            L1_VALIDATION_INSTRUCTIONS
            + "\n問題文:\n"
            + fields["question"],
        )
        return validation.get("machine_answer") == canonical_solution

    validation = _request_json(
        client,
        model,
        L3_VALIDATION_INSTRUCTIONS
        + "\n問題文:\n"
        + fields["question"]
        + "\n生成側の推定ルート（最終回答値は非表示）:\n"
        + fields["explanation"],
    )
    if validation.get("route_valid") is not True:
        return False
    estimated = validation.get("estimated_value")
    if isinstance(estimated, bool) or not isinstance(estimated, (int, float)):
        return False
    if not math.isfinite(float(estimated)) or float(estimated) <= 0:
        return False
    generated_value = _extract_l3_number(fields["answer"])
    return math.floor(math.log10(generated_value)) == math.floor(
        math.log10(float(estimated))
    )


def _build_illustration_prompt(
    illustration_scene: str,
    slot_code: str,
) -> str:
    """Build the code-owned illustration prompt for one deterministic slot."""
    palette = SLOT_PALETTES[slot_code]
    mood = SLOT_TIME_MOODS[slot_code]
    brand_colors = "、".join(
        (
            palette["background"],
            palette["card"],
            palette["accent"],
            palette["decoration"],
        )
    )
    return (
        "縦型ショート動画の背景用イラストを作成する。\n"
        f"情景: {illustration_scene}\n"
        f"時間帯ムード: {mood}\n"
        f"ブランド配色（調和させる）: {brand_colors}\n"
        "文字・数字・記号は一切描画しない。クイズの答えや、答えを示唆する"
        "構図・物体・ジェスチャーも描画しない。人物や主要物は中央を避け、"
        "上に情報カードを重ねても自然な背景構成にする。"
    )


def _safe_area() -> tuple[int, int, int, int]:
    """Intersect zoompan and Instagram UI safe areas."""
    zoom_width = int(OUTPUT_WIDTH / ZOOM_END) - SAFE_BOX_MARGIN
    zoom_height = int(OUTPUT_HEIGHT / ZOOM_END) - SAFE_BOX_MARGIN
    zoom_left = (OUTPUT_WIDTH - zoom_width) // 2
    zoom_top = (OUTPUT_HEIGHT - zoom_height) // 2
    zoom_right = zoom_left + zoom_width
    zoom_bottom = zoom_top + zoom_height
    instagram_right = int(OUTPUT_WIDTH * (1 - INSTAGRAM_RIGHT_RESERVED_RATIO))
    instagram_bottom = int(OUTPUT_HEIGHT * (1 - INSTAGRAM_BOTTOM_RESERVED_RATIO))
    return (
        zoom_left,
        zoom_top,
        min(zoom_right, instagram_right),
        min(zoom_bottom, instagram_bottom),
    )


def _font(path: Path, size: int) -> ImageFont.FreeTypeFont:
    """Load one configured font size."""
    return ImageFont.truetype(str(path), size=size)


def _break_with_kinsoku(current: str, char: str) -> tuple[str, str]:
    """Split one overflowing line at a position allowed by Japanese kinsoku.

    行頭禁則（句読点・閉じ括弧が行頭に来る）と行末禁則（開き括弧が行末に
    残る）を避けるため、分割位置を 1 文字ずつ手前へ追い出す。行が空になる
    まで戻すことはしない（極端に狭い幅では禁則より収まりを優先する）。
    """
    text = current + char
    index = len(current)
    while index > 1 and (
        text[index] in LINE_START_PROHIBITED
        or text[index - 1] in LINE_END_PROHIBITED
    ):
        index -= 1
    return text[:index], text[index:]


def _wrapped_lines(
    draw: ImageDraw.ImageDraw,
    text: str,
    font: ImageFont.FreeTypeFont,
    max_width: int,
) -> list[str]:
    """Wrap Japanese text character-by-character by measured width."""
    lines: list[str] = []
    current = ""
    for char in text:
        if char == "\n":
            lines.append(current)
            current = ""
            continue
        candidate = current + char
        if current and draw.textlength(candidate, font=font) > max_width:
            head, carry = _break_with_kinsoku(current, char)
            lines.append(head)
            current = carry
        else:
            current = candidate
    if current or not lines:
        lines.append(current)
    return lines


def _fit_wrapped_text(
    draw: ImageDraw.ImageDraw,
    text: str,
    font_path: Path,
    initial_size: int,
    max_width: int,
    max_height: int,
) -> tuple[ImageFont.FreeTypeFont, list[str], int]:
    """Reduce font size until all wrapped text fits its assigned box."""
    for size in range(initial_size, MIN_BODY_FONT_SIZE - 1, -2):
        font = _font(font_path, size)
        lines = _wrapped_lines(draw, text, font, max_width)
        line_height = int(size * 1.45)
        if len(lines) * line_height <= max_height:
            return font, lines, line_height
    raise RuntimeError("Quiz text does not fit the safe layout")


def _draw_wrapped(
    draw: ImageDraw.ImageDraw,
    position: tuple[int, int],
    text: str,
    font_path: Path,
    initial_size: int,
    max_width: int,
    max_height: int,
    *,
    fill: str,
) -> int:
    """Draw fitted wrapped text and return the final y coordinate."""
    font, lines, line_height = _fit_wrapped_text(
        draw,
        text,
        font_path,
        initial_size,
        max_width,
        max_height,
    )
    x, y = position
    for line in lines:
        draw.text((x, y), line, font=font, fill=fill)
        y += line_height
    return y


def _cover_illustration(png: bytes) -> Image.Image:
    """Decode a generated PNG and cover the vertical output canvas."""
    try:
        with Image.open(BytesIO(png)) as source:
            source.load()
            if source.format != "PNG":
                raise RuntimeError("Quiz illustration must be a PNG")
            return ImageOps.fit(
                source.convert("RGB"),
                (OUTPUT_WIDTH, OUTPUT_HEIGHT),
                method=Image.Resampling.LANCZOS,
                centering=(0.5, 0.5),
            )
    except RuntimeError:
        raise
    except Exception as exc:
        raise RuntimeError("Invalid quiz illustration PNG") from exc


def _base_card(
    illustration: Image.Image,
    palette: dict[str, str],
    slot_label: str,
    fonts: dict[str, Path],
    *,
    dim_illustration: bool = False,
) -> tuple[Image.Image, ImageDraw.ImageDraw, tuple[int, int, int, int]]:
    """Create the shared illustrated flat-design card background."""
    image = illustration.copy()
    if dim_illustration:
        overlay = Image.new("RGB", image.size, palette["background"])
        image = Image.blend(
            image,
            overlay,
            ANSWER_ILLUSTRATION_OVERLAY_OPACITY,
        )
    draw = ImageDraw.Draw(image)
    safe = _safe_area()
    left, top, right, bottom = safe
    draw.rounded_rectangle(
        (left, top, right, bottom),
        radius=42,
        fill=palette["card"],
    )
    draw.ellipse(
        (left + 28, top + 26, left + 150, top + 148),
        fill=palette["decoration"],
    )
    draw.ellipse(
        (right - 105, bottom - 105, right - 25, bottom - 25),
        fill=palette["accent"],
    )
    label_box = (left + 180, top + 28, right - 180, top + 94)
    draw.rounded_rectangle(
        label_box,
        radius=30,
        fill=palette["decoration"],
    )
    label_font, label_lines, _ = _fit_wrapped_text(
        draw,
        slot_label,
        fonts["bold"],
        34,
        label_box[2] - label_box[0] - 40,
        label_box[3] - label_box[1] - 16,
    )
    draw.text(
        (
            (label_box[0] + label_box[2]) // 2,
            (label_box[1] + label_box[3]) // 2,
        ),
        label_lines[0],
        font=label_font,
        fill=palette["text"],
        anchor="mm",
    )
    return image, draw, safe


def _paste_coach(
    canvas: Image.Image,
    coach: Image.Image,
    safe: tuple[int, int, int, int],
) -> None:
    """Fit and paste a transparent coach pose inside the safe area."""
    _, _, right, bottom = safe
    fitted = ImageOps.contain(coach, COACH_BOX, Image.Resampling.LANCZOS)
    x = right - fitted.width - CARD_PADDING
    y = bottom - fitted.height - CARD_PADDING
    canvas.paste(fitted, (x, y), fitted)


def _encode_png(image: Image.Image) -> bytes:
    """Encode one RGB card as PNG."""
    output = BytesIO()
    image.save(output, format="PNG")
    return output.getvalue()


def _render_hook_card(
    fields: dict[str, Any],
    quiz_type: str,
    difficulty: str,
    coach: Image.Image,
    fonts: dict[str, Path],
    illustration: Image.Image,
    palette: dict[str, str],
    slot_label: str,
) -> bytes:
    """Render cut 1."""
    image, draw, safe = _base_card(
        illustration, palette, slot_label, fonts
    )
    left, top, right, bottom = safe
    x, y = left + CARD_PADDING, top + 130
    draw.text(
        (x, y),
        "今日の脳トレ",
        font=_font(fonts["bold"], HEADING_FONT_SIZE),
        fill=palette["accent"],
    )
    y += 140
    label = "論理パズル" if quiz_type == "L1" else "フェルミ推定"
    draw.rounded_rectangle(
        (x, y, x + 480, y + 74), 30, fill=palette["accent"]
    )
    draw.text(
        (x + 24, y + 8),
        f"{label}  {difficulty}",
        font=_font(fonts["bold"], SUPPLEMENT_FONT_SIZE),
        fill=palette["background"],
    )
    _draw_wrapped(
        draw,
        (x, y + 130),
        fields["hook"],
        fonts["bold"],
        HEADING_FONT_SIZE,
        right - x - CARD_PADDING,
        520,
        fill=palette["text"],
    )
    _paste_coach(image, coach, safe)
    return _encode_png(image)


def _render_question_card(
    fields: dict[str, Any],
    coach: Image.Image,
    fonts: dict[str, Path],
    illustration: Image.Image,
    palette: dict[str, str],
    slot_label: str,
) -> bytes:
    """Render cut 2."""
    image, draw, safe = _base_card(
        illustration, palette, slot_label, fonts
    )
    left, top, right, _ = safe
    x, y = left + CARD_PADDING, top + 130
    draw.text(
        (x, y),
        "問題",
        font=_font(fonts["bold"], HEADING_FONT_SIZE),
        fill=palette["accent"],
    )
    _draw_wrapped(
        draw,
        (x, y + 145),
        fields["question"],
        fonts["regular"],
        QUESTION_FONT_SIZE,
        right - x - CARD_PADDING,
        850,
        fill=palette["text"],
    )
    _paste_coach(image, coach, safe)
    return _encode_png(image)


def _render_think_card(
    count: int,
    fields: dict[str, Any],
    coach: Image.Image,
    fonts: dict[str, Path],
    illustration: Image.Image,
    palette: dict[str, str],
    slot_label: str,
) -> bytes:
    """Render one countdown sub-card that keeps the question readable."""
    image, draw, safe = _base_card(
        illustration, palette, slot_label, fonts
    )
    left, top, right, bottom = safe
    x, y = left + CARD_PADDING, top + 130
    draw.text(
        (x, y),
        str(count),
        font=_font(fonts["bold"], THINK_COUNT_FONT_SIZE),
        fill=palette["accent"],
    )
    # 問題文はカット 2 と同座標・同サイズに据え置き、カット間で動かさない
    _draw_wrapped(
        draw,
        (x, y + 145),
        fields["question"],
        fonts["regular"],
        QUESTION_FONT_SIZE,
        right - x - CARD_PADDING,
        850,
        fill=palette["text"],
    )
    # ポーズ記号 U+23F8 は Noto Sans JP に無いグリフのため矩形 2 本で描く
    hint_x = left + CARD_PADDING
    hint_y = top + 1150
    for offset in (0, 26):
        draw.rounded_rectangle(
            (hint_x + offset, hint_y + 6, hint_x + offset + 14, hint_y + 52),
            radius=6,
            fill=palette["muted_text"],
        )
    # ヒントはコーチ画像（右下・COACH_BOX 幅）の左隣に収める
    hint_max_width = (
        right - COACH_BOX[0] - CARD_PADDING - (hint_x + 72) - 24
    )
    _draw_wrapped(
        draw,
        (hint_x + 72, hint_y),
        "止めてじっくり考えても OK",
        fonts["bold"],
        SUPPLEMENT_FONT_SIZE,
        hint_max_width,
        180,
        fill=palette["muted_text"],
    )
    _paste_coach(image, coach, (left, top, right, bottom))
    return _encode_png(image)


def _render_answer_card(
    fields: dict[str, Any],
    quiz_type: str,
    coach: Image.Image,
    fonts: dict[str, Path],
    illustration: Image.Image,
    palette: dict[str, str],
    slot_label: str,
) -> bytes:
    """Render cut 4 with a visual loop-closing title."""
    image, draw, safe = _base_card(
        illustration,
        palette,
        slot_label,
        fonts,
        dim_illustration=True,
    )
    left, top, right, _ = safe
    x, y = left + CARD_PADDING, top + 130
    label = "論理パズル" if quiz_type == "L1" else "フェルミ推定"
    draw.text(
        (x, y),
        f"答え｜{label}",
        font=_font(fonts["bold"], 66),
        fill=palette["accent"],
    )
    y = _draw_wrapped(
        draw,
        (x, y + 115),
        fields["answer"],
        fonts["bold"],
        QUESTION_FONT_SIZE,
        right - x - CARD_PADDING,
        230,
        fill=palette["text"],
    )
    y = _draw_wrapped(
        draw,
        (x, y + 38),
        fields["explanation"],
        fonts["regular"],
        SUPPLEMENT_FONT_SIZE,
        right - x - CARD_PADDING,
        430,
        fill=palette["text"],
    )
    _draw_wrapped(
        draw,
        (x, y + 40),
        fields["coach_comment"],
        fonts["bold"],
        SUPPLEMENT_FONT_SIZE,
        right - x - CARD_PADDING,
        160,
        fill=palette["accent"],
    )
    _paste_coach(image, coach, safe)
    return _encode_png(image)


def _render_cards(
    fields: dict[str, Any],
    quiz_type: str,
    difficulty: str,
    slot_code: str,
    slot_label: str,
    illustration_png: bytes,
    coaches: dict[str, Image.Image],
    fonts: dict[str, Path],
) -> tuple[list[bytes], list[bytes]]:
    """Render eight timeline cards and four representative cut cards."""
    palette = SLOT_PALETTES[slot_code]
    illustration = _cover_illustration(illustration_png)
    cut1 = _render_hook_card(
        fields,
        quiz_type,
        difficulty,
        coaches["hook"],
        fonts,
        illustration,
        palette,
        slot_label,
    )
    cut2 = _render_question_card(
        fields,
        coaches["question"],
        fonts,
        illustration,
        palette,
        slot_label,
    )
    think_cards = [
        _render_think_card(
            count,
            fields,
            coaches["think"],
            fonts,
            illustration,
            palette,
            slot_label,
        )
        for count in range(5, 0, -1)
    ]
    cut4 = _render_answer_card(
        fields,
        quiz_type,
        coaches["answer"],
        fonts,
        illustration,
        palette,
        slot_label,
    )
    timeline = [cut1, cut2, *think_cards, cut4]
    return timeline, [cut1, cut2, think_cards[0], cut4]


def _zoompan_filter(input_index: int, duration: int, output: str) -> str:
    """Build one supersampled per-segment zoompan filter."""
    total_frames = OUTPUT_FPS * duration
    denominator = total_frames - 1
    delta = ZOOM_END - ZOOM_START
    return (
        f"[{input_index}:v]"
        f"scale={OUTPUT_WIDTH * SUPERSAMPLE_FACTOR}:"
        f"{OUTPUT_HEIGHT * SUPERSAMPLE_FACTOR},"
        f"zoompan=z='{ZOOM_START:.1f}+{delta:.2f}*on/{denominator}':"
        "x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:"
        f"s={OUTPUT_WIDTH}x{OUTPUT_HEIGHT}:fps={OUTPUT_FPS},"
        f"format=yuv420p,setpts=PTS-STARTPTS[{output}]"
    )


def _run_ffmpeg(command: list[str], phase: str) -> None:
    """Run one ffmpeg pass with consistent timeout and stderr logging."""
    try:
        subprocess.run(
            command,
            check=True,
            capture_output=True,
            timeout=FFMPEG_TIMEOUT_SECONDS,
        )
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as exc:
        stderr = exc.stderr or b""
        if isinstance(stderr, bytes):
            stderr = stderr.decode(errors="replace")
        logger.error("ffmpeg %s failed: %s", phase, str(stderr)[-500:])
        raise


def _build_video(
    cards: list[bytes],
    bgm: bytes,
    tick: bytes,
    chime: bytes,
) -> bytes:
    """Encode cards sequentially, then copy-concat and mix timed audio."""
    if len(cards) != len(CUT_DURATIONS):
        raise RuntimeError("Quiz video requires exactly eight cards")
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        card_paths: list[Path] = []
        for index, content in enumerate(cards):
            path = temp_path / f"card-{index}.png"
            path.write_bytes(content)
            card_paths.append(path)
        audio_paths = [
            temp_path / "bgm.m4a",
            temp_path / "tick.m4a",
            temp_path / "chime.m4a",
        ]
        for path, content in zip(audio_paths, (bgm, tick, chime)):
            path.write_bytes(content)
        segment_paths: list[Path] = []
        for index, (card_path, duration) in enumerate(
            zip(card_paths, CUT_DURATIONS)
        ):
            segment_path = temp_path / f"segment-{index}.mp4"
            segment_command = [
                FFMPEG_BINARY,
                "-y",
                "-loglevel",
                "error",
                "-loop",
                "1",
                "-framerate",
                str(OUTPUT_FPS),
                "-t",
                str(duration),
                "-i",
                str(card_path),
                "-filter_complex",
                _zoompan_filter(0, duration, "v"),
                "-map",
                "[v]",
                "-an",
                "-c:v",
                "libx264",
                "-crf",
                str(OUTPUT_CRF),
                "-preset",
                "medium",
                "-t",
                str(duration),
                str(segment_path),
            ]
            _run_ffmpeg(segment_command, f"segment-{index + 1}")
            if not segment_path.is_file() or segment_path.stat().st_size == 0:
                raise RuntimeError(
                    f"ffmpeg produced an empty segment: index={index}"
                )
            segment_paths.append(segment_path)

        filelist_path = temp_path / "segments.txt"
        filelist_path.write_text(
            "".join(f"file '{path.as_posix()}'\n" for path in segment_paths),
            encoding="utf-8",
        )
        output_path = temp_path / "quiz.mp4"
        audio_filters = [
            f"[1:a]volume={BGM_VOLUME:.6f},"
            f"atrim=0:{OUTPUT_DURATION_SECONDS},asetpts=PTS-STARTPTS[bgm]",
            f"[2:a]volume={TICK_VOLUME:.6f},"
            f"adelay={TICK_DELAY_MILLISECONDS}|{TICK_DELAY_MILLISECONDS}[tick]",
            f"[3:a]volume={CHIME_VOLUME:.6f},"
            f"adelay={CHIME_DELAY_MILLISECONDS}|{CHIME_DELAY_MILLISECONDS}[chime]",
            f"[bgm][tick][chime]amix=inputs=3:duration=longest:"
            f"normalize=0,atrim=0:{OUTPUT_DURATION_SECONDS}[a]",
        ]
        final_command = [
            FFMPEG_BINARY,
            "-y",
            "-loglevel",
            "error",
            "-f",
            "concat",
            "-safe",
            "0",
            "-i",
            str(filelist_path),
            "-stream_loop",
            "-1",
            "-i",
            str(audio_paths[0]),
            "-i",
            str(audio_paths[1]),
            "-i",
            str(audio_paths[2]),
            "-filter_complex",
            ";".join(audio_filters),
            "-map",
            "0:v:0",
            "-map",
            "[a]",
            "-c:v",
            "copy",
            "-movflags",
            "+faststart",
            "-c:a",
            "aac",
            "-t",
            str(OUTPUT_DURATION_SECONDS),
            str(output_path),
        ]
        _run_ffmpeg(final_command, "concat-and-audio")
        result = output_path.read_bytes()
        if not result:
            raise RuntimeError("ffmpeg produced an empty output file")
        return result


def _insert_quiz_item(
    context: GeneratorContext,
    quiz_type: str,
    difficulty: str,
    fields: dict[str, Any],
) -> None:
    """Stage quiz history in the shared media transaction."""
    context.cursor.execute(
        "INSERT INTO quiz_items "
        "(set_id, generation_run_id, quiz_type, difficulty, summary, "
        "question_text, answer_text, content_fields) "
        "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
        (
            context.prompt_config.set_id,
            context.generation_run_id,
            quiz_type,
            difficulty,
            fields["summary"],
            fields["question"],
            fields["answer"],
            json.dumps(fields, ensure_ascii=False),
        ),
    )


def generate(context: GeneratorContext) -> GeneratorResult:
    """Generate a validated 20-second, eight-card quiz reel."""
    llm_model, slots, max_regenerations = _parse_parameters(
        context.prompt_config.parameters
    )
    slot = resolve_slot(context.scheduled_at, slots)
    quiz_type = slot["quiz_type"]
    difficulty = slot["difficulty"]
    slot_code = slot["slot_code"]
    tone_hint = slot["tone_hint"]
    slot_label = slot["slot_label"]

    # All fixed assets are checked before the first LLM call.
    fonts = _load_fonts()
    set_code = _fetch_set_code(context)
    coaches = _load_coach_assets(context, set_code)
    bgm_id, bgm, tick, chime = _load_audio_assets(
        context, set_code, slot_code
    )
    summaries, recent_questions = _fetch_history(context, quiz_type)

    api_key = openai_image.load_api_key()
    client = openai_image.build_client(api_key)
    selected_fields: dict[str, Any] | None = None
    last_reason = "unknown validation failure"
    for attempt in range(max_regenerations + 1):
        prompt = _build_generation_prompt(
            context.prompt_config.prompt_text,
            quiz_type,
            difficulty,
            tone_hint,
            summaries,
            attempt,
        )
        try:
            fields = _request_quiz_fields(client, llm_model, prompt)
            canonical = validate_content_fields(fields, quiz_type)
            if not _independent_validation(
                client, llm_model, fields, quiz_type, canonical
            ):
                raise QuizValidationError("independent LLM validation failed")
            if _is_duplicate(fields["question"], recent_questions):
                raise QuizValidationError("question duplicates recent history")
        except (QuizValidationError, json.JSONDecodeError, TypeError) as exc:
            last_reason = str(exc)
            logger.warning(
                "クイズ検証 NG、再生成: attempt=%s/%s reason=%s",
                attempt + 1,
                max_regenerations + 1,
                last_reason,
            )
            continue
        selected_fields = fields
        break
    if selected_fields is None:
        raise RuntimeError(
            "Quiz generation exhausted regeneration limit: " + last_reason
        )

    illustration_prompt = _build_illustration_prompt(
        selected_fields["illustration_scene"],
        slot_code,
    )
    illustration_png = openai_image.request_illustration(
        client,
        illustration_prompt,
    )
    timeline_cards, cut_cards = _render_cards(
        selected_fields,
        quiz_type,
        difficulty,
        slot_code,
        slot_label,
        illustration_png,
        coaches,
        fonts,
    )
    video = _build_video(timeline_cards, bgm, tick, chime)
    _insert_quiz_item(
        context, quiz_type, difficulty, selected_fields
    )
    context.cursor.execute(
        "UPDATE audio_assets SET last_used_at = %s WHERE id = %s",
        (now_utc(), bgm_id),
    )

    return GeneratorResult(
        media=[
            MediaOutput(
                content=video,
                file_format="mp4",
                width=OUTPUT_WIDTH,
                height=OUTPUT_HEIGHT,
                duration_seconds=OUTPUT_DURATION_SECONDS,
                audio_asset_id=bgm_id,
            )
        ],
        intermediates=[
            *[
                IntermediateOutput(
                    content=content,
                    file_format="png",
                    suffix=f"_cut{index}",
                    output_index=0,
                )
                for index, content in enumerate(cut_cards, start=1)
            ],
            IntermediateOutput(
                content=illustration_png,
                file_format="png",
                suffix="_illustration",
                output_index=0,
            ),
        ],
    )
