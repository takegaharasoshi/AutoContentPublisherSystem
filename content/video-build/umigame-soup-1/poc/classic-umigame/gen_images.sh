#!/usr/bin/env bash
# PoC 用: Codex CLI の image_gen.imagegen ツールでイラストを生成する（1 枚ずつ）。
# 使い方: bash gen_images.sh <name> "<prompt>"   → ./<name>.png
set -euo pipefail
name="$1"; prompt="$2"
here="$(cd "$(dirname "$0")" && pwd)"
timeout 600 codex exec --sandbox workspace-write -C "$here" \
  "Use the image_gen.imagegen tool to generate ONE image with exactly this prompt, then save it as $name.png in the current directory and reply only with the saved path. Prompt: $prompt" \
  > "$here/work_gen_$name.log" 2>&1
ls -la "$here/$name.png"
