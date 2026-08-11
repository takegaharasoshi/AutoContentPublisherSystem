"""Remotion props の検査・組み立てロジックのテスト。"""

import copy

import pytest

from build import (
    PropsValidationError,
    build_props,
    resolve_bgm_source,
    validate_props_input,
)
from common import LABELS


CUES_20S = {
    "intro": "導入",
    "teaser": "予想して",
    "r5": "5位、北海道",
    "r4": "4位、青森県",
    "r3": "3位、岩手県",
    "r2": "2位、宮城県",
    "r1_call": "1位は",
    "r1_name": "秋田県",
    "outro": "わかったかな",
}
CUES_30S = {
    "intro": "導入",
    "teaser": "予想して",
    "r5": "5位、北海道",
    "r5_comment": "コメント5",
    "r4": "4位、青森県",
    "r4_comment": "コメント4",
    "r3": "3位、岩手県",
    "r3_comment": "コメント3",
    "r2": "2位、宮城県",
    "r2_comment": "コメント2",
    "r1_call": "1位は",
    "r1_name": "秋田県",
    "closing": "締め",
}


def valid_row() -> dict[str, object]:
    """検査を通る最小のストック行を返す。"""
    return {
        "id": 10,
        "content_key": "001-test",
        "title": "テストランキング",
        "content_fields": {
            "source_display": "出典表示",
            "value_suffix": "円",
            "value_prefix": "年間",
            "subtitle": "全国平均",
            "bg_motif": "背景モチーフ",
        },
        "ranking_data": {
            "entries": [
                {"rank": 5, "pref_code": 1, "value": 50},
                {"rank": 3, "pref_code": 3, "value": 30},
                {"rank": 1, "pref_code": 5, "value": 10},
                {"rank": 4, "pref_code": 2, "value": 40},
                {"rank": 2, "pref_code": 4, "value": 20},
            ]
        },
        "narration": {"20s": CUES_20S, "30s": CUES_30S},
    }


def test_resolve_bgm_source_uses_lru_only_without_existing_id() -> None:
    assert resolve_bgm_source({"video_audio_asset_id": None}, rebuild=False) is None
    assert resolve_bgm_source({"video_audio_asset_id": 7}, rebuild=False) == 7


def test_resolve_bgm_source_keeps_rebuild_behavior() -> None:
    assert resolve_bgm_source({"video_audio_asset_id": 9}, rebuild=True) == 9
    with pytest.raises(ValueError, match="video_audio_asset_id が NULL"):
        resolve_bgm_source({"video_audio_asset_id": None}, rebuild=True)


def test_build_props_resolves_entries_cues_and_assets() -> None:
    props = build_props(
        valid_row(), "20s", background_src="bg/001-test.jpg",
        bgm_src="bgm/music.m4a",
    )

    assert props["duration"] == "20s"
    assert props["backgroundSrc"] == "bg/001-test.jpg"
    assert props["bgmSrc"] == "bgm/music.m4a"
    assert props["labels"] == LABELS
    assert [entry["rank"] for entry in props["entries"]] == [1, 2, 3, 4, 5]
    assert [entry["prefName"] for entry in props["entries"]] == [
        "秋田県", "宮城県", "岩手県", "青森県", "北海道"
    ]
    assert props["cues"]["intro"] == {
        "id": "intro", "text": "導入", "audioSrc": None, "startFrame": 0
    }
    assert list(props["cues"]) == list(CUES_20S)


@pytest.mark.parametrize(
    ("mutate", "message"),
    [
        (
            lambda row: row["ranking_data"]["entries"].__setitem__(
                1, {"rank": 5, "pref_code": 3, "value": 30}
            ),
            "rank は 1〜5",
        ),
        (
            lambda row: row["ranking_data"]["entries"][0].__setitem__("pref_code", 48),
            "pref_code は 1〜47",
        ),
        (
            lambda row: row["narration"]["20s"].pop("teaser"),
            "cue が不一致",
        ),
        (
            lambda row: row["narration"]["20s"].__setitem__("unknown", "余分"),
            "余分: unknown",
        ),
        (
            lambda row: row["content_fields"].pop("source_display"),
            "content_fields.source_display",
        ),
    ],
)
def test_validate_props_input_rejects_defensive_cases(mutate, message: str) -> None:
    row = copy.deepcopy(valid_row())
    mutate(row)

    errors = validate_props_input(row, "20s")

    assert any(message in error for error in errors)
    with pytest.raises(PropsValidationError):
        build_props(row, "20s", background_src="bg/a.jpg", bgm_src=None)
