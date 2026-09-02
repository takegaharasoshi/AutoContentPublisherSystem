"""R-1-2 プロトタイプの一括実行（1 問だけ Remotion で 16 秒版を作る）。

  python scripts/prototype.py --item 85

処理の順:
  1. npm install（`node_modules` が無いときだけ。remotion-render イメージ内）
  2. フォントの配置（pref-ranking-1 の public/fonts から複製）
  3. コーチ立ち絵の取得・共通トリミング（image-batch イメージ内 / S3）
  4. props JSON の生成とイラストの配置（ホスト・ローカル DB）
  5. Remotion レンダリング（映像のみ・音声なし）
  6. 音声ミックス（image-batch イメージ内 / 現行版と同じ ffmpeg フィルタ）

R-1-4 でこの手順を build.py へ畳み込む。プロトタイプの間は S3 へも DB へも
書き戻さない（読むだけ）。
"""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

REMOTION = Path(__file__).resolve().parents[1]
BASE = REMOTION.parent
ROOT = BASE.parents[2]
WORK = REMOTION / "work"
COMPOSITION_ID = "Quiz16s"
FONT_FILES = ("NotoSansJP-Regular.otf", "NotoSansJP-Bold.otf")
FONT_SOURCE = ROOT / "content" / "video-build" / "pref-ranking-1" / "remotion" / "public" / "fonts"


def _container_path(path: Path) -> str:
    """Map a repository path onto the /repo mount used by both images."""
    return f"/repo/{path.resolve().relative_to(ROOT).as_posix()}"


def _run(command: list[str], label: str) -> None:
    """Run one step, surfacing the tail of its output when it fails."""
    print(f"\n=== {label}\n$ {' '.join(command)}", flush=True)
    completed = subprocess.run(command, capture_output=True, text=True, check=False)
    output = (completed.stdout + completed.stderr).strip()
    tail = "\n".join(output.splitlines()[-20:])
    if completed.returncode != 0:
        raise RuntimeError(f"{label} が失敗しました（{completed.returncode}）:\n{tail}")
    if tail:
        print(tail, flush=True)


def _docker(image: str, inner: list[str], *, entrypoint: str | None = None) -> list[str]:
    """Build a docker run command with the shared mounts of this repository."""
    command = [
        "docker", "run", "--rm",
        "-v", f"{ROOT}:/repo",
        "-v", f"{Path.home()}/.aws:/aws-config:ro",
        "-w", _container_path(REMOTION),
        "-e", "HOME=/tmp",
        "-e", f"S3_BUCKET_NAME={os.environ.get('S3_BUCKET_NAME', '')}",
        "-e", "AWS_SHARED_CREDENTIALS_FILE=/aws-config/credentials",
        "-e", "AWS_CONFIG_FILE=/aws-config/config",
        "-e", "AWS_DEFAULT_REGION=ap-northeast-1",
        "--user", f"{os.getuid()}:{os.getgid()}",
    ]
    if entrypoint is not None:
        command += ["--entrypoint", entrypoint]
    return command + [image] + inner


def main() -> None:
    """Render one stock item with the Remotion composition and mix its audio."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--item", type=int, required=True, help="quiz_stock_items.id")
    parser.add_argument("--skip-assets", action="store_true")
    args = parser.parse_args()

    remotion_image = os.environ.get("REMOTION_IMAGE", "remotion-render")
    ffmpeg_image = os.environ.get("FFMPEG_IMAGE", "image-batch:ffmpeg-check")

    if not (REMOTION / "node_modules").is_dir():
        _run(_docker(remotion_image, ["npm", "install", "--no-audit", "--no-fund"]),
             "npm install")

    fonts = REMOTION / "public" / "fonts"
    fonts.mkdir(parents=True, exist_ok=True)
    for name in FONT_FILES:
        if (fonts / name).is_file():
            continue
        source = FONT_SOURCE / name
        if not source.is_file():
            raise RuntimeError(f"フォントがありません: {source}（README.md 参照）")
        shutil.copyfile(source, fonts / name)
        print(f"font staged: {name}")

    if not args.skip_assets:
        _run(
            _docker(ffmpeg_image, ["scripts/fetch_assets.py"], entrypoint="python"),
            "コーチ立ち絵の取得",
        )

    _run([sys.executable, "scripts/build_props.py", "--item", str(args.item)],
         "props の生成")

    props_path = WORK / "props" / f"{args.item}.json"
    silent = WORK / "prototype" / f"{args.item}-silent.mp4"
    silent.parent.mkdir(parents=True, exist_ok=True)
    _run(
        _docker(remotion_image, [
            "npx", "remotion", "render", "src/index.ts", COMPOSITION_ID,
            _container_path(silent),
            f"--props={_container_path(props_path)}",
            "--concurrency=3", "--timeout=120000",
        ]),
        "Remotion レンダリング（映像のみ）",
    )

    manifest = json.loads((BASE / "work" / "build_manifest.json").read_text("utf-8"))
    entry = manifest.get(str(args.item))
    if entry is None:
        raise RuntimeError(f"build_manifest.json に台帳がありません: id={args.item}")
    output = WORK / "prototype" / f"{args.item}.mp4"
    _run(
        _docker(ffmpeg_image, [
            "scripts/mix_audio.py",
            "--video", _container_path(silent),
            "--bgm-key", entry["bgm_s3_key"],
            "--output", _container_path(output),
        ], entrypoint="python"),
        "音声ミックス",
    )

    print(f"\n新版 (Remotion): {output}")
    print(f"現行版 (Pillow+ffmpeg): {BASE / 'work' / 'videos' / f'{args.item}.mp4'}")


if __name__ == "__main__":
    main()
