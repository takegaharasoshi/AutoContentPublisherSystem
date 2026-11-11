#!/usr/bin/env bash
# スマホ閲覧用の配信サーバー（serve-docs.sh の 4 インスタンス）を自動で立ち上げて見張る。
#
# Windows のタスク スケジューラ「ACPS docs autostart」（ログオン時 + 10 分おき）が
# `wsl.exe -d Ubuntu-20.04 -- <このスクリプト>` で起動する。WSL が再起動して
# サーバーが落ちても、次の起動で戻る。常駐して 5 分おきに各ポートを確認し、
# 止まったものだけ起動し直す。常駐している間は wsl.exe のセッションが残るため、
# WSL がアイドルで自動停止しない。
#
# 配信するポートとルートは下の INSTANCES が正（スキル docs-mobile-view の 2.5 節の一覧と揃える）。
set -uo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
LOCK_FILE="/tmp/acps-docs-autostart.lock"
LOG_FILE="/tmp/acps-docs-autostart.log"
CHECK_INTERVAL_SEC=300

# "ポート 配信ルート（リポジトリルートからの相対パス）"
INSTANCES=(
  "8765 docs"
  "8766 content/video-build/logic-training-1/work"
  "8767 content/umigame-stock/umigame-soup-1/batch-01"
  "8768 content/video-build/umigame-soup-1/work"
)

# 二重起動を防ぐ（タスクの 10 分おきの起動は、常駐中ならここで終わる）
exec 9>"$LOCK_FILE"
flock -n 9 || exit 0

log() {
  echo "$(date '+%F %T') $*" >>"$LOG_FILE"
}

is_listening() {
  ss -ltn "sport = :$1" 2>/dev/null | grep -q LISTEN
}

ensure_all() {
  local entry port root
  for entry in "${INSTANCES[@]}"; do
    port="${entry%% *}"
    root="${REPO_ROOT}/${entry#* }"
    is_listening "$port" && continue
    # WSL の再起動をまたいだ古い pid ファイルが別プロセスに当たらないよう消してから起動する
    rm -f "/tmp/acps-docs-server-${port}.pid"
    if DOCS_PORT="$port" DOCS_ROOT="$root" "${REPO_ROOT}/tools/serve-docs.sh" start >/dev/null 2>&1; then
      log "port ${port} を起動しました (root=${root})"
    else
      log "port ${port} の起動に失敗しました。/tmp/acps-docs-server-${port}.log を参照"
    fi
  done
}

log "見張りを開始しました (pid=$$)"
while true; do
  ensure_all
  sleep "$CHECK_INTERVAL_SEC"
done
