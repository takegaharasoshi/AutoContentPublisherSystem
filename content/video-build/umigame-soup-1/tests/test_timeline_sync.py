"""build.py の定数と remotion/src/timeline.ts の定数が一致することを検査する。"""

from __future__ import annotations

from pathlib import Path
import re
import sys

HERE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(HERE))

import build  # noqa: E402
import common  # noqa: E402

TIMELINE_TS = HERE / "remotion" / "src" / "timeline.ts"


def _ts_const(name: str) -> str:
    text = TIMELINE_TS.read_text(encoding="utf-8")
    match = re.search(rf"export const {name} = (.+?);", text)
    assert match, f"{name} が timeline.ts にありません"
    return match.group(1)


def test_fps_and_total_frames() -> None:
    assert _ts_const("FPS") == str(common.FPS)
    assert common.TOTAL_FRAMES == common.FPS * 24
    assert "DURATION_SECONDS = 24" in TIMELINE_TS.read_text(encoding="utf-8")


def test_narration_constants() -> None:
    assert _ts_const("NARRATION_START") == "Math.round(0.5 * FPS)"
    assert common.NARRATION_START == round(0.5 * common.FPS)
    assert _ts_const("NARRATION_GAP") == "Math.round(1.2 * FPS)"
    assert common.NARRATION_GAP == round(1.2 * common.FPS)
    # 継ぎ目の開始（720 - 12）
    assert _ts_const("NARRATION_DEADLINE") == "SEAM_START"
    assert common.NARRATION_START + round(common.NARRATION_BUDGET_SECONDS * common.FPS) < 708


def test_still_frames_within_beats() -> None:
    assert all(0 <= frame < common.TOTAL_FRAMES for frame in build.STILL_FRAMES.values())
    assert build.STILL_FRAMES["seam_tail"] >= 708
