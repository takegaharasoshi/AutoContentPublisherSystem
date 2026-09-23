#!/usr/bin/env bash
# 背景イラストを Codex CLI の image_gen.imagegen ツールで生成する（工程 3。umigame-prebuilt.html 8.1）。
# 入力: work/prompts/<content_key>.txt（export_prompts.py の出力）
# 出力: work/backgrounds/raw/<content_key>.png（生成済みはスキップ。作り直すときはファイルを消す）
# 使い方: bash scripts/gen_backgrounds.sh [content_key ...]   （既定: 全プロンプト）
#   並列数は JOBS（既定 3）。生成 1 枚 1〜2 分。ログは work/backgrounds/logs/。
set -euo pipefail
here="$(cd "$(dirname "$0")/.." && pwd)"
prompts="$here/work/prompts"
out="$here/work/backgrounds/raw"
logs="$here/work/backgrounds/logs"
mkdir -p "$out" "$logs"
jobs="${JOBS:-3}"

if [ "$#" -gt 0 ]; then keys=("$@"); else
  keys=(); for f in "$prompts"/*.txt; do keys+=("$(basename "$f" .txt)"); done
fi

gen_one() {
  local key="$1"
  if [ -s "$out/$key.png" ]; then echo "skip $key"; return 0; fi
  local prompt; prompt="$(cat "$prompts/$key.txt")"
  # stdin を閉じる（codex exec が入力待ちで止まるのを防ぐ）
  if timeout 900 codex exec --sandbox workspace-write -C "$out" \
      "Use the image_gen.imagegen tool to generate ONE image with exactly this prompt, then save it as $key.png in the current directory and reply only with the saved path. Prompt: $prompt" \
      < /dev/null > "$logs/$key.log" 2>&1 && [ -s "$out/$key.png" ]; then
    echo "ok   $key"
  else
    echo "FAIL $key（ログ: $logs/$key.log）"
  fi
}
export -f gen_one
export prompts out logs
printf '%s\n' "${keys[@]}" | xargs -P "$jobs" -I{} bash -c 'gen_one "$@"' _ {}
