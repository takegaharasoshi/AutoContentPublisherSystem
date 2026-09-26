#!/usr/bin/env bash
# Claude Code から Codex へ作業を委譲するラッパー（委譲ワーカー）。
#
# Codex CLI 0.157 系で `codex mcp-server` が廃止され MCP 経由の委譲ができなくなったため、
# `codex exec` の直接実行に置き換えた（2026-09-26）。規約は CLAUDE.md「Codex 連携」。
#
# 使い方:
#   tools/codex_delegate.sh new    [-s SANDBOX] [-m MODEL] [-e EFFORT] [-n NAME] PROMPT_FILE
#   tools/codex_delegate.sh resume [-s SANDBOX] [-m MODEL] [-e EFFORT] [-n NAME] SESSION_ID PROMPT_FILE
#
#   SANDBOX: workspace-write（既定）| read-only
#   MODEL / EFFORT: 省略時は ~/.codex/config.toml の既定（gpt-6-luna / max）
#   NAME: ログファイル名の接頭辞（既定 task）
#
# 出力: 標準出力には session id・終了コード・Codex の最終メッセージだけを出す。
# 実行ログ全文は $CODEX_DELEGATE_DIR（既定 /tmp/codex-delegate）に保存し、必要時に tail / grep で読む。
set -euo pipefail

usage() {
  sed -n '7,12p' "$0" | sed 's/^# \{0,1\}//' >&2
  exit 2
}

[[ $# -ge 1 ]] || usage
mode="$1"
shift
[[ "$mode" == "new" || "$mode" == "resume" ]] || usage

sandbox="workspace-write"
model=""
effort=""
name="task"
while getopts "s:m:e:n:" opt; do
  case "$opt" in
    s) sandbox="$OPTARG" ;;
    m) model="$OPTARG" ;;
    e) effort="$OPTARG" ;;
    n) name="$OPTARG" ;;
    *) usage ;;
  esac
done
shift $((OPTIND - 1))

if [[ "$mode" == "resume" ]]; then
  [[ $# -eq 2 ]] || usage
  session_id="$1"
  prompt_file="$2"
else
  [[ $# -eq 1 ]] || usage
  prompt_file="$1"
fi
[[ -f "$prompt_file" ]] || { echo "プロンプトファイルがありません: $prompt_file" >&2; exit 2; }
case "$sandbox" in
  workspace-write | read-only) ;;
  *) echo "SANDBOX は workspace-write か read-only: $sandbox" >&2; exit 2 ;;
esac

repo_root="$(git -C "$(dirname "$0")" rev-parse --show-toplevel)"
out_dir="${CODEX_DELEGATE_DIR:-/tmp/codex-delegate}"
mkdir -p "$out_dir"
stamp="$(date +%Y%m%d-%H%M%S)"
log_file="$out_dir/${name}-${stamp}.log"
last_file="$out_dir/${name}-${stamp}.last.md"

# 委譲ワーカーであることを AGENTS.md の判定に使う先頭行（直接セッションと区別する）。
header="【委譲ワーカー】Claude Code からの委譲タスク。AGENTS.md「委譲ワーカー時のルール」に従うこと。"
prompt="${header}"$'\n\n'"$(cat "$prompt_file")"

opts=(-c "sandbox_mode=\"${sandbox}\"" -o "$last_file")
[[ -n "$model" ]] && opts+=(-m "$model")
[[ -n "$effort" ]] && opts+=(-c "model_reasoning_effort=\"${effort}\"")

cd "$repo_root"
set +e
if [[ "$mode" == "resume" ]]; then
  codex exec resume "${opts[@]}" "$session_id" "$prompt" </dev/null >"$log_file" 2>&1
else
  codex exec "${opts[@]}" -C "$repo_root" "$prompt" </dev/null >"$log_file" 2>&1
fi
status=$?
set -e

sid="$(grep -m1 -oE 'session id: [0-9a-f-]+' "$log_file" | awk '{print $3}' || true)"
echo "session_id: ${sid:-${session_id:-unknown}}"
echo "exit: $status"
echo "log: $log_file"
echo "--- 最終メッセージ ---"
if [[ -s "$last_file" ]]; then
  cat "$last_file"
else
  echo "(最終メッセージなし。ログ末尾)"
  tail -n 30 "$log_file"
fi
exit "$status"
