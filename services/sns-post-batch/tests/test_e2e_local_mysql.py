"""Local MySQL E2E coverage for the SNS posting batch."""

from __future__ import annotations

import io
import json
import urllib.error
import urllib.parse
from typing import Any
from uuid import uuid4

import pymysql
import pytest

import app.processing as processing_module
from app.main import main


LOCAL_DB_SECRET = {
    "username": "app",
    "password": "password",
    "host": "127.0.0.1",
    "port": 3306,
    "dbname": "acps",
}


class FakeS3Client:
    """S3 fake that records presigned URL requests."""

    def __init__(self) -> None:
        """Initialize the URL call collection."""
        self.calls: list[dict[str, Any]] = []

    def generate_presigned_url(
        self,
        operation: str,
        *,
        Params: dict[str, str],
        ExpiresIn: int,
    ) -> str:
        """Return a stable URL for the fake image object."""
        self.calls.append(
            {
                "operation": operation,
                "Params": Params,
                "ExpiresIn": ExpiresIn,
            }
        )
        return "https://signed.example/image.jpg"


class FakeResponse:
    """Minimal response object for the three Graph API calls."""

    def __init__(self, payload: dict[str, str]) -> None:
        """Store one JSON payload."""
        self.payload = payload

    def read(self) -> bytes:
        """Return the payload as JSON bytes."""
        return json.dumps(self.payload).encode("utf-8")

    def close(self) -> None:
        """Match the standard response interface."""


def _connect_local_mysql(secret: dict[str, Any]) -> pymysql.connections.Connection:
    """Connect to local MySQL using the shared secret field naming."""
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
def local_batch_set() -> tuple[dict[str, Any], str, int, int, int]:
    """Create local E2E rows and always remove them in FK-safe order."""
    try:
        connection = _connect_local_mysql(LOCAL_DB_SECRET)
    except Exception:
        pytest.skip("Local MySQL not reachable; skipping E2E test")

    set_code = f"e2e-sns-{uuid4().hex[:8]}"
    set_id: int | None = None
    generation_run_id: int | None = None
    account_id: int | None = None
    caption_template_id: int | None = None
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO batch_sets "
                "(set_code, name, description, generator_name, is_active) "
                "VALUES (%s, %s, %s, %s, %s)",
                (set_code, "SNS local E2E", "pytest temporary row", "fake", 1),
            )
            set_id = cursor.lastrowid
            cursor.execute(
                "INSERT INTO prompt_configs "
                "(set_id, prompt_text, negative_prompt, parameters, is_active) "
                "VALUES (%s, %s, %s, %s, %s)",
                (set_id, "local test prompt", None, None, 1),
            )
            prompt_config_id = cursor.lastrowid
            cursor.execute(
                "INSERT INTO generation_runs (set_id, scheduled_at) "
                "VALUES (%s, %s)",
                (set_id, "2026-07-19 00:00:00"),
            )
            generation_run_id = cursor.lastrowid
            cursor.execute(
                "INSERT INTO generated_images "
                "(set_id, generation_run_id, prompt_config_id, output_index, "
                "prompt_text_snapshot, s3_key, s3_bucket, file_format, "
                "file_size_bytes, generated_at) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                (
                    set_id,
                    generation_run_id,
                    prompt_config_id,
                    0,
                    "local test prompt",
                    "images/e2e.jpg",
                    "local-test-bucket",
                    "jpg",
                    10,
                    "2026-07-19 00:00:00",
                ),
            )
            generated_image_id = cursor.lastrowid
            cursor.execute(
                "INSERT INTO sns_accounts "
                "(set_id, platform, account_code, account_name, is_active) "
                "VALUES (%s, %s, %s, %s, %s)",
                (set_id, "instagram", "e2e-account", "E2E Account", 1),
            )
            account_id = cursor.lastrowid
            cursor.execute(
                "INSERT INTO caption_templates "
                "(set_id, template_text, is_active) VALUES (%s, %s, %s)",
                (set_id, "E2E caption", 1),
            )
            caption_template_id = cursor.lastrowid
        connection.commit()
        yield (
            LOCAL_DB_SECRET,
            set_code,
            set_id,
            generation_run_id,
            generated_image_id,
        )
    except Exception:
        connection.rollback()
        raise
    finally:
        if set_id is not None:
            with connection.cursor() as cursor:
                cursor.execute(
                    "DELETE FROM post_images WHERE post_id IN "
                    "(SELECT id FROM posts WHERE set_id = %s)",
                    (set_id,),
                )
                cursor.execute("DELETE FROM posts WHERE set_id = %s", (set_id,))
                cursor.execute(
                    "DELETE FROM batch_execution_logs WHERE set_id = %s", (set_id,)
                )
                cursor.execute(
                    "DELETE FROM generated_images WHERE set_id = %s", (set_id,)
                )
                cursor.execute(
                    "DELETE FROM generation_runs WHERE set_id = %s", (set_id,)
                )
                if account_id is not None:
                    cursor.execute("DELETE FROM sns_accounts WHERE id = %s", (account_id,))
                if caption_template_id is not None:
                    cursor.execute(
                        "DELETE FROM caption_templates WHERE id = %s",
                        (caption_template_id,),
                    )
                cursor.execute("DELETE FROM prompt_configs WHERE set_id = %s", (set_id,))
                cursor.execute("DELETE FROM batch_sets WHERE id = %s", (set_id,))
            connection.commit()
        connection.close()


def test_main_persists_successful_post_to_local_mysql(
    local_batch_set: tuple[dict[str, Any], str, int, int, int],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The fake Graph flow reaches success and records all post relations."""
    secret, set_code, set_id, generation_run_id, generated_image_id = local_batch_set
    execution_arn = f"arn:aws:states:local:e2e:{uuid4().hex}"
    monkeypatch.setenv("ENV_NAME", "local")
    monkeypatch.setenv("DB_SECRET_JSON", json.dumps(secret))
    monkeypatch.setenv("SET_CODE", set_code)
    monkeypatch.setenv("EXECUTION_ARN", execution_arn)
    monkeypatch.setenv("S3_BUCKET_NAME", "local-test-bucket")
    monkeypatch.setattr(
        processing_module,
        "get_secret_string",
        lambda name: '{"access_token":"test-token","ig_user_id":"test-ig"}',
    )

    responses = iter(
        [
            FakeResponse({"id": "container-e2e"}),
            FakeResponse({"status_code": "FINISHED"}),
            FakeResponse({"id": "post-e2e"}),
        ]
    )

    def fake_urlopen(request, *, timeout: int):
        """Return the next fake Graph response."""
        assert timeout == 30
        return next(responses)

    fake_s3 = FakeS3Client()
    assert main(s3_client=fake_s3, urlopen=fake_urlopen) == 0

    connection = _connect_local_mysql(secret)
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT status, platform_post_id, caption_text_snapshot "
                "FROM posts WHERE generation_run_id = %s",
                (generation_run_id,),
            )
            post = cursor.fetchone()
            cursor.execute(
                "SELECT COUNT(*) FROM post_images WHERE generated_image_id = %s",
                (generated_image_id,),
            )
            post_image_count = cursor.fetchone()[0]
            cursor.execute(
                "SELECT status, attempt_count, records_processed "
                "FROM batch_execution_logs "
                "WHERE set_id = %s AND execution_arn = %s AND batch_type = 'sns_posting'",
                (set_id, execution_arn),
            )
            execution_log = cursor.fetchone()
    finally:
        connection.close()

    assert post == ("success", "post-e2e", "E2E caption")
    assert post_image_count == 1
    assert execution_log == ("succeeded", 1, 1)
    assert len(fake_s3.calls) == 1


def test_main_resumes_container_created_post_without_creating_a_duplicate(
    local_batch_set: tuple[dict[str, Any], str, int, int, int],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A retry resumes a saved container without creating another one."""
    secret, set_code, _, generation_run_id, _ = local_batch_set
    execution_arn = f"arn:aws:states:local:e2e:{uuid4().hex}"
    monkeypatch.setenv("ENV_NAME", "local")
    monkeypatch.setenv("DB_SECRET_JSON", json.dumps(secret))
    monkeypatch.setenv("SET_CODE", set_code)
    monkeypatch.setenv("EXECUTION_ARN", execution_arn)
    monkeypatch.setenv("S3_BUCKET_NAME", "local-test-bucket")
    monkeypatch.setattr(
        processing_module,
        "get_secret_string",
        lambda name: '{"access_token":"test-token","ig_user_id":"test-ig"}',
    )

    first_requests: list[str] = []

    def first_fake_urlopen(request: Any, *, timeout: int) -> FakeResponse:
        """Create a container and then simulate an ECS task crash."""
        assert timeout == 30
        first_requests.append(request.full_url)
        if len(first_requests) == 1:
            return FakeResponse({"id": "container-e2e-retry"})
        if len(first_requests) == 2:
            raise RuntimeError("simulated task crash")
        pytest.fail("Unexpected Instagram API call during initial execution")

    assert main(s3_client=FakeS3Client(), urlopen=first_fake_urlopen) == 1
    assert len(first_requests) == 2

    connection = _connect_local_mysql(secret)
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT sns_account_id, status, platform_container_id, "
                "platform_post_id FROM posts WHERE generation_run_id = %s",
                (generation_run_id,),
            )
            first_post = cursor.fetchone()
    finally:
        connection.close()

    assert first_post is not None
    sns_account_id = first_post[0]
    assert first_post[1:] == ("container_created", "container-e2e-retry", None)

    retry_responses = iter(
        [
            FakeResponse({"status_code": "FINISHED"}),
            FakeResponse({"id": "post-e2e-retry"}),
        ]
    )
    retry_requests: list[str] = []

    def retry_fake_urlopen(request: Any, *, timeout: int) -> FakeResponse:
        """Return retry responses while rejecting a duplicate container request."""
        assert timeout == 30
        retry_requests.append(request.full_url)
        request_path = urllib.parse.urlparse(request.full_url).path
        request_data = request.data or b""
        assert not (
            request_path.endswith("/media") and b"image_url=" in request_data
        )
        try:
            return next(retry_responses)
        except StopIteration:
            pytest.fail("Unexpected extra Instagram API call during retry")

    assert main(s3_client=FakeS3Client(), urlopen=retry_fake_urlopen) == 0
    assert len(retry_requests) == 2

    connection = _connect_local_mysql(secret)
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT COUNT(*), MAX(status), MAX(platform_container_id), "
                "MAX(platform_post_id) FROM posts "
                "WHERE generation_run_id = %s AND sns_account_id = %s",
                (generation_run_id, sns_account_id),
            )
            retry_post = cursor.fetchone()
    finally:
        connection.close()

    assert retry_post == (1, "success", "container-e2e-retry", "post-e2e-retry")


def test_main_skips_published_unconfirmed_post_on_retry(
    local_batch_set: tuple[dict[str, Any], str, int, int, int],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A retry leaves a published-unconfirmed post untouched."""
    secret, set_code, _, generation_run_id, _ = local_batch_set
    execution_arn = f"arn:aws:states:local:e2e:{uuid4().hex}"
    monkeypatch.setenv("ENV_NAME", "local")
    monkeypatch.setenv("DB_SECRET_JSON", json.dumps(secret))
    monkeypatch.setenv("SET_CODE", set_code)
    monkeypatch.setenv("EXECUTION_ARN", execution_arn)
    monkeypatch.setenv("S3_BUCKET_NAME", "local-test-bucket")
    monkeypatch.setattr(
        processing_module,
        "get_secret_string",
        lambda name: '{"access_token":"test-token","ig_user_id":"test-ig"}',
    )

    first_call_count = 0

    def first_fake_urlopen(request: Any, *, timeout: int) -> FakeResponse:
        """Return a duplicate-publish error after creating a ready container."""
        nonlocal first_call_count
        assert timeout == 30
        first_call_count += 1
        if first_call_count == 1:
            return FakeResponse({"id": "container-e2e-unconfirmed"})
        if first_call_count == 2:
            return FakeResponse({"status_code": "FINISHED"})
        if first_call_count == 3:
            raise urllib.error.HTTPError(
                request.full_url,
                400,
                "Bad Request",
                None,
                io.BytesIO(
                    b'{"error":{"message":"Media has already been published"}}'
                ),
            )
        pytest.fail("Unexpected extra Instagram API call during initial execution")

    assert main(s3_client=FakeS3Client(), urlopen=first_fake_urlopen) == 1
    assert first_call_count == 3

    connection = _connect_local_mysql(secret)
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT sns_account_id, status, platform_post_id FROM posts "
                "WHERE generation_run_id = %s",
                (generation_run_id,),
            )
            first_post = cursor.fetchone()
    finally:
        connection.close()

    assert first_post is not None
    sns_account_id = first_post[0]
    assert first_post[1:] == ("published_unconfirmed", None)

    def terminal_fake_urlopen(request: Any, *, timeout: int) -> FakeResponse:
        """Fail if a terminal post retry reaches the Instagram API."""
        pytest.fail("Instagram API should not be called for a terminal post state")

    # The only sns_account is now terminal, so resolve_target_generation_run
    # (app/target_selection.py) excludes this generation run from selection
    # entirely: main() exits via the "no target" path (0 accounts processed)
    # without ever reaching process_target_generation_run/urlopen.
    assert main(s3_client=FakeS3Client(), urlopen=terminal_fake_urlopen) == 0

    connection = _connect_local_mysql(secret)
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT COUNT(*), MAX(status), MAX(platform_post_id) FROM posts "
                "WHERE generation_run_id = %s AND sns_account_id = %s",
                (generation_run_id, sns_account_id),
            )
            retry_post = cursor.fetchone()
    finally:
        connection.close()

    assert retry_post == (1, "published_unconfirmed", None)
