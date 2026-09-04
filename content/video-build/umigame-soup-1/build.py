"""umigame-soup-1 PoC ビルド（21-2）。

1 問分の素材ディレクトリ（poc/<content_key>/）から完成版リール MP4 を 1 本作る。
Remotion と ffmpeg は Docker で実行し（WSL に Chrome の共有ライブラリと ffmpeg が無い）、
本スクリプト自体は WSL ホストの Python 3 で動く。既存 2 セットの build.py と同じ経路。

工程:
  1. 素材を remotion/public/ へ配置（フォントは pref-ranking-1 の public/fonts から、
     背景・キャラ・音源は poc/<key>/normalized から、ナレーションは poc/<key>/narration/speaker<id> から）
  2. ナレーション実測長の予算検査（NARRATION_DEADLINE までに終わらなければエラー）→ props JSON
  3. docker run remotion-render npx remotion render → work/out/<key>.raw.mp4
  4. docker run image-batch:ffmpeg-check normalize_loudness.py（pref-ranking-1 のスクリプトを流用）→ work/videos/<key>.mp4
  5. 各カット 1 枚の静止フレーム（ffmpeg で最終 MP4 から抽出）→ work/stills/<key>_<label>.jpg
  6. ffprobe（寸法・尺・音声トラック）→ work/probe/<key>.txt に保存し標準出力へ
  7. work/review.html（動画 + 静止フレーム + 素材一覧）

使い方（このディレクトリで）:
  python build.py classic-umigame --speaker 11
"""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
REMOTION_DIR = HERE / "remotion"
PUBLIC_DIR = REMOTION_DIR / "public"
WORK_DIR = HERE / "work"
PREF_DIR = HERE.parent / "pref-ranking-1"
FONT_SOURCE = PREF_DIR / "remotion" / "public" / "fonts"
FONT_FILES = ("ZenKakuGothicNew-Black.ttf", "ZenKakuGothicNew-Bold.ttf", "ZenKakuGothicNew-Medium.ttf")
NORMALIZE_SCRIPT = PREF_DIR / "remotion" / "scripts" / "normalize_loudness.py"

REMOTION_IMAGE = os.environ.get("REMOTION_IMAGE", "remotion-render")
FFMPEG_IMAGE = os.environ.get("FFMPEG_IMAGE", "image-batch:ffmpeg-check")
COMPOSITION_ID = "UmigameReel20s"

# remotion/src/timeline.ts と同じ値（tests/test_timeline_sync.py で同期を検査する）
FPS = 30
TOTAL_FRAMES = 600
NARRATION_START = 15
NARRATION_GAP = 15
NARRATION_DEADLINE = 510

# レビュー用の静止フレーム（各カット 1 枚 + 継ぎ目の前後）
STILL_FRAMES = {
    "intro": 45,
    "q1": 120,
    "a1": 180,
    "q2": 240,
    "a2": 300,
    "q3": 360,
    "a3": 420,
    "outro": 500,
    "seam_tail": 594,
}


def _container_path(path: Path) -> str:
    return "/repo/" + str(path.resolve().relative_to(ROOT))


def _docker(image: str, workdir: Path, args: list[str], *, entrypoint: str | None = None) -> None:
    command = [
        "docker", "run", "--rm",
        "-v", f"{ROOT}:/repo",
        "-w", _container_path(workdir),
        "-e", "HOME=/tmp",
        "--user", f"{os.getuid()}:{os.getgid()}",
    ]
    if entrypoint:
        command += ["--entrypoint", entrypoint]
    command += [image, *args]
    print("+", " ".join(command), flush=True)
    subprocess.run(command, check=True)


def stage_assets(item_dir: Path, key: str, speaker: int) -> dict[str, object]:
    """素材を public/ に配置し、props に書くパス（public 相対）を返す。"""
    normalized = item_dir / "normalized"
    narration_dir = item_dir / "narration" / f"speaker{speaker}"
    if not narration_dir.exists():
        raise SystemExit(f"ナレーションがありません: {narration_dir}（scripts/narration.py を先に実行）")

    for sub in ("fonts", "bg", "char", "audio", f"narration/{key}"):
        (PUBLIC_DIR / sub).mkdir(parents=True, exist_ok=True)
    for name in FONT_FILES:
        shutil.copy2(FONT_SOURCE / name, PUBLIC_DIR / "fonts" / name)
    shutil.copy2(normalized / "background.jpg", PUBLIC_DIR / "bg" / f"{key}.jpg")
    for name in ("master_base", "master_happy", "assistant_base"):
        shutil.copy2(normalized / f"{name}.png", PUBLIC_DIR / "char" / f"{name}.png")
    shutil.copy2(normalized / "bgm_20s.m4a", PUBLIC_DIR / "audio" / "bgm.m4a")
    shutil.copy2(normalized / "se_pop.wav", PUBLIC_DIR / "audio" / "se_pop.wav")
    for cue in ("problem", "rule"):
        shutil.copy2(narration_dir / f"{cue}.wav", PUBLIC_DIR / "narration" / key / f"{cue}.wav")

    report = json.loads((narration_dir / "narration.json").read_text(encoding="utf-8"))
    return {
        "background": f"bg/{key}.jpg",
        "master_base": "char/master_base.png",
        "master_happy": "char/master_happy.png",
        "assistant_base": "char/assistant_base.png",
        "bgm": "audio/bgm.m4a",
        "se": "audio/se_pop.wav",
        "narration": {
            cue: {"file": f"narration/{key}/{cue}.wav", "frames": report["cues"][cue]["frames"]}
            for cue in ("problem", "rule")
        },
        "engine_id": report["engine_id"],
    }


def build_props(problem: dict, key: str, characters: dict, assets: dict) -> dict:
    narration = assets["narration"]
    rule_start = NARRATION_START + narration["problem"]["frames"] + NARRATION_GAP
    end = rule_start + narration["rule"]["frames"]
    print(
        f"narration: problem {narration['problem']['frames']}f + gap {NARRATION_GAP}f + "
        f"rule {narration['rule']['frames']}f → 終了フレーム {end} / 期限 {NARRATION_DEADLINE} "
        f"({end / FPS:.2f}s) [{assets['engine_id']}]"
    )
    if end > NARRATION_DEADLINE:
        raise SystemExit(f"ナレーションが期限フレーム {NARRATION_DEADLINE} を超えています（{end}）。文言を短くしてください")
    play = problem["play_example"]
    if len(play) != 6:
        raise SystemExit("play_example は質問 → 返答 × 3 往復（6 件）にしてください")
    chars = characters["characters"]
    return {
        "contentKey": key,
        "hook": problem["hook"],
        "problemText": problem["problem_text"],
        "ruleText": problem["rule_text"],
        "background": assets["background"],
        "master": {"name": chars["master"]["adopted_name"], "base": assets["master_base"], "happy": assets["master_happy"]},
        "assistant": {"name": chars["assistant"]["adopted_name"], "base": assets["assistant_base"]},
        "masterLines": problem["master_lines"],
        "playExample": [{"role": p["role"], "text": p["text"]} for p in play],
        "narration": narration,
        "bgm": assets["bgm"],
        "bubbleSe": assets["se"],
    }


def render(props_path: Path, raw_path: Path) -> None:
    raw_path.parent.mkdir(parents=True, exist_ok=True)
    _docker(REMOTION_IMAGE, REMOTION_DIR, [
        "npx", "remotion", "render", "src/index.ts", COMPOSITION_ID, _container_path(raw_path),
        f"--props={_container_path(props_path)}", "--concurrency=3", "--timeout=120000",
    ])


def normalize(raw_path: Path, final_path: Path) -> None:
    final_path.parent.mkdir(parents=True, exist_ok=True)
    _docker(FFMPEG_IMAGE, HERE, [
        _container_path(NORMALIZE_SCRIPT), _container_path(raw_path), _container_path(final_path),
    ], entrypoint="python")


def extract_stills(final_path: Path, key: str) -> dict[str, Path]:
    stills_dir = WORK_DIR / "stills"
    stills_dir.mkdir(parents=True, exist_ok=True)
    out: dict[str, Path] = {}
    for label, frame in STILL_FRAMES.items():
        path = stills_dir / f"{key}_{label}.jpg"
        _docker(FFMPEG_IMAGE, HERE, [
            "-v", "error", "-y", "-i", _container_path(final_path),
            "-vf", f"select=eq(n\\,{frame})", "-frames:v", "1", "-q:v", "3", _container_path(path),
        ], entrypoint="ffmpeg")
        out[label] = path
    return out


def probe(final_path: Path, key: str) -> str:
    probe_dir = WORK_DIR / "probe"
    probe_dir.mkdir(parents=True, exist_ok=True)
    command = [
        "docker", "run", "--rm", "-v", f"{ROOT}:/repo", "--user", f"{os.getuid()}:{os.getgid()}",
        "--entrypoint", "ffprobe", FFMPEG_IMAGE, "-v", "error",
        "-show_entries", "stream=index,codec_type,codec_name,width,height,r_frame_rate,sample_rate,channels:format=duration,size",
        "-of", "default=noprint_wrappers=1", _container_path(final_path),
    ]
    result = subprocess.run(command, check=True, capture_output=True, text=True)
    (probe_dir / f"{key}.txt").write_text(result.stdout, encoding="utf-8")
    return result.stdout


def write_review(key: str, item_dir: Path, props: dict, final_path: Path, stills: dict[str, Path], probe_text: str) -> Path:
    def rel(path: Path) -> str:
        return os.path.relpath(path, WORK_DIR)

    still_cards = "".join(
        f'<figure><img src="{rel(path)}" alt="{label}"><figcaption>{label} (frame {STILL_FRAMES[label]})</figcaption></figure>'
        for label, path in stills.items()
    )
    play = "".join(f"<li><b>{p['role']}</b>: {p['text']}</li>" for p in props["playExample"])
    html = f"""<!DOCTYPE html><html lang="ja"><head><meta charset="utf-8"><title>umigame-soup-1 PoC review: {key}</title>
<style>body{{font-family:sans-serif;margin:24px;background:#111;color:#eee}}video{{width:360px;border:1px solid #555}}
.stills{{display:flex;flex-wrap:wrap;gap:12px}}figure{{margin:0;width:216px}}figure img{{width:216px;border:1px solid #555}}
figcaption{{font-size:12px;color:#aaa}}pre{{background:#222;padding:12px;overflow:auto}}section{{margin-bottom:32px}}</style></head><body>
<h1>umigame-soup-1 PoC: {key}</h1>
<section><h2>完成版 MP4</h2><video controls loop src="{rel(final_path)}"></video><pre>{probe_text}</pre></section>
<section><h2>静止フレーム（各カット 1 枚）</h2><div class="stills">{still_cards}</div></section>
<section><h2>版面の文言</h2><p><b>フック</b>: {props['hook']}</p><p><b>問題文</b>: {props['problemText']}</p><p><b>ルール帯</b>: {props['ruleText']}</p>
<p><b>導入</b>: {props['masterLines']['intro']} / <b>締め</b>: {props['masterLines']['outro']}</p><ol>{play}</ol></section>
<section><h2>素材</h2><p>{rel(item_dir)}/ の problem.json / characters.json / normalized/ / narration/ を参照</p></section>
</body></html>"""
    review = WORK_DIR / "review.html"
    review.write_text(html, encoding="utf-8")
    return review


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("content_key")
    parser.add_argument("--speaker", type=int, default=11, help="VOICEVOX 話者スタイル ID（既定 11 = 玄野武宏 ノーマル）")
    parser.add_argument("--skip-render", action="store_true", help="props 生成までで止める")
    args = parser.parse_args()

    key = args.content_key
    item_dir = HERE / "poc" / key
    problem = json.loads((item_dir / "problem.json").read_text(encoding="utf-8"))
    characters = json.loads((item_dir / "characters.json").read_text(encoding="utf-8"))

    assets = stage_assets(item_dir, key, args.speaker)
    props = build_props(problem, key, characters, assets)
    props_path = WORK_DIR / "props" / f"{key}.json"
    props_path.parent.mkdir(parents=True, exist_ok=True)
    props_path.write_text(json.dumps(props, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"props: {props_path}")
    if args.skip_render:
        return 0

    raw_path = WORK_DIR / "out" / f"{key}.raw.mp4"
    final_path = WORK_DIR / "videos" / f"{key}.mp4"
    render(props_path, raw_path)
    normalize(raw_path, final_path)
    stills = extract_stills(final_path, key)
    probe_text = probe(final_path, key)
    print("ffprobe:\n" + probe_text)
    review = write_review(key, item_dir, props, final_path, stills, probe_text)
    print(f"video: {final_path}\nstills: {WORK_DIR / 'stills'}\nreview: {review}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
