"""build.py と remotion/src/timeline.ts の定数同期と、タイムラインの不変条件を検査する。

2026-10-17（R-1-1）でループの作りをやめて一本道にしたため、継ぎ目（フレーム 0 と末尾の一致）の
検査は外し、「ビートが順序どおり・隙間なし・末尾が尺に一致」を timeline.ts の実体で確かめる。
"""

from __future__ import annotations

import json
from pathlib import Path
import re
import shutil
import subprocess
import sys

import pytest

HERE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(HERE))

import build  # noqa: E402
import common  # noqa: E402

TIMELINE_TS = HERE / "remotion" / "src" / "timeline.ts"
ESBUILD = HERE / "remotion" / "node_modules" / ".bin" / "esbuild"


def _ts_const(name: str) -> str:
    text = TIMELINE_TS.read_text(encoding="utf-8")
    match = re.search(rf"export const {name} = (.+?);", text)
    assert match, f"{name} が timeline.ts にありません"
    return match.group(1)


def _timeline_module() -> dict:
    """timeline.ts を esbuild で束ねて node で評価し、BEATS と定数を返す。"""
    if not ESBUILD.is_file() or shutil.which("node") is None:
        pytest.skip("remotion/node_modules（esbuild）または node がありません")
    bundled = subprocess.run(
        [str(ESBUILD), str(TIMELINE_TS), "--bundle", "--format=cjs", "--platform=node"],
        capture_output=True, text=True, check=True,
    ).stdout
    script = (
        "const m = {exports: {}};"
        "(function (module, exports) {" + bundled + "})(m, m.exports);"
        "const t = m.exports;"
        "console.log(JSON.stringify({beats: t.BEATS, total: t.TOTAL_FRAMES, fps: t.FPS,"
        " openingEnd: t.OPENING_END, openingFade: t.OPENING_FADE_FRAMES,"
        " narrationStart: t.NARRATION_START, budget: t.NARRATION_BUDGET_FRAMES,"
        " deadline: t.NARRATION_DEADLINE, switches: t.BUBBLE_SWITCH_FRAMES}));"
    )
    completed = subprocess.run(
        ["node", "-e", script], capture_output=True, text=True, check=True
    )
    return json.loads(completed.stdout)


def test_fps_and_total_frames() -> None:
    assert _ts_const("FPS") == str(common.FPS)
    assert _ts_const("DURATION_SECONDS") == str(common.DURATION_SECONDS)
    assert common.TOTAL_FRAMES == common.FPS * common.DURATION_SECONDS
    assert common.DURATION_SECONDS < 30


def test_narration_constants() -> None:
    assert _ts_const("OPENING_END") == "Math.round(4.5 * FPS)"
    assert common.OPENING_END == round(4.5 * common.FPS)
    assert _ts_const("OPENING_FADE_FRAMES") == str(common.OPENING_FADE_FRAMES)
    assert _ts_const("OPENING_NARRATION_START") == str(common.OPENING_NARRATION_START)
    assert _ts_const("NARRATION_START") == "OPENING_END + Math.round(0.5 * FPS)"
    assert common.NARRATION_START == common.OPENING_END + round(0.5 * common.FPS)
    assert _ts_const("NARRATION_GAP") == "Math.round(1.2 * FPS)"
    assert common.NARRATION_GAP == round(1.2 * common.FPS)
    assert _ts_const("NARRATION_BUDGET_FRAMES") == "21 * FPS"
    assert common.NARRATION_BUDGET_SECONDS == 21.0
    # 予算を使い切っても尺の内側で終わる
    assert (
        common.NARRATION_START + round(common.NARRATION_BUDGET_SECONDS * common.FPS)
        <= common.TOTAL_FRAMES
    )


def test_beats_are_ordered_contiguous_and_end_at_total() -> None:
    module = _timeline_module()
    beats = module["beats"]
    assert module["total"] == common.TOTAL_FRAMES
    assert beats[0]["kind"] == "opening"
    assert beats[0]["from"] == 0
    assert beats[0]["to"] == common.OPENING_END
    for previous, current in zip(beats, beats[1:]):
        assert current["from"] == previous["to"], (previous, current)
    assert all(beat["to"] > beat["from"] for beat in beats)
    assert beats[-1]["to"] == common.TOTAL_FRAMES
    assert beats[-1]["kind"] == "jr_outro"
    assert all(beat["kind"] != "seam" for beat in beats)
    assert module["narrationStart"] + module["budget"] <= module["deadline"] <= module["total"]
    # 吹き出しの SE は導入シーン・出題では鳴らさない
    assert min(module["switches"]) >= beats[1]["to"]


def test_still_frames_within_beats() -> None:
    assert all(0 <= frame < common.TOTAL_FRAMES for frame in build.STILL_FRAMES.values())
    assert build.STILL_FRAMES["opening"] == 0
    assert common.OPENING_END <= build.STILL_FRAMES["switch"] < (
        common.OPENING_END + common.OPENING_FADE_FRAMES
    )
    assert build.STILL_FRAMES["end"] == common.TOTAL_FRAMES - 1
    assert "seam_tail" not in build.STILL_FRAMES

