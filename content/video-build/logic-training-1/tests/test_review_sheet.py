"""レビュー HTML の出力テスト。"""

from pathlib import Path

import pytest

from review_sheet import (
    filter_manifest,
    generate_review_html,
    page_name,
    paginate,
)
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


def test_page_name_keeps_first_page_at_review_html() -> None:
    assert page_name(1) == "review.html"
    assert page_name(2) == "review-2.html"
    assert page_name(4) == "review-4.html"


def test_paginate_splits_in_id_order() -> None:
    manifest = {str(stock_id): {"slot_code": "morning"} for stock_id in range(1, 16)}

    pages = paginate(manifest, 14)

    assert [len(page) for page in pages] == [14, 1]
    assert list(pages[0]) == [str(i) for i in range(1, 15)]
    assert list(pages[1]) == ["15"]


def test_paginate_returns_single_empty_page_for_empty_manifest() -> None:
    assert paginate({}, 14) == [{}]


def test_paginate_rejects_non_positive_page_size() -> None:
    with pytest.raises(ValueError, match="1 以上"):
        paginate({"1": {}}, 0)


def test_generate_review_html_renders_pager_only_when_split() -> None:
    manifest = {"1": {"slot_code": "morning"}}

    single = generate_review_html(manifest)
    split = generate_review_html(manifest, page=2, total_pages=4, total_items=56)

    assert '<nav class="pager"' not in single
    assert 'href="review.html"' in split
    assert 'href="review-3.html"' in split
    assert "ページ 2 / 4（全 56 件）" in split
