"""承認・manifest 検査と Aurora SQL 生成のテスト。"""

from pathlib import Path

import pytest

from publish import (
    ManifestValidationError,
    generate_aurora_sql,
    parse_approved_file,
    validate_manifest,
)


def test_parse_approved_file_ignores_comments_and_blank_lines(tmp_path: Path) -> None:
    path = tmp_path / "approved.txt"
    path.write_text("# 承認済み\n\n001-one\n  002-two  \n", encoding="utf-8")

    assert parse_approved_file(path) == ["001-one", "002-two"]


def test_generate_aurora_sql_uses_content_key_and_partial_duration() -> None:
    targets = [
        {
            "content_key": "001-o'ne\\test",
            "bgm_s3_key": "audio/pref-ranking-1/bgm/o'ne.m4a",
            "durations": {"20s": {}},
        }
    ]

    sql = generate_aurora_sql(targets, "2026-08-12 01:02:03")

    assert "video_s3_key_20s" in sql
    assert "video_s3_key_30s" not in sql
    assert "r.content_key = '001-o''ne\\\\test'" in sql
    assert "a.s3_key = 'audio/pref-ranking-1/bgm/o''ne.m4a'" in sql
    assert (
        "AND EXISTS (SELECT 1 FROM audio_assets a WHERE a.set_id = r.set_id "
        "AND a.s3_key = 'audio/pref-ranking-1/bgm/o''ne.m4a')" in sql
    )
    assert "更新行数が承認件数と一致することを確認する" in sql
    assert "stock_item_id" not in sql


def _valid_manifest(base: Path) -> dict[str, object]:
    video = base / "work" / "videos" / "001-one_20s.mp4"
    background = base / "work" / "backgrounds" / "001-one.png"
    video.parent.mkdir(parents=True)
    background.parent.mkdir(parents=True)
    video.write_bytes(b"video")
    background.write_bytes(b"png")
    return {
        "001-one": {
            "content_key": "001-one",
            "audio_asset_id": 3,
            "bgm_s3_key": "audio/pref-ranking-1/bgm/music.m4a",
            "durations": {
                "20s": {"video": "work/videos/001-one_20s.mp4"}
            },
        }
    }


def test_validate_manifest_resolves_existing_artifacts(tmp_path: Path) -> None:
    targets = validate_manifest(_valid_manifest(tmp_path), ["001-one"], base=tmp_path)

    assert targets[0]["durations"]["20s"]["video_path"].is_file()
    assert targets[0]["background_path"].is_file()


@pytest.mark.parametrize(
    "damage", ["missing_record", "null_audio", "missing_video", "missing_background"]
)
def test_validate_manifest_reports_all_publish_blockers(
    tmp_path: Path, damage: str
) -> None:
    manifest = _valid_manifest(tmp_path)
    approved = ["001-one"]
    if damage == "missing_record":
        approved = ["999-missing"]
    elif damage == "null_audio":
        manifest["001-one"]["audio_asset_id"] = None
    elif damage == "missing_video":
        (tmp_path / "work" / "videos" / "001-one_20s.mp4").unlink()
    else:
        (tmp_path / "work" / "backgrounds" / "001-one.png").unlink()

    with pytest.raises(ManifestValidationError):
        validate_manifest(manifest, approved, base=tmp_path)
