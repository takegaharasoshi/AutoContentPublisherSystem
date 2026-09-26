"""props・ナレーション予算・BGM 割当・継ぎ目差分のテスト。"""

from __future__ import annotations

import json
from pathlib import Path

from PIL import Image
import pytest

import build
from build import (
    NarrationBudgetError,
    build_props,
    seam_mean_diff,
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


def test_build_props_matches_schema_shape() -> None:
    props = build_props(
        _item(), {"master": {"name": "父"}, "jr": {"name": "子"}},
        _report(), _tracks()[0],
    )

    assert props["contentKey"] == "001-test"
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


def test_seam_mean_diff(tmp_path: Path) -> None:
    first = tmp_path / "first.png"
    last = tmp_path / "last.png"
    Image.new("RGB", (4, 4), (10, 20, 30)).save(first)
    Image.new("RGB", (4, 4), (13, 23, 33)).save(last)

    assert seam_mean_diff(first, last) == pytest.approx(3.0)


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
        {}, {}, 0.1,
    )
    assert record["narration"]["problem_sec"] == 10.123
    assert record["narration"]["tempo"] == 1.146
    assert record["narration"]["engine_id"] == "gemini/gemini-3.8-flash-tts/voice-test"
