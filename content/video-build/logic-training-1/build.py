"""Build reviewed-candidate quiz videos inside the image-batch Docker image."""

from __future__ import annotations

from io import BytesIO
import os
from pathlib import Path
from typing import Any

import boto3
from PIL import Image

from common import (
    SET_CODE,
    WORK,
    dump_json,
    fetch_unbuilt_items,
    local_connection,
    resolve_slots,
    utc_now,
)
from acps_shared.s3 import get_object
from app.generators import gpt_quiz_multicut as quiz


def _bucket() -> str:
    bucket = os.environ.get("S3_BUCKET_NAME")
    if not bucket:
        raise RuntimeError("S3_BUCKET_NAME is required")
    return bucket


def _load_coaches(bucket: str, client: Any) -> dict[str, Image.Image]:
    """Load the fixed renderer assets once for the batch."""
    coaches: dict[str, Image.Image] = {}
    for pose, filename in quiz.COACH_FILENAMES.items():
        content = get_object(bucket, f"assets/{SET_CODE}/{filename}", client=client)
        with Image.open(BytesIO(content)) as image:
            image.load()
            coaches[pose] = image.convert("RGBA")
    return coaches


def _load_audio(
    connection: Any,
    bucket: str,
    client: Any,
    slot_code: str,
) -> tuple[int, str, bytes, bytes, bytes]:
    """Choose BGM by slot LRU and load the mandatory audio assets."""
    with connection.cursor() as cursor:
        cursor.execute("SELECT id FROM batch_sets WHERE set_code = %s", (SET_CODE,))
        set_row = cursor.fetchone()
        if set_row is None:
            raise RuntimeError(f"batch_sets row not found: {SET_CODE}")
        set_id = int(set_row[0])
        cursor.execute(
            "SELECT id, s3_key FROM audio_assets WHERE set_id = %s "
            "AND asset_type = 'se' AND is_active = 1",
            (set_id,),
        )
        se_rows = {str(row[1]): int(row[0]) for row in cursor.fetchall()}
        tick_key = f"audio/{SET_CODE}/se/countdown_tick.m4a"
        chime_key = f"audio/{SET_CODE}/se/answer_chime.m4a"
        if tick_key not in se_rows or chime_key not in se_rows:
            raise RuntimeError("Required quiz sound effects are not registered")
        cursor.execute(
            "SELECT id, s3_key FROM audio_assets WHERE set_id = %s "
            "AND asset_type = 'bgm' AND is_active = 1 "
            "AND (time_slot = %s OR time_slot IS NULL) "
            "ORDER BY last_used_at ASC, id ASC LIMIT 1",
            (set_id, slot_code),
        )
        bgm_row = cursor.fetchone()
        if bgm_row is None:
            raise RuntimeError(f"No active BGM for slot {slot_code}")
        bgm_id, bgm_key = int(bgm_row[0]), str(bgm_row[1])
    return (
        bgm_id,
        bgm_key,
        get_object(bucket, bgm_key, client=client),
        get_object(bucket, tick_key, client=client),
        get_object(bucket, chime_key, client=client),
    )


def _record_bgm_use(connection: Any, bgm_id: int) -> None:
    """Persist an LRU consumption only after the corresponding video was built."""
    with connection.cursor() as cursor:
        cursor.execute(
            "UPDATE audio_assets SET last_used_at = %s WHERE id = %s",
            (utc_now(), bgm_id),
        )
    connection.commit()


def main() -> None:
    """Render all unbuilt items for which normalized illustrations are present."""
    bucket = _bucket()
    s3_client = boto3.client("s3")
    connection = local_connection()
    try:
        slots = resolve_slots(connection)
        items = fetch_unbuilt_items(connection)
        coaches = _load_coaches(bucket, s3_client)
        fonts = quiz._load_fonts()
        manifest: dict[str, Any] = {}
        for item in items:
            illustration_path = WORK / "illustrations" / f"{item['id']}.png"
            if not illustration_path.is_file():
                print(f"{item['id']}: illustration missing; skipped")
                continue
            slot = slots.get((item["quiz_type"], item["difficulty"]))
            if slot is None:
                raise RuntimeError(f"No unique slot for stock item {item['id']}")
            bgm_id, bgm_s3_key, bgm, tick, chime = _load_audio(
                connection, bucket, s3_client, slot["slot_code"]
            )
            fields = dict(item["content_fields"])
            fields["question"] = item["question_text"]
            timeline, cuts = quiz._render_cards(
                fields,
                slot["slot_code"],
                slot["slot_label"],
                illustration_path.read_bytes(),
                coaches,
                fonts,
            )
            video = quiz._build_video(timeline, bgm, tick, chime)
            video_path = WORK / "videos" / f"{item['id']}.mp4"
            video_path.parent.mkdir(parents=True, exist_ok=True)
            video_path.write_bytes(video)
            cut_dir = WORK / "cuts"
            cut_dir.mkdir(parents=True, exist_ok=True)
            for index, cut in enumerate(cuts, start=1):
                (cut_dir / f"{item['id']}_cut{index}.png").write_bytes(cut)
            _record_bgm_use(connection, bgm_id)
            manifest[str(item["id"])] = {
                "audio_asset_id": bgm_id,
                "bgm_s3_key": bgm_s3_key,
                "question_text": item["question_text"],
                "slot_code": slot["slot_code"],
            }
            print(f"{item['id']}: built with BGM {bgm_id}")
        dump_json(WORK / "build_manifest.json", manifest)
    finally:
        connection.close()


if __name__ == "__main__":
    main()
