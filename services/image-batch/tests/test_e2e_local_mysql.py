"""Local MySQL E2E coverage for the image batch common skeleton."""

from __future__ import annotations

import json
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


class FakeS3Client:
    """S3 fake that records uploads without contacting AWS."""

    def __init__(self) -> None:
        """Initialize the upload call collection."""
        self.calls: list[dict[str, Any]] = []

    def put_object(self, **kwargs: Any) -> None:
        """Record one requested object upload."""
        self.calls.append(kwargs)


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


@pytest.fixture
def local_batch_set() -> tuple[dict[str, Any], str, int]:
    """Create a local E2E batch set and always remove its test rows."""
    try:
        connection = _connect_local_mysql(LOCAL_DB_SECRET)
    except Exception:
        pytest.skip("Local MySQL not reachable; skipping E2E test")

    set_code = f"e2e-{uuid4().hex[:8]}"
    set_id: int | None = None
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO batch_sets "
                "(set_code, name, description, generator_name, is_active) "
                "VALUES (%s, %s, %s, %s, %s)",
                (set_code, "Local E2E", "pytest temporary row", "fake", 1),
            )
            set_id = cursor.lastrowid
            cursor.execute(
                "INSERT INTO prompt_configs "
                "(set_id, prompt_text, negative_prompt, parameters, is_active) "
                "VALUES (%s, %s, %s, %s, %s)",
                (set_id, "local test prompt", None, None, 1),
            )
        connection.commit()
        yield LOCAL_DB_SECRET, set_code, set_id
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


def test_main_persists_fake_generated_image_to_local_mysql(
    local_batch_set: tuple[dict[str, Any], str, int],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The fake generator completes the full DB flow without real S3 access."""
    secret, set_code, set_id = local_batch_set
    execution_arn = f"arn:aws:states:local:000000000000:execution:e2e:{uuid4().hex}"
    monkeypatch.setenv("ENV_NAME", "local")
    monkeypatch.setenv("DB_SECRET_JSON", json.dumps(secret))
    monkeypatch.setenv("SET_CODE", set_code)
    monkeypatch.setenv("EXECUTION_ARN", execution_arn)
    monkeypatch.setenv("SCHEDULED_AT", "2026-07-19T00:00:00Z")
    monkeypatch.setenv("API_SECRET_ARN", "arn:local:api")
    monkeypatch.setenv("S3_BUCKET_NAME", "local-test-bucket")
    fake_s3 = FakeS3Client()

    assert main(s3_client=fake_s3) == 0

    connection = _connect_local_mysql(secret)
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT id FROM generation_runs WHERE set_id = %s "
                "AND scheduled_at = %s",
                (set_id, "2026-07-19 00:00:00"),
            )
            generation_run = cursor.fetchone()
            cursor.execute(
                "SELECT COUNT(*) FROM generated_media WHERE set_id = %s", (set_id,)
            )
            image_count = cursor.fetchone()[0]
            cursor.execute(
                "SELECT status, attempt_count, records_processed "
                "FROM batch_execution_logs WHERE set_id = %s AND execution_arn = %s",
                (set_id, execution_arn),
            )
            execution_log = cursor.fetchone()
    finally:
        connection.close()

    assert generation_run is not None
    assert image_count == 1
    assert execution_log == ("succeeded", 1, 1)
    assert len(fake_s3.calls) == 1
