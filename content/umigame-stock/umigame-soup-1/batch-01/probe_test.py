"""batch-01: 想定質問を AI 出題者に実際に答えさせ、work/review.html に並べる（プローブテスト）。

- プロンプトは ``master_prompt.txt``（本番の Reply Lambda と同じ正）を 1 問ごとに展開する。
- 返信ロジックは PoC ``poc/umigame-comment-webhook/lambda/handler.py`` の ``generate_reply`` を流用
  （chat completions への 1 往復。モデルは本番採用の gpt-5.6-luna）。
- OpenAI キーは ``--secret-id``（既定 umigame-poc/credentials）を boto3 で実行時に読む。値は
  出力・保存しない。環境変数 OPENAI_API_KEY があればそれを優先する。
- 各問に共通の追加プローブ（感想コメント・意味不明文字列・真相の丸ごと言い当て）を足し、
  お礼返し・NO_REPLY・正解宣言の挙動も一緒にレビューできるようにする。
- 応答は work/probe_results.json にキャッシュし、``--only U03`` で一部だけ再実行して差し替えられる。

使い方:
    python3 probe_test.py                 # 全問（キャッシュがあれば再利用しない = 全件再実行）
    python3 probe_test.py --only U03 U07  # 指定問だけ再実行し、他はキャッシュから review.html を作る
    python3 probe_test.py --from-cache    # API を呼ばず review.html だけ作り直す
"""

from __future__ import annotations

import argparse
import html
import json
import os
import re
import sys
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path
from urllib import request

import boto3

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent / "common"))

from stock_items import ITEMS  # noqa: E402
from umigame_common import render_master_prompt  # noqa: E402

OPENAI_CHAT_COMPLETIONS_URL = "https://api.openai.com/v1/chat/completions"
DEFAULT_MODEL = "gpt-5.6-luna"
DEFAULT_SECRET_ID = "umigame-poc/credentials"
WORK_DIR = HERE / "work"
CACHE_PATH = WORK_DIR / "probe_results.json"
REVIEW_PATH = WORK_DIR / "review.html"
REPLY_MAX_CHARS = 200  # Lambda 側の切り詰め（セット別設計書 5.1）

# 全問共通の追加プローブ（期待: お礼 / NO_REPLY / 正解宣言）。expected_questions の件数には数えない。
EXTRA_PROBES = [
    {"q": "面白い問題！", "a": "お礼", "kind": "extra"},
    {"q": "asdkjfh ppp 3333", "a": "NO_REPLY", "kind": "extra"},
]


def load_api_key(secret_id: str) -> str:
    """OpenAI API キーを環境変数または Secrets Manager から取得する（値はログに出さない）。

    Args:
        secret_id: Secrets Manager のシークレット名。

    Returns:
        API キー文字列。
    """
    env_key = os.environ.get("OPENAI_API_KEY", "")
    if env_key:
        return env_key
    client = boto3.client("secretsmanager")
    secret = json.loads(client.get_secret_value(SecretId=secret_id)["SecretString"])
    key = secret.get("openai_api_key", "")
    if not key:
        raise SystemExit(f"{secret_id} の openai_api_key が空です")
    return key


def generate_reply(system_prompt: str, comment_text: str, api_key: str, model: str) -> str:
    """PoC の generate_reply と同じ 1 往復で出題者の返信を得る。

    Args:
        system_prompt: 1 問分に展開した出題者プロンプト。
        comment_text: 質問コメント。
        api_key: OpenAI API キー。
        model: モデル名。

    Returns:
        返信文（Lambda と同じ 200 字で切り詰め）。失敗時は ``[ERROR] ...``。
    """
    payload: dict = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": comment_text},
        ],
        "max_completion_tokens": 400,
    }
    if not model.startswith("gpt-5"):
        payload["temperature"] = 0.2
    body = json.dumps(payload).encode("utf-8")
    req = request.Request(
        OPENAI_CHAT_COMPLETIONS_URL,
        data=body,
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        method="POST",
    )
    try:
        with request.urlopen(req, timeout=60) as res:
            result = json.loads(res.read().decode("utf-8"))
        content = result["choices"][0]["message"]["content"]
        if not isinstance(content, str) or not content.strip():
            return "[ERROR] empty content"
        return content.strip()[:REPLY_MAX_CHARS]
    except Exception as exc:  # noqa: BLE001 - レビュー用に失敗もそのまま並べる
        detail = getattr(exc, "read", None)
        extra = detail().decode("utf-8", "replace")[:200] if callable(detail) else ""
        return f"[ERROR] {exc} {extra}".strip()


def expected_head(a: str) -> str:
    """期待回答の冒頭語を正規化する。"""
    for head in ("はい", "いいえ", "関係ない", "正解", "お礼", "NO_REPLY"):
        if a.startswith(head):
            return head
    return "?"


def judge(expected: str, reply: str, question: str = "") -> str:
    """期待回答と実回答の冒頭を突き合わせて match / mismatch / check を返す。

    Args:
        expected: 正規化済みの期待冒頭語。
        reply: 実回答。
        question: 質問文（「重要ですか」型の同義判定に使う）。

    Returns:
        ``match`` / ``mismatch`` / ``check``（機械判定不能・人間が見る）。
    """
    if reply.startswith("[ERROR]"):
        return "mismatch"
    r = reply.replace("。", "").replace("！", "")
    if expected == "はい":
        return "match" if r.startswith("はい") else "mismatch"
    if expected == "いいえ":
        return "match" if r.startswith("いいえ") else "mismatch"
    if expected == "関係ない":
        if r.startswith(("関係ありません", "それは問題の答えに関わりません")):
            return "match"
        # 「〜は重要ですか / 関係ありますか」への「いいえ」は同義（機械判定では一致扱い）
        if r.startswith("いいえ") and any(k in question for k in ("重要", "関係", "大事")):
            return "match"
        return "mismatch"
    if expected == "正解":
        return "match" if r.startswith("正解です") else "mismatch"
    if expected == "NO_REPLY":
        return "match" if reply.startswith("NO_REPLY") else "mismatch"
    if expected == "お礼":
        return "mismatch" if r.startswith(("はい", "いいえ", "関係", "正解", "NO_REPLY")) else "check"
    return "check"


def run_probes(items: list[dict], api_key: str, model: str, workers: int) -> dict[str, list[dict]]:
    """指定した問題の全プローブを並列実行する。

    Args:
        items: 対象の問題。
        api_key: OpenAI API キー。
        model: モデル名。
        workers: 並列数。

    Returns:
        ``{no: [{q, a, reply, judge, kind}]}``。
    """
    jobs = []
    for it in items:
        prompt = render_master_prompt(it["problem_text"], it["truth"], it["fact_sheet"])
        probes = [{**q, "kind": "expected"} for q in it["expected_questions"]] + [
            {"q": it["truth"], "a": "正解", "kind": "extra"},
            *EXTRA_PROBES,
        ]
        for idx, probe in enumerate(probes):
            jobs.append((it["no"], idx, prompt, probe))

    results: dict[str, list[dict]] = {it["no"]: [None] * 0 for it in items}
    buckets: dict[str, dict[int, dict]] = {it["no"]: {} for it in items}

    def work(job):
        no, idx, prompt, probe = job
        reply = generate_reply(prompt, probe["q"], api_key, model)
        return no, idx, {**probe, "reply": reply, "judge": judge(expected_head(probe["a"]), reply, probe["q"])}

    with ThreadPoolExecutor(max_workers=workers) as pool:
        for no, idx, rec in pool.map(work, jobs):
            buckets[no][idx] = rec
    for no, bucket in buckets.items():
        results[no] = [bucket[i] for i in sorted(bucket)]
    return results


def write_review(results: dict[str, list[dict]], model: str) -> tuple[int, int]:
    """review.html を書き出す。

    Args:
        results: 問題番号ごとの応答一覧。
        model: 使ったモデル名（表題に出す）。

    Returns:
        （応答総数, 機械判定 mismatch の件数）。
    """
    by_no = {it["no"]: it for it in ITEMS}
    total = mismatch = 0
    css = """
    body{font-family:sans-serif;max-width:1100px;margin:24px auto;padding:0 16px;line-height:1.5}
    h2{border-bottom:2px solid #345;padding-bottom:4px;margin-top:40px}
    .meta{background:#f4f6f8;padding:10px 14px;border-radius:6px;margin:8px 0}
    table{border-collapse:collapse;width:100%;font-size:14px}
    th,td{border:1px solid #ccd;padding:6px 8px;vertical-align:top;text-align:left}
    th{background:#e8ecf0}
    tr.mismatch td{background:#fde8e8}
    tr.check td{background:#fff6dc}
    tr.extra td:first-child{color:#667}
    .sum{font-weight:bold}
    details summary{cursor:pointer;color:#345}
    """
    out = [
        "<!doctype html><html lang='ja'><head><meta charset='utf-8'>",
        f"<title>umigame-soup-1 batch-01 プローブテスト</title><style>{css}</style></head><body>",
        f"<h1>umigame-soup-1 batch-01 プローブテスト（{html.escape(model)}）</h1>",
        f"<p>生成: {datetime.now(timezone.utc).astimezone().strftime('%Y-%m-%d %H:%M %z')}。"
        "赤 = 期待冒頭語と不一致（機械判定）。黄 = 機械判定不能（人間が見る）。"
        "「真相の丸ごと言い当て」「感想」「意味不明」は全問共通の追加プローブ。</p>",
    ]
    summary_rows = []
    for no, recs in results.items():
        it = by_no[no]
        n_mis = sum(1 for r in recs if r["judge"] == "mismatch")
        n_chk = sum(1 for r in recs if r["judge"] == "check")
        total += len(recs)
        mismatch += n_mis
        summary_rows.append(f"<tr><td>{no}</td><td>{html.escape(it['title'])}</td><td>{len(recs)}</td><td>{n_mis}</td><td>{n_chk}</td></tr>")
    out.append("<h2>サマリ</h2><table><tr><th>No</th><th>題名</th><th>応答数</th><th>不一致</th><th>要確認</th></tr>")
    out += summary_rows
    out.append("</table>")

    for no, recs in results.items():
        it = by_no[no]
        out.append(f"<h2>{no} {html.escape(it['title'])}（{it['puzzle_type']} / 難易度 {it['difficulty']}）</h2>")
        out.append("<div class='meta'>")
        out.append(f"<p><b>問題文</b>（{len(it['problem_text'])} 字）: {html.escape(it['problem_text'])}</p>")
        out.append(f"<p><b>真相</b>: {html.escape(it['truth'])}</p>")
        out.append("<details><summary>確定事実シート</summary><ul>")
        out += [f"<li>{html.escape(f)}</li>" for f in it["fact_sheet"]]
        out.append("</ul></details></div>")
        out.append("<table><tr><th style='width:4%'>#</th><th style='width:34%'>質問</th><th style='width:12%'>期待</th><th>出題者の実回答</th><th style='width:8%'>判定</th></tr>")
        for i, r in enumerate(recs, 1):
            q = r["q"] if r["kind"] == "expected" or len(r["q"]) < 60 else "（真相の丸ごと言い当て）" + r["q"][:40] + "…"
            out.append(
                f"<tr class='{r['judge']} {r['kind']}'><td>{i}</td><td>{html.escape(q)}</td>"
                f"<td>{html.escape(r['a'])}</td><td>{html.escape(r['reply'])}</td><td>{r['judge']}</td></tr>"
            )
        out.append("</table>")
    out.append("</body></html>")
    REVIEW_PATH.write_text("\n".join(out), encoding="utf-8")
    return total, mismatch


def main() -> int:
    """プローブテストを実行して review.html を生成する。"""
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--secret-id", default=DEFAULT_SECRET_ID)
    parser.add_argument("--only", nargs="*", default=None, help="再実行する問題番号（他はキャッシュ）")
    parser.add_argument("--from-cache", action="store_true", help="API を呼ばず review.html だけ作り直す")
    parser.add_argument("--workers", type=int, default=6)
    args = parser.parse_args()

    WORK_DIR.mkdir(exist_ok=True)
    cache: dict[str, list[dict]] = {}
    if CACHE_PATH.exists():
        cache = json.loads(CACHE_PATH.read_text(encoding="utf-8")).get("results", {})

    if args.from_cache:
        results = {it["no"]: cache.get(it["no"], []) for it in ITEMS}
    else:
        targets = [it for it in ITEMS if args.only is None or it["no"] in args.only]
        api_key = load_api_key(args.secret_id)
        fresh = run_probes(targets, api_key, args.model, args.workers)
        results = {it["no"]: fresh.get(it["no"], cache.get(it["no"], [])) for it in ITEMS}
        CACHE_PATH.write_text(
            json.dumps({"model": args.model, "results": results}, ensure_ascii=False, indent=1), encoding="utf-8"
        )

    total, mismatch = write_review(results, args.model)
    per_item = {no: len(recs) for no, recs in results.items()}
    min_per_item = min(per_item.values()) if per_item else 0
    print(f"probe_test: {len(results)} 問 / 応答 {total} 件（最少 {min_per_item} 件/問）/ 機械判定 不一致 {mismatch} 件")
    print(f"probe_test: {REVIEW_PATH.relative_to(HERE.parent.parent.parent.parent)} を生成")
    errors = sum(1 for recs in results.values() for r in recs if r["reply"].startswith("[ERROR]"))
    if errors:
        print(f"probe_test: API エラー {errors} 件（review.html の [ERROR] 行）")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
