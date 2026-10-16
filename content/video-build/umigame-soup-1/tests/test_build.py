"""props・ナレーション予算・BGM 割当・導入シーンの固定コピーのテスト。"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

import build
from build import (
    NarrationBudgetError,
    build_props,
    opening_props,
    timeline_summary,
    select_bgm_track,
    validate_narration_budget,
)


def _item() -> dict:
    return {
        "content_key": "001-test",
        "hook": "フック",
        "problem_text": "問題文",
        "rule_text": "ルール",
        "character_lines": {
            "master": {"intro": "質問して", "outro": "コメントして"},
            "jr": {"outro": "フォローして"},
        },
        "play_example": [
            {"role": "questioner", "text": "質問1"},
            {"role": "master", "text": "いいえ"},
            {"role": "questioner", "text": "質問2"},
            {"role": "master", "text": "はい"},
            {"role": "questioner", "text": "質問3"},
            {"role": "master", "text": "関係ない"},
        ],
    }


def _report(problem: float = 10.0, rule: float = 5.0) -> dict:
    return {
        "cues": {
            "problem": {"seconds": problem, "frames": round(problem * 30)},
            "rule": {"seconds": rule, "frames": round(rule * 30)},
        }
    }


def _tracks() -> list[dict]:
    return [
        {"output": "track01.m4a", "s3_key": "audio/u/track01.m4a", "provisional": False},
        {"output": "track02.m4a", "s3_key": "audio/u/track02.m4a", "provisional": True},
    ]


def _design() -> dict:
    return {
        "master": {"name": "父"},
        "jr": {"name": "子"},
        "opening": {
            "badge": "新体験",
            "headline": ["見出し"],
            "lead": [[{"text": "謎の"}, {"text": "真相", "em": "accent"}], [{"text": "質問", "em": "tag"}]],
            "hook_label": "今日の謎",
            "narration": {"text": "みだし", "seconds": 2.2, "max_seconds": 2.5},
            "self_intro": {"master": "父です", "jr": "子です"},
        },
    }


def test_build_props_matches_schema_shape() -> None:
    props = build_props(_item(), _design(), _report(), _tracks()[0])

    assert props["contentKey"] == "001-test"
    assert props["opening"]["badge"] == "新体験"
    assert props["opening"]["lead"][0][1] == {"text": "真相", "em": "accent"}
    assert props["opening"]["selfIntro"] == {"master": "父です", "jr": "子です"}
    assert props["opening"]["hookLabel"] == "今日の謎"
    assert props["narration"]["opening"] == {"file": "narration/_opening/line.wav", "frames": 75}
    with_frames = build_props(_item(), _design(), _report(), _tracks()[0], opening_frames=65)
    assert with_frames["narration"]["opening"]["frames"] == 65
    assert props["master"] == {
        "name": "父", "base": "char/master_base.png", "happy": "char/master_happy.png"
    }
    assert props["jr"]["name"] == "子"
    assert len(props["playExample"]) == 6
    assert props["narration"]["rule"]["frames"] == 150
    assert props["bgm"] == "audio/bgm/track01.m4a"


def test_narration_budget_rejects_overage() -> None:
    assert validate_narration_budget(_report(10, 9))["total_sec"] == pytest.approx(20.2)
    with pytest.raises(NarrationBudgetError, match="予算超過"):
        validate_narration_budget(_report(12, 8))


def test_bgm_assignment_keeps_existing_and_uses_least_count() -> None:
    tracks = _tracks()
    manifest = {
        "001-a": {"bgm": {"track": "track01.m4a"}},
        "002-b": {"bgm": {"track": "track01.m4a"}},
        "003-c": {"bgm": {"track": "track02.m4a"}},
    }

    assert select_bgm_track(manifest, "001-a", tracks)["output"] == "track01.m4a"
    assert select_bgm_track(manifest, "004-d", tracks)["output"] == "track02.m4a"
    assert select_bgm_track({}, "004-d", tracks)["output"] == "track01.m4a"


def test_no_tts_preflight_reports_background_and_narration(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setattr(build, "WORK", tmp_path)

    errors = build._preflight_inputs(
        [{"content_key": "001-test"}], no_tts=True
    )

    assert any("背景 JPEG がありません" in error for error in errors)
    assert any("ナレーション未合成です" in error for error in errors)


def test_no_tts_rejects_cached_gemini_over_tempo(tmp_path: Path) -> None:
    for name in ("problem.wav", "rule.wav"):
        (tmp_path / name).write_bytes(b"wav")
    (tmp_path / "narration.json").write_text(json.dumps({
        "texts": {"problem": "問題", "rule": "ルール"},
        "engine_id": "gemini/model/voice", "tempo": 1.2,
    }), encoding="utf-8")
    with pytest.raises(build.narration_gemini.TempoLimitError):
        build._load_cached_narration(
            {"narration": {"problem": "問題", "rule": "ルール"}}, tmp_path
        )


def test_opening_props_rejects_unknown_emphasis() -> None:
    design = _design()
    design["opening"]["lead"][0][0]["em"] = "bold"
    with pytest.raises(ValueError, match="accent / tag"):
        opening_props(design)


def test_opening_props_requires_self_intro() -> None:
    design = _design()
    del design["opening"]["self_intro"]
    with pytest.raises(ValueError, match="self_intro"):
        opening_props(design)


def test_repo_design_opening_is_valid() -> None:
    design = json.loads((build.ASSETS_DIR / "design.json").read_text(encoding="utf-8"))
    opening = opening_props(design)
    assert opening["badge"] == "新体験"
    assert opening["headline"] == ["コメントで紐解く！", "推理ゲーム"]


def test_timeline_summary_places_narration_after_opening() -> None:
    summary = timeline_summary(_report(10.0, 5.0), 65)
    assert summary["narration_opening_start"] == 6
    assert summary["narration_opening_end"] == 71
    assert summary["opening_end"] == 150
    assert summary["main_fully_visible"] == 158
    assert summary["narration_problem_start"] == 165
    assert summary["narration_rule_start"] == 165 + 300 + 36
    assert summary["narration_end"] == 165 + 300 + 36 + 150
    assert summary["narration_end"] <= summary["total_frames"]


def test_validate_probe_accepts_new_duration_and_rejects_old() -> None:
    probe = {"width": 1080, "height": 1920, "fps": 30, "duration": 29.02, "audio_codec": "aac"}
    assert build.validate_probe(probe) == []
    assert any("尺が" in error for error in build.validate_probe({**probe, "duration": 24.0}))


def test_manifest_narration_keeps_engine_and_tempo(
    tmp_path: Path, monkeypatch
) -> None:
    monkeypatch.setattr(build, "WORK", tmp_path)
    record = build._record(
        {"content_key": "001-test", "title": "テスト"},
        tmp_path / "props.json", tmp_path / "video.mp4",
        _tracks()[0],
        {
            "problem_sec": 10.12345,
            "rule_sec": 5.0,
            "total_sec": 16.32345,
            "tempo": 1.146,
            "engine_id": "gemini/gemini-3.8-flash-tts/voice-test",
        },
        {}, {}, timeline_summary(_report()),
    )
    assert record["narration"]["problem_sec"] == 10.123
    assert record["narration"]["tempo"] == 1.146
    assert record["narration"]["engine_id"] == "gemini/gemini-3.8-flash-tts/voice-test"
    assert record["timeline"]["narration_problem_start"] == 165
    assert "seam_mean_diff" not in record
