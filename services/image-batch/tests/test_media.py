"""Tests for generated media repository helpers."""

import datetime
from unittest.mock import Mock

from app.media import build_s3_key, has_generated_media, insert_generated_media


def test_build_s3_key_builds_final_jpg_key() -> None:
    """Image media uses the images prefix and jpg extension."""
    assert build_s3_key(
        "daily",
        datetime.datetime(2026, 7, 19),
        12,
        4,
        1,
        prefix="images",
        extension="jpg",
    ) == "images/daily/20260719/12/4_1.jpg"


def test_build_s3_key_builds_final_mp4_and_source_jpg_keys() -> None:
    """Video and its source image share the videos prefix."""
    args = ("daily", datetime.datetime(2026, 7, 19), 12, 4, 0)
    assert build_s3_key(
        *args, prefix="videos", extension="mp4"
    ) == "videos/daily/20260719/12/4_0.mp4"
    assert build_s3_key(
        *args, prefix="videos", extension="jpg", suffix="_source"
    ) == "videos/daily/20260719/12/4_0_source.jpg"


def test_has_generated_media_returns_database_existence() -> None:
    """A single selected row means the prompt is complete."""
    cursor = Mock()
    cursor.fetchone.return_value = (1,)

    assert has_generated_media(cursor, 8, 3)
    cursor.execute.assert_called_once_with(
        "SELECT 1 FROM generated_media WHERE generation_run_id = %s "
        "AND prompt_config_id = %s LIMIT 1",
        (8, 3),
    )


def test_insert_generated_media_uses_all_metadata() -> None:
    """Metadata insertion preserves snapshot fields and returns its ID."""
    cursor = Mock(lastrowid=20)
    generated_at = datetime.datetime(2026, 7, 19)

    assert insert_generated_media(
        cursor,
        set_id=1,
        generation_run_id=2,
        prompt_config_id=3,
        output_index=0,
        prompt_text_snapshot="draw a cat",
        negative_prompt_snapshot=None,
        parameters_snapshot='{"size":"small"}',
        s3_key="images/a.jpg",
        s3_bucket="bucket",
        file_format="mp4",
        file_size_bytes=10,
        width=1080,
        height=1920,
        duration_seconds=10,
        audio_asset_id=9,
        generated_at=generated_at,
    ) == 20
    assert cursor.execute.call_args.args[1] == (
        1,
        2,
        3,
        0,
        "draw a cat",
        None,
        '{"size":"small"}',
        "images/a.jpg",
        "bucket",
        "mp4",
        10,
        1080,
        1920,
        10,
        9,
        generated_at,
    )
