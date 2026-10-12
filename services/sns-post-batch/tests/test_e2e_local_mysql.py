"""Local MySQL E2E coverage for the SNS posting batch."""

from __future__ import annotations

import io
import json
import urllib.error
import urllib.parse
from contextlib import contextmanager
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Iterator
from unittest.mock import Mock
from uuid import uuid4

import pymysql
import pytest

import app.main as main_module
import app.processing as processing_module
from app.main import main


LOCAL_DB_SECRET = {
    "username": "app",
    "password": "password",
    "host": "127.0.0.1",
    "port": 3306,
    "dbname": "acps",
}

DEFAULT_SCHEDULED_AT = datetime(2026, 7, 19)
CURRENT_SCHEDULED_AT = datetime(2026, 10, 13, 12)
MORNING_SCHEDULED_AT = datetime(2026, 10, 12, 22, 30)


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
        """Return a stable URL for the fake media object."""
        self.calls.append(
            {
                "operation": operation,
                "Params": Params,
                "ExpiresIn": ExpiresIn,
            }
        )
        return f"https://signed.example/{Params['Key']}"


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


@contextmanager
def _local_batch_set(
    *,
    file_format: str,
    s3_key: str,
    duration_seconds: int | None = None,
    stories_enabled: int = 0,
    caption_text: str = "E2E caption",
    seed_quiz_item: bool = False,
) -> Iterator[tuple[dict[str, Any], str, int, int, int]]:
    """Require local MySQL; create rows and remove them in FK-safe order."""
    connection = _connect_local_mysql(LOCAL_DB_SECRET)

    set_code = f"e2e-sns-{uuid4().hex[:8]}"
    set_id: int | None = None
    generation_run_id: int | None = None
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO batch_sets "
                "(set_code, name, description, generator_name, is_active, "
                "stories_enabled) VALUES (%s, %s, %s, %s, %s, %s)",
                (
                    set_code,
                    "SNS local E2E",
                    "pytest temporary row",
                    "fake",
                    1,
                    stories_enabled,
                ),
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
                (set_id, DEFAULT_SCHEDULED_AT),
            )
            generation_run_id = cursor.lastrowid
            cursor.execute(
                "INSERT INTO generated_media "
                "(set_id, generation_run_id, prompt_config_id, output_index, "
                "prompt_text_snapshot, s3_key, s3_bucket, file_format, "
                "duration_seconds, audio_asset_id, file_size_bytes, generated_at) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                (
                    set_id,
                    generation_run_id,
                    prompt_config_id,
                    0,
                    "local test prompt",
                    s3_key,
                    "local-test-bucket",
                    file_format,
                    duration_seconds,
                    None,
                    10,
                    DEFAULT_SCHEDULED_AT,
                ),
            )
            generated_media_id = cursor.lastrowid
            cursor.execute(
                "INSERT INTO sns_accounts "
                "(set_id, platform, account_code, account_name, is_active) "
                "VALUES (%s, %s, %s, %s, %s)",
                (set_id, "instagram", "e2e-account", "E2E Account", 1),
            )
            cursor.execute(
                "INSERT INTO caption_templates "
                "(set_id, template_text, is_active) VALUES (%s, %s, %s)",
                (set_id, caption_text, 1),
            )
            if seed_quiz_item:
                fields = {
                    "hook": "この問題、解ける？",
                    "explanation": "順番に整理すると解けます。",
                    "coach_comment": "ひらめきが大切！",
                }
                cursor.execute(
                    "INSERT INTO quiz_items "
                    "(set_id, generation_run_id, quiz_type, difficulty, summary, "
                    "question_text, answer_text, content_fields) "
                    "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                    (
                        set_id,
                        generation_run_id,
                        "L1",
                        "light",
                        "E2E quiz",
                        "問題文です",
                        "答えです",
                        json.dumps(fields, ensure_ascii=False),
                    ),
                )
        connection.commit()
        yield (
            LOCAL_DB_SECRET,
            set_code,
            set_id,
            generation_run_id,
            generated_media_id,
        )
    except Exception:
        connection.rollback()
        raise
    finally:
        if set_id is not None:
            with connection.cursor() as cursor:
                cursor.execute(
                    "DELETE FROM post_media WHERE post_id IN "
                    "(SELECT id FROM posts WHERE set_id = %s)",
                    (set_id,),
                )
                cursor.execute("DELETE FROM posts WHERE set_id = %s", (set_id,))
                cursor.execute(
                    "DELETE FROM batch_execution_logs WHERE set_id = %s", (set_id,)
                )
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
                    "DELETE FROM sns_accounts WHERE set_id = %s", (set_id,)
                )
                cursor.execute(
                    "DELETE FROM caption_templates WHERE set_id = %s", (set_id,)
                )
                cursor.execute(
                    "DELETE FROM prompt_configs WHERE set_id = %s", (set_id,)
                )
                cursor.execute("DELETE FROM batch_sets WHERE id = %s", (set_id,))
            connection.commit()
        connection.close()


@pytest.fixture
def local_batch_set() -> Iterator[tuple[dict[str, Any], str, int, int, int]]:
    """Create a local E2E batch set containing generated feed media."""
    with _local_batch_set(file_format="jpg", s3_key="images/e2e.jpg") as batch_set:
        yield batch_set


@pytest.fixture
def local_reel_batch_set() -> Iterator[tuple[dict[str, Any], str, int, int, int]]:
    """Create a local E2E batch set containing a generated reel video."""
    with _local_batch_set(
        file_format="mp4",
        s3_key="videos/e2e.mp4",
        duration_seconds=10,
    ) as batch_set:
        yield batch_set


@pytest.fixture
def local_stories_batch_set() -> Iterator[tuple[dict[str, Any], str, int, int, int]]:
    """Create a local E2E batch set with reels and stories enabled."""
    with _local_batch_set(
        file_format="mp4",
        s3_key="videos/e2e-story.mp4",
        duration_seconds=10,
        stories_enabled=1,
    ) as batch_set:
        yield batch_set


@pytest.fixture
def local_placeholder_batch_set() -> Iterator[
    tuple[dict[str, Any], str, int, int, int]
]:
    """Create a local E2E set with a dynamic quiz caption."""
    with _local_batch_set(
        file_format="jpg",
        s3_key="images/e2e-placeholder.jpg",
        caption_text=(
            "{{hook}}\n{{question}}\n答え: {{answer}}\n"
            "{{explanation}}\n{{coach_comment}}"
        ),
        seed_quiz_item=True,
    ) as batch_set:
        yield batch_set


def test_main_persists_successful_post_to_local_mysql(
    local_batch_set: tuple[dict[str, Any], str, int, int, int],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The fake Graph flow reaches success and records all post relations."""
    secret, set_code, set_id, generation_run_id, generated_media_id = local_batch_set
    execution_arn = f"arn:aws:states:local:e2e:{uuid4().hex}"
    monkeypatch.setenv("ENV_NAME", "local")
    monkeypatch.setenv("DB_SECRET_JSON", json.dumps(secret))
    monkeypatch.setenv("SET_CODE", set_code)
    monkeypatch.setenv(
        "SCHEDULED_AT", DEFAULT_SCHEDULED_AT.isoformat(timespec="seconds") + "Z"
    )
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
                "SELECT COUNT(*) FROM post_media WHERE generated_media_id = %s",
                (generated_media_id,),
            )
            post_media_count = cursor.fetchone()[0]
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
    assert post_media_count == 1
    assert execution_log == ("succeeded", 1, 1)
    assert len(fake_s3.calls) == 1


def test_main_expands_quiz_caption_in_local_mysql(
    local_placeholder_batch_set: tuple[dict[str, Any], str, int, int, int],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Placeholder templates persist their fully expanded snapshot."""
    secret, set_code, _, generation_run_id, _ = local_placeholder_batch_set
    monkeypatch.setenv("ENV_NAME", "local")
    monkeypatch.setenv("DB_SECRET_JSON", json.dumps(secret))
    monkeypatch.setenv("SET_CODE", set_code)
    monkeypatch.setenv(
        "SCHEDULED_AT", DEFAULT_SCHEDULED_AT.isoformat(timespec="seconds") + "Z"
    )
    monkeypatch.setenv("EXECUTION_ARN", f"arn:aws:states:local:e2e:{uuid4().hex}")
    monkeypatch.setenv("S3_BUCKET_NAME", "local-test-bucket")
    monkeypatch.setattr(
        processing_module,
        "get_secret_string",
        lambda name: '{"access_token":"test-token","ig_user_id":"test-ig"}',
    )
    responses = iter(
        [
            FakeResponse({"id": "container-caption"}),
            FakeResponse({"status_code": "FINISHED"}),
            FakeResponse({"id": "post-caption"}),
        ]
    )

    assert main(
        s3_client=FakeS3Client(),
        urlopen=lambda request, timeout: next(responses),
    ) == 0

    connection = _connect_local_mysql(secret)
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT caption_text_snapshot FROM posts "
                "WHERE generation_run_id = %s",
                (generation_run_id,),
            )
            snapshot = cursor.fetchone()[0]
    finally:
        connection.close()
    assert snapshot == (
        "この問題、解ける？\n問題文です\n答え: 答えです\n"
        "順番に整理すると解けます。\nひらめきが大切！"
    )


def test_main_persists_successful_reel_post_to_local_mysql(
    local_reel_batch_set: tuple[dict[str, Any], str, int, int, int],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """An MP4 generated media item is published as a successful reel."""
    secret, set_code, _, generation_run_id, generated_media_id = local_reel_batch_set
    monkeypatch.setenv("ENV_NAME", "local")
    monkeypatch.setenv("DB_SECRET_JSON", json.dumps(secret))
    monkeypatch.setenv("SET_CODE", set_code)
    monkeypatch.setenv(
        "SCHEDULED_AT", DEFAULT_SCHEDULED_AT.isoformat(timespec="seconds") + "Z"
    )
    monkeypatch.setenv("EXECUTION_ARN", f"arn:aws:states:local:e2e:{uuid4().hex}")
    monkeypatch.setenv("S3_BUCKET_NAME", "local-test-bucket")
    monkeypatch.setattr(
        processing_module,
        "get_secret_string",
        lambda name: '{"access_token":"test-token","ig_user_id":"test-ig"}',
    )

    responses = iter(
        [
            FakeResponse({"id": "container-e2e-reel"}),
            FakeResponse({"status_code": "FINISHED"}),
            FakeResponse({"id": "post-e2e-reel"}),
        ]
    )
    requests: list[Any] = []

    def fake_urlopen(request: Any, *, timeout: int) -> FakeResponse:
        """Record each Graph request and return the next fake response."""
        assert timeout == 30
        requests.append(request)
        return next(responses)

    assert main(s3_client=FakeS3Client(), urlopen=fake_urlopen) == 0

    connection = _connect_local_mysql(secret)
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT status, media_type FROM posts WHERE generation_run_id = %s",
                (generation_run_id,),
            )
            post = cursor.fetchone()
            cursor.execute(
                "SELECT COUNT(*) FROM post_media WHERE generated_media_id = %s",
                (generated_media_id,),
            )
            post_media_count = cursor.fetchone()[0]
    finally:
        connection.close()

    reel_values = urllib.parse.parse_qs((requests[0].data or b"").decode())
    assert post == ("success", "reel")
    assert post_media_count == 1
    assert reel_values["media_type"] == ["REELS"]
    assert reel_values["video_url"] == ["https://signed.example/videos/e2e.mp4"]
    assert reel_values["share_to_feed"] == ["true"]


def test_main_persists_successful_reel_and_story_to_local_mysql(
    local_stories_batch_set: tuple[dict[str, Any], str, int, int, int],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """An enabled reel stores independent successful reel and story posts."""
    secret, set_code, _, generation_run_id, generated_media_id = local_stories_batch_set
    monkeypatch.setenv("ENV_NAME", "local")
    monkeypatch.setenv("DB_SECRET_JSON", json.dumps(secret))
    monkeypatch.setenv("SET_CODE", set_code)
    monkeypatch.setenv(
        "SCHEDULED_AT", DEFAULT_SCHEDULED_AT.isoformat(timespec="seconds") + "Z"
    )
    monkeypatch.setenv("EXECUTION_ARN", f"arn:aws:states:local:e2e:{uuid4().hex}")
    monkeypatch.setenv("S3_BUCKET_NAME", "local-test-bucket")
    monkeypatch.setattr(
        processing_module,
        "get_secret_string",
        lambda name: '{"access_token":"test-token","ig_user_id":"test-ig"}',
    )

    responses = iter(
        [
            FakeResponse({"id": "container-e2e-reel"}),
            FakeResponse({"status_code": "FINISHED"}),
            FakeResponse({"id": "post-e2e-reel"}),
            FakeResponse({"id": "container-e2e-story"}),
            FakeResponse({"status_code": "FINISHED"}),
            FakeResponse({"id": "post-e2e-story"}),
        ]
    )
    requests: list[Any] = []

    def fake_urlopen(request: Any, *, timeout: int) -> FakeResponse:
        """Record the Graph requests for the consecutive publications."""
        assert timeout == 30
        requests.append(request)
        return next(responses)

    fake_s3 = FakeS3Client()
    assert main(s3_client=fake_s3, urlopen=fake_urlopen) == 0

    connection = _connect_local_mysql(secret)
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT id, media_type, status, caption_template_id, "
                "caption_text_snapshot, platform_post_id FROM posts "
                "WHERE generation_run_id = %s ORDER BY media_type",
                (generation_run_id,),
            )
            posts = cursor.fetchall()
            cursor.execute(
                "SELECT post_id, COUNT(*) FROM post_media "
                "WHERE generated_media_id = %s GROUP BY post_id",
                (generated_media_id,),
            )
            post_media_counts = cursor.fetchall()
    finally:
        connection.close()

    assert len(posts) == 2
    reel, story = posts
    assert reel[1:] == ("reel", "success", reel[3], "E2E caption", "post-e2e-reel")
    assert story[1:] == ("story", "success", None, None, "post-e2e-story")
    assert reel[5] != story[5]
    assert {post_id for post_id, _ in post_media_counts} == {reel[0], story[0]}
    assert all(count == 1 for _, count in post_media_counts)
    story_values = urllib.parse.parse_qs((requests[3].data or b"").decode())
    assert story_values == {
        "access_token": ["test-token"],
        "media_type": ["STORIES"],
        "video_url": ["https://signed.example/videos/e2e-story.mp4"],
    }
    assert len(fake_s3.calls) == 2


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
    monkeypatch.setenv(
        "SCHEDULED_AT", DEFAULT_SCHEDULED_AT.isoformat(timespec="seconds") + "Z"
    )
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
    monkeypatch.setenv(
        "SCHEDULED_AT", DEFAULT_SCHEDULED_AT.isoformat(timespec="seconds") + "Z"
    )
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

    # The current run has only a terminal account, so selection reports
    # ALREADY_TERMINAL and main exits with zero processed accounts.
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


class RecordingUrlopen:
    """Record Graph calls, return fake responses, and simulate task crashes."""

    def __init__(self, payloads: list[dict[str, str] | Exception]) -> None:
        self.payloads = iter(payloads)
        self.requests: list[Any] = []

    def __call__(self, request: Any, *, timeout: int) -> FakeResponse:
        assert timeout == 30
        self.requests.append(request)
        try:
            payload = next(self.payloads)
        except StopIteration:
            pytest.fail("Unexpected extra Instagram API call")
        if isinstance(payload, Exception):
            raise payload
        return FakeResponse(payload)


def _success_payloads() -> list[dict[str, str] | Exception]:
    """Provide the existing create, poll, publish fake Graph flow."""
    return [
        {"id": "container-current"},
        {"status_code": "FINISHED"},
        {"id": "post-current"},
    ]


@dataclass(frozen=True)
class ScheduledBatch:
    """Committed local rows for current-run acceptance tests."""

    connection: pymysql.connections.Connection
    set_code: str
    set_id: int
    run_id: int
    media_id: int
    account_id: int
    execution_arn: str


@pytest.fixture
def scheduled_batch(
    local_batch_set: tuple[dict[str, Any], str, int, int, int],
    monkeypatch: pytest.MonkeyPatch,
) -> Iterator[ScheduledBatch]:
    """Use real MySQL without stale snapshots between main calls."""
    secret, set_code, set_id, run_id, media_id = local_batch_set
    connection = _connect_local_mysql(secret)
    try:
        connection.autocommit(True)
        with connection.cursor() as cursor:
            cursor.execute(
                "UPDATE generation_runs SET scheduled_at = %s WHERE id = %s",
                (CURRENT_SCHEDULED_AT, run_id),
            )
            cursor.execute(
                "SELECT id FROM sns_accounts WHERE set_id = %s", (set_id,)
            )
            account_id = cursor.fetchone()[0]
        execution_arn = f"arn:aws:states:local:e2e:{uuid4().hex}"
        for name, value in {
            "ENV_NAME": "local",
            "DB_SECRET_JSON": json.dumps(secret),
            "SET_CODE": set_code,
            "SCHEDULED_AT": (
                CURRENT_SCHEDULED_AT.isoformat(timespec="seconds") + "Z"
            ),
            "EXECUTION_ARN": execution_arn,
            "S3_BUCKET_NAME": "local-test-bucket",
        }.items():
            monkeypatch.setenv(name, value)
        monkeypatch.setattr(
            processing_module, "get_secret_string",
            lambda name: json.dumps({
                "access_token": "test-token",
                "ig_user_id": name.rsplit("/", 1)[-1],
            }),
        )
        yield ScheduledBatch(
            connection, set_code, set_id, run_id, media_id,
            account_id, execution_arn,
        )
    finally:
        connection.close()


def _add_generation_run(
    batch: ScheduledBatch, scheduled_at: datetime, *, with_media: bool = True
) -> int:
    """Add another run, optionally copying the fixture's local media."""
    with batch.connection.cursor() as cursor:
        cursor.execute(
            "INSERT INTO generation_runs (set_id, scheduled_at) VALUES (%s, %s)",
            (batch.set_id, scheduled_at),
        )
        run_id = cursor.lastrowid
        if with_media:
            cursor.execute(
                "INSERT INTO generated_media "
                "(set_id, generation_run_id, prompt_config_id, output_index, "
                "prompt_text_snapshot, s3_key, s3_bucket, file_format, generated_at) "
                "SELECT set_id, %s, prompt_config_id, output_index, "
                "prompt_text_snapshot, s3_key, s3_bucket, file_format, %s "
                "FROM generated_media WHERE id = %s",
                (run_id, scheduled_at, batch.media_id),
            )
            assert cursor.rowcount == 1
    return run_id


def _add_post(batch: ScheduledBatch, run_id: int, status: str) -> int:
    """Seed a post and media relation with recognizable snapshot fields."""
    with batch.connection.cursor() as cursor:
        cursor.execute(
            "INSERT INTO posts "
            "(set_id, generation_run_id, sns_account_id, status, media_type, "
            "platform_container_id, caption_text_snapshot, created_at, updated_at) "
            "VALUES (%s, %s, %s, %s, 'feed_image', %s, 'saved caption', %s, %s)",
            (
                batch.set_id, run_id, batch.account_id, status,
                f"saved-container-{run_id}" if status == "container_created" else None,
                datetime(2026, 1, 1), datetime(2026, 1, 1),
            ),
        )
        post_id = cursor.lastrowid
        cursor.execute(
            "INSERT INTO post_media (post_id, generated_media_id) "
            "SELECT %s, id FROM generated_media WHERE generation_run_id = %s",
            (post_id, run_id),
        )
        assert cursor.rowcount == 1
    return post_id


def _run_posts(
    batch: ScheduledBatch, run_id: int, *, account_id: int | None = None
) -> tuple[tuple[Any, ...], ...]:
    """Read complete post rows, including IDs, statuses, and updated_at."""
    query = "SELECT * FROM posts WHERE generation_run_id = %s"
    parameters = (run_id,)
    if account_id is not None:
        query += " AND sns_account_id = %s"
        parameters += (account_id,)
    with batch.connection.cursor() as cursor:
        cursor.execute(query + " ORDER BY id", parameters)
        return cursor.fetchall()


def _assert_successful_runs(batch: ScheduledBatch, run_ids: list[int]) -> None:
    """Verify that only the requested runs have successful posts."""
    with batch.connection.cursor() as cursor:
        cursor.execute(
            "SELECT generation_run_id, status FROM posts "
            "WHERE set_id = %s ORDER BY generation_run_id",
            (batch.set_id,),
        )
        assert cursor.fetchall() == tuple(
            (run_id, "success") for run_id in sorted(run_ids)
        )


def _assert_execution_log(
    batch: ScheduledBatch, *, status: str, records: int,
    reason: str | None = None,
) -> None:
    """Check the persisted result and current-run failure context."""
    with batch.connection.cursor() as cursor:
        cursor.execute(
            "SELECT status, records_processed, error_message "
            "FROM batch_execution_logs WHERE set_id = %s AND execution_arn = %s",
            (batch.set_id, batch.execution_arn),
        )
        row = cursor.fetchone()
    assert row is not None
    assert row[:2] == (status, records)
    if reason is not None:
        for value in (
            reason, batch.set_code,
            CURRENT_SCHEDULED_AT.isoformat(timespec="seconds") + "Z",
        ):
            assert value in row[2]
    elif status == "succeeded":
        assert row[2] is None


def test_ac_1_empty_morning_never_blocks_night_or_next_morning(
    scheduled_batch: ScheduledBatch, monkeypatch: pytest.MonkeyPatch
) -> None:
    """AC-1: An empty morning run never blocks night or the next morning's run."""
    batch = scheduled_batch
    empty_morning = _add_generation_run(batch, MORNING_SCHEDULED_AT, with_media=False)
    night_api = RecordingUrlopen(_success_payloads())

    assert main(s3_client=FakeS3Client(), urlopen=night_api) == 0
    assert len(night_api.requests) == 3
    _assert_successful_runs(batch, [batch.run_id])
    assert _run_posts(batch, empty_morning) == ()

    next_scheduled_at = datetime(2026, 10, 13, 22, 30)
    next_morning = _add_generation_run(batch, next_scheduled_at)
    monkeypatch.setenv(
        "SCHEDULED_AT", next_scheduled_at.isoformat(timespec="seconds") + "Z"
    )
    monkeypatch.setenv("EXECUTION_ARN", f"arn:aws:states:local:e2e:{uuid4().hex}")
    night_posts = _run_posts(batch, batch.run_id)
    next_api = RecordingUrlopen(_success_payloads())

    assert main(s3_client=FakeS3Client(), urlopen=next_api) == 0
    assert len(next_api.requests) == 3
    _assert_successful_runs(batch, [batch.run_id, next_morning])
    assert _run_posts(batch, batch.run_id) == night_posts
    assert _run_posts(batch, empty_morning) == ()


@pytest.mark.parametrize("morning_status", [None, "pending", "container_created"])
def test_ac_2_night_leaves_actionable_morning_posts_unchanged(
    scheduled_batch: ScheduledBatch, morning_status: str | None
) -> None:
    """AC-2: Night posting leaves every actionable morning post intact."""
    batch = scheduled_batch
    morning = _add_generation_run(batch, MORNING_SCHEDULED_AT)
    if morning_status is not None:
        _add_post(batch, morning, morning_status)
    before = _run_posts(batch, morning)
    api = RecordingUrlopen(_success_payloads())

    assert main(s3_client=FakeS3Client(), urlopen=api) == 0
    assert len(api.requests) == 3
    assert _run_posts(batch, morning) == before
    with batch.connection.cursor() as cursor:
        cursor.execute(
            "SELECT generation_run_id, status FROM posts WHERE set_id = %s "
            "AND generation_run_id != %s",
            (batch.set_id, morning),
        )
        assert cursor.fetchall() == ((batch.run_id, "success"),)
    _assert_execution_log(batch, status="succeeded", records=1)


def test_ac_3_missing_current_run_fails_without_falling_back(
    scheduled_batch: ScheduledBatch,
) -> None:
    """AC-3: A past unposted run cannot substitute for a missing current run."""
    batch = scheduled_batch
    with batch.connection.cursor() as cursor:
        cursor.execute(
            "UPDATE generation_runs SET scheduled_at = %s WHERE id = %s",
            (MORNING_SCHEDULED_AT, batch.run_id),
        )
    api = RecordingUrlopen(_success_payloads())
    s3 = FakeS3Client()

    assert main(s3_client=s3, urlopen=api) == 1
    assert api.requests == []
    assert s3.calls == []
    _assert_successful_runs(batch, [])
    _assert_execution_log(batch, status="failed", records=0, reason="RUN_NOT_FOUND")


def test_ac_4_current_run_without_media_fails_without_falling_back(
    scheduled_batch: ScheduledBatch,
) -> None:
    """AC-4: A current empty run fails even when a past run has unposted media."""
    batch = scheduled_batch
    past_run = _add_generation_run(batch, MORNING_SCHEDULED_AT)
    with batch.connection.cursor() as cursor:
        cursor.execute(
            "DELETE FROM generated_media WHERE generation_run_id = %s", (batch.run_id,)
        )
    api = RecordingUrlopen(_success_payloads())
    s3 = FakeS3Client()

    assert main(s3_client=s3, urlopen=api) == 1
    assert api.requests == []
    assert s3.calls == []
    assert _run_posts(batch, past_run) == ()
    _assert_successful_runs(batch, [])
    _assert_execution_log(batch, status="failed", records=0, reason="NO_MEDIA")


@pytest.mark.parametrize("has_current", [True, False], ids=["exact-match", "no-match"])
def test_ac_5_selects_exact_set_and_time_among_neighboring_runs(
    scheduled_batch: ScheduledBatch, has_current: bool
) -> None:
    """AC-5: Other sets, previous days, and newer runs never replace this run."""
    batch = scheduled_batch
    previous_day = _add_generation_run(batch, datetime(2026, 10, 12, 12))
    newer_run = _add_generation_run(batch, datetime(2026, 10, 14, 12))
    with _local_batch_set(file_format="jpg", s3_key="images/other-set.jpg") as other:
        _, _, other_set_id, other_run_id, _ = other
        with batch.connection.cursor() as cursor:
            cursor.execute(
                "UPDATE generation_runs SET scheduled_at = %s WHERE id = %s",
                (CURRENT_SCHEDULED_AT, other_run_id),
            )
            if not has_current:
                cursor.execute(
                    "DELETE FROM generated_media WHERE generation_run_id = %s",
                    (batch.run_id,),
                )
                cursor.execute(
                    "DELETE FROM generation_runs WHERE id = %s", (batch.run_id,)
                )
        api = RecordingUrlopen(_success_payloads())

        assert main(s3_client=FakeS3Client(), urlopen=api) == (0 if has_current else 1)
        assert len(api.requests) == (3 if has_current else 0)
        _assert_successful_runs(batch, [batch.run_id] if has_current else [])
        for run_id in (other_run_id, previous_day, newer_run):
            assert _run_posts(batch, run_id) == ()
        with batch.connection.cursor() as cursor:
            cursor.execute(
                "SELECT COUNT(*) FROM posts WHERE set_id = %s", (other_set_id,)
            )
            assert cursor.fetchone()[0] == 0
        _assert_execution_log(
            batch, status="succeeded" if has_current else "failed",
            records=1 if has_current else 0,
            reason=None if has_current else "RUN_NOT_FOUND",
        )


@pytest.mark.parametrize("status", ["success", "failed", "published_unconfirmed"])
def test_ac_6_terminal_current_run_succeeds_without_api_calls(
    scheduled_batch: ScheduledBatch, status: str
) -> None:
    """AC-6: Every terminal status finishes with zero posts and zero API calls."""
    batch = scheduled_batch
    _add_post(batch, batch.run_id, status)
    before = _run_posts(batch, batch.run_id)
    api = RecordingUrlopen(_success_payloads())
    s3 = FakeS3Client()

    assert main(s3_client=s3, urlopen=api) == 0
    assert api.requests == []
    assert s3.calls == []
    assert _run_posts(batch, batch.run_id) == before
    _assert_execution_log(batch, status="succeeded", records=0)


@pytest.mark.parametrize(
    "terminal_status", ["success", "failed", "published_unconfirmed"]
)
def test_ac_6_processes_only_unfinished_active_account(
    scheduled_batch: ScheduledBatch, monkeypatch: pytest.MonkeyPatch,
    terminal_status: str,
) -> None:
    """AC-6: Only the unfinished of two active accounts reaches the API."""
    batch = scheduled_batch
    _add_post(batch, batch.run_id, terminal_status)
    terminal_before = _run_posts(
        batch, batch.run_id, account_id=batch.account_id
    )
    with batch.connection.cursor() as cursor:
        cursor.execute(
            "INSERT INTO sns_accounts "
            "(set_id, platform, account_code, account_name, is_active) "
            "VALUES (%s, 'instagram', 'unfinished-account', 'Unfinished', 1)",
            (batch.set_id,),
        )
        unfinished_account_id = cursor.lastrowid
    secret_reader = Mock(return_value=json.dumps({
        "access_token": "test-token", "ig_user_id": "unfinished-account"
    }))
    monkeypatch.setattr(processing_module, "get_secret_string", secret_reader)
    api = RecordingUrlopen(_success_payloads())

    # The existing processor still marks the batch failed when a skipped
    # account has failed/published_unconfirmed, while posting the unfinished one.
    return_code = 0 if terminal_status == "success" else 1
    assert main(s3_client=FakeS3Client(), urlopen=api) == return_code
    assert len(api.requests) == 3
    secret_reader.assert_called_once_with(
        f"acps/local/{batch.set_code}/sns/instagram/unfinished-account"
    )
    assert urllib.parse.urlparse(api.requests[0].full_url).path.endswith(
        "/unfinished-account/media"
    )
    assert urllib.parse.urlparse(api.requests[2].full_url).path.endswith(
        "/unfinished-account/media_publish"
    )
    assert (
        _run_posts(batch, batch.run_id, account_id=batch.account_id)
        == terminal_before
    )
    with batch.connection.cursor() as cursor:
        cursor.execute(
            "SELECT sns_account_id, status FROM posts "
            "WHERE generation_run_id = %s ORDER BY sns_account_id",
            (batch.run_id,),
        )
        assert cursor.fetchall() == (
            (batch.account_id, terminal_status), (unfinished_account_id, "success")
        )
    _assert_execution_log(
        batch, status="succeeded" if return_code == 0 else "failed", records=1
    )


@pytest.mark.parametrize("resume_status", ["pending", "container_created"])
def test_ac_7_retry_resumes_same_run_despite_newer_media(
    scheduled_batch: ScheduledBatch, resume_status: str
) -> None:
    """AC-7: Retry keeps the scheduled run and resumes any saved container."""
    batch = scheduled_batch
    initial_payloads: list[dict[str, str] | Exception] = []
    if resume_status == "container_created":
        initial_payloads.append({"id": "container-current"})
    initial_payloads.append(RuntimeError("simulated task crash"))
    initial_api = RecordingUrlopen(initial_payloads)

    assert main(s3_client=FakeS3Client(), urlopen=initial_api) == 1
    assert len(initial_api.requests) == len(initial_payloads)
    with batch.connection.cursor() as cursor:
        cursor.execute(
            "SELECT id, status, platform_container_id FROM posts "
            "WHERE generation_run_id = %s", (batch.run_id,),
        )
        saved_post = cursor.fetchone()
    assert saved_post is not None
    assert saved_post[1:] == (
        resume_status,
        "container-current" if resume_status == "container_created" else None,
    )
    newer_run = _add_generation_run(batch, datetime(2026, 10, 13, 22, 30))
    retry_payloads = _success_payloads()
    if resume_status == "container_created":
        retry_payloads = retry_payloads[1:]
    retry_api = RecordingUrlopen(retry_payloads)
    s3 = FakeS3Client()

    assert main(s3_client=s3, urlopen=retry_api) == 0
    assert len(retry_api.requests) == len(retry_payloads)
    if resume_status == "container_created":
        assert s3.calls == []
        assert retry_api.requests[0].get_method() == "GET"
        assert urllib.parse.urlparse(retry_api.requests[0].full_url).path.endswith(
            "/container-current"
        )
        assert not any(
            urllib.parse.urlparse(request.full_url).path.endswith("/media")
            for request in retry_api.requests
        )
    else:
        assert len(s3.calls) == 1
        assert urllib.parse.urlparse(
            retry_api.requests[0].full_url
        ).path.endswith("/media")
    _assert_successful_runs(batch, [batch.run_id])
    assert _run_posts(batch, newer_run) == ()
    with batch.connection.cursor() as cursor:
        cursor.execute(
            "SELECT id, status, platform_container_id, platform_post_id "
            "FROM posts WHERE generation_run_id = %s", (batch.run_id,),
        )
        assert cursor.fetchall() == (
            (saved_post[0], "success", "container-current", "post-current"),
        )
        cursor.execute(
            "SELECT status, attempt_count, records_processed FROM batch_execution_logs "
            "WHERE execution_arn = %s", (batch.execution_arn,),
        )
        assert cursor.fetchall() == (("succeeded", 2, 1),)


@pytest.mark.parametrize(
    "scheduled_at",
    [
        None,
        "",
        "2026-10-13 21:00:00",
        "2026-10-13T21:00:00+09:00",
        "2026-10-13T12:00:00.000Z",
        "2026-10-13",
        "2026-1-13T12:00:00Z",
        "2026-02-30T12:00:00Z",
    ],
)
def test_ac_8_invalid_scheduled_at_never_connects_or_writes(
    scheduled_batch: ScheduledBatch, monkeypatch: pytest.MonkeyPatch,
    scheduled_at: str | None,
) -> None:
    """AC-8: Invalid scheduled times fail before DB access or row changes."""
    batch = scheduled_batch

    def counts() -> tuple[int, int]:
        with batch.connection.cursor() as cursor:
            cursor.execute(
                "SELECT (SELECT COUNT(*) FROM posts WHERE set_id = %s), "
                "(SELECT COUNT(*) FROM batch_execution_logs WHERE set_id = %s)",
                (batch.set_id, batch.set_id),
            )
            return cursor.fetchone()

    before = counts()
    if scheduled_at is None:
        monkeypatch.delenv("SCHEDULED_AT", raising=False)
    else:
        monkeypatch.setenv("SCHEDULED_AT", scheduled_at)
    forbidden_connection = Mock(
        side_effect=AssertionError("DB must not be opened")
    )
    monkeypatch.setattr(main_module, "open_connection", forbidden_connection)
    api = RecordingUrlopen(_success_payloads())

    assert main(s3_client=FakeS3Client(), urlopen=api) == 1
    assert api.requests == []
    forbidden_connection.assert_not_called()
    assert counts() == before == (0, 0)


def test_ac_9_jst_morning_selects_previous_utc_date(
    scheduled_batch: ScheduledBatch, monkeypatch: pytest.MonkeyPatch
) -> None:
    """AC-9: JST Oct 13 at 07:30 selects UTC Oct 12 at 22:30 unchanged."""
    batch = scheduled_batch
    morning = _add_generation_run(batch, MORNING_SCHEDULED_AT)
    wrong_jst_date = _add_generation_run(batch, datetime(2026, 10, 13, 22, 30))
    monkeypatch.setenv("SCHEDULED_AT", "2026-10-12T22:30:00Z")
    api = RecordingUrlopen(_success_payloads())

    assert main(s3_client=FakeS3Client(), urlopen=api) == 0
    assert len(api.requests) == 3
    _assert_successful_runs(batch, [morning])
    # Oct 13 at 12:00 UTC is JST night, not the requested morning.
    assert _run_posts(batch, batch.run_id) == ()
    assert _run_posts(batch, wrong_jst_date) == ()
