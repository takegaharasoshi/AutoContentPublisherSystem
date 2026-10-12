"""Shared offline problem fixture."""

from __future__ import annotations

import json
from pathlib import Path
from urllib import request

import pytest

from app.judge.contract import Problem

# U01 の判定用 2 項目の写し（21-8c2 でツール経由の読み込みをやめた。判定の検査用で、ストックとの同期は不要）
JUDGE_POINTS_PATH = Path(__file__).resolve().parent / "fixtures/u01_judge_points.json"


@pytest.fixture(autouse=True)
def block_live_http(monkeypatch) -> None:
    """Require tests to install their own HTTP mocks before any request."""
    def blocked(*args, **kwargs):
        raise AssertionError("live HTTP requests are forbidden in offline tests")

    monkeypatch.setattr(request, "urlopen", blocked)


@pytest.fixture
def problem() -> Problem:
    """Return a schema-v3 problem using U01's authored judge criteria."""
    points = json.loads(JUDGE_POINTS_PATH.read_text(encoding="utf-8"))
    return Problem.from_snapshot({
        "schema_version": 3, "set_code": "umigame-soup-1",
        "media_id": "media-1", "content_key": "001-test",
        "problem_text": "男はなぜ泣いた？", "truth": "男は回復を知った",
        "fact_sheet": ["病院に行った"], "core_points": points["core_points"],
        "judge_criteria": points["judge_criteria"],
        "reveal_text": "病気が回復したと知った。",
    })
