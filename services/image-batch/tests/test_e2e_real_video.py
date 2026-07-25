"""Opt-in real API, S3 audio, ffmpeg, and MySQL video E2E coverage."""

from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess
import tempfile
from typing import Any
from uuid import uuid4

import boto3
import pymysql
import pytest

from app.main import main


LOCAL_DB_SECRET = {
    "username": "app",
    "password": "password",
    "host": "127.0.0.1",
    "port": 3306,
    "dbname": "acps",
}
VIDEO_PARAMETERS = json.dumps(
    {"model": "gpt-image-2", "size": "1024x1536", "quality": "high", "n": 1}
)


def _connect() -> pymysql.connections.Connection:
    """Connect to the V001 and V002 local MySQL database."""
    return pymysql.connect(
        host=LOCAL_DB_SECRET["host"],
        port=LOCAL_DB_SECRET["port"],
        user=LOCAL_DB_SECRET["username"],
        password=LOCAL_DB_SECRET["password"],
        database=LOCAL_DB_SECRET["dbname"],
        connect_timeout=2,
        charset="utf8mb4",
    )


class HybridS3Client:
    """Delegate downloads to boto3 while recording uploads in memory."""

    def __init__(self) -> None:
        """Create the real read client and upload collection."""
        self.real_client = boto3.client("s3")
        self.put_calls: list[dict[str, Any]] = []

    def get_object(self, **kwargs: Any) -> dict[str, Any]:
        """Download a real existing audio object."""
        return self.real_client.get_object(**kwargs)

    def put_object(self, **kwargs: Any) -> None:
        """Record generated objects without writing them to S3."""
        self.put_calls.append(kwargs)


def _write_e2e_artifacts(
    video_upload: dict[str, Any],
    source_upload: dict[str, Any],
) -> None:
    """Write generated artifacts when an output directory is configured."""
    configured_dir = os.environ.get("E2E_VIDEO_OUTPUT_DIR")
    if not configured_dir:
        return
    output_dir = Path(configured_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    for upload in (video_upload, source_upload):
        output_path = output_dir / Path(upload["Key"]).name
        output_path.write_bytes(upload["Body"])


def test_write_e2e_artifacts_when_output_dir_is_configured(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Optional E2E output preserves the generated S3 filenames."""
    output_dir = tmp_path / "artifacts"
    monkeypatch.setenv("E2E_VIDEO_OUTPUT_DIR", str(output_dir))

    _write_e2e_artifacts(
        {"Key": "videos/set/run/1_0.mp4", "Body": b"video"},
        {"Key": "videos/set/run/1_0_source.jpg", "Body": b"source"},
    )

    assert (output_dir / "1_0.mp4").read_bytes() == b"video"
    assert (output_dir / "1_0_source.jpg").read_bytes() == b"source"


@pytest.fixture
def real_video_rows() -> tuple[str, int, int, int]:
    """Insert video test rows using an existing S3 audio key."""
    if os.environ.get("RUN_REAL_VIDEO_E2E") != "1":
        pytest.skip("RUN_REAL_VIDEO_E2E is not set; skipping real video E2E")
    try:
        connection = _connect()
    except Exception:
        pytest.skip("Local MySQL not reachable; skipping real video E2E")

    set_code = f"e2e-video-{uuid4().hex[:8]}"
    set_id = prompt_id = audio_id = None
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT s3_key FROM audio_assets WHERE is_active = 1 "
                "ORDER BY id LIMIT 1"
            )
            existing_audio = cursor.fetchone()
            if existing_audio is None:
                pytest.skip("No existing active audio asset to reuse")
            cursor.execute(
                "INSERT INTO batch_sets "
                "(set_code, name, description, generator_name, is_active) "
                "VALUES (%s, %s, %s, %s, %s)",
                (
                    set_code,
                    "Real Video E2E",
                    "pytest temporary row",
                    "gpt-image-kenburns",
                    1,
                ),
            )
            set_id = cursor.lastrowid
            cursor.execute(
                "INSERT INTO prompt_configs "
                "(set_id, prompt_text, negative_prompt, parameters, is_active) "
                "VALUES (%s, %s, %s, %s, %s)",
                (
                    set_id,
                    "A cinematic vertical view of a quiet Japanese landscape",
                    None,
                    VIDEO_PARAMETERS,
                    1,
                ),
            )
            prompt_id = cursor.lastrowid
            cursor.execute(
                "INSERT INTO audio_assets "
                "(set_id, s3_key, title, source_url, license_type, "
                "license_note, acquired_at, duration_seconds, is_active, "
                "last_used_at) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, "
                "%s, %s)",
                (
                    set_id,
                    existing_audio[0],
                    "E2E reused audio",
                    "https://example.com/e2e",
                    "test",
                    None,
                    "2026-07-25 00:00:00",
                    10,
                    1,
                    None,
                ),
            )
            audio_id = cursor.lastrowid
        connection.commit()
        yield set_code, set_id, prompt_id, audio_id
    finally:
        if set_id is not None:
            with connection.cursor() as cursor:
                cursor.execute(
                    "DELETE FROM generated_media WHERE set_id = %s", (set_id,)
                )
                cursor.execute(
                    "DELETE FROM generation_runs WHERE set_id = %s", (set_id,)
                )
                cursor.execute(
                    "DELETE FROM prompt_configs WHERE set_id = %s", (set_id,)
                )
                cursor.execute(
                    "DELETE FROM batch_execution_logs WHERE set_id = %s",
                    (set_id,),
                )
                cursor.execute(
                    "DELETE FROM audio_assets WHERE set_id = %s", (set_id,)
                )
                cursor.execute("DELETE FROM batch_sets WHERE id = %s", (set_id,))
            connection.commit()
        connection.close()


def test_main_generates_real_kenburns_video(
    real_video_rows: tuple[str, int, int, int],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The full video path produces valid MP4 and transactional metadata."""
    set_code, set_id, prompt_id, audio_id = real_video_rows
    bucket = os.environ.get("S3_BUCKET_NAME")
    if not bucket:
        pytest.fail("S3_BUCKET_NAME is required for RUN_REAL_VIDEO_E2E=1")
    env_name = os.environ.get("ENV_NAME", "prod")
    execution_arn = (
        f"arn:aws:states:local:000000000000:execution:e2e:{uuid4().hex}"
    )
    monkeypatch.setenv("ENV_NAME", env_name)
    monkeypatch.setenv("DB_SECRET_JSON", json.dumps(LOCAL_DB_SECRET))
    monkeypatch.setenv("SET_CODE", set_code)
    monkeypatch.setenv("EXECUTION_ARN", execution_arn)
    monkeypatch.setenv("SCHEDULED_AT", "2026-07-25T00:00:00Z")
    monkeypatch.setenv("API_SECRET_ARN", f"acps/{env_name}/image/api-key")
    monkeypatch.setenv("S3_BUCKET_NAME", bucket)
    hybrid_s3 = HybridS3Client()

    assert main(s3_client=hybrid_s3) == 0

    video_uploads = [
        call
        for call in hybrid_s3.put_calls
        if call["ContentType"] == "video/mp4"
    ]
    source_uploads = [
        call
        for call in hybrid_s3.put_calls
        if call["ContentType"] == "image/jpeg"
    ]
    assert len(video_uploads) == 1
    assert len(source_uploads) == 1
    assert source_uploads[0]["Key"].endswith(f"/{prompt_id}_0_source.jpg")
    _write_e2e_artifacts(video_uploads[0], source_uploads[0])

    with tempfile.TemporaryDirectory() as temp_dir:
        video_path = Path(temp_dir) / "result.mp4"
        video_path.write_bytes(video_uploads[0]["Body"])
        probe = subprocess.run(
            [
                "ffprobe",
                "-v",
                "error",
                "-show_entries",
                "format=duration:stream=codec_name,codec_type,width,height",
                "-of",
                "json",
                str(video_path),
            ],
            check=True,
            capture_output=True,
            text=True,
        )
    metadata = json.loads(probe.stdout)
    streams = metadata["streams"]
    video_stream = next(item for item in streams if item["codec_type"] == "video")
    audio_stream = next(item for item in streams if item["codec_type"] == "audio")
    assert video_stream["codec_name"] == "h264"
    assert (video_stream["width"], video_stream["height"]) == (1080, 1920)
    assert audio_stream["codec_name"] == "aac"
    assert len(streams) == 2
    assert float(metadata["format"]["duration"]) == pytest.approx(10, abs=0.5)

    connection = _connect()
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT file_format, duration_seconds, audio_asset_id "
                "FROM generated_media WHERE set_id = %s",
                (set_id,),
            )
            media_rows = cursor.fetchall()
            cursor.execute(
                "SELECT last_used_at FROM audio_assets WHERE id = %s",
                (audio_id,),
            )
            last_used_at = cursor.fetchone()[0]
    finally:
        connection.close()
    assert media_rows == (("mp4", 10, audio_id),)
    assert last_used_at is not None
