"""Opt-in real OpenAI text, local MySQL, and ffmpeg quiz E2E coverage."""

from __future__ import annotations

from io import BytesIO
import json
import os
from pathlib import Path
import subprocess
import tempfile
from typing import Any
from uuid import uuid4

from PIL import Image, ImageDraw
import pymysql
import pytest

from app.generators import gpt_quiz_multicut as quiz
from app.generators import openai_image
from app.main import main


LOCAL_DB_SECRET = {
    "username": "app",
    "password": "password",
    "host": "127.0.0.1",
    "port": 3306,
    "dbname": "acps",
}


def _connect() -> pymysql.connections.Connection:
    """Connect to the local V003 MySQL database."""
    return pymysql.connect(
        host=LOCAL_DB_SECRET["host"],
        port=LOCAL_DB_SECRET["port"],
        user=LOCAL_DB_SECRET["username"],
        password=LOCAL_DB_SECRET["password"],
        database=LOCAL_DB_SECRET["dbname"],
        connect_timeout=2,
        charset="utf8mb4",
    )


def _coach_png(color: str) -> bytes:
    """Create a transparent RGBA coach silhouette."""
    image = Image.new("RGBA", (400, 600), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    draw.ellipse((110, 30, 290, 210), fill=color)
    draw.rounded_rectangle((70, 190, 330, 570), 80, fill=color)
    output = BytesIO()
    image.save(output, format="PNG")
    return output.getvalue()


def _sine_m4a(duration: float, frequency: int) -> bytes:
    """Generate a small AAC-in-M4A placeholder with ffmpeg."""
    with tempfile.TemporaryDirectory() as temp_dir:
        output_path = Path(temp_dir) / "tone.m4a"
        subprocess.run(
            [
                "ffmpeg",
                "-y",
                "-loglevel",
                "error",
                "-f",
                "lavfi",
                "-i",
                f"sine=frequency={frequency}:duration={duration}",
                "-c:a",
                "aac",
                str(output_path),
            ],
            check=True,
            capture_output=True,
        )
        return output_path.read_bytes()


class MemoryQuizS3Client:
    """Return generated placeholders for downloads and record uploads."""

    def __init__(self, objects: dict[str, bytes]) -> None:
        """Initialize object fixtures and upload history."""
        self.objects = objects
        self.put_calls: list[dict[str, Any]] = []

    def get_object(self, **kwargs: Any) -> dict[str, Any]:
        """Return a requested placeholder through the boto3 body shape."""
        return {"Body": BytesIO(self.objects[kwargs["Key"]])}

    def put_object(self, **kwargs: Any) -> None:
        """Record a generated object without external storage."""
        self.put_calls.append(kwargs)


def _write_e2e_artifacts(uploads: list[dict[str, Any]]) -> None:
    """Write MP4 and cut PNG uploads when explicitly configured."""
    configured_dir = os.environ.get("E2E_QUIZ_OUTPUT_DIR")
    if not configured_dir:
        return
    output_dir = Path(configured_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    for upload in uploads:
        if upload["ContentType"] in {"video/mp4", "image/png"}:
            (output_dir / Path(upload["Key"]).name).write_bytes(upload["Body"])


def test_write_quiz_e2e_artifacts_when_configured(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The opt-in output directory preserves generated filenames."""
    output_dir = tmp_path / "quiz-artifacts"
    monkeypatch.setenv("E2E_QUIZ_OUTPUT_DIR", str(output_dir))
    uploads = [
        {
            "Key": "videos/set/run/1_0.mp4",
            "Body": b"video",
            "ContentType": "video/mp4",
        },
        {
            "Key": "videos/set/run/1_0_cut1.png",
            "Body": b"cut",
            "ContentType": "image/png",
        },
    ]

    _write_e2e_artifacts(uploads)

    assert (output_dir / "1_0.mp4").read_bytes() == b"video"
    assert (output_dir / "1_0_cut1.png").read_bytes() == b"cut"


@pytest.fixture
def real_quiz_rows() -> tuple[str, int, int, int, str]:
    """Insert temporary quiz configuration and audio metadata."""
    if os.environ.get("RUN_REAL_QUIZ_E2E") != "1":
        pytest.skip("RUN_REAL_QUIZ_E2E is not set; skipping real quiz E2E")
    try:
        connection = _connect()
    except Exception:
        pytest.skip("Local MySQL with V003 is not reachable")

    model = os.environ.get("E2E_QUIZ_LLM_MODEL", quiz.DEFAULT_LLM_MODEL)
    set_code = f"e2e-quiz-{uuid4().hex[:8]}"
    set_id = prompt_id = bgm_id = None
    parameters = json.dumps(
        {
            "llm_model": model,
            "slots": [
                {
                    "from_jst_hour": 0,
                    "quiz_type": "L3",
                    "difficulty": "standard",
                }
            ],
            "max_regenerations": 3,
        }
    )
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO batch_sets "
                "(set_code, name, description, generator_name, is_active) "
                "VALUES (%s, %s, %s, %s, %s)",
                (
                    set_code,
                    "Real Quiz E2E",
                    "pytest temporary row",
                    "gpt-quiz-multicut",
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
                    "日本の日常生活を題材に、明るく学べる問題にする。",
                    None,
                    parameters,
                    1,
                ),
            )
            prompt_id = cursor.lastrowid
            rows = [
                (
                    f"audio/{set_code}/bgm/track.m4a",
                    "E2E BGM",
                    "bgm",
                    20,
                ),
                (
                    f"audio/{set_code}/se/countdown_tick.m4a",
                    "E2E tick",
                    "se",
                    1,
                ),
                (
                    f"audio/{set_code}/se/answer_chime.m4a",
                    "E2E chime",
                    "se",
                    1,
                ),
            ]
            for key, title, asset_type, duration in rows:
                cursor.execute(
                    "INSERT INTO audio_assets "
                    "(set_id, s3_key, asset_type, title, source_url, "
                    "license_type, license_note, acquired_at, "
                    "duration_seconds, is_active, last_used_at) "
                    "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                    (
                        set_id,
                        key,
                        asset_type,
                        title,
                        "https://example.com/e2e",
                        "test",
                        None,
                        "2026-07-27 00:00:00",
                        duration,
                        1,
                        None,
                    ),
                )
                if asset_type == "bgm":
                    bgm_id = cursor.lastrowid
        connection.commit()
        yield set_code, set_id, prompt_id, bgm_id, model
    finally:
        if set_id is not None:
            with connection.cursor() as cursor:
                cursor.execute(
                    "DELETE FROM generated_media WHERE set_id = %s", (set_id,)
                )
                cursor.execute(
                    "DELETE FROM quiz_items WHERE set_id = %s", (set_id,)
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


def _check_minimal_llm_connectivity(model: str) -> None:
    """Fail clearly if the configured text model cannot answer minimally."""
    try:
        client = openai_image.build_client(openai_image.load_api_key())
        response = client.responses.create(
            model=model,
            input="Reply with OK.",
        )
        if not response.output_text:
            raise RuntimeError("empty response")
    except Exception as exc:
        pytest.fail(
            f"Minimal OpenAI text connectivity failed for llm_model={model}: "
            f"{type(exc).__name__}: {exc}"
        )


def test_main_generates_real_quiz_video(
    real_quiz_rows: tuple[str, int, int, int, str],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The complete quiz path produces media and transactional history."""
    set_code, set_id, prompt_id, bgm_id, model = real_quiz_rows
    env_name = os.environ.get("ENV_NAME", "prod")
    monkeypatch.setenv("API_SECRET_ARN", f"acps/{env_name}/image/api-key")
    _check_minimal_llm_connectivity(model)

    objects = {
        **{
            f"assets/{set_code}/{filename}": _coach_png(color)
            for filename, color in zip(
                quiz.COACH_FILENAMES.values(),
                ("#e87979", "#69b3e7", "#77c593", "#f0b857"),
            )
        },
        f"audio/{set_code}/bgm/track.m4a": _sine_m4a(20, 220),
        f"audio/{set_code}/se/countdown_tick.m4a": _sine_m4a(0.2, 880),
        f"audio/{set_code}/se/answer_chime.m4a": _sine_m4a(0.7, 660),
    }
    memory_s3 = MemoryQuizS3Client(objects)
    execution_arn = (
        f"arn:aws:states:local:000000000000:execution:e2e:{uuid4().hex}"
    )
    monkeypatch.setenv("ENV_NAME", env_name)
    monkeypatch.setenv("DB_SECRET_JSON", json.dumps(LOCAL_DB_SECRET))
    monkeypatch.setenv("SET_CODE", set_code)
    monkeypatch.setenv("EXECUTION_ARN", execution_arn)
    monkeypatch.setenv("SCHEDULED_AT", "2026-07-27T02:00:00Z")
    monkeypatch.setenv("S3_BUCKET_NAME", "local-quiz-test-bucket")

    assert main(s3_client=memory_s3) == 0

    video_uploads = [
        item
        for item in memory_s3.put_calls
        if item["ContentType"] == "video/mp4"
    ]
    cut_uploads = [
        item
        for item in memory_s3.put_calls
        if item["ContentType"] == "image/png"
    ]
    assert len(video_uploads) == 1
    assert len(cut_uploads) == 4
    assert [Path(item["Key"]).stem[-5:] for item in cut_uploads] == [
        "_cut1",
        "_cut2",
        "_cut3",
        "_cut4",
    ]
    _write_e2e_artifacts(memory_s3.put_calls)

    with tempfile.TemporaryDirectory() as temp_dir:
        path = Path(temp_dir) / "quiz.mp4"
        path.write_bytes(video_uploads[0]["Body"])
        probe = subprocess.run(
            [
                "ffprobe",
                "-v",
                "error",
                "-show_entries",
                "format=duration:stream=codec_name,codec_type,width,height",
                "-of",
                "json",
                str(path),
            ],
            check=True,
            capture_output=True,
            text=True,
        )
    metadata = json.loads(probe.stdout)
    video_stream = next(
        item for item in metadata["streams"] if item["codec_type"] == "video"
    )
    audio_stream = next(
        item for item in metadata["streams"] if item["codec_type"] == "audio"
    )
    assert video_stream["codec_name"] == "h264"
    assert (video_stream["width"], video_stream["height"]) == (1080, 1920)
    assert audio_stream["codec_name"] == "aac"
    assert float(metadata["format"]["duration"]) == pytest.approx(20, abs=0.2)

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
                "SELECT generation_run_id, quiz_type, content_fields "
                "FROM quiz_items WHERE set_id = %s",
                (set_id,),
            )
            quiz_rows = cursor.fetchall()
            cursor.execute(
                "SELECT asset_type, last_used_at FROM audio_assets "
                "WHERE set_id = %s ORDER BY id",
                (set_id,),
            )
            audio_rows = cursor.fetchall()
    finally:
        connection.close()
    assert media_rows == (("mp4", 20, bgm_id),)
    assert len(quiz_rows) == 1
    assert quiz_rows[0][1] == "L3"
    assert quiz_rows[0][2]
    assert audio_rows[0][0] == "bgm" and audio_rows[0][1] is not None
    assert all(
        last_used_at is None
        for asset_type, last_used_at in audio_rows
        if asset_type == "se"
    )
    assert prompt_id is not None
