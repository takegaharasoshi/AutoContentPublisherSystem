"""Tests for the generated Remotion timeline and cue placement."""

from __future__ import annotations

from pathlib import Path
import sys


sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

import build_timeline  # noqa: E402


EXPECTED_CUES = {
    "20s": {
        "intro", "teaser", "r5", "r4", "r3", "r2",
        "r1_call", "r1_name", "outro",
    },
    "30s": {
        "intro", "teaser", "r5", "r5_comment", "r4", "r4_comment",
        "r3", "r3_comment", "r2", "r2_comment", "r1_call", "r1_name",
        "closing",
    },
}


def all_fitting_measures(
    timeline: build_timeline.Timeline,
) -> dict[str, build_timeline.CueMeasure]:
    """Return short valid measures for every cue in a timeline."""
    return {
        anchor.id: build_timeline.CueMeasure(
            frames=20,
            name_offset_frames=10 if anchor.align == "name" else None,
        )
        for anchor in timeline.cue_anchors
    }


def violation_kinds(result: build_timeline.ResolvedCues, cue_id: str) -> set[str]:
    """Return violation kinds emitted for one cue ID."""
    return {item.kind for item in result.violations if item.id == cue_id}


def cue_anchor(
    timeline: build_timeline.Timeline, cue_id: str
) -> build_timeline.CueAnchor:
    """Return one narration cue anchor by ID."""
    return next(anchor for anchor in timeline.cue_anchors if anchor.id == cue_id)


def test_timelines_fill_each_duration_without_gaps_or_overlaps() -> None:
    """Every derived scene is contiguous and ends at the requested duration."""
    timelines = build_timeline.build_timelines()
    assert timelines["20s"].total == 600
    assert timelines["30s"].total == 900

    for duration, timeline in timelines.items():
        spec = build_timeline.DURATION_SPECS[duration]
        assert timeline.teaser_at == spec.intro
        assert timeline.rounds[5].start == timeline.teaser_at + spec.teaser
        for rank in (5, 4, 3):
            assert timeline.rounds[rank].end == timeline.rounds[rank - 1].start
        assert timeline.rounds[2].end == timeline.rounds[1].start
        assert timeline.rounds[1].end == timeline.closing_at
        assert timeline.total - timeline.rounds[1].end == spec.recap + spec.closing
        if spec.recap:
            assert timeline.recap_at == timeline.rounds[1].end
            assert timeline.closing_at == timeline.recap_at
        else:
            assert timeline.recap_at is None


def test_20s_keeps_the_fixed_17_4d_spacing_values() -> None:
    """17-4dで順位間の間を空けるため見直した20秒尺配分を固定する。"""
    timeline = build_timeline.build_timelines()["20s"]
    assert timeline.teaser_at == 70
    assert timeline.closing_at == 542
    assert timeline.rounds[5].stop == 164
    assert timeline.rounds[5].row_at == 186
    assert timeline.rounds[1].start == 422
    assert timeline.rounds[1].stop == 494
    assert timeline.rounds[1].row_at == 552


def test_cue_anchor_ids_and_budgets_match_narration_stock() -> None:
    """Each duration exposes exactly its stock narration keys in time order."""
    for duration, timeline in build_timeline.build_timelines().items():
        anchors = timeline.cue_anchors
        assert len(anchors) == len(EXPECTED_CUES[duration])
        assert {anchor.id for anchor in anchors} == EXPECTED_CUES[duration]
        assert all(anchor.budget_start < anchor.budget_end for anchor in anchors)
        assert all(
            current.budget_end <= following.budget_start
            for current, following in zip(anchors, anchors[1:])
        )


def test_resolve_cues_fits_budget_and_aligns_name_to_stop() -> None:
    """A name-aligned cue places its measured prefecture name at the flash."""
    timeline = build_timeline.build_timelines()["20s"]
    result = build_timeline.resolve_cue_frames(
        timeline, all_fitting_measures(timeline)
    )
    teaser = cue_anchor(timeline, "teaser")
    r5 = cue_anchor(timeline, "r5")
    r4 = cue_anchor(timeline, "r4")
    measures = all_fitting_measures(timeline)
    r5_name_offset = measures["r5"].name_offset_frames
    r4_name_offset = measures["r4"].name_offset_frames
    assert r5_name_offset is not None
    assert r4_name_offset is not None
    expected_start = r5.anchor - r5_name_offset
    assert result.ok
    assert result.cues["r5"].start_frame == expected_start
    assert result.cues["r5"].head_slack == (
        expected_start
        - (teaser.anchor + measures["teaser"].frames + build_timeline.MIN_GAP_FRAMES)
    )
    assert result.cues["r5"].tail_slack == (
        r4.anchor
        - r4_name_offset
        - build_timeline.MIN_GAP_FRAMES
        - (expected_start + measures["r5"].frames)
    )
    assert result.cues["r5"].name_lag_frames == 0


def test_name_aligned_cue_moves_later_within_name_lag_limit() -> None:
    """A name cue moves after the preceding cue while keeping an allowed lag."""
    timeline = build_timeline.build_timelines()["20s"]
    measures = all_fitting_measures(timeline)
    teaser = cue_anchor(timeline, "teaser")
    r5 = cue_anchor(timeline, "r5")
    name_offset = 30
    intended_name_lag = 5
    measures["teaser"] = build_timeline.CueMeasure(
        frames=(
            r5.anchor
            - name_offset
            + intended_name_lag
            - teaser.anchor
            - build_timeline.MIN_GAP_FRAMES
        )
    )
    measures["r5"] = build_timeline.CueMeasure(
        frames=20, name_offset_frames=name_offset
    )
    result = build_timeline.resolve_cue_frames(timeline, measures)
    assert result.ok
    assert result.cues["r5"].start_frame == (
        r5.anchor - name_offset + intended_name_lag
    )
    assert result.cues["r5"].head_slack == 0
    assert result.cues["r5"].name_lag_frames == intended_name_lag


def test_name_aligned_cue_reports_head_overrun_beyond_lag_limit() -> None:
    """A name cue reports overlap when the allowed lag cannot reach the lower bound."""
    timeline = build_timeline.build_timelines()["20s"]
    measures = all_fitting_measures(timeline)
    teaser = cue_anchor(timeline, "teaser")
    r5 = cue_anchor(timeline, "r5")
    name_offset = 30
    intended_overrun = 2
    latest_start = r5.anchor + build_timeline.NAME_LAG_MAX_FRAMES - name_offset
    measures["teaser"] = build_timeline.CueMeasure(
        frames=(
            latest_start
            + intended_overrun
            - teaser.anchor
            - build_timeline.MIN_GAP_FRAMES
        )
    )
    measures["r5"] = build_timeline.CueMeasure(
        frames=20, name_offset_frames=name_offset
    )
    result = build_timeline.resolve_cue_frames(timeline, measures)
    assert result.cues["r5"].start_frame == latest_start
    assert result.cues["r5"].name_lag_frames == build_timeline.NAME_LAG_MAX_FRAMES
    assert result.cues["r5"].head_slack == -intended_overrun
    assert "head_overrun" in violation_kinds(result, "r5")
    assert f"{intended_overrun} フレーム" in next(
        item.message
        for item in result.violations
        if item.id == "r5" and item.kind == "head_overrun"
    )


def test_head_aligned_cue_stays_fixed_and_reports_head_overrun() -> None:
    """A head cue never moves away from its fixed anchor."""
    timeline = build_timeline.build_timelines()["20s"]
    measures = all_fitting_measures(timeline)
    intro = cue_anchor(timeline, "intro")
    teaser = cue_anchor(timeline, "teaser")
    intended_overrun = 2
    measures["intro"] = build_timeline.CueMeasure(
        frames=(
            teaser.anchor
            + intended_overrun
            - intro.anchor
            - build_timeline.MIN_GAP_FRAMES
        )
    )
    result = build_timeline.resolve_cue_frames(timeline, measures)
    assert result.cues["teaser"].start_frame == timeline.teaser_at
    assert result.cues["teaser"].head_slack == -intended_overrun
    assert "head_overrun" in violation_kinds(result, "teaser")


def test_resolve_cues_reports_tail_overrun_at_timeline_end() -> None:
    """Audio crossing the total duration is reported as a tail overrun."""
    timeline = build_timeline.build_timelines()["20s"]
    measures = all_fitting_measures(timeline)
    outro = cue_anchor(timeline, "outro")
    intended_overrun = 1
    measures["outro"] = build_timeline.CueMeasure(
        frames=timeline.total - outro.anchor + intended_overrun
    )
    result = build_timeline.resolve_cue_frames(timeline, measures)
    assert "tail_overrun" in violation_kinds(result, "outro")
    assert result.cues["outro"].tail_slack == -intended_overrun


def test_resolve_cues_uses_each_resolved_end_for_the_next_lower_bound() -> None:
    """Sequential name cues use the preceding cue's adjusted placement."""
    timeline = build_timeline.build_timelines()["20s"]
    measures = all_fitting_measures(timeline)
    teaser = cue_anchor(timeline, "teaser")
    r5 = cue_anchor(timeline, "r5")
    r4 = cue_anchor(timeline, "r4")
    r5_name_offset = 30
    r4_name_offset = 35
    r5_name_lag = 5
    r4_name_lag = 2
    r5_start = r5.anchor - r5_name_offset + r5_name_lag
    r4_start = r4.anchor - r4_name_offset + r4_name_lag
    measures["teaser"] = build_timeline.CueMeasure(
        frames=r5_start - teaser.anchor - build_timeline.MIN_GAP_FRAMES
    )
    measures["r5"] = build_timeline.CueMeasure(
        frames=r4_start - r5_start - build_timeline.MIN_GAP_FRAMES,
        name_offset_frames=r5_name_offset,
    )
    measures["r4"] = build_timeline.CueMeasure(
        frames=20, name_offset_frames=r4_name_offset
    )
    result = build_timeline.resolve_cue_frames(timeline, measures)
    assert result.ok
    assert result.cues["r5"].start_frame == r5_start
    assert result.cues["r4"].start_frame == (
        result.cues["r5"].start_frame
        + measures["r5"].frames
        + build_timeline.MIN_GAP_FRAMES
    )
    assert result.cues["r4"].start_frame == r4_start
    assert result.cues["r4"].name_lag_frames == r4_name_lag


def test_resolve_cues_collects_missing_unknown_and_name_offset_errors() -> None:
    """All input errors are collected and every known cue still resolves."""
    timeline = build_timeline.build_timelines()["20s"]
    measures = all_fitting_measures(timeline)
    del measures["intro"]
    measures["r5"] = build_timeline.CueMeasure(frames=20)
    measures["not_in_stock"] = build_timeline.CueMeasure(frames=10)

    result = build_timeline.resolve_cue_frames(timeline, measures)

    assert not result.ok
    assert "missing" in violation_kinds(result, "intro")
    assert "unknown" in violation_kinds(result, "not_in_stock")
    assert "missing_name_offset" in violation_kinds(result, "r5")
    assert set(result.cues) == EXPECTED_CUES["20s"]
    assert result.cues["r5"].start_frame == timeline.rounds[5].stop


def test_generated_timeline_json_is_current() -> None:
    """The checked-in JSON exactly matches the Python single source."""
    assert build_timeline.check_output()
