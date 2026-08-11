"""レビュー HTML の出力テスト。"""

import json
from pathlib import Path

from review_sheet import generate_review_html


def _props(source: str, cue_text: str) -> dict[str, object]:
    return {
        "subtitle": "<全国平均>",
        "sourceDisplay": source,
        "valuePrefix": "年間",
        "valueSuffix": "円",
        "entries": [{"rank": 1, "prefName": "宮崎県", "value": 1234}],
        "cues": {"intro": {"text": cue_text}},
    }


def test_review_html_escapes_values_and_contains_both_durations(tmp_path: Path) -> None:
    props_dir = tmp_path / "work" / "props"
    props_dir.mkdir(parents=True)
    for duration in ("20s", "30s"):
        (props_dir / f"001-{duration}.json").write_text(
            json.dumps(_props("A&B <出典>", '<script>alert("x")</script>')),
            encoding="utf-8",
        )
    manifest = {
        "001-unsafe": {
            "title": "<危険&タイトル>",
            "audio_asset_id": 3,
            "bgm_s3_key": "audio/&music.m4a",
            "durations": {
                "20s": {
                    "video": "work/videos/001_20s.mp4",
                    "props": "work/props/001-20s.json",
                    "loudness_i": -15.0,
                    "loudness_tp": -1.1,
                },
                "30s": {
                    "video": "work/videos/001_30s.mp4",
                    "props": "work/props/001-30s.json",
                    "loudness_i": -14.9,
                    "loudness_tp": -1.2,
                },
            },
        }
    }

    html = generate_review_html(manifest, base=tmp_path)

    assert "001_20s.mp4" in html
    assert "001_30s.mp4" in html
    assert "&lt;危険&amp;タイトル&gt;" in html
    assert "A&amp;B &lt;出典&gt;" in html
    assert '&lt;script&gt;alert(&quot;' in html
    assert "<script>alert" not in html
