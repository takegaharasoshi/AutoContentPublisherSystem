"""Local MySQL coverage for the previous-truth caption block."""

from __future__ import annotations

from typing import Any, Iterator
from uuid import uuid4

import pymysql
import pytest

from app.captions import build_caption


LOCAL_DB = {
    "host": "127.0.0.1",
    "port": 3306,
    "user": "app",
    "password": "password",
    "database": "acps",
}
TEMPLATE = "{{caption}}{{prev_truth_block}}"


@pytest.fixture
def umigame_set() -> Iterator[tuple[Any, int, int]]:
    """Create a temporary umigame set with one active account."""
    try:
        connection = pymysql.connect(**LOCAL_DB, connect_timeout=2, charset="utf8mb4")
    except Exception:
        pytest.skip("Local MySQL not reachable; skipping E2E test")
    set_id: int | None = None
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO batch_sets (set_code, name, description, generator_name, "
                "is_active) VALUES (%s, %s, %s, %s, %s)",
                (f"e2e-umi-{uuid4().hex[:8]}", "umigame E2E", "pytest", "fake", 0),
            )
            set_id = cursor.lastrowid
            cursor.execute(
                "INSERT INTO sns_accounts (set_id, platform, account_code, "
                "account_name, is_active) VALUES (%s, %s, %s, %s, %s)",
                (set_id, "instagram", "e2e-account", "E2E Account", 1),
            )
            account_id = cursor.lastrowid
        connection.commit()
        yield connection, set_id, account_id
    finally:
        if set_id is not None:
            connection.rollback()
            with connection.cursor() as cursor:
                for table in (
                    "posts", "umigame_items", "generation_runs",
                    "umigame_stock_items", "sns_accounts",
                ):
                    cursor.execute(f"DELETE FROM {table} WHERE set_id = %s", (set_id,))
                cursor.execute("DELETE FROM batch_sets WHERE id = %s", (set_id,))
            connection.commit()
        connection.close()


def _add_run(
    cursor: Any,
    set_id: int,
    account_id: int,
    number: int,
    *,
    post_status: str | None,
    posted_at: str | None = None,
) -> int:
    """Add a generation run with its umigame item and optional post row."""
    cursor.execute(
        "INSERT INTO umigame_stock_items (set_id, content_key, title, difficulty, "
        "problem_text, truth, fact_sheet, expected_questions, hook, rule_text, "
        "narration, play_example, character_lines, illustration_prompt, caption, "
        "source_note) VALUES (%s, %s, %s, 3, %s, %s, '[\"事実\"]', '[]', %s, %s, "
        "'[]', '[]', '[]', 'p', %s, 's')",
        (
            set_id, f"{number:03d}-e2e", f"題{number}", f"問題{number}",
            f"真相{number}", "フック", "ルール", f"本文{number} #AIart",
        ),
    )
    stock_id = cursor.lastrowid
    cursor.execute(
        "INSERT INTO generation_runs (set_id, scheduled_at) VALUES (%s, %s)",
        (set_id, f"2026-10-{number:02d} 11:00:00"),
    )
    run_id = cursor.lastrowid
    cursor.execute(
        "INSERT INTO umigame_items (set_id, generation_run_id, stock_item_id, "
        "content_key, title, problem_text, truth, fact_sheet, rule_text, hook, "
        "caption) VALUES (%s, %s, %s, %s, %s, %s, %s, '[\"事実\"]', %s, %s, %s)",
        (
            set_id, run_id, stock_id, f"{number:03d}-e2e", f"題{number}",
            f"問題{number}", f"真相{number}", "ルール", "フック",
            f"本文{number} #AIart",
        ),
    )
    if post_status is not None:
        cursor.execute(
            "INSERT INTO posts (set_id, generation_run_id, sns_account_id, status, "
            "media_type, posted_at) VALUES (%s, %s, %s, %s, 'reel', %s)",
            (set_id, run_id, account_id, post_status, posted_at),
        )
    return run_id


def test_first_post_has_no_previous_truth_block(umigame_set) -> None:
    connection, set_id, account_id = umigame_set
    with connection.cursor() as cursor:
        run_id = _add_run(cursor, set_id, account_id, 1, post_status=None)
        assert build_caption(cursor, run_id, TEMPLATE, set_id=set_id) == "本文1 #AIart"


def test_previous_truth_skips_failed_run(umigame_set) -> None:
    connection, set_id, account_id = umigame_set
    with connection.cursor() as cursor:
        _add_run(
            cursor, set_id, account_id, 1,
            post_status="success", posted_at="2026-10-01 11:05:00",
        )
        _add_run(cursor, set_id, account_id, 2, post_status="failed")
        _add_run(
            cursor, set_id, account_id, 3,
            post_status="published_unconfirmed",
        )
        run_id = _add_run(cursor, set_id, account_id, 4, post_status=None)
        caption = build_caption(cursor, run_id, TEMPLATE, set_id=set_id)
    assert caption == (
        "本文4 #AIart\n\n\n\n"
        "――― 前回の問題「題1」の真相（ネタバレ注意）―――\n"
        "・\n・\n・\n・\n【真相】\n真相1"
    )


def test_previous_truth_uses_latest_success_and_ignores_current_run(
    umigame_set,
) -> None:
    connection, set_id, account_id = umigame_set
    with connection.cursor() as cursor:
        _add_run(
            cursor, set_id, account_id, 1,
            post_status="success", posted_at="2026-10-01 11:05:00",
        )
        _add_run(
            cursor, set_id, account_id, 2,
            post_status="success", posted_at="2026-10-02 11:05:00",
        )
        # A retry of the current run after its own success must not reveal itself.
        run_id = _add_run(
            cursor, set_id, account_id, 3,
            post_status="success", posted_at="2026-10-03 11:05:00",
        )
        caption = build_caption(cursor, run_id, TEMPLATE, set_id=set_id)
    assert "前回の問題「題2」" in caption
    assert caption.endswith("【真相】\n真相2")
