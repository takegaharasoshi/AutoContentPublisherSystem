"""Local MySQL E2E coverage for the insights collection batch."""

from __future__ import annotations

import datetime
from contextlib import contextmanager
import json
from pathlib import Path
from typing import Any, Iterator
from uuid import uuid4

import pymysql
import pytest

from app.comment_logs import import_comment_logs
from app.models import SnsAccount
from app.processing import process_accounts
from app import processing as processing_module


LOCAL_DB_SECRET = {
    "username": "app",
    "password": "password",
    "host": "127.0.0.1",
    "port": 3306,
    "dbname": "acps",
}
COMMENT_LOG_FIXTURE = (
    Path(__file__).parent / "fixtures" / "comment_log_sample.json"
)


def _connect_local_mysql() -> pymysql.connections.Connection:
    """Connect using the documented local-development credentials."""
    return pymysql.connect(
        host=LOCAL_DB_SECRET["host"],
        port=LOCAL_DB_SECRET["port"],
        user=LOCAL_DB_SECRET["username"],
        password=LOCAL_DB_SECRET["password"],
        database=LOCAL_DB_SECRET["dbname"],
        connect_timeout=2,
        charset="utf8mb4",
    )


@contextmanager
def _seed() -> Iterator[tuple[Any, int, int, int, str]]:
    """Create isolated rows and remove them in foreign-key-safe order."""
    try:
        connection = _connect_local_mysql()
    except Exception:
        pytest.skip("Local MySQL not reachable; skipping E2E test")

    suffix = uuid4().hex[:10]
    set_id = account_id = generation_run_id = post_id = None
    set_code = f"e2e-insights-{suffix}"
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO batch_sets "
                "(set_code, name, generator_name, is_active) VALUES (%s, %s, %s, 1)",
                (set_code, "Insights local E2E", "fake"),
            )
            set_id = cursor.lastrowid
            cursor.execute(
                "INSERT INTO sns_accounts "
                "(set_id, platform, account_code, account_name, is_active) "
                "VALUES (%s, 'instagram', %s, %s, 1)",
                (set_id, f"account-{suffix}", "Insights E2E"),
            )
            account_id = cursor.lastrowid
            cursor.execute(
                "INSERT INTO generation_runs (set_id, scheduled_at) VALUES (%s, %s)",
                (set_id, datetime.datetime(2026, 8, 10, 8)),
            )
            generation_run_id = cursor.lastrowid
            cursor.execute(
                "INSERT INTO posts "
                "(set_id, generation_run_id, sns_account_id, status, media_type, "
                "platform_post_id, posted_at) "
                "VALUES (%s, %s, %s, 'success', 'reel', %s, %s)",
                (
                    set_id,
                    generation_run_id,
                    account_id,
                    f"media-{suffix}",
                    datetime.datetime(2026, 8, 10, 8),
                ),
            )
            post_id = cursor.lastrowid
        connection.commit()
        yield connection, set_id, account_id, post_id, set_code
    finally:
        try:
            connection.rollback()
            with connection.cursor() as cursor:
                if set_id is not None:
                    cursor.execute(
                        "DELETE FROM umigame_comment_logs WHERE set_id = %s",
                        (set_id,),
                    )
                if post_id is not None:
                    cursor.execute("DELETE FROM post_insights WHERE post_id = %s", (post_id,))
                if account_id is not None:
                    cursor.execute(
                        "DELETE FROM account_insights_daily WHERE sns_account_id = %s",
                        (account_id,),
                    )
                if post_id is not None:
                    cursor.execute("DELETE FROM posts WHERE id = %s", (post_id,))
                if generation_run_id is not None:
                    cursor.execute(
                        "DELETE FROM generation_runs WHERE id = %s", (generation_run_id,)
                    )
                if account_id is not None:
                    cursor.execute("DELETE FROM sns_accounts WHERE id = %s", (account_id,))
                if set_id is not None:
                    cursor.execute("DELETE FROM batch_sets WHERE id = %s", (set_id,))
            connection.commit()
        finally:
            connection.close()


def test_same_scheduled_run_is_idempotent(monkeypatch) -> None:
    """A retry adds neither post snapshots nor account daily rows."""
    monkeypatch.setattr(
        processing_module,
        "get_secret_string",
        lambda *args, **kwargs: '{"access_token":"token","ig_user_id":"user"}',
    )
    monkeypatch.setattr(
        processing_module,
        "fetch_account_insights",
        lambda *args, **kwargs: {"reach": 10},
    )
    monkeypatch.setattr(
        processing_module,
        "fetch_followers_count",
        lambda *args, **kwargs: 100,
    )
    monkeypatch.setattr(
        processing_module,
        "fetch_media_insights",
        lambda *args, **kwargs: {"views": 20},
    )

    scheduled_at = datetime.datetime(2026, 8, 10, 9)
    with _seed() as (connection, set_id, account_id, post_id, set_code):
        account = SnsAccount(account_id, "instagram", "unused", "E2E")
        for _ in range(2):
            with connection.cursor() as cursor:
                result = process_accounts(
                    cursor,
                    connection,
                    set_id=set_id,
                    accounts=[account],
                    env_name="local",
                    set_code=set_code,
                    scheduled_at=scheduled_at,
                    media_lookback_days=14,
                    current_time=scheduled_at,
                )
                assert result.failure_count == 0
        with connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM post_insights WHERE post_id = %s", (post_id,))
            post_count = cursor.fetchone()[0]
            cursor.execute(
                "SELECT COUNT(*) FROM account_insights_daily WHERE sns_account_id = %s",
                (account_id,),
            )
            account_count = cursor.fetchone()[0]
        assert post_count == 1
        assert account_count == 90


def test_comment_log_insert_is_idempotent_and_expired_rows_are_deleted() -> None:
    """INSERT IGNORE keeps one row on retries and retention removes only old rows."""

    class FakeS3:
        def __init__(self) -> None:
            self.objects: dict[str, bytes] = {}

        def list_objects_v2(self, *, Bucket: str, Prefix: str, **kwargs: Any) -> dict[str, Any]:
            return {
                "IsTruncated": False,
                "Contents": [
                    {"Key": key} for key in sorted(self.objects) if key.startswith(Prefix)
                ],
            }

        def get_object(self, *, Bucket: str, Key: str) -> dict[str, bytes]:
            return {"Body": self.objects[Key]}

    now = datetime.datetime(2026, 10, 12, 12, 0)
    first_id = f"e2e-{uuid4().hex}"
    second_id = f"e2e-{uuid4().hex}"

    def make_record(comment_id: str, set_code: str) -> dict[str, Any]:
        record = json.loads(COMMENT_LOG_FIXTURE.read_text(encoding="utf-8"))
        record["comment_id"] = comment_id
        record["set_code"] = set_code
        return record

    with _seed() as (connection, set_id, _account_id, _post_id, set_code):
        s3 = FakeS3()
        first_key = f"comment-log/{set_code}/dt=2026-10-11/{first_id}.json"
        s3.objects[first_key] = json.dumps(
            make_record(first_id, set_code), ensure_ascii=False
        ).encode("utf-8")

        for _ in range(2):
            with connection.cursor() as cursor:
                result = import_comment_logs(
                    cursor,
                    connection,
                    set_id=set_id,
                    set_code=set_code,
                    bucket="e2e-assets",
                    now=now,
                    lookback_days=3,
                    retention_days=365,
                    s3_client=s3,
                )
                assert result.skipped_invalid == 0
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT COUNT(*) FROM umigame_comment_logs WHERE set_id = %s",
                (set_id,),
            )
            assert cursor.fetchone()[0] == 1

        second_key = f"comment-log/{set_code}/dt=2026-10-11/{second_id}.json"
        s3.objects[second_key] = json.dumps(
            make_record(second_id, set_code), ensure_ascii=False
        ).encode("utf-8")
        with connection.cursor() as cursor:
            import_comment_logs(
                cursor,
                connection,
                set_id=set_id,
                set_code=set_code,
                bucket="e2e-assets",
                now=now,
                lookback_days=3,
                retention_days=365,
                s3_client=s3,
            )

        old_received_at = now - datetime.timedelta(days=2)
        with connection.cursor() as cursor:
            cursor.execute(
                "UPDATE umigame_comment_logs SET webhook_received_at = %s "
                "WHERE comment_id = %s",
                (old_received_at, first_id),
            )
        connection.commit()

        with connection.cursor() as cursor:
            result = import_comment_logs(
                cursor,
                connection,
                set_id=set_id,
                set_code=set_code,
                bucket="e2e-assets",
                now=now,
                lookback_days=3,
                retention_days=1,
                s3_client=s3,
            )
            assert result.deleted_expired == 1
            cursor.execute(
                "SELECT comment_id FROM umigame_comment_logs WHERE set_id = %s",
                (set_id,),
            )
            remaining_ids = {row[0] for row in cursor.fetchall()}
        assert remaining_ids == {second_id}
