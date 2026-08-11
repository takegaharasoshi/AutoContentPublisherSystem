"""尺別タイムラインを導出し、Remotion 用 JSON を生成する。

このファイルの ``DURATION_SPECS`` がタイムライン定数の単一ソースである。
TypeScript 側は生成物 ``src/timeline.json`` を読み込み、数値を二重管理しない。
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass, replace
import difflib
import json
from pathlib import Path
import sys
from typing import Literal, Mapping


PROJECT_DIR = Path(__file__).resolve().parent.parent
OUTPUT_PATH = PROJECT_DIR / "src" / "timeline.json"
MIN_GAP_FRAMES = 2
NAME_LAG_MAX_FRAMES = 8


@dataclass(frozen=True)
class DurationSpec:
    """タイムラインの全フレームを導出するためのコンパクトな尺仕様。"""

    fps: int
    intro: int
    teaser: int
    round_spin: int
    round_reveal: int
    round_comment: int
    first_hold: int
    first_reveal: int
    recap: int
    closing: int
    fly_delay: int
    fly_dur: int
    first_fly_delay: int
    first_fly_dur: int


DURATION_SPECS: dict[str, DurationSpec] = {
    "20s": DurationSpec(
        fps=30,
        intro=67,
        teaser=67,
        round_spin=30,
        round_reveal=42,
        round_comment=0,
        first_hold=72,
        first_reveal=45,
        recap=0,
        closing=61,
        fly_delay=8,
        fly_dur=16,
        first_fly_delay=42,
        first_fly_dur=18,
    ),
    "30s": DurationSpec(
        fps=30,
        intro=91,
        teaser=61,
        round_spin=30,
        round_reveal=33,
        round_comment=57,
        first_hold=90,
        first_reveal=60,
        recap=75,
        closing=43,
        fly_delay=8,
        fly_dur=16,
        first_fly_delay=42,
        first_fly_dur=18,
    ),
}


@dataclass(frozen=True)
class RoundTiming:
    """1 順位分のタイミング。"""

    start: int
    spin: int
    stop: int
    fly_start: int
    fly_dur: int
    row_at: int
    comment_at: int | None
    end: int


@dataclass(frozen=True)
class CueAnchor:
    """音声 cue の配置アンカーと参考用のシーン区間。"""

    id: str
    align: Literal["head", "name"]
    anchor: int
    budget_start: int
    budget_end: int


@dataclass(frozen=True)
class Timeline:
    """コンパクトな尺仕様から導出したタイムライン。"""

    duration: str
    fps: int
    total: int
    teaser_at: int
    recap_at: int | None
    closing_at: int
    rounds: dict[int, RoundTiming]
    cue_anchors: list[CueAnchor]


@dataclass(frozen=True)
class CueMeasure:
    """合成音声の実測値。"""

    frames: int
    name_offset_frames: int | None = None


@dataclass(frozen=True)
class ResolvedCue:
    """アンカーに対して配置済みの cue。"""

    id: str
    start_frame: int
    frames: int
    budget_start: int
    budget_end: int
    align: str
    head_slack: int
    tail_slack: int
    name_lag_frames: int


@dataclass(frozen=True)
class CueViolation:
    """cue の不足・未知 ID・隣接 cue または尺との競合。"""

    id: str
    kind: str
    message: str


@dataclass(frozen=True)
class ResolvedCues:
    """尺内の全 cue の解決結果と、まとめて表示可能な違反一覧。"""

    duration: str
    cues: dict[str, ResolvedCue]
    violations: list[CueViolation]

    @property
    def ok(self) -> bool:
        """違反が一件もないときだけ真を返す。"""
        return not self.violations


def build_timeline(duration: str, spec: DurationSpec) -> Timeline:
    """コンパクトな尺仕様から全タイミングを導出する。"""
    round_len = spec.round_spin + spec.round_reveal + spec.round_comment
    first_round_start = spec.intro + spec.teaser
    rounds: dict[int, RoundTiming] = {}

    for rank in (5, 4, 3, 2):
        index = 5 - rank
        start = first_round_start + index * round_len
        stop = start + spec.round_spin
        fly_start = stop + spec.fly_delay
        comment_at = (
            start + spec.round_spin + spec.round_reveal
            if spec.round_comment
            else None
        )
        rounds[rank] = RoundTiming(
            start=start,
            spin=spec.round_spin,
            stop=stop,
            fly_start=fly_start,
            fly_dur=spec.fly_dur,
            row_at=fly_start + spec.fly_dur - 2,
            comment_at=comment_at,
            end=start + round_len,
        )

    start = first_round_start + 4 * round_len
    stop = start + spec.first_hold
    fly_start = stop + spec.first_fly_delay
    rounds[1] = RoundTiming(
        start=start,
        spin=spec.first_hold,
        stop=stop,
        fly_start=fly_start,
        fly_dur=spec.first_fly_dur,
        row_at=fly_start + spec.first_fly_dur - 2,
        comment_at=None,
        end=start + spec.first_hold + spec.first_reveal,
    )

    recap_at = rounds[1].end if spec.recap else None
    closing_at = recap_at if recap_at is not None else rounds[1].end
    timeline = Timeline(
        duration=duration,
        fps=spec.fps,
        total=rounds[1].end + spec.recap + spec.closing,
        teaser_at=spec.intro,
        recap_at=recap_at,
        closing_at=closing_at,
        rounds=rounds,
        cue_anchors=[],
    )
    return replace(timeline, cue_anchors=cue_anchors(timeline))


def cue_anchors(timeline: Timeline) -> list[CueAnchor]:
    """尺に存在するナレーション cue のアンカー表を時系列で返す。"""
    anchors = [
        CueAnchor("intro", "head", 0, 0, timeline.teaser_at),
        CueAnchor(
            "teaser",
            "head",
            timeline.teaser_at,
            timeline.teaser_at,
            timeline.rounds[5].start,
        ),
    ]
    for rank in (5, 4, 3, 2):
        timing = timeline.rounds[rank]
        anchors.append(
            CueAnchor(
                f"r{rank}",
                "name",
                timing.stop,
                timing.start,
                timing.end if timing.comment_at is None else timing.comment_at,
            )
        )
        if timing.comment_at is not None:
            anchors.append(
                CueAnchor(
                    f"r{rank}_comment",
                    "head",
                    timing.comment_at,
                    timing.comment_at,
                    timing.end,
                )
            )
    first = timeline.rounds[1]
    anchors.extend(
        [
            CueAnchor("r1_call", "head", first.start, first.start, first.stop),
            CueAnchor("r1_name", "head", first.stop, first.stop, first.end),
        ]
    )
    final_id = "closing" if timeline.recap_at is not None else "outro"
    anchors.append(
        CueAnchor(
            final_id,
            "head",
            timeline.closing_at,
            timeline.closing_at,
            timeline.total,
        )
    )
    return anchors


def _tail_overrun_message(frames: int, fps: int) -> str:
    seconds = frames / fps
    return (
        f"cue の終端が次の cue に必要な無音区間を {frames} フレーム"
        f"（{seconds:.2f} 秒）超過しています。"
        "セリフを短くするか、話速を上げてください。"
    )


def _head_overrun_message(frames: int, fps: int) -> str:
    seconds = frames / fps
    return (
        f"直前 cue と重なり、必要な間隔まで {frames} フレーム"
        f"（{seconds:.2f} 秒）不足しています。"
        "対処: 呼び込みを短くする / 話速を上げる。"
    )


def resolve_cue_frames(
    timeline: Timeline,
    measures: Mapping[str, CueMeasure],
    *,
    min_gap_frames: int = MIN_GAP_FRAMES,
    name_lag_max_frames: int = NAME_LAG_MAX_FRAMES,
) -> ResolvedCues:
    """実測音声を時系列に配置し、隣接 cue との全違反を返す。"""
    ordered_anchors = sorted(timeline.cue_anchors, key=lambda item: item.anchor)
    anchors = {anchor.id: anchor for anchor in ordered_anchors}
    violations: list[CueViolation] = []
    resolved: dict[str, ResolvedCue] = {}

    for cue_id in sorted(measures.keys() - anchors.keys()):
        violations.append(
            CueViolation(
                cue_id,
                "unknown",
                f"未知の cue ID「{cue_id}」です。尺 {timeline.duration} の原稿から削除してください。",
            )
        )

    previous_end: int | None = None
    for anchor in ordered_anchors:
        cue_id = anchor.id
        measure = measures.get(cue_id)
        if measure is None:
            violations.append(
                CueViolation(
                    cue_id,
                    "missing",
                    f"cue「{cue_id}」の実測長がありません。音声を合成して計測値を渡してください。",
                )
            )
            # 全アンカーの解決結果を返すため、欠落 cue は長さ 0 で仮配置する。
            measure = CueMeasure(frames=0, name_offset_frames=0)

        lower_bound = 0 if previous_end is None else previous_end + min_gap_frames
        if anchor.align == "name":
            if measure.name_offset_frames is None:
                violations.append(
                    CueViolation(
                        cue_id,
                        "missing_name_offset",
                        f"後ろ合わせ cue「{cue_id}」に県名開始位置がありません。音声を再計測してください。",
                    )
                )
                name_offset = 0
            else:
                name_offset = measure.name_offset_frames
            desired_start = anchor.anchor - name_offset
            latest_start = anchor.anchor + name_lag_max_frames - name_offset
            if desired_start < lower_bound:
                start_frame = min(lower_bound, latest_start)
                if start_frame < lower_bound:
                    violations.append(
                        CueViolation(
                            cue_id,
                            "head_overrun",
                            _head_overrun_message(
                                lower_bound - start_frame, timeline.fps
                            ),
                        )
                    )
            else:
                start_frame = desired_start
            name_lag_frames = start_frame + name_offset - anchor.anchor
        else:
            start_frame = anchor.anchor
            name_lag_frames = 0
            if start_frame < lower_bound:
                violations.append(
                    CueViolation(
                        cue_id,
                        "head_overrun",
                        _head_overrun_message(lower_bound - start_frame, timeline.fps),
                    )
                )

        head_slack = start_frame - lower_bound
        resolved[cue_id] = ResolvedCue(
            id=cue_id,
            start_frame=start_frame,
            frames=measure.frames,
            budget_start=anchor.budget_start,
            budget_end=anchor.budget_end,
            align=anchor.align,
            head_slack=head_slack,
            tail_slack=0,
            name_lag_frames=name_lag_frames,
        )
        previous_end = start_frame + measure.frames

    for index, anchor in enumerate(ordered_anchors):
        cue = resolved[anchor.id]
        if index + 1 < len(ordered_anchors):
            upper_bound = resolved[ordered_anchors[index + 1].id].start_frame - min_gap_frames
        else:
            upper_bound = timeline.total
        tail_slack = upper_bound - (cue.start_frame + cue.frames)
        resolved[anchor.id] = replace(cue, tail_slack=tail_slack)
        if tail_slack < 0:
            violations.append(
                CueViolation(
                    anchor.id,
                    "tail_overrun",
                    _tail_overrun_message(-tail_slack, timeline.fps),
                )
            )

    return ResolvedCues(timeline.duration, resolved, violations)


def build_timelines() -> dict[str, Timeline]:
    """全尺を導出し、仕様上の総尺を検査する。"""
    timelines = {
        duration: build_timeline(duration, spec)
        for duration, spec in DURATION_SPECS.items()
    }
    assert timelines["20s"].total == 600
    assert timelines["30s"].total == 900
    return timelines


def _round_json(timing: RoundTiming) -> dict[str, int | None]:
    return {
        "start": timing.start,
        "spin": timing.spin,
        "stop": timing.stop,
        "flyStart": timing.fly_start,
        "flyDur": timing.fly_dur,
        "rowAt": timing.row_at,
        "commentAt": timing.comment_at,
        "end": timing.end,
    }


def _anchor_json(anchor: CueAnchor) -> dict[str, str | int]:
    return {
        "id": anchor.id,
        "align": anchor.align,
        "anchor": anchor.anchor,
        "budgetStart": anchor.budget_start,
        "budgetEnd": anchor.budget_end,
    }


def timeline_document() -> dict[str, object]:
    """TypeScript が読む camelCase の JSON オブジェクトを返す。"""
    durations: dict[str, object] = {}
    for duration, timeline in build_timelines().items():
        durations[duration] = {
            "duration": timeline.duration,
            "fps": timeline.fps,
            "total": timeline.total,
            "teaserAt": timeline.teaser_at,
            "recapAt": timeline.recap_at,
            "closingAt": timeline.closing_at,
            "rounds": {
                str(rank): _round_json(timeline.rounds[rank])
                for rank in (1, 2, 3, 4, 5)
            },
            "cueAnchors": [_anchor_json(anchor) for anchor in timeline.cue_anchors],
        }
    return {
        "_comment": "生成物。scripts/build_timeline.py が正。手で編集しない",
        "durations": durations,
    }


def rendered_json() -> str:
    """安定した整形の生成物本文を返す。"""
    return json.dumps(timeline_document(), ensure_ascii=False, indent=2) + "\n"


def check_output(path: Path = OUTPUT_PATH) -> bool:
    """現在の生成物が最新なら真を返す。"""
    expected = rendered_json()
    try:
        actual = path.read_text(encoding="utf-8")
    except FileNotFoundError:
        print(f"生成物がありません: {path}", file=sys.stderr)
        return False
    if actual == expected:
        return True
    diff = difflib.unified_diff(
        actual.splitlines(),
        expected.splitlines(),
        fromfile=str(path),
        tofile="scripts/build_timeline.py からの期待値",
        n=2,
    )
    print("timeline.json が最新ではありません。差分:", file=sys.stderr)
    for line in list(diff)[:40]:
        print(line, file=sys.stderr)
    return False


def main(argv: list[str] | None = None) -> int:
    """JSON を生成するか、``--check`` で鮮度を検査する。"""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="生成物が最新か検査")
    args = parser.parse_args(argv)
    if args.check:
        return 0 if check_output() else 1
    OUTPUT_PATH.write_text(rendered_json(), encoding="utf-8")
    print(f"generated {OUTPUT_PATH.relative_to(PROJECT_DIR)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
