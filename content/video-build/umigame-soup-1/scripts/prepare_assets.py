"""PoC 素材の正規化（PIL が要るため image-batch:ffmpeg-check コンテナで実行する）。

- 背景: imagegen 出力（9:16 近似）を 1080x1920 に中央クロップ・リサイズし JPEG q88 で保存
  （多 MB の PNG は Remotion の delayRender がタイムアウトする。pref-ranking-1 17-3 の教訓）
- キャラ: 透過 PNG の不透明 bbox を切り出し、ポーズ間で「bbox 高さ = 共通」になる倍率で
  共通キャンバス（CHAR_CANVAS）へ下端中央揃えで配置する（pref-ranking-1 の五郎と同じ方式。
  ポーズ切替でキャラが跳ねないようにする）
- BGM: 元トラック（bgm_*.m4a の 1 本目）を動画尺 20 秒ちょうどに切り出す（不足はループ）
- SE: 吹き出し出現音「ポン」を ffmpeg の sine で合成する（0.14 秒・880 + 1320 Hz。ライセンス不要）

normalized/ は git 管理外で、本スクリプトで再生成する。

使い方（リポジトリルートから）:
  docker run --rm -u $(id -u):$(id -g) -v "$PWD:/repo" -w /repo/content/video-build/umigame-soup-1 \
    --entrypoint python image-batch:ffmpeg-check scripts/prepare_assets.py poc/classic-umigame
"""

from __future__ import annotations

from pathlib import Path
import subprocess
import sys

from PIL import Image, ImageOps

BG_SIZE = (1080, 1920)
CHAR_CANVAS = (1000, 1100)
CHAR_HEIGHT = 1000  # 共通キャンバス上のキャラ bbox 高さ
GROUPS = {"master": ["master_base", "master_happy"], "assistant": ["assistant_base"]}


def prepare_background(src: Path, dst: Path) -> None:
    with Image.open(src) as image:
        rgb = image.convert("RGB")
        loss = 1 - min(rgb.width / rgb.height / (BG_SIZE[0] / BG_SIZE[1]),
                       (rgb.height / rgb.width) / (BG_SIZE[1] / BG_SIZE[0]))
        fitted = ImageOps.fit(rgb, BG_SIZE, Image.LANCZOS, centering=(0.5, 0.5))
        fitted.save(dst, "JPEG", quality=88, optimize=True)
        print(f"background: {rgb.width}x{rgb.height} -> {dst} (crop loss {loss:.1%})")


def prepare_group(src_dir: Path, dst_dir: Path, names: list[str]) -> None:
    images = {name: Image.open(src_dir / f"{name}.png").convert("RGBA") for name in names}
    boxes = {name: img.getbbox() for name, img in images.items()}
    for name in names:
        img, box = images[name], boxes[name]
        cropped = img.crop(box)
        scale = CHAR_HEIGHT / cropped.height
        resized = cropped.resize(
            (round(cropped.width * scale), CHAR_HEIGHT), Image.LANCZOS)
        canvas = Image.new("RGBA", CHAR_CANVAS, (0, 0, 0, 0))
        x = (CHAR_CANVAS[0] - resized.width) // 2
        y = CHAR_CANVAS[1] - CHAR_HEIGHT
        canvas.paste(resized, (x, y), resized)
        canvas.save(dst_dir / f"{name}.png", "PNG", optimize=True)
        print(f"{name}: bbox {box} scale {scale:.3f} -> {CHAR_CANVAS[0]}x{CHAR_CANVAS[1]} "
              f"(w {resized.width})")


def prepare_audio(src_dir: Path, dst_dir: Path) -> None:
    sources = sorted(src_dir.glob("bgm_*.m4a"))
    if not sources:
        raise SystemExit(f"BGM の元トラック（bgm_*.m4a）が {src_dir} にありません")
    subprocess.run([
        "ffmpeg", "-v", "error", "-y", "-stream_loop", "-1", "-i", str(sources[0]), "-t", "20",
        "-c:a", "aac", "-b:a", "128k", "-ar", "48000", str(dst_dir / "bgm_20s.m4a"),
    ], check=True)
    subprocess.run([
        "ffmpeg", "-v", "error", "-y",
        "-f", "lavfi", "-i", "sine=frequency=880:duration=0.14",
        "-f", "lavfi", "-i", "sine=frequency=1320:duration=0.14",
        "-filter_complex",
        "[0:a][1:a]amix=inputs=2:normalize=0,afade=t=in:st=0:d=0.005,afade=t=out:st=0.05:d=0.09,volume=0.5,aresample=48000",
        "-c:a", "pcm_s16le", str(dst_dir / "se_pop.wav"),
    ], check=True)
    print(f"audio: {sources[0].name} -> bgm_20s.m4a, se_pop.wav (synth)")


def main() -> int:
    src = Path(sys.argv[1])
    dst = src / "normalized"
    dst.mkdir(exist_ok=True)
    prepare_background(src / "background.png", dst / "background.jpg")
    for names in GROUPS.values():
        prepare_group(src, dst, names)
    prepare_audio(src, dst)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
