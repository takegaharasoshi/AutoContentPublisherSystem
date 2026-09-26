"""Gemini 3.8 Flash TTS の聞き比べ PoC（アイデア umigame-tts-gemini-flash）。

承認済みの props（``work/props/<key>.json``）のナレーションだけを Gemini の音声に
差し替え、本番と同じ Remotion コンポジションで比較用動画を ``out/`` に描き出す。
``work/videos`` など承認済みの成果物には書き込まない。

使い方::

    python3 poc/gemini-tts/run_poc.py            # 合成 + レンダリング + 比較ページ
    python3 poc/gemini-tts/run_poc.py --tts-only # 合成と尺の実測だけ
    python3 poc/gemini-tts/run_poc.py --force    # 既存の合成結果を捨てて取り直す

API キーは環境変数 ``GEMINI_API_KEY`` か ``~/.config/gemini/api_key`` から読む。
"""

from __future__ import annotations

import argparse
import array
import base64
import html
import io
import json
import os
from pathlib import Path
import shutil
import sys
from typing import Any
import urllib.error
import urllib.request
import wave

HERE = Path(__file__).resolve().parent
SET_DIR = HERE.parents[1]
sys.path.insert(0, str(SET_DIR))

import build  # noqa: E402

API_BASE = "https://generativelanguage.googleapis.com/v1beta"
OUT = HERE / "out"
FPS = 30


def _api_key() -> str:
    key = os.environ.get("GEMINI_API_KEY")
    if key:
        return key.strip()
    path = Path.home() / ".config" / "gemini" / "api_key"
    if path.is_file():
        return path.read_text(encoding="utf-8").strip()
    raise SystemExit("GEMINI_API_KEY も ~/.config/gemini/api_key もありません")


def _post(path: str, body: dict[str, Any]) -> dict[str, Any]:
    request = urllib.request.Request(
        f"{API_BASE}/{path}",
        data=json.dumps(body, ensure_ascii=False).encode("utf-8"),
        headers={"x-goog-api-key": _api_key(), "Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=180) as response:
            return json.loads(response.read())
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", "replace")[:2000]
        raise RuntimeError(f"{path}: HTTP {exc.code}: {detail}") from exc


def _find_audio(node: Any) -> bytes | None:
    """レスポンス JSON から base64 の音声データを探す（形の差に強くする）。"""
    if isinstance(node, dict):
        mime = str(node.get("mime_type") or node.get("mimeType") or "")
        data = node.get("data")
        if isinstance(data, str) and (mime.startswith("audio") or len(data) > 1000):
            return base64.b64decode(data)
        for value in node.values():
            found = _find_audio(value)
            if found:
                return found
    elif isinstance(node, list):
        for value in node:
            found = _find_audio(value)
            if found:
                return found
    return None


def _to_wav(audio: bytes, out_wav: Path) -> float:
    """WAV ならそのまま、ヘッダなし PCM なら 24 kHz mono で包んで保存し秒数を返す。"""
    out_wav.parent.mkdir(parents=True, exist_ok=True)
    if audio[:4] == b"RIFF":
        out_wav.write_bytes(audio)
    else:
        with wave.open(str(out_wav), "wb") as wav:
            wav.setnchannels(1)
            wav.setsampwidth(2)
            wav.setframerate(24000)
            wav.writeframes(audio)
    with wave.open(str(out_wav), "rb") as wav:
        return wav.getnframes() / wav.getframerate()


def _designed_voice(design: dict[str, str]) -> str:
    cache = OUT / "voices.json"
    voices = json.loads(cache.read_text(encoding="utf-8")) if cache.is_file() else {}
    name = design["display_name"]
    if name in voices:
        return voices[name]["id"]
    response = _post("voices", {
        "store": True,
        "voice": {
            "type": "prompted",
            "display_name": name,
            "language_code": "ja-JP",
            "prompted": {"input": design["description"]},
        },
    })
    voice_id = response.get("id") or (response.get("voice") or {}).get("id")
    if not voice_id:
        raise RuntimeError(f"voices: id がありません: {json.dumps(response)[:500]}")
    voices[name] = {"id": voice_id, **design}
    sample = _find_audio(response)
    if sample:
        _to_wav(sample, OUT / f"voice_sample_{name}.wav")
    OUT.mkdir(parents=True, exist_ok=True)
    cache.write_text(json.dumps(voices, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return voice_id


def synthesize(text: str, style: str, model: str, voice: str, out_wav: Path) -> float:
    body = {
        "model": model,
        "input": [{
            "type": "user_input",
            "content": [{
                "type": "text",
                "text": text,
                "annotations": [{"type": "speech_metadata", "style": style}],
            }],
        }],
        "response_format": {"type": "audio"},
        "generation_config": {"speech_config": [{"voice": voice}]},
    }
    response = _post("interactions", body)
    audio = _find_audio(response)
    if not audio:
        raise RuntimeError(f"音声がありません: {json.dumps(response)[:800]}")
    return _to_wav(audio, out_wav)


def _fit(wav: Path, tempo: float) -> float:
    """前後の無音を 0.05 秒残して削り、tempo > 1 なら話速を上げる（ffmpeg）。秒数を返す。"""
    filters = [
        "silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.05",
        "areverse",
        "silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.05",
        "areverse",
    ]
    if tempo > 1.0:
        filters.append(f"atempo={tempo}")
    tmp = wav.with_suffix(".tmp.wav")
    build._docker(
        build.FFMPEG_IMAGE, build.HERE,
        ["-v", "error", "-y", "-i", build._container_path(wav), "-af", ",".join(filters),
         "-ar", "24000", "-ac", "1", build._container_path(tmp)],
        entrypoint="ffmpeg",
    )
    tmp.replace(wav)
    with wave.open(str(wav), "rb") as handle:
        return handle.getnframes() / handle.getframerate()


def _split(combined: Path, ratio: float, first: Path, second: Path) -> float:
    """文字数比に最も近い位置の無音（0.3 秒以上）で WAV を 2 つに切り、切断秒を返す。"""
    with wave.open(str(combined), "rb") as handle:
        params = handle.getparams()
        samples = array.array("h", handle.readframes(handle.getnframes()))
    rate = params.framerate
    window = rate // 100
    quiet = [
        max((abs(v) for v in samples[i:i + window]), default=0) < 600
        for i in range(0, len(samples), window)
    ]
    gaps: list[tuple[int, int]] = []
    start = None
    for index, flag in enumerate(quiet + [False]):
        if flag and start is None:
            start = index
        elif not flag and start is not None:
            if index - start >= 30 and start > 0 and index < len(quiet):
                gaps.append((start, index))
            start = None
    if not gaps:
        raise RuntimeError(f"{combined}: 切り分け用の無音が見つかりません")
    total = len(quiet)
    best = min(gaps, key=lambda g: abs((g[0] + g[1]) / 2 / total - ratio))
    cut = (best[0] + best[1]) // 2 * window
    for path, chunk in ((first, samples[:cut]), (second, samples[cut:])):
        with wave.open(str(path), "wb") as out:
            out.setparams(params)
            out.writeframes(chunk.tobytes())
    return round(cut / rate, 3)


def run_tts(key: str, variant: dict[str, Any], cfg: dict[str, Any], force: bool) -> dict[str, Any]:
    out_dir = OUT / key / variant["id"]
    report_path = out_dir / "narration.json"
    if report_path.is_file() and not force:
        return json.loads(report_path.read_text(encoding="utf-8"))
    texts = json.loads((build.WORK / "narration" / key / "narration.json").read_text(encoding="utf-8"))["texts"]
    voice = _designed_voice(variant["design"]) if "design" in variant else variant["voice"]
    report: dict[str, Any] = {"texts": texts, "variant": variant, "voice_id": voice, "cues": {}}
    raw: dict[str, float] = {}
    if variant.get("single_call"):
        # 2 cue を 1 回の演技で読ませ、間の無音で切り分ける（cue 間の口調のずれを防ぐ）
        combined = out_dir / "combined.wav"
        synthesize(f"{texts['problem']}\n\n{variant.get('rule_prefix', '')}{texts['rule']}", variant["style"], variant["model"], voice, combined)
        ratio = len(texts["problem"]) / (len(texts["problem"]) + len(texts["rule"]))
        report["split_at_seconds"] = _split(combined, ratio, out_dir / "problem.wav", out_dir / "rule.wav")
    for cue in ("problem", "rule"):
        wav = out_dir / f"{cue}.wav"
        if not variant.get("single_call"):
            synthesize(texts[cue], variant[f"style_{cue}"], variant["model"], voice, wav)
        raw[cue] = _fit(wav, 1.0)
    natural = raw["problem"] + cfg["gap_seconds"] + raw["rule"]
    # 予算を超える分だけ話速を上げ、target_seconds に合わせる（Polly の 125% と同じ扱い）
    tempo = max(1.0, round((natural - cfg["gap_seconds"]) / (cfg["target_seconds"] - cfg["gap_seconds"]), 3)) \
        if natural > cfg["budget_seconds"] else 1.0
    report["natural_seconds"] = round(natural, 3)
    report["tempo"] = tempo
    for cue in ("problem", "rule"):
        seconds = _fit(out_dir / f"{cue}.wav", tempo)
        report["cues"][cue] = {"seconds": round(seconds, 3), "frames": round(seconds * FPS)}
    total = report["cues"]["problem"]["seconds"] + cfg["gap_seconds"] + report["cues"]["rule"]["seconds"]
    report["total_seconds"] = round(total, 3)
    report["within_budget"] = total <= cfg["budget_seconds"]
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return report


def render_variant(key: str, variant_id: str, report: dict[str, Any]) -> Path:
    staged = f"{key}__{variant_id}"
    public_dir = build.PUBLIC_DIR / "narration" / staged
    public_dir.mkdir(parents=True, exist_ok=True)
    for cue in ("problem", "rule"):
        shutil.copy2(OUT / key / variant_id / f"{cue}.wav", public_dir / f"{cue}.wav")
    props = json.loads((build.WORK / "props" / f"{key}.json").read_text(encoding="utf-8"))
    for cue in ("problem", "rule"):
        props["narration"][cue] = {
            "file": f"narration/{staged}/{cue}.wav",
            "frames": int(report["cues"][cue]["frames"]),
        }
    props_path = OUT / key / variant_id / "props.json"
    props_path.write_text(json.dumps(props, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    raw = OUT / key / variant_id / "raw.mp4"
    final = OUT / key / f"{variant_id}.mp4"
    build.render(props_path, raw)
    build.normalize_loudness(raw, final)
    raw.unlink(missing_ok=True)
    return final


def write_page(cfg: dict[str, Any], reports: dict[str, dict[str, Any]]) -> Path:
    rows = []
    for key in cfg["problems"]:
        baseline = OUT / key / "t0-takumi.mp4"
        shutil.copy2(build.WORK / "videos" / f"{key}.mp4", baseline)
        takumi = json.loads((build.WORK / "narration" / key / "narration.json").read_text(encoding="utf-8"))
        cells = [("t0-takumi", f"Polly Takumi 125%（現行） {takumi['total_seconds']:.1f}s")]
        shown = cfg.get("compare")
        for variant in cfg["variants"]:
            if shown and variant["id"] not in shown:
                continue
            rep = reports.get(f"{key}/{variant['id']}")
            saved = OUT / key / variant["id"] / "narration.json"
            if rep is None and saved.is_file():
                rep = json.loads(saved.read_text(encoding="utf-8"))
            if rep:
                flag = "" if rep["within_budget"] else " ⚠予算超過"
                tempo = f" ×{rep['tempo']}" if rep.get("tempo", 1.0) > 1.0 else ""
                cells.append((
                    variant["id"],
                    f"{variant['id']} {rep['total_seconds']:.1f}s{tempo}{flag}｜{variant.get('label', '')}",
                ))
        videos = "".join(
            f'<figure><video controls preload="metadata" src="{key}/{vid}.mp4"></video>'
            f"<figcaption>{html.escape(label)}</figcaption></figure>"
            for vid, label in cells if (OUT / key / f"{vid}.mp4").is_file()
        )
        rows.append(f"<h2>{html.escape(key)}</h2><div class=grid>{videos}</div>")
    page = OUT / "compare.html"
    page.write_text(
        "<!doctype html><meta charset=utf-8><title>Gemini TTS 聞き比べ</title>"
        "<style>body{font-family:sans-serif;margin:16px;background:#111;color:#eee}"
        ".grid{display:flex;flex-wrap:wrap;gap:12px}figure{margin:0;width:220px}"
        "video{width:220px}figcaption{font-size:13px}</style>"
        "<h1>Gemini 3.8 Flash TTS 聞き比べ</h1>" + "".join(rows),
        encoding="utf-8",
    )
    return page


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tts-only", action="store_true")
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--variant", action="append", help="対象の variant id（既定は全部）")
    args = parser.parse_args(argv)
    cfg = json.loads((HERE / "variants.json").read_text(encoding="utf-8"))
    variants = [v for v in cfg["variants"] if not args.variant or v["id"] in args.variant]
    reports: dict[str, dict[str, Any]] = {}
    for key in cfg["problems"]:
        for variant in variants:
            rep = run_tts(key, variant, cfg, args.force)
            reports[f"{key}/{variant['id']}"] = rep
            c = rep["cues"]
            print(
                f"{key} {variant['id']}: problem {c['problem']['seconds']}s + rule "
                f"{c['rule']['seconds']}s = {rep['total_seconds']}s "
                f"{'OK' if rep['within_budget'] else 'OVER BUDGET'}"
            )
            if not args.tts_only:
                print(f"  -> {render_variant(key, variant['id'], rep)}")
    if not args.tts_only:
        print(write_page(cfg, reports))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
