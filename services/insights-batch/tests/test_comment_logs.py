"""Tests for importing comment logs from S3."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
import json
from pathlib import Path
from typing import Any

from app.comment_logs import import_comment_logs


FIXTURE_PATH = Path(__file__).parent / "fixtures" / "comment_log_sample.json"
FIXTURE_RECORD = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
NOW = datetime(2026, 10, 12, 0, 0, tzinfo=timezone.utc)
BUCKET = "test-assets"
SET_ID = 42
SET_CODE = "umigame-soup-1"


class FakeS3:
    """Small S3 client fake with optional per-prefix pages."""

    def __init__(
        self,
        objects: dict[str, Any] | None = None,
        pages: dict[tuple[str, str | None], dict[str, Any]] | None = None,
    ) -> None:
        self.objects = objects or {}
        self.pages = pages or {}
        self.list_calls: list[dict[str, Any]] = []
        self.get_calls: list[dict[str, str]] = []

    def list_objects_v2(self, **kwargs: Any) -> dict[str, Any]:
        self.list_calls.append(kwargs)
        prefix = kwargs["Prefix"]
        token = kwargs.get("ContinuationToken")
        page = self.pages.get((prefix, token))
        if page is not None:
            return page
        return {
            "IsTruncated": False,
            "Contents": [
                {"Key": key} for key in sorted(self.objects) if key.startswith(prefix)
            ],
        }

    def get_object(self, *, Bucket: str, Key: str) -> dict[str, Any]:
        self.get_calls.append({"Bucket": Bucket, "Key": Key})
        value = self.objects[Key]
        if isinstance(value, Exception):
            raise value
        if isinstance(value, bytes):
            body = value
        elif isinstance(value, str):
            body = value.encode("utf-8")
        else:
            body = json.dumps(value, ensure_ascii=False).encode("utf-8")
        return {"Body": body}


class FakeCursor:
    """Cursor fake that models stored comment IDs and SQL results."""

    def __init__(self) -> None:
        self.rows: dict[str, tuple[Any, ...]] = {}
        self.rowcount = 0
        self.select_params: list[tuple[Any, ...]] = []
        self.insert_values: list[tuple[Any, ...]] = []
        self.delete_params: tuple[Any, ...] | None = None
        self.delete_rowcount = 0
        self._fetch_rows: list[tuple[Any, ...]] = []

    def execute(self, sql: str, params: tuple[Any, ...]) -> None:
        if sql.startswith("SELECT comment_id"):
            self.select_params.append(params)
            self._fetch_rows = [(comment_id,) for comment_id in params if comment_id in self.rows]
            self.rowcount = len(self._fetch_rows)
        elif sql.startswith("INSERT IGNORE INTO umigame_comment_logs"):
            self.insert_values.append(params)
            comment_id = params[0]
            self.rowcount = 0 if comment_id in self.rows else 1
            if self.rowcount:
                self.rows[comment_id] = params
        elif sql.startswith("DELETE FROM umigame_comment_logs"):
            self.delete_params = params
            self.rowcount = self.delete_rowcount
        else:
            raise AssertionError(f"Unexpected SQL: {sql}")

    def fetchall(self) -> list[tuple[Any, ...]]:
        return self._fetch_rows


class FakeConnection:
    """Connection fake that records commit calls."""

    def __init__(self) -> None:
        self.commits = 0

    def commit(self) -> None:
        self.commits += 1


def _key(comment_id: str, day: str = "2026-10-12") -> str:
    return f"comment-log/{SET_CODE}/dt={day}/{comment_id}.json"


def _run(
    cursor: FakeCursor,
    connection: FakeConnection,
    s3: FakeS3,
    *,
    now: datetime = NOW,
    lookback_days: int = 1,
    retention_days: int = 365,
):
    return import_comment_logs(
        cursor,
        connection,
        set_id=SET_ID,
        set_code=SET_CODE,
        bucket=BUCKET,
        now=now,
        lookback_days=lookback_days,
        retention_days=retention_days,
        s3_client=s3,
    )


def test_imports_sample_record_with_column_mappings() -> None:
    """Sample JSON fields are converted into the DDL columns."""
    comment_id = FIXTURE_RECORD["comment_id"]
    key = _key(comment_id, "2026-10-11")
    cursor = FakeCursor()
    connection = FakeConnection()
    s3 = FakeS3({key: FIXTURE_RECORD})

    result = _run(cursor, connection, s3)

    values = cursor.rows[comment_id]
    assert result.listed == 1
    assert result.fetched == 1
    assert result.inserted == 1
    assert result.skipped_invalid == 0
    assert values[0:9] == (
        comment_id,
        SET_ID,
        "18092935040666829",
        "18114604907104987",
        "016-umigame-soup",
        3,
        "c81ff384e8a1",
        "2348976535875935",
        "主人公は、窓の外に何を見つけたのでしょうか？",
    )
    assert values[9:13] == (
        datetime(2026, 10, 11, 19, 19, 28),
        datetime(2026, 10, 11, 19, 19, 29),
        datetime(2026, 10, 11, 19, 19, 36),
        datetime(2026, 10, 11, 19, 19, 43),
    )
    assert values[13:22] == (
        "haiku",
        "1b-haiku",
        "9c2045d7fa0d",
        "guess_correct",
        "haiku",
        "正解です！よく気づきましたね。",
        "llm",
        "18081406364651154",
        2,
    )
    stored_record = json.loads(values[22])
    assert stored_record == FIXTURE_RECORD
    assert values[23] == key
    assert values[24] == datetime(2026, 10, 12, 0, 0)
    assert connection.commits == 2


def test_repeat_import_does_not_get_existing_objects() -> None:
    """The existing ID lookup makes repeated imports skip S3 GET."""
    comment_id = FIXTURE_RECORD["comment_id"]
    key = _key(comment_id, "2026-10-11")
    cursor = FakeCursor()
    connection = FakeConnection()
    s3 = FakeS3({key: FIXTURE_RECORD})

    first = _run(cursor, connection, s3)
    second = _run(cursor, connection, s3)

    assert first.inserted == 1
    assert second.inserted == 0
    assert second.listed == 1
    assert second.fetched == 0
    assert len(s3.get_calls) == 1


def test_invalid_json_and_mismatched_records_are_skipped() -> None:
    """Malformed data, wrong schema, IDs, and set codes do not stop import."""
    records: dict[str, Any] = {
        _key("bad-json"): b"{not json",
        _key("wrong-version"): {**FIXTURE_RECORD, "comment_id": "wrong-version", "schema_version": 2},
        _key("wrong-id"): {**FIXTURE_RECORD, "comment_id": "different-id"},
        _key("wrong-set"): {**FIXTURE_RECORD, "comment_id": "wrong-set", "set_code": "another-set"},
    }
    cursor = FakeCursor()
    result = _run(cursor, FakeConnection(), FakeS3(records))

    assert result.listed == 4
    assert result.fetched == 4
    assert result.inserted == 0
    assert result.skipped_invalid == 4
    assert cursor.rows == {}


def test_username_keys_are_removed_recursively_before_storage() -> None:
    """No username field is persisted, including at nested levels."""
    record = json.loads(json.dumps(FIXTURE_RECORD))
    record["username"] = "private-user"
    record["judgements"]["haiku"]["debug"]["username"] = "nested-private-user"
    record["extras"] = [{"nested": {"username": "deep-private-user", "safe": True}}]
    key = _key(record["comment_id"], "2026-10-11")
    cursor = FakeCursor()

    _run(cursor, FakeConnection(), FakeS3({key: record}))

    stored_record = json.loads(cursor.rows[record["comment_id"]][22])
    assert "username" not in stored_record
    assert "username" not in stored_record["judgements"]["haiku"]["debug"]
    assert "username" not in stored_record["extras"][0]["nested"]
    assert stored_record["extras"][0]["nested"]["safe"] is True


def test_date_range_and_s3_pagination() -> None:
    """All inclusive UTC dates are listed and continuation tokens are followed."""
    first_prefix = "comment-log/umigame-soup-1/dt=2026-10-10/"
    page_one = _key("first", "2026-10-10")
    page_two = _key("second", "2026-10-10")
    first_record = {**FIXTURE_RECORD, "comment_id": "first"}
    second_record = {**FIXTURE_RECORD, "comment_id": "second"}
    pages = {
        (first_prefix, None): {
            "IsTruncated": True,
            "NextContinuationToken": "page-2",
            "Contents": [{"Key": page_one}, {"Key": page_one + ".tmp"}],
        },
        (first_prefix, "page-2"): {
            "IsTruncated": False,
            "Contents": [{"Key": page_two}],
        },
    }
    s3 = FakeS3({page_one: first_record, page_two: second_record}, pages)

    result = _run(FakeCursor(), FakeConnection(), s3, lookback_days=2)

    assert [call["Prefix"] for call in s3.list_calls] == [
        "comment-log/umigame-soup-1/dt=2026-10-10/",
        "comment-log/umigame-soup-1/dt=2026-10-10/",
        "comment-log/umigame-soup-1/dt=2026-10-11/",
        "comment-log/umigame-soup-1/dt=2026-10-12/",
    ]
    assert s3.list_calls[1]["ContinuationToken"] == "page-2"
    assert result.listed == 2
    assert result.fetched == 2


def test_retention_delete_uses_set_and_utc_cutoff() -> None:
    """Expired deletion is scoped to the set and receives now minus retention."""
    cursor = FakeCursor()
    cursor.delete_rowcount = 3
    now = datetime(2026, 10, 12, 9, tzinfo=timezone(timedelta(hours=9)))

    result = _run(cursor, FakeConnection(), FakeS3(), now=now, retention_days=30)

    assert result.deleted_expired == 3
    assert cursor.delete_params == (SET_ID, datetime(2026, 9, 12, 0, 0))
