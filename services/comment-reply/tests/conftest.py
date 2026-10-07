"""Shared offline problem fixture."""

from __future__ import annotations

from dataclasses import replace

import pytest

from app.judge.contract import Problem
from tools.local_trial import _load_stock_problem


@pytest.fixture
def problem() -> Problem:
    """Return a schema-v3 problem using U01's authored judge criteria."""
    return replace(
        _load_stock_problem("U01"), media_id="media-1", content_key="001-test",
        problem_text="男はなぜ泣いた？", truth="男は回復を知った",
        fact_sheet=("病院に行った",), reveal_text="病気が回復したと知った。",
    )
