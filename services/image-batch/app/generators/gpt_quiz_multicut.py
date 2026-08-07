"""Stock-backed quiz multi-cut video generator."""

from __future__ import annotations

import datetime
from io import BytesIO
import json
import logging
from pathlib import Path
import subprocess
import tempfile
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

JST = datetime.timezone(datetime.timedelta(hours=9))

FIELD_LIMITS = {
    "hook": 20,
    "hint": 20,
    "question": 90,
    "answer": 30,
    "explanation": 80,
    "coach_comment": 30,
    "summary": 100,
    "illustration_scene": 200,
}
TAG_COUNT = 3
TAG_MAX_LENGTH = 10

OUTPUT_WIDTH = 1080
OUTPUT_HEIGHT = 1920
OUTPUT_FPS = 30
OUTPUT_DURATION_SECONDS = 16
OUTPUT_CRF = 20
FFMPEG_BINARY = "ffmpeg"
FFMPEG_TIMEOUT_SECONDS = 600
ZOOM_START = 1.0
ZOOM_END = 1.04
SUPERSAMPLE_FACTOR = 2
SAFE_BOX_MARGIN = 8
INSTAGRAM_RIGHT_RESERVED_RATIO = 0.12
INSTAGRAM_BOTTOM_RESERVED_RATIO = 0.15

HOOK_DURATION_SECONDS = 4
THINK_DURATION_SECONDS = 4
COUNTDOWN_DURATION_SECONDS = 1
GUIDANCE_DURATION_SECONDS = 3
CUT_DURATIONS = (
    HOOK_DURATION_SECONDS,
    THINK_DURATION_SECONDS,
    COUNTDOWN_DURATION_SECONDS,
    COUNTDOWN_DURATION_SECONDS,
    COUNTDOWN_DURATION_SECONDS,
    COUNTDOWN_DURATION_SECONDS,
    COUNTDOWN_DURATION_SECONDS,
    GUIDANCE_DURATION_SECONDS,
)

BGM_VOLUME = 1.0
TICK_VOLUME = 10 ** (-6 / 20)
CHIME_VOLUME = 10 ** (-3 / 20)
TICK_DELAY_MILLISECONDS = 8_000
CHIME_DELAY_MILLISECONDS = 13_000

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
HEADING_FONT_SIZE = 88
# カウントダウン数字は円バッジ（COUNT_BADGE_DIAMETER）に収まる大きさにする
THINK_COUNT_FONT_SIZE = 90
QUESTION_FONT_SIZE = 56
# 問題文とヒントの高さ上限は、テキストが最大まで伸びても
# カード内に MIN_ILLUSTRATION_HEIGHT のイラスト領域が残る値にする
QUESTION_MAX_HEIGHT = 420
THINK_BUBBLE_TEXT = "止めてじっくり考えても OK"
GUIDANCE_BUBBLE_TEXT = "答えは投稿のキャプションへ！"
SUPPLEMENT_FONT_SIZE = 40
MIN_BODY_FONT_SIZE = 30
LINE_START_PROHIBITED = "、。，．,.)）]］｝」』】〉》!！?？:：;；ー〜…‥・%％℃"
LINE_END_PROHIBITED = "（(「『【〈《[［｛"
CARD_PADDING = 64
COACH_BOX = (300, 430)
# コーチはカード下端から一定距離に立たせる（本文ではなく装飾のため、
# Instagram UI 予約域に足元が掛かることは許容し、上に空いた分をイラストへ回す）
COACH_BOTTOM_MARGIN = 140
# 情景イラストはカード内の横長ブロックとして、テキストの下・コーチの真上に常駐させる
# （コーチとは重ねない）。ブロックの上端は共通の問題文の最下端に
# 合わせ、カット間でイラストが動かないようにする。
CARD_CONTENT_GAP = 48
ILLUSTRATION_RADIUS = 28
MIN_ILLUSTRATION_HEIGHT = 200
# イラストの下端はコーチのすぐ上まで伸ばす
ILLUSTRATION_COACH_GAP = 16
# コーチのセリフは左隣の吹き出しに置く
BUBBLE_PADDING = 28
BUBBLE_TAIL_WIDTH = 28
BUBBLE_TOP_OFFSET = 60
BUBBLE_MAX_TEXT_HEIGHT = 200
# 時間帯ラベルのピル（テキスト幅 + アクセントドット）
LABEL_FONT_SIZE = 34
LABEL_PILL_HEIGHT = 66
LABEL_PILL_PADDING_X = 34
LABEL_DOT_DIAMETER = 16
# 見出し「問題」の左に添えるアクセントバー
HEADING_BAR_WIDTH = 14
# カウントダウンはアクセント色の円バッジに白抜きで表示する
COUNT_BADGE_DIAMETER = 150

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


def _parse_parameters(raw: str | None) -> list[dict[str, Any]]:
    """Parse and validate time-slot parameters."""
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
        quiz_type = quiz_type.strip()
        difficulty = slot["difficulty"].strip()
        if quiz_type not in {"L1", "L3"}:
            raise RuntimeError(f"unknown quiz_type: {quiz_type}")
        slot_code = slot["slot_code"].strip()
        if slot_code not in SLOT_PALETTES:
            raise RuntimeError(f"unknown slot_code: {slot_code}")
        validated_slots.append(
            {
                "from_jst_hour": hour,
                "quiz_type": quiz_type,
                "difficulty": difficulty,
                "slot_code": slot_code,
                "slot_label": slot["slot_label"].strip(),
            }
        )
    return validated_slots


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
    """Fail loudly before stock and API work when a font is missing."""
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


def validate_content_fields(fields: Any, quiz_type: str) -> dict[str, Any]:
    """Validate one stock item's structured fields defensively."""
    if isinstance(fields, (bytes, bytearray)):
        fields = fields.decode("utf-8")
    if isinstance(fields, str):
        try:
            fields = json.loads(fields)
        except json.JSONDecodeError as exc:
            raise RuntimeError("content_fields must be valid JSON") from exc
    if not isinstance(fields, dict):
        raise RuntimeError("content_fields must be a JSON object")

    for name, default_limit in FIELD_LIMITS.items():
        value = fields.get(name)
        if not isinstance(value, str) or not value.strip():
            raise RuntimeError(f"content_fields.{name} is required")
        limit = 240 if name == "explanation" and quiz_type == "L3" else default_limit
        if len(value) > limit:
            raise RuntimeError(
                f"content_fields.{name} exceeds {limit} characters"
            )

    tags = fields.get("tags")
    if (
        not isinstance(tags, list)
        or len(tags) != TAG_COUNT
        or any(
            not isinstance(tag, str)
            or not tag.strip()
            or len(tag) > TAG_MAX_LENGTH
            for tag in tags
        )
    ):
        raise RuntimeError(
            "content_fields.tags must contain exactly three non-empty "
            "strings of <=10 characters"
        )
    return fields


def _fetch_stock_item(
    cursor: Any,
    set_id: int,
    quiz_type: str,
    difficulty: str,
) -> dict[str, Any]:
    """Fetch and validate the least-recently-used active stock item."""
    cursor.execute(
        "SELECT id, question_text, answer_text, content_fields, last_used_at "
        "FROM quiz_stock_items WHERE set_id = %s AND quiz_type = %s "
        "AND difficulty = %s AND is_active = 1 "
        "ORDER BY last_used_at ASC, id ASC LIMIT 1",
        (set_id, quiz_type, difficulty),
    )
    row = cursor.fetchone()
    if row is None:
        raise RuntimeError(
            "No active quiz stock item for "
            f"set_id={set_id} quiz_type={quiz_type} difficulty={difficulty}"
        )

    stock_id = int(row[0])
    question_text = row[1]
    answer_text = row[2]
    for name, value, limit in (
        ("question_text", question_text, 90),
        ("answer_text", answer_text, 30),
    ):
        if not isinstance(value, str) or not value.strip():
            raise RuntimeError(f"quiz_stock_items.{name} is required")
        if len(value) > limit:
            raise RuntimeError(
                f"quiz_stock_items.{name} exceeds {limit} characters"
            )

    fields = validate_content_fields(row[3], quiz_type)
    if row[4] is not None:
        logger.warning(
            "Quiz stock item is being reused: stock_id=%s quiz_type=%s "
            "difficulty=%s",
            stock_id,
            quiz_type,
            difficulty,
        )
    return {
        "id": stock_id,
        "question_text": question_text,
        "answer_text": answer_text,
        "content_fields": fields,
    }


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


def _card_area() -> tuple[int, int, int, int]:
    """Card rectangle: the zoompan-safe box (content stays in _safe_area())."""
    zoom_width = int(OUTPUT_WIDTH / ZOOM_END) - SAFE_BOX_MARGIN
    zoom_height = int(OUTPUT_HEIGHT / ZOOM_END) - SAFE_BOX_MARGIN
    zoom_left = (OUTPUT_WIDTH - zoom_width) // 2
    zoom_top = (OUTPUT_HEIGHT - zoom_height) // 2
    return (zoom_left, zoom_top, zoom_left + zoom_width, zoom_top + zoom_height)


def _safe_area() -> tuple[int, int, int, int]:
    """Intersect zoompan and Instagram UI safe areas."""
    zoom_left, zoom_top, zoom_right, zoom_bottom = _card_area()
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


def _decode_illustration(png: bytes) -> Image.Image:
    """Decode one generated scene illustration."""
    try:
        with Image.open(BytesIO(png)) as source:
            source.load()
            if source.format != "PNG":
                raise RuntimeError("Quiz illustration must be a PNG")
            return source.convert("RGB")
    except RuntimeError:
        raise
    except Exception as exc:
        raise RuntimeError("Invalid quiz illustration PNG") from exc


def _paste_illustration(
    canvas: Image.Image,
    illustration: Image.Image,
    box: tuple[int, int, int, int],
    border_color: str,
) -> None:
    """Paste the scene illustration as a rounded block inside the card."""
    left, top, right, bottom = box
    width, height = right - left, bottom - top
    fitted = ImageOps.fit(
        illustration,
        (width, height),
        method=Image.Resampling.LANCZOS,
        centering=(0.5, 0.5),
    )
    mask = Image.new("L", (width, height), 0)
    ImageDraw.Draw(mask).rounded_rectangle(
        (0, 0, width - 1, height - 1),
        radius=ILLUSTRATION_RADIUS,
        fill=255,
    )
    canvas.paste(fitted, (left, top), mask)
    # 細い縁取りでカードと写真調ブロックの境界を整える
    ImageDraw.Draw(canvas).rounded_rectangle(
        (left, top, right - 1, bottom - 1),
        radius=ILLUSTRATION_RADIUS,
        outline=border_color,
        width=2,
    )


def _base_card(
    palette: dict[str, str],
    slot_label: str,
    fonts: dict[str, Path],
) -> tuple[Image.Image, ImageDraw.ImageDraw, tuple[int, int, int, int]]:
    """Create the shared flat-design card background."""
    image = Image.new("RGB", (OUTPUT_WIDTH, OUTPUT_HEIGHT), palette["background"])
    draw = ImageDraw.Draw(image)
    safe = _safe_area()
    left, top, right, bottom = safe
    # カードはズームセーフ枠いっぱい、本文はセーフエリア内（Instagram UI 予約域を避ける）
    draw.rounded_rectangle(
        _card_area(),
        radius=42,
        fill=palette["card"],
    )
    # 時間帯ラベルはテキスト幅に合わせたピルを上部中央に置き、
    # 左にアクセント色のドットを添える（空の飾り円は置かない）
    label_font = _font(fonts["bold"], LABEL_FONT_SIZE)
    label_width = int(draw.textlength(slot_label, font=label_font))
    dot = LABEL_DOT_DIAMETER
    inner_width = dot + 20 + label_width
    pill_left = (left + right - inner_width) // 2 - LABEL_PILL_PADDING_X
    pill_right = pill_left + inner_width + 2 * LABEL_PILL_PADDING_X
    pill_top = top + 30
    pill_bottom = pill_top + LABEL_PILL_HEIGHT
    draw.rounded_rectangle(
        (pill_left, pill_top, pill_right, pill_bottom),
        radius=LABEL_PILL_HEIGHT // 2,
        fill=palette["decoration"],
    )
    dot_top = (pill_top + pill_bottom - dot) // 2
    draw.ellipse(
        (
            pill_left + LABEL_PILL_PADDING_X,
            dot_top,
            pill_left + LABEL_PILL_PADDING_X + dot,
            dot_top + dot,
        ),
        fill=palette["accent"],
    )
    draw.text(
        (
            pill_left + LABEL_PILL_PADDING_X + dot + 20,
            (pill_top + pill_bottom) // 2,
        ),
        slot_label,
        font=label_font,
        fill=palette["text"],
        anchor="lm",
    )
    return image, draw, safe


def _draw_heading(
    draw: ImageDraw.ImageDraw,
    position: tuple[int, int],
    text: str,
    palette: dict[str, str],
    fonts: dict[str, Path],
    *,
    size: int = HEADING_FONT_SIZE,
) -> None:
    """Draw one section heading with the shared accent bar on its left."""
    x, y = position
    bar_height = int(size * 0.82)
    bar_top = y + (int(size * 1.18) - bar_height) // 2
    draw.rounded_rectangle(
        (x, bar_top, x + HEADING_BAR_WIDTH, bar_top + bar_height),
        radius=HEADING_BAR_WIDTH // 2,
        fill=palette["accent"],
    )
    draw.text(
        (x + HEADING_BAR_WIDTH + 28, y),
        text,
        font=_font(fonts["bold"], size),
        fill=palette["text"],
    )


def _paste_coach(
    canvas: Image.Image,
    coach: Image.Image,
    safe: tuple[int, int, int, int],
) -> None:
    """Fit and paste a transparent coach pose at the bottom of the safe area."""
    _, _, right, bottom = safe
    # アセットは 4 表情共通のキャンバス（下端中央そろえ）のため、
    # トリミングせずそのまま収めてカット間で大きさ・立ち位置を動かさない
    fitted = ImageOps.contain(coach, COACH_BOX, Image.Resampling.LANCZOS)
    x = right - fitted.width - CARD_PADDING
    y = _coach_top(bottom) + (COACH_BOX[1] - fitted.height)
    canvas.paste(fitted, (x, y), fitted)


def _coach_top(safe_bottom: int) -> int:
    """Top of the coach band (the illustration block ends above it)."""
    del safe_bottom  # コーチはカード下端を基準に立たせる
    return _card_area()[3] - COACH_BOTTOM_MARGIN - COACH_BOX[1]


def _trim_coaches(coaches: dict[str, Image.Image]) -> dict[str, Image.Image]:
    """Crop the shared empty margin of the four coach assets.

    アセットは 4 表情共通のキャンバス（下端中央そろえ）で作られているため、
    4 枚の不透明領域の和で同じ矩形を切り出せば、カット間の相対サイズ・
    立ち位置を保ったまま余白だけを取り除ける。
    """
    boxes = [image.getbbox() for image in coaches.values()]
    if any(box is None for box in boxes):
        return coaches
    left = min(box[0] for box in boxes)
    top = min(box[1] for box in boxes)
    right = max(box[2] for box in boxes)
    bottom = max(box[3] for box in boxes)
    return {
        pose: image.crop((left, top, right, bottom))
        for pose, image in coaches.items()
    }


def _draw_speech_bubble(
    draw: ImageDraw.ImageDraw,
    text: str,
    fonts: dict[str, Path],
    palette: dict[str, str],
    safe: tuple[int, int, int, int],
) -> None:
    """Draw one coach line as a speech bubble to the left of the coach."""
    left, _, right, bottom = safe
    bubble_right = right - CARD_PADDING - COACH_BOX[0] - BUBBLE_TAIL_WIDTH
    bubble_left = left + CARD_PADDING
    inner_width = bubble_right - bubble_left - 2 * BUBBLE_PADDING
    font, lines, line_height = _fit_wrapped_text(
        draw,
        text,
        fonts["bold"],
        SUPPLEMENT_FONT_SIZE,
        inner_width,
        BUBBLE_MAX_TEXT_HEIGHT,
    )
    text_height = len(lines) * line_height
    bubble_top = _coach_top(bottom) + BUBBLE_TOP_OFFSET
    bubble_bottom = bubble_top + text_height + 2 * BUBBLE_PADDING
    draw.rounded_rectangle(
        (bubble_left, bubble_top, bubble_right, bubble_bottom),
        radius=32,
        fill=palette["decoration"],
    )
    # コーチへ向かうしっぽ
    tail_y = (bubble_top + bubble_bottom) // 2
    draw.polygon(
        [
            (bubble_right - 4, tail_y - 26),
            (bubble_right - 4, tail_y + 26),
            (bubble_right + BUBBLE_TAIL_WIDTH, tail_y),
        ],
        fill=palette["decoration"],
    )
    y = bubble_top + BUBBLE_PADDING
    for line in lines:
        draw.text(
            (bubble_left + BUBBLE_PADDING, y),
            line,
            font=font,
            fill=palette["text"],
        )
        y += line_height


def _encode_png(image: Image.Image) -> bytes:
    """Encode one RGB card as PNG."""
    output = BytesIO()
    image.save(output, format="PNG")
    return output.getvalue()


def _render_card(
    fields: dict[str, Any],
    coach: Image.Image,
    bubble_text: str,
    fonts: dict[str, Path],
    illustration: Image.Image,
    palette: dict[str, str],
    slot_label: str,
    illustration_box: tuple[int, int, int, int] | None,
    *,
    countdown: int | None = None,
) -> tuple[bytes, int]:
    """Render the shared layout with only cut-specific details changed."""
    image, draw, safe = _base_card(palette, slot_label, fonts)
    left, top, right, _ = safe
    x, y = left + CARD_PADDING, top + 130
    _draw_heading(draw, (x, y), "問題", palette, fonts)

    if countdown is not None:
        badge = COUNT_BADGE_DIAMETER
        # バッジの数字も文字のため、カード右端ではなくセーフエリア
        # （Instagram UI 予約域を除いた領域）の右端に収める
        badge_left = right - badge
        badge_top = y - (badge - 104) // 2
        draw.ellipse(
            (
                badge_left,
                badge_top,
                badge_left + badge,
                badge_top + badge,
            ),
            fill=palette["accent"],
        )
        draw.text(
            (badge_left + badge // 2, badge_top + badge // 2),
            str(countdown),
            font=_font(fonts["bold"], THINK_COUNT_FONT_SIZE),
            fill=palette["card"],
            anchor="mm",
        )

    content_bottom = _draw_wrapped(
        draw,
        (x, y + 145),
        fields["question"],
        fonts["regular"],
        QUESTION_FONT_SIZE,
        right - x - CARD_PADDING,
        QUESTION_MAX_HEIGHT,
        fill=palette["text"],
    )
    if illustration_box is not None:
        _paste_illustration(
            image, illustration, illustration_box, palette["decoration"]
        )
    _draw_speech_bubble(draw, bubble_text, fonts, palette, safe)
    _paste_coach(image, coach, safe)
    return _encode_png(image), content_bottom


def _render_cards(
    fields: dict[str, Any],
    slot_code: str,
    slot_label: str,
    illustration_png: bytes,
    coaches: dict[str, Image.Image],
    fonts: dict[str, Path],
) -> tuple[list[bytes], list[bytes]]:
    """Render eight fixed-layout timeline cards and four cut leaders."""
    palette = SLOT_PALETTES[slot_code]
    illustration = _decode_illustration(illustration_png)
    coaches = _trim_coaches(coaches)

    _, content_bottom = _render_card(
        fields,
        coaches["hook"],
        fields["hook"],
        fonts,
        illustration,
        palette,
        slot_label,
        None,
    )
    left, _, right, bottom = _safe_area()
    box_top = content_bottom + CARD_CONTENT_GAP
    box_bottom = _coach_top(bottom) - ILLUSTRATION_COACH_GAP
    if box_bottom - box_top < MIN_ILLUSTRATION_HEIGHT:
        raise RuntimeError("Quiz text leaves no room for the scene illustration")
    illustration_box = (
        left + CARD_PADDING,
        box_top,
        right - CARD_PADDING,
        box_bottom,
    )

    cut1, _ = _render_card(
        fields,
        coaches["hook"],
        fields["hook"],
        fonts,
        illustration,
        palette,
        slot_label,
        illustration_box,
    )
    cut2, _ = _render_card(
        fields,
        coaches["think"],
        THINK_BUBBLE_TEXT,
        fonts,
        illustration,
        palette,
        slot_label,
        illustration_box,
    )
    countdown_cards = [
        _render_card(
            fields,
            coaches["question"],
            fields["hint"],
            fonts,
            illustration,
            palette,
            slot_label,
            illustration_box,
            countdown=count,
        )[0]
        for count in range(5, 0, -1)
    ]
    cut4, _ = _render_card(
        fields,
        coaches["answer"],
        GUIDANCE_BUBBLE_TEXT,
        fonts,
        illustration,
        palette,
        slot_label,
        illustration_box,
    )
    return (
        [cut1, cut2, *countdown_cards, cut4],
        [cut1, cut2, countdown_cards[0], cut4],
    )


def _zoompan_filter(
    input_index: int,
    duration: int,
    output: str,
    start_seconds: int = 0,
) -> str:
    """Build one segment of the continuous full-video zoom."""
    total_frames = OUTPUT_FPS * duration
    denominator = total_frames - 1
    full_delta = ZOOM_END - ZOOM_START
    segment_start = ZOOM_START + full_delta * (
        start_seconds / OUTPUT_DURATION_SECONDS
    )
    segment_end = ZOOM_START + full_delta * (
        (start_seconds + duration) / OUTPUT_DURATION_SECONDS
    )
    segment_delta = segment_end - segment_start
    return (
        f"[{input_index}:v]"
        f"scale={OUTPUT_WIDTH * SUPERSAMPLE_FACTOR}:"
        f"{OUTPUT_HEIGHT * SUPERSAMPLE_FACTOR},"
        f"zoompan=z='{segment_start:.5f}+{segment_delta:.5f}*on/"
        f"{denominator}':"
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
                _zoompan_filter(
                    0,
                    duration,
                    "v",
                    start_seconds=sum(CUT_DURATIONS[:index]),
                ),
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
            f"atrim=0:{OUTPUT_DURATION_SECONDS},"
            "afade=t=out:st=15:d=1,asetpts=PTS-STARTPTS[bgm]",
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
    stock_item_id: int,
    quiz_type: str,
    difficulty: str,
    question_text: str,
    answer_text: str,
    fields: dict[str, Any],
) -> None:
    """Stage quiz history in the shared media transaction."""
    context.cursor.execute(
        "INSERT INTO quiz_items "
        "(set_id, generation_run_id, stock_item_id, quiz_type, difficulty, summary, "
        "question_text, answer_text, content_fields) "
        "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
        (
            context.prompt_config.set_id,
            context.generation_run_id,
            stock_item_id,
            quiz_type,
            difficulty,
            fields["summary"],
            question_text,
            answer_text,
            json.dumps(fields, ensure_ascii=False),
        ),
    )


def generate(context: GeneratorContext) -> GeneratorResult:
    """Generate a stock-backed 16-second, eight-card quiz reel."""
    slots = _parse_parameters(context.prompt_config.parameters)
    slot = resolve_slot(context.scheduled_at, slots)
    quiz_type = slot["quiz_type"]
    difficulty = slot["difficulty"]
    slot_code = slot["slot_code"]
    slot_label = slot["slot_label"]

    # Fixed assets are checked before stock selection and the Images API call.
    fonts = _load_fonts()
    set_code = _fetch_set_code(context)
    coaches = _load_coach_assets(context, set_code)
    bgm_id, bgm, tick, chime = _load_audio_assets(
        context, set_code, slot_code
    )
    stock_item = _fetch_stock_item(
        context.cursor,
        context.prompt_config.set_id,
        quiz_type,
        difficulty,
    )
    fields = stock_item["content_fields"]

    api_key = openai_image.load_api_key()
    client = openai_image.build_client(api_key)

    illustration_prompt = _build_illustration_prompt(
        fields["illustration_scene"],
        slot_code,
    )
    illustration_png = openai_image.request_illustration(
        client,
        illustration_prompt,
    )
    render_fields = {**fields, "question": stock_item["question_text"]}
    timeline_cards, cut_cards = _render_cards(
        render_fields,
        slot_code,
        slot_label,
        illustration_png,
        coaches,
        fonts,
    )
    video = _build_video(timeline_cards, bgm, tick, chime)
    _insert_quiz_item(
        context,
        stock_item["id"],
        quiz_type,
        difficulty,
        stock_item["question_text"],
        stock_item["answer_text"],
        fields,
    )
    used_at = now_utc()
    context.cursor.execute(
        "UPDATE quiz_stock_items SET last_used_at = %s, "
        "use_count = use_count + 1 WHERE id = %s",
        (used_at, stock_item["id"]),
    )
    context.cursor.execute(
        "UPDATE audio_assets SET last_used_at = %s WHERE id = %s",
        (used_at, bgm_id),
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
