"""Repository functions for generated umigame items."""

from __future__ import annotations

import json
from typing import Any

from .models import UmigameItem


def fetch_umigame_item(cursor: Any, generation_run_id: int) -> UmigameItem | None:
    """Fetch and JSON-decode the problem recorded for one generation run."""
    cursor.execute(
        "SELECT id, content_key, problem_text, truth, fact_sheet, core_points, "
        "reveal_text, rule_text, "
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
    core_points = row[5]
    if core_points is not None:
        if isinstance(core_points, (bytes, bytearray)):
            try:
                core_points = core_points.decode("utf-8")
            except UnicodeDecodeError as exc:
                raise RuntimeError(
                    "umigame_items.core_points is invalid UTF-8"
                ) from exc
        if isinstance(core_points, str):
            try:
                core_points = json.loads(core_points)
            except json.JSONDecodeError as exc:
                raise RuntimeError(
                    "umigame_items.core_points is invalid JSON"
                ) from exc
        if (
            not isinstance(core_points, list)
            or not 1 <= len(core_points) <= 3
            or any(
                not isinstance(point, str) or not point.strip()
                for point in core_points
            )
        ):
            raise RuntimeError(
                "umigame_items.core_points must be an array of 1 to 3 non-empty strings"
            )
    return UmigameItem(
        id=row[0],
        content_key=row[1],
        problem_text=row[2],
        truth=row[3],
        fact_sheet=facts,
        core_points=core_points,
        reveal_text=row[6],
        rule_text=row[7],
        hook=row[8],
        caption=row[9],
    )
