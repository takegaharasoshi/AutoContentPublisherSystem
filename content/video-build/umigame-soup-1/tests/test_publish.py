"""承認解析・publish 検査・SQL・dry-run の副作用境界テスト。"""

from __future__ import annotations

from pathlib import Path

import pytest

import publish
from publish import (
    ManifestValidationError,
    generate_update_sql,
    parse_approved_file,
    validate_manifest,
)


def _manifest(base: Path, *, provisional: bool = False) -> dict:
    video = base / "work" / "videos" / "001-one.mp4"
    background = base / "work" / "backgrounds" / "raw" / "001-one.png"
    video.parent.mkdir(parents=True, exist_ok=True)
    background.parent.mkdir(parents=True, exist_ok=True)
    video.write_bytes(b"mp4")
    background.write_bytes(b"png")
    return {
        "001-one": {
            "content_key": "001-one",
            "video": "videos/001-one.mp4",
            "background_png": "backgrounds/raw/001-one.png",
            "bgm": {
                "track": "track01.m4a",
                "s3_key": "audio/umigame-soup-1/track01.m4a",
                "provisional": provisional,
            },
            "probe": {
                "width": 1080, "height": 1920, "fps": 30.0, "duration": 24.05,
                "audio_codec": "aac", "valid": True,
            },
            "built_at": "2026-09-23T01:02:03Z",
        }
    }


def test_parse_approved_file(tmp_path: Path) -> None:
    path = tmp_path / "approved.txt"
    path.write_text("# comment\n\n001-one\n 002-two \n", encoding="utf-8")
    assert parse_approved_file(path) == ["001-one", "002-two"]


def test_validate_manifest_and_provisional_blocker(tmp_path: Path) -> None:
    targets = validate_manifest(_manifest(tmp_path), ["001-one"], base=tmp_path)
    assert targets[0]["video_path"].is_file()

    with pytest.raises(ManifestValidationError, match="暫定 BGM"):
        validate_manifest(_manifest(tmp_path, provisional=True), ["001-one"], base=tmp_path)


def test_generate_update_sql_uses_joined_audio_asset() -> None:
    target = next(iter(_manifest(Path("/tmp"), provisional=False).values()))
    target = {**target, "content_key": "001-o'ne"}
    sql = generate_update_sql([target])

    assert "UPDATE umigame_stock_items u" in sql
    assert "b.set_code = 'umigame-soup-1'" in sql
    assert "a.s3_key = 'audio/umigame-soup-1/track01.m4a'" in sql
    assert "u.video_audio_asset_id = a.id" in sql
    assert "assets/umigame-soup-1/prebuilt/001-o''ne.mp4" in sql
    assert "2026-09-23 01:02:03" in sql


def test_dry_run_never_calls_subprocess(tmp_path: Path, monkeypatch) -> None:
    approved = tmp_path / "approved.txt"
    approved.write_text("001-one\n", encoding="utf-8")
    target = {
        "content_key": "001-one",
        "video_path": tmp_path / "video.mp4",
        "background_path": tmp_path / "background.png",
        "bgm": {"s3_key": "audio/umigame-soup-1/track01.m4a", "provisional": False},
        "built_at": "2026-09-23T01:02:03Z",
    }
    monkeypatch.setattr(publish, "load_items", lambda batch: [{"content_key": "001-one"}])
    monkeypatch.setattr(publish, "load_manifest", lambda: {})
    monkeypatch.setattr(publish, "inspect_manifest", lambda manifest, keys: ([target], []))
    monkeypatch.setattr(publish, "SQL_PATH", tmp_path / "update.sql")

    def forbidden(*args, **kwargs):
        raise AssertionError("dry-run で subprocess を呼びました")

    monkeypatch.setattr(publish.subprocess, "run", forbidden)

    assert publish.main(["--approved", str(approved), "--dry-run"]) == 0
