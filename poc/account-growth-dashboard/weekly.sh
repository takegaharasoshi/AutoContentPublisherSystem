#!/usr/bin/env bash
# アカウント成長ノートの週次処理（Windows のタスクスケジューラから wsl.exe 経由で呼ぶ）。
#
#   weekly.sh build   集計 → ページを Windows 側の作業フォルダへ書き出す
#   weekly.sh send    届くレポートを LINE へ送る
#
# 実行の記録は out/weekly.log に足していく（out/ は git 管理外）。
# 書き出し先は GROWTH_NOTE_DIR で変えられる（既定は Windows 側の growth-note フォルダ）。
set -euo pipefail

here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
repo="$(cd "$here/../.." && pwd)"
dest="${GROWTH_NOTE_DIR:-/mnt/c/Users/TakegahraWork/growth-note}"
export PATH="/usr/local/bin:/usr/bin:/bin:$PATH"

mkdir -p "$here/out"
exec >>"$here/out/weekly.log" 2>&1
echo "== $(date '+%Y-%m-%d %H:%M:%S') ${1:-}"

case "${1:-}" in
  build)
    python3 "$repo/content/insights-analysis/run_queries.py" \
      growth_account_weekly growth_post_weekly >/dev/null
    python3 "$here/build.py" --out "$dest/growth.html"
    ;;
  send)
    python3 "$here/report.py" --send
    ;;
  *)
    echo "使い方: weekly.sh build|send"
    exit 2
    ;;
esac
echo "== 完了"
