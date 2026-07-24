"""Real OpenAI API E2E coverage for the gpt-image-single generator.

This test makes one real call to the OpenAI Images API (model
``gpt-image-2``, ``quality=high``) using the production
``acps/{ENV_NAME}/image/api-key`` secret. It costs real money and takes on
the order of minutes, so it is skipped by default and only runs when
``RUN_REAL_IMAGE_API_E2E=1`` is set explicitly.
"""

from __future__ import annotations

import json
import os
from typing import Any
from uuid import uuid4

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

REAL_PROMPT_TEXT = (
    "A photorealistic, whimsical animal that looks like it could exist in "
    "the wild but does not. Square image suitable for an Instagram post."
)
REAL_PARAMETERS = json.dumps(
    {"model": "gpt-image-2", "size": "1024x1024", "quality": "high", "n": 1}
)


def _connect_local_mysql(secret: dict[str, Any]) -> pymysql.connections.Connection:
    """Connect to local MySQL using the shared secret field naming.

    Args:
        secret: Database secret using ``username`` and ``dbname`` fields.

    Returns:
        An open local MySQL connection.
    """
    return pymysql.connect(
        host=secret["host"],
        port=secret["port"],
        user=secret["username"],
        password=secret["password"],
        database=secret["dbname"],
        connect_timeout=2,
        charset="utf8mb4",
    )


class FakeS3Client:
    """S3 fake that records uploads without contacting AWS."""

    def __init__(self) -> None:
        """Initialize the upload call collection."""
        self.calls: list[dict[str, Any]] = []

    def put_object(self, **kwargs: Any) -> None:
        """Record one requested object upload."""
        self.calls.append(kwargs)


@pytest.fixture
def real_api_batch_set() -> tuple[str, int, int]:
    """Create a temporary gpt-image-single batch set and always remove it."""
    if os.environ.get("RUN_REAL_IMAGE_API_E2E") != "1":
        pytest.skip("RUN_REAL_IMAGE_API_E2E is not set; skipping real API E2E test")

    try:
        connection = _connect_local_mysql(LOCAL_DB_SECRET)
    except Exception:
        pytest.skip("Local MySQL not reachable; skipping E2E test")

    set_code = f"e2e-real-{uuid4().hex[:8]}"
    set_id: int | None = None
    prompt_config_id: int | None = None
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO batch_sets "
                "(set_code, name, description, generator_name, is_active) "
                "VALUES (%s, %s, %s, %s, %s)",
                (set_code, "Real API E2E", "pytest temporary row", "gpt-image-single", 1),
            )
            set_id = cursor.lastrowid
            cursor.execute(
                "INSERT INTO prompt_configs "
                "(set_id, prompt_text, negative_prompt, parameters, is_active) "
                "VALUES (%s, %s, %s, %s, %s)",
                (set_id, REAL_PROMPT_TEXT, None, REAL_PARAMETERS, 1),
            )
            prompt_config_id = cursor.lastrowid
        connection.commit()
        yield set_code, set_id, prompt_config_id
    finally:
        if set_id is not None:
            with connection.cursor() as cursor:
                cursor.execute(
                    "DELETE FROM generated_media WHERE set_id = %s", (set_id,)
                )
                cursor.execute("DELETE FROM generation_runs WHERE set_id = %s", (set_id,))
                cursor.execute("DELETE FROM prompt_configs WHERE set_id = %s", (set_id,))
                cursor.execute(
                    "DELETE FROM batch_execution_logs WHERE set_id = %s", (set_id,)
                )
                cursor.execute("DELETE FROM batch_sets WHERE id = %s", (set_id,))
            connection.commit()
        connection.close()


def test_main_generates_real_image_via_gpt_image_single(
    real_api_batch_set: tuple[str, int, int],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The real generator produces a JPEG image and persists it end to end."""
    set_code, set_id, prompt_config_id = real_api_batch_set
    env_name = os.environ.get("ENV_NAME", "prod")
    execution_arn = f"arn:aws:states:local:000000000000:execution:e2e:{uuid4().hex}"

    monkeypatch.setenv("ENV_NAME", env_name)
    monkeypatch.setenv("DB_SECRET_JSON", json.dumps(LOCAL_DB_SECRET))
    monkeypatch.setenv("SET_CODE", set_code)
    monkeypatch.setenv("EXECUTION_ARN", execution_arn)
    monkeypatch.setenv("SCHEDULED_AT", "2026-07-19T00:00:00Z")
    monkeypatch.setenv("API_SECRET_ARN", f"acps/{env_name}/image/api-key")
    monkeypatch.setenv("S3_BUCKET_NAME", "local-test-bucket")
    fake_s3 = FakeS3Client()

    assert main(s3_client=fake_s3) == 0

    connection = _connect_local_mysql(LOCAL_DB_SECRET)
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT id FROM generation_runs WHERE set_id = %s "
                "AND scheduled_at = %s",
                (set_id, "2026-07-19 00:00:00"),
            )
            generation_run = cursor.fetchone()
            cursor.execute(
                "SELECT file_size_bytes, s3_key, s3_bucket, file_format "
                "FROM generated_media WHERE set_id = %s",
                (set_id,),
            )
            image_rows = cursor.fetchall()
            cursor.execute(
                "SELECT status, attempt_count, records_processed "
                "FROM batch_execution_logs WHERE set_id = %s AND execution_arn = %s",
                (set_id, execution_arn),
            )
            execution_log = cursor.fetchone()
    finally:
        connection.close()

    assert generation_run is not None
    assert len(image_rows) == 1
    file_size_bytes, s3_key, s3_bucket, file_format = image_rows[0]
    # A real JPEG photo at 1024x1024 is well above a trivial byte count;
    # this guards against silently persisting an empty or error payload.
    assert file_size_bytes > 10_000
    assert file_format == "jpg"
    assert s3_key == (
        f"images/{set_code}/20260719/{generation_run[0]}/{prompt_config_id}_0.jpg"
    )
    assert s3_bucket == "local-test-bucket"
    assert execution_log == ("succeeded", 1, 1)
    assert len(fake_s3.calls) == 1
    uploaded_body = fake_s3.calls[0]["Body"]
    assert uploaded_body[:2] == b"\xff\xd8"  # JPEG magic bytes
    assert fake_s3.calls[0]["Bucket"] == "local-test-bucket"
    assert fake_s3.calls[0]["ContentType"] == "image/jpeg"
