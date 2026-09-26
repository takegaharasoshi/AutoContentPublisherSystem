"""Irodori-TTS の息継ぎ対策・別声クローンの試作（リポジトリ外の PoC）。

Irodori の venv で実行する: cd ~/tools/Irodori-TTS && uv run --no-sync python <this>
"""

from __future__ import annotations

import json
from pathlib import Path
import subprocess

import numpy as np
import soundfile as sf

IRODORI = Path.home() / "tools" / "Irodori-TTS"
OUT = IRODORI / "outputs" / "poc2"
NARR = Path(
    "/home/takegaharawork/projects/AutoContentPublisherSystem/content/video-build/"
    "umigame-soup-1/work/narration"
)
VOICE2 = Path.home() / "tools" / "irodori-refs" / "voice2"
PROBLEMS = ["016-umigame-soup", "008-who-made-the-mistake"]
G4_REFS = [
    NARR / k / f"{c}.wav"
    for k in ("001-faint-shadow", "004-fifty-year-letter", "006-frozen-tag")
    for c in ("problem", "rule")
]
NO_BREATH = "息継ぎの音を立てず、息を吸う音が聞こえないように、なめらかに読む。"


def breath_gate(src: Path, dst: Path, *, below_peak_db: float = 18.0,
                min_ms: int = 80, guard_ms: int = 20, cut_db: float = 30.0,
                fade_ms: int = 15) -> int:
    """声のピークより十分小さい区間（息・残響・雑音）だけ音量を下げる。

    10ms ごとの RMS が「上位 5% の音量 - below_peak_db」を下回る区間を探し、
    min_ms 以上続くものについて、両端を guard_ms 残して cut_db 下げる（端は fade_ms で滑らかに）。
    戻り値は下げた区間の数。
    """
    x, sr = sf.read(src, always_2d=True)
    mono = x.mean(axis=1)
    hop = sr // 100
    n = len(mono) // hop
    rms = np.sqrt(np.array([np.mean(mono[i * hop:(i + 1) * hop] ** 2) for i in range(n)]) + 1e-12)
    db = 20 * np.log10(rms)
    threshold = np.percentile(db, 95) - below_peak_db
    low = db < threshold
    gain = np.ones(len(mono))
    guard = guard_ms // 10
    fade = int(sr * fade_ms / 1000)
    count = 0
    start = None
    for i, flag in enumerate(list(low) + [False]):
        if flag and start is None:
            start = i
        elif not flag and start is not None:
            if (i - start) * 10 >= min_ms:
                a = (start + guard) * hop
                b = (i - guard) * hop
                if b - a > 2 * fade:
                    floor = 10 ** (-cut_db / 20)
                    seg = np.full(b - a, floor)
                    seg[:fade] = np.linspace(1.0, floor, fade)
                    seg[-fade:] = np.linspace(floor, 1.0, fade)
                    gain[a:b] = np.minimum(gain[a:b], seg)
                    count += 1
            start = None
    sf.write(dst, x * gain[:, None], sr)
    return count


def infer(text: str, out: Path, *, refs: list[Path] | None, caption: str | None,
          seed: int = 1) -> None:
    cmd = [
        "uv", "run", "--no-sync", "python", "infer.py",
        "--hf-checkpoint", "Aratako/Irodori-TTS-v4.1-Small",
        "--model-device", "cuda", "--codec-device", "cuda",
        "--model-precision", "bf16", "--codec-precision", "bf16",
        "--seed", str(seed), "--text", text, "--output-wav", str(out),
    ]
    cmd += ["--ref-wavs", *map(str, refs)] if refs else ["--no-ref"]
    if caption:
        cmd += ["--caption", caption]
    with open(OUT / "infer.log", "a", encoding="utf-8") as log:
        subprocess.run(cmd, cwd=IRODORI, check=True, stdout=log, stderr=subprocess.STDOUT)


def split_reference(src: Path, dst_dir: Path) -> list[Path]:
    """1 本の長い参照音声を 0.3 秒以上の無音で 4〜12 秒程度のクリップに分ける。"""
    x, sr = sf.read(src, always_2d=True)
    mono = x.mean(axis=1)
    hop = sr // 100
    n = len(mono) // hop
    db = 20 * np.log10(np.sqrt(np.array([np.mean(mono[i * hop:(i + 1) * hop] ** 2) for i in range(n)]) + 1e-12))
    quiet = db < np.percentile(db, 95) - 30
    cuts, run = [], 0
    for i, q in enumerate(quiet):
        run = run + 1 if q else 0
        if run == 30:
            cuts.append(i - 15)
    clips, last = [], 0
    for c in cuts + [n]:
        if (c - last) >= 400 or c == n:
            if c - last >= 100:
                clips.append((last, c))
            last = c
    dst_dir.mkdir(parents=True, exist_ok=True)
    paths = []
    for idx, (a, b) in enumerate(clips):
        p = dst_dir / f"clip{idx:02d}.wav"
        sf.write(p, x[a * hop:b * hop], sr)
        paths.append(p)
    return paths


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    report: dict[str, object] = {}
    # ① 参照音声の息を下げたもの
    clean_dir = OUT / "g4_refs_gated"
    clean_dir.mkdir(exist_ok=True)
    clean_refs = []
    for ref in G4_REFS:
        dst = clean_dir / f"{ref.parent.name}_{ref.stem}.wav"
        report[f"gate_ref/{dst.name}"] = breath_gate(ref, dst)
        clean_refs.append(dst)
    # 別の声: 1 本を短いクリップに分ける（1 本しかなければそのまま）
    v2_src = sorted(VOICE2.glob("*.wav"))
    v2_refs: list[Path] = []
    for src in v2_src:
        v2_refs += split_reference(src, OUT / "voice2_clips" / src.stem)
    report["voice2_clips"] = [p.name for p in v2_refs]
    for key in PROBLEMS:
        texts = json.loads((NARR / key / "narration.json").read_text(encoding="utf-8"))["texts"]
        text = f"{texts['problem']} {texts['rule']}"
        base = IRODORI / "outputs" / "poc" / f"{key}_b_ref.wav"
        # ③ 既存の (b) に後処理だけ
        report[f"{key}/b_post"] = breath_gate(base, OUT / f"{key}_b_post.wav")
        # ① 息を下げた参照で作り直し
        infer(text, OUT / f"{key}_e_cleanref.wav", refs=clean_refs, caption=None)
        report[f"{key}/e_post"] = breath_gate(OUT / f"{key}_e_cleanref.wav", OUT / f"{key}_e_cleanref_post.wav")
        # ② 説明文で指示 + ① + ③
        infer(text, OUT / f"{key}_f_cleanref_caption.wav", refs=clean_refs, caption=NO_BREATH)
        report[f"{key}/f_post"] = breath_gate(OUT / f"{key}_f_cleanref_caption.wav", OUT / f"{key}_f_cleanref_caption_post.wav")
        # 別の声
        if v2_refs:
            infer(text, OUT / f"{key}_v2.wav", refs=v2_refs, caption=None)
            report[f"{key}/v2_post"] = breath_gate(OUT / f"{key}_v2.wav", OUT / f"{key}_v2_post.wav")
    (OUT / "report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
