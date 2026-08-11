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


def test_20s_keeps_the_fixed_17_4a_b_values() -> None:
    """The generated 20-second timeline remains identical to the fixed mock."""
    timeline = build_timeline.build_timelines()["20s"]
    assert timeline.teaser_at == 75
    assert timeline.closing_at == 510
    assert timeline.rounds[5].stop == 165
    assert timeline.rounds[5].row_at == 187
    assert timeline.rounds[1].start == 375
    assert timeline.rounds[1].stop == 450
    assert timeline.rounds[1].row_at == 508


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
    assert result.ok
    assert result.cues["r5"].start_frame == timeline.rounds[5].stop - 10
    assert result.cues["r5"].head_slack == 58
    assert result.cues["r5"].tail_slack == 38
    assert result.cues["r5"].name_lag_frames == 0


def test_name_aligned_cue_moves_later_within_name_lag_limit() -> None:
    """A name cue moves after the preceding cue while keeping an allowed lag."""
    timeline = build_timeline.build_timelines()["20s"]
    measures = all_fitting_measures(timeline)
    measures["teaser"] = build_timeline.CueMeasure(frames=63)
    measures["r5"] = build_timeline.CueMeasure(
        frames=20, name_offset_frames=30
    )
    result = build_timeline.resolve_cue_frames(timeline, measures)
    assert result.ok
    assert result.cues["r5"].start_frame == 140
    assert result.cues["r5"].head_slack == 0
    assert result.cues["r5"].name_lag_frames == 5


def test_name_aligned_cue_reports_head_overrun_beyond_lag_limit() -> None:
    """A name cue reports overlap when the allowed lag cannot reach the lower bound."""
    timeline = build_timeline.build_timelines()["20s"]
    measures = all_fitting_measures(timeline)
    measures["teaser"] = build_timeline.CueMeasure(frames=68)
    measures["r5"] = build_timeline.CueMeasure(frames=20, name_offset_frames=30)
    result = build_timeline.resolve_cue_frames(timeline, measures)
    assert result.cues["r5"].start_frame == 143
    assert result.cues["r5"].name_lag_frames == 8
    assert "head_overrun" in violation_kinds(result, "r5")
    assert "2 フレーム" in next(
        item.message
        for item in result.violations
        if item.id == "r5" and item.kind == "head_overrun"
    )


def test_head_aligned_cue_stays_fixed_and_reports_head_overrun() -> None:
    """A head cue never moves away from its fixed anchor."""
    timeline = build_timeline.build_timelines()["20s"]
    measures = all_fitting_measures(timeline)
    measures["intro"] = build_timeline.CueMeasure(frames=75)
    result = build_timeline.resolve_cue_frames(timeline, measures)
    assert result.cues["teaser"].start_frame == timeline.teaser_at
    assert result.cues["teaser"].head_slack == -2
    assert "head_overrun" in violation_kinds(result, "teaser")


def test_resolve_cues_reports_tail_overrun_at_timeline_end() -> None:
    """Audio crossing the total duration is reported as a tail overrun."""
    timeline = build_timeline.build_timelines()["20s"]
    measures = all_fitting_measures(timeline)
    measures["outro"] = build_timeline.CueMeasure(frames=91)
    result = build_timeline.resolve_cue_frames(timeline, measures)
    assert "tail_overrun" in violation_kinds(result, "outro")
    assert result.cues["outro"].tail_slack == -1


def test_resolve_cues_uses_each_resolved_end_for_the_next_lower_bound() -> None:
    """Sequential name cues use the preceding cue's adjusted placement."""
    timeline = build_timeline.build_timelines()["20s"]
    measures = all_fitting_measures(timeline)
    measures["teaser"] = build_timeline.CueMeasure(frames=63)
    measures["r5"] = build_timeline.CueMeasure(frames=50, name_offset_frames=30)
    measures["r4"] = build_timeline.CueMeasure(frames=20, name_offset_frames=35)
    result = build_timeline.resolve_cue_frames(timeline, measures)
    assert result.ok
    assert result.cues["r5"].start_frame == 140
    assert result.cues["r4"].start_frame == 192
    assert result.cues["r4"].name_lag_frames == 2


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
