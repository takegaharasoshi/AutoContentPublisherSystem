"""build.py の定数と remotion/src/timeline.ts の定数が一致することを検査する。"""

from __future__ import annotations

from pathlib import Path
import re
import sys

HERE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(HERE))

import build  # noqa: E402

TIMELINE_TS = HERE / "remotion" / "src" / "timeline.ts"


def _ts_const(name: str) -> str:
    text = TIMELINE_TS.read_text(encoding="utf-8")
    match = re.search(rf"export const {name} = (.+?);", text)
    assert match, f"{name} が timeline.ts にありません"
    return match.group(1)


def test_fps_and_total_frames() -> None:
    assert _ts_const("FPS") == str(build.FPS)
    assert build.TOTAL_FRAMES == build.FPS * 20
    assert "DURATION_SECONDS = 20" in TIMELINE_TS.read_text(encoding="utf-8")


def test_narration_constants() -> None:
    assert _ts_const("NARRATION_START") == "Math.round(0.5 * FPS)"
    assert build.NARRATION_START == round(0.5 * build.FPS)
    assert _ts_const("NARRATION_GAP") == "Math.round(0.5 * FPS)"
    assert build.NARRATION_GAP == round(0.5 * build.FPS)
    # OUTRO_START(450) + 2 秒
    assert _ts_const("NARRATION_DEADLINE") == "OUTRO_START + 2 * FPS"
    assert build.NARRATION_DEADLINE == 3 * build.FPS + 4 * build.FPS * 3 + 2 * build.FPS


def test_still_frames_within_beats() -> None:
    assert all(0 <= frame < build.TOTAL_FRAMES for frame in build.STILL_FRAMES.values())
    assert build.STILL_FRAMES["seam_tail"] >= 588
