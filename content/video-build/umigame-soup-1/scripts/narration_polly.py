"""Amazon Polly でナレーション 2 cue（問題文・ルール帯）を合成し、実測長を出す。

2026-09-04 のレビューで VOICEVOX から Polly Neural（Takumi・話速 125%）へ切り替えた（記録は README）。
AWS 認証は手元の ~/.aws を使い、新しい秘密情報は不要。日本語は Neural エンジンのみ
（Generative は日本語未対応。ap-northeast-1 / us-east-1 で確認）。

出力: ``<out_dir>/{problem,rule}.wav``（16 kHz mono PCM。Polly の pcm 出力にヘッダを付ける）と
``<out_dir>/narration.json``（実測秒・フレーム数・engine_id）。実測長は PCM のバイト数から求める。

使い方: python3 scripts/narration_polly.py poc/classic-umigame/problem.json poc/classic-umigame/narration/polly_Takumi_x125 --voice Takumi --rate 125
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess
import wave
from xml.sax.saxutils import escape

FPS = 30
SAMPLE_RATE = 16000


def synthesize(text: str, voice: str, rate: int, region: str, out_wav: Path) -> float:
    ssml = f'<speak><prosody rate="{rate}%">{escape(text)}</prosody></speak>'
    out_wav.parent.mkdir(parents=True, exist_ok=True)
    pcm_path = out_wav.with_suffix(".pcm")
    subprocess.run([
        "aws", "polly", "synthesize-speech", "--region", region, "--engine", "neural",
        "--voice-id", voice, "--output-format", "pcm", "--sample-rate", str(SAMPLE_RATE),
        "--text-type", "ssml", "--text", ssml, str(pcm_path),
    ], check=True, capture_output=True)
    data = pcm_path.read_bytes()
    pcm_path.unlink()
    with wave.open(str(out_wav), "wb") as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(SAMPLE_RATE)
        wav.writeframes(data)
    return len(data) / (2 * SAMPLE_RATE)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("problem_json", type=Path)
    parser.add_argument("out_dir", type=Path)
    parser.add_argument("--voice", default="Takumi")
    parser.add_argument("--rate", type=int, default=125, help="SSML prosody rate（%）")
    parser.add_argument("--region", default="ap-northeast-1")
    parser.add_argument("--gap-seconds", type=float, default=1.2)
    parser.add_argument("--budget-seconds", type=float, default=21.0)
    args = parser.parse_args()

    cues = json.loads(args.problem_json.read_text(encoding="utf-8"))["narration_cue"]
    engine_id = f"polly/neural/{args.voice}/rate{args.rate}"
    report: dict[str, object] = {"engine_id": engine_id, "voice": args.voice, "rate": args.rate,
                                 "gap_seconds": args.gap_seconds, "cues": {}}
    total = 0.0
    for cue_id in ("problem", "rule"):
        seconds = synthesize(cues[cue_id], args.voice, args.rate, args.region, args.out_dir / f"{cue_id}.wav")
        report["cues"][cue_id] = {"seconds": round(seconds, 3), "frames": round(seconds * FPS)}
        total += seconds
    total += args.gap_seconds
    report["total_seconds"] = round(total, 3)
    (args.out_dir / "narration.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    flag = "OK" if total <= args.budget_seconds else "OVER BUDGET"
    print(f"{engine_id}: problem {report['cues']['problem']['seconds']}s + gap {args.gap_seconds}s + "
          f"rule {report['cues']['rule']['seconds']}s = {total:.2f}s (budget {args.budget_seconds}s) {flag}")
    return 0 if total <= args.budget_seconds else 1


if __name__ == "__main__":
    raise SystemExit(main())
