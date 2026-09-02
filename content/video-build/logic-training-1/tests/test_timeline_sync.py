"""Python の R-1 仕様と Remotion タイムラインの同期テスト。"""

from pathlib import Path
import re

import spec


TIMELINE = Path(__file__).resolve().parent.parent / "remotion" / "src" / "timeline.ts"


def _integer(source: str, name: str) -> int:
    match = re.search(rf"export const {name} = (\d+);", source)
    assert match, f"timeline.ts の {name} を数値定数として読み取れません"
    return int(match.group(1))


def _fps_multiple(source: str, name: str) -> int:
    match = re.search(rf"export const {name} = (\d+) \* FPS;", source)
    assert match, f"timeline.ts の {name} を FPS 倍として読み取れません"
    return int(match.group(1)) * spec.FPS


def test_fps_duration_and_total_frames_match_timeline() -> None:
    source = TIMELINE.read_text(encoding="utf-8")
    timeline_fps = _integer(source, "FPS")
    timeline_duration = _integer(source, "DURATION_SECONDS")

    assert timeline_fps == spec.FPS, (
        "spec.py の FPS と remotion/src/timeline.ts の FPS を一致させてください"
    )
    assert timeline_duration == spec.DURATION_SECONDS, (
        "spec.py の DURATION_SECONDS と timeline.ts を一致させてください"
    )
    assert spec.TOTAL_FRAMES == 480, (
        "R-1 の固定尺は 480f です。spec.py の FPS/尺を戻してください"
    )


def test_all_loop_periods_divide_total_frames() -> None:
    source = TIMELINE.read_text(encoding="utf-8")
    block = re.search(
        r"export const LOOP_PERIODS = \{(?P<body>.*?)\} as const;",
        source,
        re.DOTALL,
    )
    assert block, "timeline.ts の LOOP_PERIODS を読み取れません"
    periods = [
        (name, int(value))
        for name, value in re.findall(
            r"^\s*(\w+):\s*(\d+),", block.group("body"), re.MULTILINE
        )
    ]
    assert periods, "timeline.ts の LOOP_PERIODS が空か形式不一致です"
    invalid = [(name, value) for name, value in periods if 480 % value != 0]

    assert not invalid, (
        "timeline.ts の LOOP_PERIODS は 480 の約数にしてください: "
        f"{invalid}"
    )


def test_cut_boundaries_match_sound_effect_spec() -> None:
    source = TIMELINE.read_text(encoding="utf-8")
    intro_end = _fps_multiple(source, "INTRO_END")
    countdown_step = _fps_multiple(source, "COUNTDOWN_STEP")
    countdown_count = _integer(source, "COUNTDOWN_COUNT")
    countdown_end = intro_end + countdown_step * countdown_count

    assert intro_end == spec.TICK_SECONDS * spec.FPS, (
        "tick 時刻が不一致です。R-1 不変条件に合わせて spec.py または "
        "timeline.ts の INTRO_END を修正してください"
    )
    assert countdown_end == spec.CHIME_SECONDS * spec.FPS, (
        "chime 時刻が不一致です。R-1 不変条件に合わせて spec.py または "
        "timeline.ts の COUNTDOWN_END を修正してください"
    )


def test_review_still_frames_cover_cuts_and_loop_seam() -> None:
    intro_end = int(spec.TICK_SECONDS * spec.FPS)
    countdown_end = int(spec.CHIME_SECONDS * spec.FPS)
    frames = spec.STILL_FRAMES

    assert frames["seam_head"] == 0, "spec.py の seam_head は先頭 0f にしてください"
    assert frames["seam_tail"] == spec.TOTAL_FRAMES - 1, (
        "spec.py の seam_tail は最終フレーム TOTAL_FRAMES - 1 にしてください"
    )
    assert (
        frames["cut1"]
        < intro_end
        <= frames["cut2"]
        < countdown_end
        <= frames["cut3"]
        < spec.TOTAL_FRAMES
    ), "spec.py の cut1/cut2/cut3 を各カット内のフレームへ修正してください"


def test_still_labels_cover_every_still_frame() -> None:
    # review_sheet.py が STILL_FRAMES の順で STILL_LABELS を引くため、
    # キーが欠けると全数レビューの生成が KeyError で落ちる
    assert set(spec.STILL_LABELS) == set(spec.STILL_FRAMES), (
        "spec.py の STILL_LABELS と STILL_FRAMES のキーを一致させてください"
    )
