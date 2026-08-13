"""Prebuilt-video ranking generator used at runtime."""

from __future__ import annotations

import json
import logging
from typing import Any

from acps_shared.s3 import get_object

from ..clock import now_utc
from .contracts import GeneratorContext, GeneratorResult, MediaOutput
from .gpt_quiz_multicut import resolve_slot


logger = logging.getLogger(__name__)

OUTPUT_WIDTH = 1080
OUTPUT_HEIGHT = 1920
ALLOWED_DURATIONS = {20, 30}


def _parse_parameters(raw: str | None) -> list[dict[str, Any]]:
    """Parse and validate ranking time-slot parameters."""
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
    required_fields = {"from_jst_hour", "slot_code", "duration_seconds"}
    for slot in slots:
        if not isinstance(slot, dict):
            raise RuntimeError("each slots entry must be an object")
        missing = required_fields - set(slot)
        if missing:
            raise RuntimeError(
                "slots entry is missing required fields: "
                + ", ".join(sorted(missing))
            )
        hour = slot["from_jst_hour"]
        duration_seconds = slot["duration_seconds"]
        slot_code = slot["slot_code"]
        if isinstance(hour, bool) or not isinstance(hour, int) or not 0 <= hour <= 23:
            raise RuntimeError("from_jst_hour must be an integer from 0 to 23")
        if not isinstance(slot_code, str) or not slot_code.strip():
            raise RuntimeError("slot_code must be a non-empty string")
        if isinstance(duration_seconds, bool) or not isinstance(duration_seconds, int):
            raise RuntimeError("duration_seconds must be an integer")
        if duration_seconds not in ALLOWED_DURATIONS:
            raise RuntimeError("duration_seconds must be 20 or 30")
        validated_slots.append(
            {
                "from_jst_hour": hour,
                "slot_code": slot_code.strip(),
                "duration_seconds": duration_seconds,
            }
        )
    return validated_slots


def _video_s3_key_column(duration_seconds: int) -> str:
    """Return the allow-listed stock column for one output duration."""
    columns = {
        20: "video_s3_key_20s",
        30: "video_s3_key_30s",
    }
    try:
        return columns[duration_seconds]
    except KeyError:
        raise RuntimeError(
            f"Unsupported ranking video duration: {duration_seconds}"
        ) from None


def _decode_json_object(value: Any, field_name: str) -> dict[str, Any]:
    """Decode a JSON object stored in a ranking stock row."""
    if isinstance(value, (bytes, bytearray)):
        value = value.decode("utf-8")
    if isinstance(value, str):
        try:
            value = json.loads(value)
        except json.JSONDecodeError as exc:
            raise RuntimeError(f"{field_name} must be valid JSON") from exc
    if not isinstance(value, dict):
        raise RuntimeError(f"{field_name} must be a JSON object")
    return value


def _validate_content_fields(value: Any) -> dict[str, Any]:
    """Validate caption-relevant ranking content fields."""
    fields = _decode_json_object(value, "content_fields")
    for name in ("hook", "trivia", "source_display", "result_list"):
        field_value = fields.get(name)
        if not isinstance(field_value, str) or not field_value.strip():
            raise RuntimeError(f"content_fields.{name} is required")
    return fields


def _validate_ranking_data(value: Any) -> dict[str, Any]:
    """Validate the ranked TOP5 data snapshot defensively."""
    ranking_data = _decode_json_object(value, "ranking_data")
    entries = ranking_data.get("entries")
    if not isinstance(entries, list) or len(entries) != 5:
        raise RuntimeError("ranking_data.entries must contain exactly five entries")
    ranks: list[int] = []
    for entry in entries:
        if not isinstance(entry, dict):
            raise RuntimeError("ranking_data.entries entries must be objects")
        rank = entry.get("rank")
        if isinstance(rank, bool) or not isinstance(rank, int) or not 1 <= rank <= 5:
            raise RuntimeError(
                "ranking_data.entries.rank must be an integer from 1 to 5"
            )
        ranks.append(rank)
    if set(ranks) != {1, 2, 3, 4, 5}:
        raise RuntimeError("ranking_data.entries.rank must contain ranks 1 through 5")
    return ranking_data


def _fetch_prebuilt_stock_item(
    cursor: Any,
    set_id: int,
    duration_seconds: int,
) -> dict[str, Any]:
    """Fetch and validate the least-recently-used built ranking stock item."""
    video_column = _video_s3_key_column(duration_seconds)
    cursor.execute(
        "SELECT id, format, title, content_fields, ranking_data, "
        f"{video_column} AS video_s3_key, video_audio_asset_id, last_used_at "
        "FROM ranking_stock_items WHERE set_id = %s AND is_active = 1 "
        f"AND {video_column} IS NOT NULL "
        "ORDER BY last_used_at ASC, id ASC LIMIT 1",
        (set_id,),
    )
    row = cursor.fetchone()
    if row is None:
        raise RuntimeError(
            "No built active ranking stock item for "
            f"set_id={set_id} duration_seconds={duration_seconds}"
        )

    stock_id = int(row[0])
    format_name = row[1]
    title = row[2]
    if not isinstance(format_name, str) or not format_name.strip():
        raise RuntimeError("ranking_stock_items.format is required")
    if len(format_name) > 20:
        raise RuntimeError("ranking_stock_items.format exceeds 20 characters")
    if not isinstance(title, str) or not title.strip():
        raise RuntimeError("ranking_stock_items.title is required")
    if len(title) > 100:
        raise RuntimeError("ranking_stock_items.title exceeds 100 characters")

    content_fields = _validate_content_fields(row[3])
    ranking_data = _validate_ranking_data(row[4])
    video_s3_key = row[5]
    if not isinstance(video_s3_key, str) or not video_s3_key.strip():
        raise RuntimeError("ranking_stock_items.video_s3_key is required")
    if row[6] is None:
        raise RuntimeError(
            "ranking_stock_items.video_audio_asset_id is required: "
            f"stock_id={stock_id}"
        )

    if row[7] is not None:
        logger.warning(
            "Built ranking stock item is being reused: stock_id=%s "
            "duration_seconds=%s",
            stock_id,
            duration_seconds,
        )

    cursor.execute(
        "SELECT COUNT(*) FROM ranking_stock_items WHERE set_id = %s "
        "AND is_active = 1 "
        f"AND {video_column} IS NULL",
        (set_id,),
    )
    unbuilt_count_row = cursor.fetchone()
    if unbuilt_count_row is not None and int(unbuilt_count_row[0]) > 0:
        logger.warning(
            "Active ranking stock items remain unbuilt: count=%s "
            "duration_seconds=%s",
            unbuilt_count_row[0],
            duration_seconds,
        )

    return {
        "id": stock_id,
        "format": format_name,
        "title": title,
        "content_fields": content_fields,
        "ranking_data": ranking_data,
        "video_s3_key": video_s3_key,
        "video_audio_asset_id": int(row[6]),
    }


def _insert_ranking_item(
    context: GeneratorContext,
    stock_item: dict[str, Any],
    duration_seconds: int,
) -> None:
    """Stage the ranking item history in the shared media transaction."""
    context.cursor.execute(
        "INSERT INTO ranking_items "
        "(set_id, generation_run_id, format, title, content_fields, ranking_data, "
        "duration_seconds, stock_item_id) "
        "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
        (
            context.prompt_config.set_id,
            context.generation_run_id,
            stock_item["format"],
            stock_item["title"],
            json.dumps(stock_item["content_fields"], ensure_ascii=False),
            json.dumps(stock_item["ranking_data"], ensure_ascii=False),
            duration_seconds,
            stock_item["id"],
        ),
    )


def generate(context: GeneratorContext) -> GeneratorResult:
    """Return one prebuilt ranking MP4 and stage its stock consumption."""
    slots = _parse_parameters(context.prompt_config.parameters)
    slot = resolve_slot(context.scheduled_at, slots)
    duration_seconds = slot["duration_seconds"]
    stock_item = _fetch_prebuilt_stock_item(
        context.cursor,
        context.prompt_config.set_id,
        duration_seconds,
    )

    video = get_object(
        context.s3_bucket,
        stock_item["video_s3_key"],
        client=context.s3_client,
    )
    _insert_ranking_item(context, stock_item, duration_seconds)
    context.cursor.execute(
        "UPDATE ranking_stock_items SET last_used_at = %s, "
        "use_count = use_count + 1 WHERE id = %s",
        (now_utc(), stock_item["id"]),
    )
    return GeneratorResult(
        media=[
            MediaOutput(
                content=video,
                file_format="mp4",
                width=OUTPUT_WIDTH,
                height=OUTPUT_HEIGHT,
                duration_seconds=duration_seconds,
                audio_asset_id=stock_item["video_audio_asset_id"],
            )
        ]
    )
