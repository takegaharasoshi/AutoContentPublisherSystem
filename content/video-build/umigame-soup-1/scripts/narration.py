"""PoC 用ナレーション合成（VOICEVOX）。

pref-ranking-1 の TTS アダプタ（``remotion/scripts/tts.py``）を流用し、問題文 + ルール帯の
2 cue を合成して実測長を出す。話者候補の比較にも使う（``--speaker`` を複数回指定）。

出力: ``<out_dir>/speaker<id>/{problem,rule}.wav`` と ``<out_dir>/speaker<id>/narration.json``
（実測秒・フレーム数・engine_id）。尺の予算検査は ``--budget-seconds`` で行い、超過は exit 1。
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
PREF_SCRIPTS = HERE.parent.parent / "pref-ranking-1" / "remotion" / "scripts"
sys.path.insert(0, str(PREF_SCRIPTS))

import tts  # noqa: E402
from tts import CueRequest, TtsError, VoicevoxEngine  # noqa: E402

# pref の許容差 0.08 秒は 2〜4 秒の短い cue で実測した値。問題文は 12 秒超の長い cue のため
# 予測長との差が 0.1 秒程度出る（speaker 12 で実測）。PoC では 0.3 秒に緩める（README に記録）。
tts.LENGTH_TOLERANCE_SECONDS = 0.3

FPS = 30


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("problem_json", type=Path)
    parser.add_argument("out_dir", type=Path)
    parser.add_argument("--speaker", type=int, action="append", required=True)
    parser.add_argument("--speed", type=float, default=1.2)
    parser.add_argument("--intonation", type=float, default=1.6)
    parser.add_argument("--gap-seconds", type=float, default=0.5)
    parser.add_argument("--budget-seconds", type=float, default=17.0)
    parser.add_argument("--engine", default="http://127.0.0.1:50021")
    args = parser.parse_args()

    cues = json.loads(args.problem_json.read_text(encoding="utf-8"))["narration_cue"]
    over_budget = False
    for speaker in args.speaker:
        engine = VoicevoxEngine(
            base_url=args.engine, speaker=speaker,
            intonation_scale=args.intonation, fps=FPS,
        )
        out = args.out_dir / f"speaker{speaker}"
        report: dict[str, object] = {"speaker": speaker, "speed_scale": args.speed,
                                     "intonation_scale": args.intonation, "cues": {}}
        total = 0.0
        for cue_id in ("problem", "rule"):
            try:
                audio = engine.synthesize(
                    CueRequest(id=cue_id, text=cues[cue_id]),
                    out / f"{cue_id}.wav", speed_scale=args.speed,
                )
            except TtsError as exc:
                print(f"speaker {speaker} {cue_id}: {exc}")
                return 1
            report["cues"][cue_id] = {"seconds": round(audio.seconds, 3), "frames": audio.frames}
            total += audio.seconds
        total += args.gap_seconds
        report["total_seconds"] = round(total, 3)
        report["total_frames"] = round(total * FPS)
        report["engine_id"] = engine.engine_id
        report["gap_seconds"] = args.gap_seconds
        (out / "narration.json").write_text(
            json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
        flag = "OK" if total <= args.budget_seconds else "OVER BUDGET"
        print(f"speaker {speaker}: problem {report['cues']['problem']['seconds']}s "
              f"+ gap {args.gap_seconds}s + rule {report['cues']['rule']['seconds']}s "
              f"= {total:.2f}s (budget {args.budget_seconds}s) {flag} [{engine.engine_id}]")
        over_budget |= total > args.budget_seconds
    return 1 if over_budget else 0


if __name__ == "__main__":
    raise SystemExit(main())
