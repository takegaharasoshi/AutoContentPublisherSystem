"""Amazon Polly Neural で問題文・ルールの 2 cue を WAV 化する。"""

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
    """Polly の raw PCM を 16 kHz mono WAV に包み、実測秒を返す。"""
    ssml = f'<speak><prosody rate="{rate}%">{escape(text)}</prosody></speak>'
    out_wav.parent.mkdir(parents=True, exist_ok=True)
    pcm_path = out_wav.with_suffix(".pcm")
    try:
        subprocess.run(
            [
                "aws", "polly", "synthesize-speech", "--region", region,
                "--engine", "neural", "--voice-id", voice,
                "--output-format", "pcm", "--sample-rate", str(SAMPLE_RATE),
                "--text-type", "ssml", "--text", ssml, str(pcm_path),
            ],
            check=True, capture_output=True, text=True,
        )
        data = pcm_path.read_bytes()
    finally:
        pcm_path.unlink(missing_ok=True)
    with wave.open(str(out_wav), "wb") as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(SAMPLE_RATE)
        wav.writeframes(data)
    return len(data) / (2 * SAMPLE_RATE)


def _cached_report(
    texts: dict[str, str], out_dir: Path, voice: str, rate: int
) -> dict | None:
    path = out_dir / "narration.json"
    if not path.is_file() or not all((out_dir / f"{cue}.wav").is_file() for cue in texts):
        return None
    try:
        report = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    if (
        isinstance(report, dict)
        and report.get("texts") == texts
        and report.get("voice") == voice
        and report.get("rate") == rate
    ):
        return report
    return None


def synthesize_cues(
    problem_text: str,
    rule_text: str,
    out_dir: Path,
    voice: str = "Takumi",
    rate: int = 125,
    region: str = "ap-northeast-1",
) -> dict:
    """2 cue を合成し、実測値を ``narration.json`` に保存する。

    texts・voice・rate が一致し、WAV も存在する場合は既存レポートを返して
    Polly を呼ばない。
    """
    texts = {"problem": problem_text, "rule": rule_text}
    cached = _cached_report(texts, out_dir, voice, rate)
    if cached is not None:
        return cached
    engine_id = f"polly/neural/{voice}/rate{rate}"
    report = {
        "texts": texts,
        "voice": voice,
        "rate": rate,
        "region": region,
        "engine_id": engine_id,
        "gap_seconds": 1.2,
        "cues": {},
    }
    total = 0.0
    for cue, text in texts.items():
        seconds = synthesize(text, voice, rate, region, out_dir / f"{cue}.wav")
        report["cues"][cue] = {
            "seconds": round(seconds, 3),
            "frames": round(seconds * FPS),
        }
        total += seconds
    report["total_seconds"] = round(total + 1.2, 3)
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "narration.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    return report


def main(argv: list[str] | None = None) -> int:
    """旧 PoC と互換の CLI を提供する。"""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("problem_json", type=Path)
    parser.add_argument("out_dir", type=Path)
    parser.add_argument("--voice", default="Takumi")
    parser.add_argument("--rate", type=int, default=125)
    parser.add_argument("--region", default="ap-northeast-1")
    parser.add_argument("--gap-seconds", type=float, default=1.2)
    parser.add_argument("--budget-seconds", type=float, default=21.0)
    args = parser.parse_args(argv)
    source = json.loads(args.problem_json.read_text(encoding="utf-8"))
    cues = source.get("narration_cue", source.get("narration"))
    if not isinstance(cues, dict):
        raise SystemExit("narration_cue または narration がありません")
    report = synthesize_cues(
        str(cues["problem"]), str(cues["rule"]), args.out_dir,
        voice=args.voice, rate=args.rate, region=args.region,
    )
    total = (
        float(report["cues"]["problem"]["seconds"])
        + args.gap_seconds
        + float(report["cues"]["rule"]["seconds"])
    )
    flag = "OK" if total <= args.budget_seconds else "OVER BUDGET"
    print(
        f"{report['engine_id']}: problem {report['cues']['problem']['seconds']}s + "
        f"gap {args.gap_seconds}s + rule {report['cues']['rule']['seconds']}s = "
        f"{total:.2f}s (budget {args.budget_seconds}s) {flag}"
    )
    return 0 if total <= args.budget_seconds else 1


if __name__ == "__main__":
    raise SystemExit(main())
