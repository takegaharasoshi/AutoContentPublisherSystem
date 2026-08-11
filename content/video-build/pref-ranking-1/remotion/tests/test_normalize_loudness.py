"""Tests for the delivery-loudness normalisation pass."""

from __future__ import annotations

from pathlib import Path
import sys

import pytest


sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

import normalize_loudness  # noqa: E402


EBUR128_SUMMARY = """
[Parsed_ebur128_0 @ 0x1] t: 19.9  TARGET:-23 LUFS  M: -20.5 S: -21.0  I: -24.1 LUFS
[Parsed_ebur128_0 @ 0x1] Summary:

  Integrated loudness:
    I:         -24.1 LUFS
    Threshold: -34.3 LUFS

  Loudness range:
    LRA:         3.6 LU
    Threshold: -44.2 LUFS
    LRA low:   -26.4 LUFS
    LRA high:  -22.8 LUFS

  True peak:
    Peak:       -7.0 dBFS
"""

LOUDNORM_JSON = """
{
	"input_i" : "-24.11",
	"input_tp" : "-7.00",
	"input_lra" : "3.60",
	"input_thresh" : "-34.33",
	"output_i" : "-14.00",
	"target_offset" : "0.12"
}
"""


def test_measure_reads_the_summary_block(monkeypatch: pytest.MonkeyPatch) -> None:
    """サマリ末尾の統合ラウドネス・LRA・トゥルーピークを読む。"""
    monkeypatch.setattr(normalize_loudness, "_run", lambda command: EBUR128_SUMMARY)
    values = normalize_loudness.measure(Path("video.mp4"))
    assert values == {"integrated": -24.1, "lra": 3.6, "true_peak": -7.0}


def test_measure_reports_unparsable_output(monkeypatch: pytest.MonkeyPatch) -> None:
    """ffmpeg の出力から読み取れないときは利用者向けの例外にする。"""
    monkeypatch.setattr(normalize_loudness, "_run", lambda command: "Summary:")
    with pytest.raises(normalize_loudness.LoudnessError):
        normalize_loudness.measure(Path("video.mp4"))


def test_normalize_passes_measured_values_and_copies_video(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """2 パス目に 1 パス目の計測値を渡し、映像は再エンコードしない。"""
    commands: list[list[str]] = []

    def run(command: list[str]) -> str:
        commands.append(command)
        if "ebur128=peak=true" in command:
            return EBUR128_SUMMARY
        if any("print_format=json" in part for part in command):
            return LOUDNORM_JSON
        Path(command[-1]).write_bytes(b"encoded")
        return ""

    monkeypatch.setattr(normalize_loudness, "_run", run)
    source = tmp_path / "in.mp4"
    source.write_bytes(b"source")
    result = normalize_loudness.normalize(source, tmp_path / "out.mp4")

    encode = next(command for command in commands if "-c:v" in command)
    filters = encode[encode.index("-af") + 1]
    assert encode[encode.index("-c:v") + 1] == "copy"
    assert "measured_I=-24.11" in filters
    assert "measured_thresh=-34.33" in filters
    assert f"I={normalize_loudness.TARGET_I}" in filters
    assert f"TP={normalize_loudness.TARGET_TP}" in filters
    assert result["before"]["integrated"] == -24.1


def test_normalize_in_place_replaces_the_source(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """入力と同じパスを指定しても、ffmpeg に自分自身を上書きさせない。"""
    outputs: list[str] = []

    def run(command: list[str]) -> str:
        if "ebur128=peak=true" in command:
            return EBUR128_SUMMARY
        if any("print_format=json" in part for part in command):
            return LOUDNORM_JSON
        outputs.append(command[-1])
        Path(command[-1]).write_bytes(b"encoded")
        return ""

    monkeypatch.setattr(normalize_loudness, "_run", run)
    source = tmp_path / "in.mp4"
    source.write_bytes(b"source")
    normalize_loudness.normalize(source, source)
    assert outputs and outputs[0] != str(source)
    assert source.read_bytes() == b"encoded"
