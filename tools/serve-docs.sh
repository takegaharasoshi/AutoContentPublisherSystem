#!/usr/bin/env bash
# 設計書（docs/）を Tailscale 経由でスマホから閲覧できるように配信する。
#
#   tools/serve-docs.sh start    配信開始（WSL の HTTP サーバー + Windows の tailscale serve）
#   tools/serve-docs.sh stop     配信停止（tailscale serve の公開設定も解除）
#   tools/serve-docs.sh status   稼働状況と閲覧 URL を表示
#
# 前提: Windows 側に Tailscale がインストール済みでログイン済みであること。
# WSL からは localhost 転送（Windows → WSL）を利用するため、サーバーは 127.0.0.1 に bind する。
set -euo pipefail

PORT="${DOCS_PORT:-8765}"
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PID_FILE="/tmp/acps-docs-server-${PORT}.pid"
LOG_FILE="/tmp/acps-docs-server-${PORT}.log"
TAILSCALE="/mnt/c/Program Files/Tailscale/tailscale.exe"

is_running() {
  [[ -f "$PID_FILE" ]] && kill -0 "$(cat "$PID_FILE")" 2>/dev/null
}

require_tailscale() {
  if [[ ! -x "$TAILSCALE" ]]; then
    echo "エラー: Windows 側の Tailscale が見つかりません: $TAILSCALE" >&2
    exit 1
  fi
}

print_urls() {
  local host
  host="$("$TAILSCALE" status --json 2>/dev/null | python3 -c \
    'import json,sys; print(json.load(sys.stdin)["Self"]["DNSName"].rstrip("."))' 2>/dev/null || true)"
  echo
  echo "スマホ（同じ Tailscale アカウント）から次の URL を開く:"
  if [[ -n "$host" ]]; then
    echo "  http://${host}:${PORT}/"
    echo "  http://${host%%.*}:${PORT}/   （MagicDNS の短い名前）"
  else
    echo "  http://<このPCのTailscale名>:${PORT}/"
  fi
}

start() {
  require_tailscale
  if is_running; then
    echo "HTTP サーバーは既に稼働中です (pid=$(cat "$PID_FILE"), port=${PORT})"
  else
    nohup python3 "${REPO_ROOT}/tools/docs_server.py" --port "$PORT" --bind 127.0.0.1 \
      >"$LOG_FILE" 2>&1 &
    echo $! >"$PID_FILE"
    sleep 1
    if ! is_running; then
      echo "エラー: HTTP サーバーの起動に失敗しました。ログ: $LOG_FILE" >&2
      cat "$LOG_FILE" >&2
      exit 1
    fi
    echo "HTTP サーバーを起動しました (pid=$(cat "$PID_FILE"), port=${PORT})"
  fi

  # tailscale serve の設定は tailscaled 側に永続化されるため、再実行しても冪等。
  "$TAILSCALE" serve --bg --http="${PORT}" "http://127.0.0.1:${PORT}" >/dev/null
  echo "tailscale serve を設定しました（tailnet 内のみ公開・インターネット非公開）"
  print_urls
}

stop() {
  if is_running; then
    kill "$(cat "$PID_FILE")"
    echo "HTTP サーバーを停止しました (pid=$(cat "$PID_FILE"))"
  else
    echo "HTTP サーバーは稼働していません"
  fi
  rm -f "$PID_FILE"
  if [[ -x "$TAILSCALE" ]]; then
    "$TAILSCALE" serve --http="${PORT}" off >/dev/null 2>&1 || true
    echo "tailscale serve の公開設定を解除しました"
  fi
}

status() {
  if is_running; then
    echo "HTTP サーバー: 稼働中 (pid=$(cat "$PID_FILE"), port=${PORT})"
  else
    echo "HTTP サーバー: 停止中"
  fi
  if [[ -x "$TAILSCALE" ]]; then
    echo "--- tailscale serve ---"
    "$TAILSCALE" serve status 2>&1 || true
  fi
  if is_running; then
    print_urls
  fi
}

case "${1:-start}" in
  start) start ;;
  stop) stop ;;
  status) status ;;
  restart) stop; start ;;
  *)
    echo "使い方: $0 [start|stop|status|restart]" >&2
    exit 1
    ;;
esac
