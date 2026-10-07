"""Repository functions for generated umigame items."""

from __future__ import annotations

import json
from typing import Any

from .models import UmigameItem


def fetch_umigame_item(cursor: Any, generation_run_id: int) -> UmigameItem | None:
    """Fetch and JSON-decode the problem recorded for one generation run."""
    cursor.execute(
        "SELECT id, content_key, problem_text, truth, fact_sheet, core_points, judge_criteria, "
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
    judge_criteria = row[6]
    if judge_criteria is not None:
        if isinstance(judge_criteria, (bytes, bytearray)):
            try:
                judge_criteria = judge_criteria.decode("utf-8")
            except UnicodeDecodeError as exc:
                raise RuntimeError("umigame_items.judge_criteria is invalid UTF-8") from exc
        if isinstance(judge_criteria, str):
            try:
                judge_criteria = json.loads(judge_criteria)
            except json.JSONDecodeError as exc:
                raise RuntimeError("umigame_items.judge_criteria is invalid JSON") from exc
        if not isinstance(judge_criteria, dict):
            raise RuntimeError("umigame_items.judge_criteria must be an object")
        points = judge_criteria.get("points")
        errors = judge_criteria.get("errors")
        if (
            not isinstance(points, list)
            or core_points is None
            or len(points) != len(core_points)
            or any(
                not isinstance(point, dict)
                or any(not isinstance(point.get(key), str) or not point[key].strip()
                       for key in ("hit", "touch"))
                for point in points
            )
            or not isinstance(errors, list)
            or len(errors) > 3
            or any(not isinstance(error, str) or not error.strip() for error in errors)
        ):
            raise RuntimeError(
                "umigame_items.judge_criteria must match core_points and contain valid points and errors"
            )
    return UmigameItem(
        id=row[0],
        content_key=row[1],
        problem_text=row[2],
        truth=row[3],
        fact_sheet=facts,
        core_points=core_points,
        judge_criteria=judge_criteria,
        reveal_text=row[7],
        rule_text=row[8],
        hook=row[9],
        caption=row[10],
    )
