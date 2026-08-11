"""レンダリング済み動画の配信ラウドネスを揃える（音声のみ再エンコード）。

コンポジション（src/audio.ts）が決めるのはナレーションと BGM の相対バランスだけで、
配信レベルはここで揃える。VOICEVOX の出力は素で -24 LUFS 前後と静かなため、
Remotion の出力をそのまま投稿するとプラットフォーム側で持ち上がらず小さいまま聞こえる。

ffmpeg の loudnorm を 2 パス（計測 → 計測値を渡して適用）で使う。映像は再エンコードしない。
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile


TARGET_I = -14.0
"""配信ラウドネス（LUFS）。リール系プラットフォームの一般的な基準値。"""

TARGET_TP = -1.5
"""トゥルーピーク上限（dBTP）。AAC 化で 0.5 dB ほど持ち上がるぶんを見て -1 dBTP より下げてある。"""

TARGET_LRA = 11.0
"""ラウドネスレンジ（LU）。"""

AUDIO_BITRATE = "192k"
SAMPLE_RATE = "48000"


class LoudnessError(RuntimeError):
    """計測または正規化に失敗したことを表す。"""


def _run(command: list[str]) -> str:
    try:
        completed = subprocess.run(
            command, capture_output=True, text=True, check=False
        )
    except FileNotFoundError as exc:
        raise LoudnessError(
            f"ffmpeg を実行できません: {exc}。--ffmpeg で実行可能なパスを指定するか、"
            "image-batch の Docker イメージ経由で実行してください。"
        ) from exc
    if completed.returncode != 0:
        tail = "\n".join(completed.stderr.strip().splitlines()[-5:])
        raise LoudnessError(f"ffmpeg が失敗しました（{completed.returncode}）:\n{tail}")
    return completed.stderr


def measure(path: Path, *, ffmpeg: str = "ffmpeg") -> dict[str, float]:
    """ebur128 で統合ラウドネス・LRA・トゥルーピークを計測する。"""
    stderr = _run(
        [ffmpeg, "-hide_banner", "-nostats", "-i", str(path),
         "-af", "ebur128=peak=true", "-f", "null", "-"]
    )
    summary = stderr[stderr.rfind("Integrated loudness"):]
    values: dict[str, float] = {}
    for key, pattern in (
        ("integrated", r"I:\s*(-?\d+(?:\.\d+)?) LUFS"),
        ("lra", r"LRA:\s*(-?\d+(?:\.\d+)?) LU"),
        ("true_peak", r"Peak:\s*(-?\d+(?:\.\d+)?) dBFS"),
    ):
        match = re.search(pattern, summary)
        if match is None:
            raise LoudnessError(f"ffmpeg の出力から {key} を読み取れません。")
        values[key] = float(match.group(1))
    return values


def _measure_for_loudnorm(path: Path, *, ffmpeg: str) -> dict[str, str]:
    """loudnorm の 1 パス目（計測）を実行し、JSON の計測値を返す。"""
    stderr = _run(
        [ffmpeg, "-hide_banner", "-nostats", "-i", str(path),
         "-af",
         f"loudnorm=I={TARGET_I}:TP={TARGET_TP}:LRA={TARGET_LRA}:print_format=json",
         "-f", "null", "-"]
    )
    start = stderr.rfind("{")
    end = stderr.rfind("}")
    if start < 0 or end < start:
        raise LoudnessError("loudnorm の計測 JSON が見つかりません。")
    try:
        return json.loads(stderr[start : end + 1])
    except json.JSONDecodeError as exc:
        raise LoudnessError(f"loudnorm の計測 JSON が不正です: {exc}") from exc


def normalize(
    source: Path, destination: Path, *, ffmpeg: str = "ffmpeg"
) -> dict[str, dict[str, float]]:
    """配信ラウドネスへ正規化し、前後の計測値を返す。"""
    source = Path(source)
    destination = Path(destination)
    before = measure(source, ffmpeg=ffmpeg)
    measured = _measure_for_loudnorm(source, ffmpeg=ffmpeg)
    loudnorm = (
        f"loudnorm=I={TARGET_I}:TP={TARGET_TP}:LRA={TARGET_LRA}"
        f":measured_I={measured['input_i']}"
        f":measured_TP={measured['input_tp']}"
        f":measured_LRA={measured['input_lra']}"
        f":measured_thresh={measured['input_thresh']}"
        f":offset={measured['target_offset']}:linear=true:print_format=summary"
    )
    in_place = source.resolve() == destination.resolve()
    with tempfile.TemporaryDirectory() as work_dir:
        staged = Path(work_dir) / f"normalized{destination.suffix or '.mp4'}"
        target = staged if in_place else destination
        target.parent.mkdir(parents=True, exist_ok=True)
        _run(
            [ffmpeg, "-hide_banner", "-nostats", "-y", "-i", str(source),
             "-c:v", "copy", "-af", loudnorm,
             "-c:a", "aac", "-b:a", AUDIO_BITRATE, "-ar", SAMPLE_RATE,
             "-movflags", "+faststart", str(target)]
        )
        if in_place:
            shutil.move(str(staged), str(destination))
    return {"before": before, "after": measure(destination, ffmpeg=ffmpeg)}


def main(argv: list[str] | None = None) -> int:
    """CLI として正規化を実行し、前後の計測値を表示する。"""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path, help="Remotion が出力した mp4")
    parser.add_argument(
        "destination", type=Path, nargs="?", help="出力先（省略時は入力を上書き）"
    )
    parser.add_argument("--ffmpeg", default="ffmpeg", help="ffmpeg の実行パス")
    parser.add_argument(
        "--measure-only", action="store_true", help="正規化せず計測値だけ表示する"
    )
    args = parser.parse_args(argv)
    try:
        if args.measure_only:
            values = measure(args.source, ffmpeg=args.ffmpeg)
            print(
                f"I={values['integrated']} LUFS / LRA={values['lra']} LU / "
                f"TP={values['true_peak']} dBFS"
            )
            return 0
        result = normalize(
            args.source, args.destination or args.source, ffmpeg=args.ffmpeg
        )
    except LoudnessError as exc:
        print(f"エラー: {exc}", file=sys.stderr)
        return 1
    for label in ("before", "after"):
        values = result[label]
        print(
            f"{label}: I={values['integrated']} LUFS / LRA={values['lra']} LU / "
            f"TP={values['true_peak']} dBFS"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
