"""BGM 台帳・SQL・フェード方針のテスト。"""

from __future__ import annotations

from pathlib import Path

import prepare_bgm
from prepare_bgm import _fade_filter, generate_audio_assets_sql, validate_tracks


def _entry(provisional: bool = False) -> dict:
    return {
        "file": "source.m4a",
        "start": 0,
        "title": "曲",
        "source_url": "https://example.test/music",
        "license_type": "CC0",
        "license_note": None,
        "acquired_at": "2026-09-23",
        "provisional": provisional,
    }


def test_provisional_track_is_numbered_but_excluded_from_sql() -> None:
    tracks = validate_tracks([_entry(True), _entry(False)])
    sql = generate_audio_assets_sql(tracks)

    assert [track["output"] for track in tracks] == ["track01.m4a", "track02.m4a"]
    assert "track01.m4a" not in sql
    assert "audio/umigame-soup-1/track02.m4a" in sql
    assert "'bgm', NULL" in sql
    assert f", {prepare_bgm.DURATION_SECONDS}, 1" in sql


def test_fade_is_baked_by_prepare_bgm() -> None:
    value = _fade_filter()
    assert "afade=t=in:st=0:d=0.5" in value
    # 動画の尺（R-1-1 で 27 秒）の末尾 1 秒でフェードアウトする
    assert f"afade=t=out:st={prepare_bgm.DURATION_SECONDS - 1.0}:d=1.0" in value


def test_init_provisional_registers_poc_track(tmp_path: Path, monkeypatch) -> None:
    tracks_path = tmp_path / "tracks.json"
    monkeypatch.setattr(prepare_bgm, "TRACKS_PATH", tracks_path)

    assert prepare_bgm.main(["--init-provisional"]) == 0
    tracks = prepare_bgm.json.loads(tracks_path.read_text(encoding="utf-8"))

    assert tracks[0]["file"] == "poc/classic-umigame/normalized/bgm_24s.m4a"
    assert tracks[0]["provisional"] is True


def test_no_sql_keeps_registration_sql(tmp_path: Path, monkeypatch) -> None:
    tracks_path = tmp_path / "tracks.json"
    sql_path = tmp_path / "03_audio_assets.sql"
    sql_path.write_text("-- 既存", encoding="utf-8")
    tracks_path.write_text(prepare_bgm.json.dumps([_entry(False)]), encoding="utf-8")
    monkeypatch.setattr(prepare_bgm, "TRACKS_PATH", tracks_path)
    monkeypatch.setattr(prepare_bgm, "SQL_PATH", sql_path)
    monkeypatch.setattr(prepare_bgm, "process_track", lambda *args, **kwargs: None)

    assert prepare_bgm.main(["--no-sql"]) == 0
    assert sql_path.read_text(encoding="utf-8") == "-- 既存"
