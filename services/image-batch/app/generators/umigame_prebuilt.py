"""Runtime generator for prebuilt umigame videos."""

from __future__ import annotations

import json
import logging
from typing import Any

from acps_shared.s3 import get_object

from ..clock import now_utc
from .contracts import GeneratorContext, GeneratorResult, MediaOutput


logger = logging.getLogger(__name__)

OUTPUT_WIDTH = 1080
OUTPUT_HEIGHT = 1920
DURATION_SECONDS = 24


def _parse_parameters(raw: str | None) -> int:
    """Require the sole supported duration and no slot configuration."""
    try:
        parameters = json.loads(raw or "{}")
    except (TypeError, json.JSONDecodeError) as exc:
        raise RuntimeError("parameters must be a JSON object") from exc
    if not isinstance(parameters, dict):
        raise RuntimeError("parameters must be a JSON object")
    if set(parameters) != {"duration_seconds"}:
        raise RuntimeError("parameters must contain only duration_seconds")
    duration = parameters["duration_seconds"]
    if (
        isinstance(duration, bool)
        or not isinstance(duration, int)
        or duration != DURATION_SECONDS
    ):
        raise RuntimeError("duration_seconds must be 24")
    return duration


def _fact_sheet(value: Any) -> list[str]:
    """Decode and validate the facts needed by the comment reply snapshot."""
    if isinstance(value, (bytes, bytearray)):
        try:
            value = value.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise RuntimeError("fact_sheet must be valid UTF-8 JSON") from exc
    if isinstance(value, str):
        try:
            value = json.loads(value)
        except json.JSONDecodeError as exc:
            raise RuntimeError("fact_sheet must be valid JSON") from exc
    if (
        not isinstance(value, list)
        or not value
        or any(not isinstance(fact, str) or not fact.strip() for fact in value)
    ):
        raise RuntimeError("fact_sheet must be a non-empty array of non-empty strings")
    return value


def _fetch_stock_item(cursor: Any, set_id: int) -> dict[str, Any]:
    """Lock the next built stock item in the configured posting order."""
    cursor.execute(
        "SELECT id, content_key, problem_text, truth, fact_sheet, rule_text, "
        "caption, hook, video_s3_key, video_audio_asset_id, use_count "
        "FROM umigame_stock_items "
        "WHERE set_id = %s AND is_active = 1 AND video_s3_key IS NOT NULL "
        "ORDER BY last_used_at IS NULL DESC, last_used_at ASC, id ASC "
        "LIMIT 1 FOR UPDATE",
        (set_id,),
    )
    row = cursor.fetchone()
    if row is None:
        raise RuntimeError(f"No built active umigame stock item for set_id={set_id}")

    names = (
        "id", "content_key", "problem_text", "truth", "fact_sheet",
        "rule_text", "caption", "hook", "video_s3_key",
        "video_audio_asset_id", "use_count",
    )
    item = dict(zip(names, row))
    for name in (
        "content_key", "problem_text", "truth", "rule_text", "hook",
        "caption", "video_s3_key",
    ):
        value = item[name]
        if not isinstance(value, str) or not value.strip():
            raise RuntimeError(f"umigame_stock_items.{name} is required")
    item["fact_sheet"] = _fact_sheet(item["fact_sheet"])
    if item["video_audio_asset_id"] is None:
        raise RuntimeError("umigame_stock_items.video_audio_asset_id is required")
    if int(item["use_count"]) >= 1:
        logger.warning("Umigame stock item is being reused: stock_id=%s", item["id"])
    return item


def generate(context: GeneratorContext) -> GeneratorResult:
    """Return one MP4 while staging its stock update and history row."""
    duration = _parse_parameters(context.prompt_config.parameters)
    item = _fetch_stock_item(context.cursor, context.prompt_config.set_id)
    video = get_object(
        context.s3_bucket,
        item["video_s3_key"],
        client=context.s3_client,
    )
    context.cursor.execute(
        "UPDATE umigame_stock_items SET last_used_at = %s, "
        "use_count = use_count + 1 WHERE id = %s",
        (now_utc(), item["id"]),
    )
    context.cursor.execute(
        "INSERT INTO umigame_items "
        "(set_id, generation_run_id, stock_item_id, content_key, problem_text, "
        "truth, fact_sheet, rule_text, hook, caption) "
        "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
        (
            context.prompt_config.set_id,
            context.generation_run_id,
            item["id"],
            item["content_key"],
            item["problem_text"],
            item["truth"],
            json.dumps(item["fact_sheet"], ensure_ascii=False),
            item["rule_text"],
            item["hook"],
            item["caption"],
        ),
    )
    return GeneratorResult(
        media=[
            MediaOutput(
                content=video,
                file_format="mp4",
                width=OUTPUT_WIDTH,
                height=OUTPUT_HEIGHT,
                duration_seconds=duration,
                audio_asset_id=item["video_audio_asset_id"],
            )
        ]
    )
