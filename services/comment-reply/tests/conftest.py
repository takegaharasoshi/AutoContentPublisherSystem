"""Shared offline problem fixture."""

from __future__ import annotations

import pytest

from app.judge.contract import Problem


@pytest.fixture
def problem() -> Problem:
    """Return a schema-v2 problem with two independent core points."""
    return Problem.from_snapshot({
        "schema_version": 2,
        "set_code": "umigame-soup-1", "media_id": "media-1",
        "content_key": "001-test", "problem_text": "男はなぜ泣いた？",
        "truth": "男は回復を知った", "fact_sheet": ["病院に行った"],
        "core_points": ["影はレントゲンの影", "病気が良くなった"],
        "reveal_text": "病気が回復したと知った。",
    })
