"""Repository functions for generated umigame items."""

from __future__ import annotations

import json
from typing import Any

from .models import UmigameItem


def fetch_umigame_item(cursor: Any, generation_run_id: int) -> UmigameItem | None:
    """Fetch and JSON-decode the problem recorded for one generation run."""
    cursor.execute(
        "SELECT id, content_key, problem_text, truth, fact_sheet, rule_text, "
        "hook, caption FROM umigame_items "
        "WHERE generation_run_id = %s LIMIT 1",
        (generation_run_id,),
    )
    row = cursor.fetchone()
    if row is None:
        return None

    facts = row[4]
    if isinstance(facts, (bytes, bytearray)):
        try:
            facts = facts.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise RuntimeError("umigame_items.fact_sheet is invalid UTF-8") from exc
    if isinstance(facts, str):
        try:
            facts = json.loads(facts)
        except json.JSONDecodeError as exc:
            raise RuntimeError("umigame_items.fact_sheet is invalid JSON") from exc
    if (
        not isinstance(facts, list)
        or not facts
        or any(not isinstance(fact, str) or not fact.strip() for fact in facts)
    ):
        raise RuntimeError(
            "umigame_items.fact_sheet must be a non-empty array of strings"
        )
    return UmigameItem(
        id=row[0],
        content_key=row[1],
        problem_text=row[2],
        truth=row[3],
        fact_sheet=facts,
        rule_text=row[5],
        hook=row[6],
        caption=row[7],
    )
