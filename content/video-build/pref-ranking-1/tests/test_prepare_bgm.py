"""BGM 前処理の manifest 検査・SQL 生成・ffmpeg 出力の読み取りのテスト。"""

from __future__ import annotations

import pytest

from prepare_bgm import (
    ManifestError,
    FfmpegError,
    generate_audio_assets_sql,
    loudnorm_filter,
    parse_ebur128_summary,
    parse_loudnorm_json,
    s3_key,
    validate_manifest,
)


def _entry(**overrides: object) -> dict[str, object]:
    entry = {
        "file": "source.mp3",
        "start": 12,
        "title": "Festival Groove",
        "source_url": "https://pixabay.com/music/1234/",
        "license_type": "Pixabay License",
        "acquired_at": "2026-08-26",
    }
    entry.update(overrides)
    return entry


def test_validate_manifest_fills_output_names() -> None:
    tracks = validate_manifest([_entry(), _entry(), _entry()])

    assert [track["output"] for track in tracks] == [
        "track01.m4a",
        "track02.m4a",
        "track03.m4a",
    ]
    assert tracks[0]["license_note"] is None


def test_validate_manifest_accepts_a_single_track() -> None:
    tracks = validate_manifest([_entry()])

    assert [track["output"] for track in tracks] == ["track01.m4a"]


def test_validate_manifest_rejects_empty_and_more_than_five_tracks() -> None:
    with pytest.raises(ManifestError, match="1 件以上"):
        validate_manifest([])
    with pytest.raises(ManifestError, match="5 曲まで"):
        validate_manifest([_entry() for _ in range(6)])


def test_validate_manifest_rejects_non_commercial_license() -> None:
    with pytest.raises(ManifestError, match="非商用"):
        validate_manifest(
            [_entry(license_type="CC BY-NC 4.0")]
        )


def test_validate_manifest_warns_on_credit_required_license(
    capsys: pytest.CaptureFixture[str],
) -> None:
    validate_manifest([_entry(license_type="CC BY 4.0")])

    assert "クレジット表記" in capsys.readouterr().err


def test_validate_manifest_rejects_missing_keys_and_bad_values() -> None:
    broken = _entry()
    del broken["source_url"]
    with pytest.raises(ManifestError, match="source_url"):
        validate_manifest([broken, _entry(), _entry()])
    with pytest.raises(ManifestError, match="start"):
        validate_manifest([_entry(start=-1), _entry(), _entry()])
    with pytest.raises(ManifestError, match="acquired_at"):
        validate_manifest([_entry(acquired_at="2026/08/26"), _entry(), _entry()])
    with pytest.raises(ManifestError, match="未知のキー"):
        validate_manifest([_entry(volume=1), _entry(), _entry()])


def test_validate_manifest_rejects_duplicate_output_names() -> None:
    with pytest.raises(ManifestError, match="重複"):
        validate_manifest(
            [
                _entry(output="track01.m4a"),
                _entry(output="track01.m4a"),
                _entry(),
            ]
        )


def test_generate_audio_assets_sql_records_evidence_and_escapes_quotes() -> None:
    tracks = validate_manifest(
        [
            _entry(title="O'Hara's Matsuri", license_note="表記不要"),
            _entry(),
            _entry(),
        ]
    )

    sql = generate_audio_assets_sql(tracks)

    assert sql.count("INSERT INTO audio_assets") == 3
    assert "'audio/pref-ranking-1/track01.m4a'" in sql
    assert "'O''Hara''s Matsuri'" in sql
    assert "'表記不要'" in sql
    assert "'2026-08-26 00:00:00'" in sql
    assert "'bgm', NULL," in sql
    assert "       30, 1" in sql
    assert "WHERE b.set_code = 'pref-ranking-1';" in sql
    assert "NULL,\n       '2026-08-26 00:00:00'" in sql


def test_s3_key_uses_flat_set_prefix() -> None:
    assert s3_key("track02.m4a") == "audio/pref-ranking-1/track02.m4a"


def test_parse_loudnorm_json_reads_the_last_object() -> None:
    stderr = 'noise {"a": 1}\n[Parsed_loudnorm] {"input_i": "-18.4"}\n'

    assert parse_loudnorm_json(stderr) == {"input_i": "-18.4"}


def test_parse_loudnorm_json_rejects_missing_json() -> None:
    with pytest.raises(FfmpegError, match="見つかりません"):
        parse_loudnorm_json("no json here")


def test_parse_ebur128_summary_reads_measurements() -> None:
    stderr = (
        "Duration: 00:00:30.02, start: 0.000000\n"
        "[Parsed_ebur128_0 @ 0x1] Summary:\n\n"
        "  Integrated loudness:\n    I:         -14.1 LUFS\n"
        "    Threshold: -24.6 LUFS\n"
        "  Loudness range:\n    LRA:         4.2 LU\n"
        "  True peak:\n    Peak:       -1.6 dBFS\n"
    )

    assert parse_ebur128_summary(stderr) == {
        "integrated": -14.1,
        "lra": 4.2,
        "true_peak": -1.6,
    }


def test_loudnorm_filter_is_linear_and_carries_measurements() -> None:
    measured = {
        "input_i": "-18.4",
        "input_tp": "-1.0",
        "input_lra": "5.0",
        "input_thresh": "-28.6",
        "target_offset": "0.3",
    }

    filter_text = loudnorm_filter(measured)

    assert "linear=true" in filter_text
    assert "measured_I=-18.4" in filter_text
    assert "I=-14.0" in filter_text
    assert "TP=-1.5" in filter_text
