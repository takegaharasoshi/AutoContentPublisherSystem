"""レビュー HTML のエスケープと暫定 BGM 警告テスト。"""

from __future__ import annotations

from review_sheet import generate_review_html


def test_review_html_escapes_stock_and_warns_provisional() -> None:
    manifest = {
        "001-test": {
            "video": "videos/<bad>.mp4",
            "bgm": {"track": "track01.m4a", "s3_key": "audio/&.m4a", "provisional": True},
            "narration": {
                "problem_sec": 10, "rule_sec": 5, "total_sec": 16.2,
                "tempo": 1.146, "engine_id": "gemini/gemini-3.8-flash-tts/voice-test",
            },
            "probe": {"width": 1080, "height": 1920, "fps": 30, "duration": 24, "audio_codec": "aac", "valid": True},
            "seam_mean_diff": 1.2,
            "stills": {"intro": "stills/<intro>.jpg"},
        }
    }
    items = [{
        "content_key": "001-test", "title": "<危険>", "hook": "A&B",
        "problem_text": '<script>alert("x")</script>', "rule_text": "rule",
        "character_lines": {"master": {"intro": "i", "outro": "o"}, "jr": {"outro": "j"}},
        "play_example": [], "caption": "caption", "truth": "truth", "fact_sheet": ["<fact>"],
    }]

    html = generate_review_html(manifest, items)

    assert "暫定 BGM が 1 件" in html
    assert "publish できません" in html
    assert "&lt;危険&gt;" in html
    assert "A&amp;B" in html
    assert "&lt;script&gt;" in html
    assert "<script>alert" not in html
    assert "videos/&lt;bad&gt;.mp4" in html
    assert "×1.146" in html
    assert "gemini/gemini-3.8-flash-tts/voice-test" in html
