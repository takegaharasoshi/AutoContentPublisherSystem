"""Tests for generated image repository helpers."""

import datetime
from unittest.mock import Mock

from app.images import build_s3_key, has_generated_image, insert_generated_image


def test_build_s3_key_uses_scheduled_date_and_output_index() -> None:
    """The key format is deterministic and uses a jpg suffix."""
    assert build_s3_key(
        "daily", datetime.datetime(2026, 7, 19), 12, 4, 1
    ) == "images/daily/20260719/12/4_1.jpg"


def test_has_generated_image_returns_database_existence() -> None:
    """A single selected row means the prompt is complete."""
    cursor = Mock()
    cursor.fetchone.return_value = (1,)

    assert has_generated_image(cursor, 8, 3)
    cursor.execute.assert_called_once_with(
        "SELECT 1 FROM generated_images WHERE generation_run_id = %s "
        "AND prompt_config_id = %s LIMIT 1",
        (8, 3),
    )


def test_insert_generated_image_uses_raw_snapshot_values() -> None:
    """Metadata insertion preserves snapshot fields and returns its ID."""
    cursor = Mock(lastrowid=20)
    generated_at = datetime.datetime(2026, 7, 19)

    assert insert_generated_image(
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
        file_size_bytes=10,
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
        10,
        generated_at,
    )
