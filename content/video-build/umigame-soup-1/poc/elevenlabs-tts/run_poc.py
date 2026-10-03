"""ElevenLabs v4 の聞き比べ PoC（21-5d・アイデア umigame-tts-elevenlabs-v4）。

承認済みの props（``work/props/<key>.json``）のナレーションだけを ElevenLabs の音声に
差し替え、本番と同じ Remotion コンポジションで比較用動画を ``out/`` に描き出す。
``work/videos`` など承認済みの成果物には書き込まない。① は現行 Irodori のビルドをそのまま使う。

使い方::

    python3 poc/elevenlabs-tts/run_poc.py --design-only  # Voice Design の候補だけ作る
    python3 poc/elevenlabs-tts/run_poc.py                # 声の用意 + 合成 + レンダリング + 比較ページ
    python3 poc/elevenlabs-tts/run_poc.py --tts-only     # 合成と尺の実測だけ
    python3 poc/elevenlabs-tts/run_poc.py --force        # 既存の合成結果を捨てて取り直す

Voice Design で使う候補は ``variants.json`` の ``design.pick``（``<版 id>-<候補番号>``）で選び、
variant ごとに ``design_pick`` で上書きできる。
作った声の ID と説明文は ``voices.lock.json``（git 管理）に残す。
API キーは環境変数 ``ELEVENLABS_API_KEY`` か ``~/.config/elevenlabs/api_key`` から読む。
"""

from __future__ import annotations

import argparse
import base64
import html
import importlib.util
import json
import os
from pathlib import Path
import shutil
import sys
from typing import Any
import wave

import requests

HERE = Path(__file__).resolve().parent
SET_DIR = HERE.parents[1]
sys.path.insert(0, str(SET_DIR))

import build  # noqa: E402

# 無音での切り分けと尺合わせは Gemini の PoC と同じ処理を使う
_spec = importlib.util.spec_from_file_location("gemini_poc", HERE.parent / "gemini-tts" / "run_poc.py")
gemini_poc = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(gemini_poc)  # type: ignore[union-attr]

API_BASE = "https://api.elevenlabs.io/v1"
OUT = HERE / "out"
LOCK = HERE / "voices.lock.json"
FPS = 30


def _api_key() -> str:
    key = os.environ.get("ELEVENLABS_API_KEY")
    if key:
        return key.strip()
    path = Path.home() / ".config" / "elevenlabs" / "api_key"
    if path.is_file():
        return path.read_text(encoding="utf-8").strip()
    raise SystemExit("ELEVENLABS_API_KEY も ~/.config/elevenlabs/api_key もありません")


def _request(method: str, path: str, **kwargs: Any) -> requests.Response:
    response = requests.request(
        method, f"{API_BASE}/{path}", headers={"xi-api-key": _api_key()}, timeout=300, **kwargs
    )
    if response.status_code >= 400:
        raise RuntimeError(f"{path}: HTTP {response.status_code}: {response.text[:2000]}")
    return response


def used_credits() -> int:
    """今期の消費クレジット（subscription.character_count）を返す。"""
    return int(_request("GET", "user/subscription").json()["character_count"])


def _load_lock() -> dict[str, Any]:
    return json.loads(LOCK.read_text(encoding="utf-8")) if LOCK.is_file() else {}


def _save_lock(lock: dict[str, Any]) -> None:
    LOCK.write_text(json.dumps(lock, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _narration_texts(key: str) -> dict[str, str]:
    path = build.WORK / "narration" / key / "narration.json"
    return json.loads(path.read_text(encoding="utf-8"))["texts"]


def clone_voice(cfg: dict[str, Any], credits: dict[str, int]) -> str:
    lock = _load_lock()
    if "clone" in lock:
        return lock["clone"]["voice_id"]
    spec = cfg["clone"]
    files_dir = SET_DIR / spec["files_dir"]
    paths = sorted(files_dir.glob("*.wav"))
    before = used_credits()
    handles = [("files", (p.name, p.open("rb"), "audio/wav")) for p in paths]
    try:
        response = _request(
            "POST", "voices/add",
            data={"name": spec["name"], "description": spec["description"], "remove_background_noise": "false"},
            files=handles,
        ).json()
    finally:
        for _, (_, handle, _) in handles:
            handle.close()
    credits["clone"] = used_credits() - before
    lock["clone"] = {
        "voice_id": response["voice_id"],
        "name": spec["name"],
        "description": spec["description"],
        "reference_files": [p.name for p in paths],
    }
    _save_lock(lock)
    return response["voice_id"]


def design_previews(cfg: dict[str, Any], credits: dict[str, int]) -> dict[str, Any]:
    """説明文の版ごとに Voice Design の候補を作り、試聴音声を out/design/ に残す。"""
    cache = OUT / "design" / "previews.json"
    previews = json.loads(cache.read_text(encoding="utf-8")) if cache.is_file() else {}
    spec = cfg["design"]
    texts = _narration_texts(spec["preview_problem"])
    text = f"{texts['problem']}{texts['rule']}"
    for version in spec["versions"]:
        if version["id"] in previews:
            continue
        before = used_credits()
        response = _request("POST", "text-to-voice/design", json={
            "voice_description": version["description"],
            "model_id": spec["model_id"],
            "text": text,
        }).json()
        credits[f"design_{version['id']}"] = used_credits() - before
        items = []
        for index, preview in enumerate(response["previews"]):
            ext = "mp3" if "mpeg" in str(preview.get("media_type", "mpeg")) else "wav"
            audio = OUT / "design" / f"{version['id']}-{index}.{ext}"
            audio.parent.mkdir(parents=True, exist_ok=True)
            audio.write_bytes(base64.b64decode(preview["audio_base_64"]))
            items.append({
                "candidate": f"{version['id']}-{index}",
                "generated_voice_id": preview["generated_voice_id"],
                "file": audio.name,
                "duration_secs": preview.get("duration_secs"),
            })
        previews[version["id"]] = {"description": version["description"], "candidates": items}
        cache.write_text(json.dumps(previews, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return previews


def designed_voice(cfg: dict[str, Any], previews: dict[str, Any], credits: dict[str, int], pick: str) -> str:
    """Voice Design の候補 pick を保存して voice_id を返す（保存済みならそれを使う）。"""
    lock = _load_lock()
    if pick in lock.get("designs", {}):
        return lock["designs"][pick]["voice_id"]
    version_id = pick.rsplit("-", 1)[0]
    version = previews[version_id]
    candidate = next(c for c in version["candidates"] if c["candidate"] == pick)
    before = used_credits()
    response = _request("POST", "text-to-voice", json={
        "voice_name": f"kamerock-design-{pick}",
        "voice_description": version["description"],
        "generated_voice_id": candidate["generated_voice_id"],
    }).json()
    credits[f"design_save_{pick}"] = used_credits() - before
    lock.setdefault("designs", {})[pick] = {
        "voice_id": response["voice_id"],
        "candidate": pick,
        "model_id": cfg["design"]["model_id"],
        "description": version["description"],
        "preview_text_problem": cfg["design"]["preview_problem"],
    }
    _save_lock(lock)
    return response["voice_id"]


def synthesize(text: str, voice_id: str, model_id: str, cfg: dict[str, Any], out_wav: Path) -> int:
    """1 回の合成で out_wav（24 kHz mono）を作り、消費クレジットを返す。

    subscription.character_count は反映が遅れるため、レスポンスヘッダー
    ``x-character-count`` を使う（無いときは送った文字数）。
    """
    response = _request(
        "POST", f"text-to-speech/{voice_id}",
        params={"output_format": cfg["output_format"]},
        json={
            "text": text,
            "model_id": model_id,
            "language_code": cfg["language_code"],
            "voice_settings": cfg["voice_settings"],
            "seed": cfg["seed"],
        },
    )
    out_wav.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(out_wav), "wb") as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(24000)
        wav.writeframes(response.content)
    return int(response.headers.get("x-character-count") or len(text))


def run_tts(key: str, variant: dict[str, Any], voice_id: str, cfg: dict[str, Any], force: bool) -> dict[str, Any]:
    out_dir = OUT / key / variant["id"]
    report_path = out_dir / "narration.json"
    if report_path.is_file() and not force:
        return json.loads(report_path.read_text(encoding="utf-8"))
    texts = _narration_texts(key)
    # 問題文とルール文を 1 回の演技で読ませ、間の無音で切り分ける（21-5c と同じ）
    # v3 は日本語の音声タグを読み上げるため、variant 側で英語のタグに差し替えられるようにする
    direction = variant.get("direction", cfg["direction"])
    rule_direction = variant.get("rule_direction", cfg["rule_direction"])
    text = f"{direction} {texts['problem']}\n\n{rule_direction} {texts['rule']}"
    combined = out_dir / "combined.wav"
    spent = synthesize(text, voice_id, variant["model_id"], cfg, combined)
    ratio = len(texts["problem"]) / (len(texts["problem"]) + len(texts["rule"]))
    report: dict[str, Any] = {
        "texts": texts, "request_text": text, "variant": variant, "voice_id": voice_id,
        "credits": spent, "cues": {},
    }
    report["split_at_seconds"] = gemini_poc._split(combined, ratio, out_dir / "problem.wav", out_dir / "rule.wav")
    raw = {cue: gemini_poc._fit(out_dir / f"{cue}.wav", 1.0) for cue in ("problem", "rule")}
    natural = raw["problem"] + cfg["gap_seconds"] + raw["rule"]
    # 予算を超える分だけ話速を上げ、target_seconds に合わせる（21-5c と同じ扱い）
    tempo = max(1.0, round((natural - cfg["gap_seconds"]) / (cfg["target_seconds"] - cfg["gap_seconds"]), 3)) \
        if natural > cfg["budget_seconds"] else 1.0
    report["natural_seconds"] = round(natural, 3)
    report["tempo"] = tempo
    for cue in ("problem", "rule"):
        seconds = gemini_poc._fit(out_dir / f"{cue}.wav", tempo) if tempo > 1.0 else raw[cue]
        report["cues"][cue] = {"seconds": round(seconds, 3), "frames": round(seconds * FPS)}
    total = report["cues"]["problem"]["seconds"] + cfg["gap_seconds"] + report["cues"]["rule"]["seconds"]
    report["total_seconds"] = round(total, 3)
    report["within_budget"] = total <= cfg["budget_seconds"]
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return report


def render_variant(key: str, variant_id: str, report: dict[str, Any]) -> Path:
    staged = f"{key}__el-{variant_id}"
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


def baseline(key: str, variant: dict[str, Any]) -> dict[str, Any]:
    """① 現行 Irodori: 承認済みの動画と尺をそのまま使う。"""
    final = OUT / key / f"{variant['id']}.mp4"
    final.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(build.WORK / "videos" / f"{key}.mp4", final)
    current = json.loads((build.WORK / "narration" / key / "narration.json").read_text(encoding="utf-8"))
    return {
        "total_seconds": current["total_seconds"], "tempo": current.get("tempo") or 1.0,
        "credits": 0, "within_budget": current["total_seconds"] <= 21.0,
    }


def write_page(cfg: dict[str, Any], reports: dict[str, dict[str, Any]], previews: dict[str, Any]) -> Path:
    rows = []
    for key in cfg["problems"]:
        figures = []
        for variant in cfg["variants"]:
            rep = reports.get(f"{key}/{variant['id']}")
            saved = OUT / key / variant["id"] / "narration.json"
            if rep is None and variant.get("baseline"):
                rep = baseline(key, variant)
            elif rep is None and saved.is_file():
                rep = json.loads(saved.read_text(encoding="utf-8"))
            if not rep or not (OUT / key / f"{variant['id']}.mp4").is_file():
                continue
            tempo = f" ×{rep['tempo']}" if rep["tempo"] > 1.0 else ""
            flag = "" if rep["within_budget"] else " ⚠予算超過"
            caption = f"{variant['label']}｜{rep['total_seconds']:.1f}s{tempo}{flag}"
            figures.append(
                f'<figure><video controls preload="metadata" src="{key}/{variant["id"]}.mp4"></video>'
                f"<figcaption>{html.escape(caption)}</figcaption></figure>"
            )
        rows.append(f"<h2>{html.escape(key)}</h2><div class=grid>{''.join(figures)}</div>")
    picks = {v.get("design_pick", cfg["design"]["pick"]) for v in cfg["variants"] if v.get("voice") == "design"}
    design_rows = []
    for version_id, version in previews.items():
        audios = "".join(
            f"<li>{'★ ' if c['candidate'] in picks else ''}{html.escape(c['candidate'])} "
            f'<audio controls preload="none" src="design/{c["file"]}"></audio></li>'
            for c in version["candidates"]
        )
        design_rows.append(
            f"<h3>{html.escape(version_id)}</h3><p class=desc>{html.escape(version['description'])}</p><ul>{audios}</ul>"
        )
    page = OUT / "compare.html"
    page.write_text(
        "<!doctype html><meta charset=utf-8><meta name=viewport content='width=device-width'>"
        "<title>ElevenLabs 聞き比べ</title>"
        "<style>body{font-family:sans-serif;margin:16px;background:#111;color:#eee}"
        ".grid{display:flex;flex-wrap:wrap;gap:12px}figure{margin:0;width:220px}"
        "video{width:220px}figcaption{font-size:13px}.desc{font-size:13px;color:#bbb}"
        "ul{list-style:none;padding:0}li{margin:4px 0}</style>"
        "<h1>ElevenLabs v4 聞き比べ（21-5d）</h1>" + "".join(rows)
        + "<h2>Voice Design の候補（★ = 動画に使った候補）</h2>" + "".join(design_rows),
        encoding="utf-8",
    )
    return page


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--design-only", action="store_true")
    parser.add_argument("--tts-only", action="store_true")
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--variant", action="append", help="対象の variant id（既定は全部）")
    args = parser.parse_args(argv)
    cfg = json.loads((HERE / "variants.json").read_text(encoding="utf-8"))
    credits: dict[str, int] = {}
    previews = design_previews(cfg, credits)
    if args.design_only:
        print(json.dumps(credits, ensure_ascii=False))
        return 0
    clone_id = clone_voice(cfg, credits)
    variants = [v for v in cfg["variants"] if not args.variant or v["id"] in args.variant]
    reports: dict[str, dict[str, Any]] = {}
    for key in cfg["problems"]:
        for variant in variants:
            if variant.get("baseline"):
                rep = baseline(key, variant)
            else:
                if variant["voice"] == "clone":
                    voice_id = clone_id
                else:
                    pick = variant.get("design_pick", cfg["design"]["pick"])
                    voice_id = designed_voice(cfg, previews, credits, pick)
                rep = run_tts(key, variant, voice_id, cfg, args.force)
            reports[f"{key}/{variant['id']}"] = rep
            print(
                f"{key} {variant['id']}: total {rep['total_seconds']}s tempo x{rep['tempo']} "
                f"credits {rep['credits']} {'OK' if rep['within_budget'] else 'OVER BUDGET'}"
            )
            if not args.tts_only and not variant.get("baseline"):
                print(f"  -> {render_variant(key, variant['id'], rep)}")
    print(f"setup credits: {json.dumps(credits, ensure_ascii=False)}")
    print(f"used this period: {used_credits()}")
    if not args.tts_only:
        print(write_page(cfg, reports, previews))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
