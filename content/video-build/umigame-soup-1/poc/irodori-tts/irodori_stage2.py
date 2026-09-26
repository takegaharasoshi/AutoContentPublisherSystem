"""Irodori の合成結果を切り分け・尺合わせして本番と同じ Remotion で動画化する（システムの python3 で実行）。"""

from __future__ import annotations

import html
import json
from pathlib import Path
import shutil
import sys
import wave

SET = Path("/home/takegaharawork/projects/AutoContentPublisherSystem/content/video-build/umigame-soup-1")
sys.path.insert(0, str(SET))

import build  # noqa: E402
from scripts import narration_gemini as ng  # noqa: E402

OUT = SET / "work" / "irodori-poc"
GAP, BUDGET, TARGET = 1.2, 21.0, 19.0


def seconds(path: Path) -> float:
    with wave.open(str(path), "rb") as handle:
        return handle.getnframes() / handle.getframerate()


def process(key: str, vid: str, texts: dict[str, str]) -> dict:
    d = OUT / key / vid
    combined = d / "combined.wav"
    ng._default_ffmpeg_runner(d / "irodori_raw.wav", combined, "anull")  # 24 kHz mono 16bit へ
    ratio = len(texts["problem"]) / (len(texts["problem"]) + len(texts["rule"]))
    split_at = ng._split(combined, ratio, d / "problem.wav", d / "rule.wav")
    raw = {c: ng._fit(d / f"{c}.wav", 1.0, ng._default_ffmpeg_runner) for c in ("problem", "rule")}
    natural = raw["problem"] + GAP + raw["rule"]
    tempo = round((natural - GAP) / (TARGET - GAP), 3) if natural > BUDGET else 1.0
    secs = {c: (ng._fit(d / f"{c}.wav", tempo, ng._default_ffmpeg_runner) if tempo > 1 else raw[c]) for c in raw}
    staged = f"{key}__irodori_{vid}"
    pub = build.PUBLIC_DIR / "narration" / staged
    pub.mkdir(parents=True, exist_ok=True)
    props = json.loads((build.WORK / "props" / f"{key}.json").read_text(encoding="utf-8"))
    for c in ("problem", "rule"):
        shutil.copy2(d / f"{c}.wav", pub / f"{c}.wav")
        props["narration"][c] = {"file": f"narration/{staged}/{c}.wav", "frames": round(secs[c] * 30)}
    props_path = d / "props.json"
    props_path.write_text(json.dumps(props, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    raw_mp4 = d / "raw.mp4"
    final = OUT / key / f"{vid}.mp4"
    build.render(props_path, raw_mp4)
    build.normalize_loudness(raw_mp4, final)
    raw_mp4.unlink(missing_ok=True)
    rep = {"split_at": split_at, "natural": round(natural, 3), "tempo": tempo,
           "problem": round(secs["problem"], 3), "rule": round(secs["rule"], 3),
           "total": round(secs["problem"] + GAP + secs["rule"], 3)}
    (d / "report.json").write_text(json.dumps(rep, ensure_ascii=False, indent=2), encoding="utf-8")
    return rep


def main() -> None:
    meta = json.loads((OUT / "stage1.json").read_text(encoding="utf-8"))
    reports = {}
    for kv, m in meta.items():
        key, vid = kv.split("/")
        texts = json.loads((build.WORK / "narration" / key / "narration.json").read_text(encoding="utf-8"))["texts"]
        reports[kv] = process(key, vid, texts)
        print(kv, reports[kv], flush=True)
    rows = []
    for key in dict.fromkeys(k.split("/")[0] for k in meta):
        cells = []
        g4 = OUT / key / "gemini_g4.mp4"
        src = build.WORK / "videos" / f"{key}.mp4"
        if src.is_file():
            shutil.copy2(src, g4)
            cells.append(f'<figure><video controls preload="metadata" src="{key}/gemini_g4.mp4"></video>'
                         f"<figcaption>現在の work/videos（016 は Gemini G4・008 は Polly）</figcaption></figure>")
        for kv, m in meta.items():
            if not kv.startswith(key + "/"):
                continue
            vid = kv.split("/")[1]
            r = reports[kv]
            tempo = f"・話速 ×{r['tempo']}" if r["tempo"] > 1 else ""
            cells.append(f'<figure><video controls preload="metadata" src="{key}/{vid}.mp4"></video>'
                         f"<figcaption>{html.escape(m['label'])}<br><small>ナレーション {r['total']:.1f} 秒{tempo}</small></figcaption></figure>")
        rows.append(f"<h2>{html.escape(key)}</h2><div class=grid>{''.join(cells)}</div>")
    page = OUT / "compare.html"
    page.write_text(
        '<!doctype html><html lang="ja"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
        "<title>Irodori 声と演技の比較</title><style>"
        ":root{--bg:#fafaf7;--fg:#1d1d1b}@media (prefers-color-scheme:dark){:root{--bg:#161615;--fg:#eee}}"
        "body{font-family:system-ui,sans-serif;margin:16px;background:var(--bg);color:var(--fg)}"
        ".grid{display:flex;flex-wrap:wrap;gap:12px}figure{margin:0;width:240px}video{width:240px}"
        "figcaption{font-size:13px;line-height:1.5}</style><h1>Irodori-TTS 声と演技の比較（動画）</h1>"
        + "".join(rows), encoding="utf-8")
    print(page)


if __name__ == "__main__":
    main()
