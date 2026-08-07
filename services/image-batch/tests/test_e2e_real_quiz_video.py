"""Opt-in real Images API, local MySQL, and ffmpeg quiz E2E coverage."""

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
from app.main import main


LOCAL_DB_SECRET = {
    "username": "app",
    "password": "password",
    "host": "127.0.0.1",
    "port": 3306,
    "dbname": "acps",
}


def _connect() -> pymysql.connections.Connection:
    """Connect to the local V005 MySQL database."""
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
def real_quiz_rows() -> tuple[str, int, int, int]:
    """Insert temporary quiz configuration, stock, and audio metadata."""
    if os.environ.get("RUN_REAL_QUIZ_E2E") != "1":
        pytest.skip("RUN_REAL_QUIZ_E2E is not set; skipping real quiz E2E")
    try:
        connection = _connect()
    except Exception:
        pytest.skip("Local MySQL with V005 is not reachable")

    set_code = f"e2e-quiz-{uuid4().hex[:8]}"
    set_id = prompt_id = bgm_id = None
    parameters = json.dumps(
        {
            "slots": [
                {
                    "from_jst_hour": 4,
                    "quiz_type": "L1",
                    "difficulty": "light",
                    "slot_code": "morning",
                    "slot_label": "朝のロジトレ",
                },
                {
                    "from_jst_hour": 11,
                    "quiz_type": "L3",
                    "difficulty": "standard",
                    "slot_code": "noon",
                    "slot_label": "昼の推定トレ",
                },
                {
                    "from_jst_hour": 17,
                    "quiz_type": "L1",
                    "difficulty": "deep",
                    "slot_code": "night",
                    "slot_label": "夜のロジトレ",
                },
            ],
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
            stock_rows = [
                (
                    "L1",
                    "light",
                    "朝のなぞなぞです。箱の中身を当ててください。",
                    "りんご",
                    "朝の一問！",
                    "言葉をよく見よう",
                ),
                (
                    "L3",
                    "standard",
                    "日本にある信号機の数を推定してください。",
                    "約20万基（目安）",
                    "推定できる？",
                    "一人あたりから考えよう",
                ),
                (
                    "L1",
                    "deep",
                    "夜にだけ開く不思議な扉の鍵は何でしょう？",
                    "月明かり",
                    "ひらめける？",
                    "時間帯がヒント",
                ),
            ]
            for quiz_type, difficulty, question, answer, hook, hint in stock_rows:
                fields = {
                    "hook": hook,
                    "hint": hint,
                    "question": question,
                    "answer": answer,
                    "explanation": "前提から順に考えると答えへたどり着きます。",
                    "coach_comment": "考え方が大切！",
                    "tags": ["脳トレ", "クイズ", "思考"],
                    "summary": question[:100],
                    "illustration_scene": "文字のない明るい街角の風景",
                }
                cursor.execute(
                    "INSERT INTO quiz_stock_items "
                    "(set_id, quiz_type, difficulty, question_text, "
                    "answer_text, content_fields, source_note, is_active) "
                    "VALUES (%s, %s, %s, %s, %s, %s, %s, 1)",
                    (
                        set_id,
                        quiz_type,
                        difficulty,
                        question,
                        answer,
                        json.dumps(fields, ensure_ascii=False),
                        "E2E fixture; original test content",
                    ),
                )
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
        yield set_code, set_id, prompt_id, bgm_id
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
                    "DELETE FROM quiz_stock_items WHERE set_id = %s", (set_id,)
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


@pytest.mark.parametrize(
    "scheduled_at, expected_quiz_type",
    [
        ("2026-07-26T19:00:00Z", "L1"),
        ("2026-07-27T02:00:00Z", "L3"),
        ("2026-07-27T08:00:00Z", "L1"),
    ],
    ids=["morning", "noon", "night"],
)
def test_main_generates_real_quiz_video(
    real_quiz_rows: tuple[str, int, int, int],
    monkeypatch: pytest.MonkeyPatch,
    scheduled_at: str,
    expected_quiz_type: str,
) -> None:
    """Each slot produces media and transactional history."""
    set_code, set_id, prompt_id, bgm_id = real_quiz_rows
    env_name = os.environ.get("ENV_NAME", "prod")
    monkeypatch.setenv("API_SECRET_ARN", f"acps/{env_name}/image/api-key")
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
    monkeypatch.setenv("SCHEDULED_AT", scheduled_at)
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
    assert len(cut_uploads) == 5
    suffixes = [
        Path(item["Key"]).stem.split(f"{prompt_id}_0", 1)[1]
        for item in cut_uploads
    ]
    assert suffixes == [
        "_cut1",
        "_cut2",
        "_cut3",
        "_cut4",
        "_illustration",
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
    assert float(metadata["format"]["duration"]) == pytest.approx(16, abs=0.2)

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
                "SELECT generation_run_id, stock_item_id, quiz_type, content_fields "
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
            cursor.execute(
                "SELECT quiz_type, use_count, last_used_at "
                "FROM quiz_stock_items WHERE set_id = %s ORDER BY id",
                (set_id,),
            )
            stock_rows = cursor.fetchall()
    finally:
        connection.close()
    assert media_rows == (("mp4", 16, bgm_id),)
    assert len(quiz_rows) == 1
    assert quiz_rows[0][1] is not None
    assert quiz_rows[0][2] == expected_quiz_type
    assert quiz_rows[0][3]
    used_stock = next(row for row in stock_rows if row[1] == 1)
    assert used_stock[0] == expected_quiz_type
    assert used_stock[2] is not None
    assert audio_rows[0][0] == "bgm" and audio_rows[0][1] is not None
    assert all(
        last_used_at is None
        for asset_type, last_used_at in audio_rows
        if asset_type == "se"
    )
    assert prompt_id is not None
