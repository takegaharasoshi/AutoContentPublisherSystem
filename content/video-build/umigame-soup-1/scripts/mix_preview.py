"""ナレーション比較用: BGM と合成したプレビュー音源を作る（長さは BGM に合わせる）（ffmpeg。Docker で実行）。

動画と同じ構成: BGM は通常 0.32・ナレーション中 0.14 にダッキング、ナレーションは 0.5 秒から開始し
cue 間 0.5 秒（2 cue の WAV を渡した場合）。最後に -14 LUFS へ正規化する。

使い方: python scripts/mix_preview.py <bgm> <out.mp3> <narration...>（narration は 1 本の mp3 か、problem.wav rule.wav の 2 本）
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


def duration(path: Path) -> float:
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)],
                         check=True, capture_output=True, text=True).stdout.strip()
    return float(out)


def main() -> int:
    bgm, out = Path(sys.argv[1]), Path(sys.argv[2])
    cues = [Path(p) for p in sys.argv[3:]]
    start, gap = 0.5, float(__import__("os").environ.get("MIX_GAP", "0.5"))
    inputs = ["-i", str(bgm)]
    parts, t = [], start
    for i, cue in enumerate(cues, start=1):
        inputs += ["-i", str(cue)]
        parts.append(f"[{i}:a]aresample=48000,adelay={int(t * 1000)}|{int(t * 1000)}[n{i}]")
        t += duration(cue) + gap
    end = t - gap
    narr = "".join(f"[n{i}]" for i in range(1, len(cues) + 1)) + f"amix=inputs={len(cues)}:normalize=0[narr]"
    duck = (f"[0:a]aresample=48000,volume='if(between(t,{start - 0.2},{end + 0.5}),0.14,0.32)':eval=frame[bgm]")
    fc = ";".join(parts + [narr, duck, "[bgm][narr]amix=inputs=2:normalize=0,loudnorm=I=-14:TP=-2:LRA=11[out]"])
    subprocess.run(["ffmpeg", "-v", "error", "-y", *inputs, "-filter_complex", fc, "-map", "[out]", "-t", f"{duration(bgm):.3f}",
                    "-c:a", "libmp3lame", "-q:a", "3", str(out)], check=True)
    print(json.dumps({"out": str(out), "narration_end_seconds": round(end, 2)}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
