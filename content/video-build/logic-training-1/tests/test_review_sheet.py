"""レビュー HTML の出力テスト。"""

from pathlib import Path

from review_sheet import filter_manifest, generate_review_html
from spec import STILL_FRAMES


def test_review_html_escapes_and_contains_review_assets(tmp_path: Path) -> None:
    manifest = {
        "85": {
            "video": "work/videos/85.mp4",
            "stills": {
                key: f"work/cuts/85_{key}.png" for key in STILL_FRAMES
            },
            "question_text": '<script>alert("x")</script>',
            "hint": "A&B <ヒント>",
            "slot_code": "morning",
            "content_key": "logic<&>",
        }
    }

    html = generate_review_html(manifest, base=tmp_path)

    assert "videos/85.mp4" in html
    assert "cuts/85_cut2.png" in html
    assert "hint: A&amp;B &lt;ヒント&gt;" in html
    assert "logic&lt;&amp;&gt;" in html
    assert "<script>alert" not in html
    assert "&lt;script&gt;alert(&quot;" in html


def test_review_html_keeps_stills_in_spec_order(tmp_path: Path) -> None:
    manifest = {
        "1": {
            "stills": {
                key: f"work/cuts/1_{key}.png" for key in STILL_FRAMES
            }
        }
    }

    html = generate_review_html(manifest, base=tmp_path)
    positions = [html.index(f"1_{key}.png") for key in STILL_FRAMES]

    assert positions == sorted(positions)
    assert ".still-seam_head{order:0}" in html
    assert ".still-seam_tail{order:1}" in html


def test_filter_manifest_keeps_requested_slots_only() -> None:
    manifest = {
        "1": {"slot_code": "morning"},
        "2": {"slot_code": "noon"},
        "3": {"slot_code": "night"},
        "4": {},
    }

    assert filter_manifest(manifest, None) == manifest
    assert filter_manifest(manifest, []) == manifest
    assert sorted(filter_manifest(manifest, ["morning", "night"])) == ["1", "3"]
