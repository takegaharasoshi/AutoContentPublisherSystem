"""Repository functions for generated ranking items."""

from __future__ import annotations

import json
from typing import Any

from .models import RankingItem


def fetch_ranking_item(cursor: Any, generation_run_id: int) -> RankingItem | None:
    """Fetch and JSON-decode the ranking item for one generation run."""
    cursor.execute(
        "SELECT title, content_fields FROM ranking_items "
        "WHERE generation_run_id = %s LIMIT 1",
        (generation_run_id,),
    )
    row = cursor.fetchone()
    if row is None:
        return None

    raw_fields = row[1]
    if isinstance(raw_fields, (bytes, bytearray)):
        raw_fields = raw_fields.decode("utf-8")
    if isinstance(raw_fields, str):
        try:
            raw_fields = json.loads(raw_fields)
        except json.JSONDecodeError as exc:
            raise RuntimeError("ranking_items.content_fields is invalid JSON") from exc
    if not isinstance(raw_fields, dict):
        raise RuntimeError("ranking_items.content_fields must be a JSON object")
    return RankingItem(row[0], raw_fields)
