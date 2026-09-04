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

# review.html のスタイル（スマホ縦持ちを既定にした 1 カラム。表は使わず縦積みのカードで出す）
REVIEW_CSS = """
:root{--bg:#fff;--fg:#1b1f24;--muted:#5c6672;--line:#d8dee6;--card:#f5f7fa;
      --bad:#c0392b;--bad-bg:#fdecea;--warn:#8a6100;--warn-bg:#fff6dc;--ok:#1e7a46;--accent:#2c5aa0}
@media (prefers-color-scheme:dark){
  :root{--bg:#14171a;--fg:#e6e9ed;--muted:#9aa4b0;--line:#2c333b;--card:#1c2126;
        --bad:#ff8a7a;--bad-bg:#3a1f1c;--warn:#f0c060;--warn-bg:#37301a;--ok:#6ed49b;--accent:#8ab4f8}}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--fg);line-height:1.65;
     font:16px/1.65 -apple-system,BlinkMacSystemFont,"Hiragino Sans","Noto Sans JP",sans-serif;
     -webkit-text-size-adjust:100%}
main{padding:0 14px 64px;max-width:820px;margin:0 auto}
.bar{position:sticky;top:0;z-index:5;background:var(--bg);border-bottom:1px solid var(--line);
     padding:8px 14px;max-width:820px;margin:0 auto}
.bar-row{display:flex;gap:8px;align-items:center;flex-wrap:wrap}
.bar-row+.bar-row{margin-top:6px}
.muted{color:var(--muted);font-size:13px}
.filters .f{font:inherit;font-size:14px;padding:7px 12px;min-height:38px;border:1px solid var(--line);
     border-radius:999px;background:var(--card);color:var(--fg);text-decoration:none;display:inline-flex;
     align-items:center;cursor:pointer}
.filters .f.on{background:var(--accent);border-color:var(--accent);color:#fff}
.note{color:var(--muted);font-size:13.5px;margin:14px 0}
h2{font-size:17px;margin:28px 0 10px;padding-bottom:6px;border-bottom:2px solid var(--line)}
.index{display:flex;flex-direction:column;gap:8px}
.idx{display:flex;align-items:center;gap:10px;padding:12px;border:1px solid var(--line);border-radius:10px;
     background:var(--card);color:inherit;text-decoration:none;min-height:52px}
.idx-no{font-weight:700;font-variant-numeric:tabular-nums}
.idx-title{flex:1;font-size:15px}
.idx-badges{display:flex;gap:5px}
.idx.done{opacity:.5}
.b{min-width:26px;text-align:center;border-radius:6px;padding:2px 6px;font-size:13px;font-weight:700}
.b.bad{background:var(--bad-bg);color:var(--bad)}
.b.warn{background:var(--warn-bg);color:var(--warn)}
.b.ok{background:transparent;color:var(--ok)}
.b.n{background:transparent;color:var(--muted);font-weight:400}
.item{scroll-margin-top:96px;padding-top:4px}
.item-h{display:flex;flex-wrap:wrap;align-items:baseline;gap:8px;margin-top:34px}
.item-h .no{color:var(--accent)}
.tag{font-size:12px;color:var(--muted);font-weight:400}
.problem{background:var(--card);border-left:4px solid var(--accent);border-radius:0 8px 8px 0;
     padding:12px 14px;margin:10px 0;font-size:16.5px}
.len{display:block;color:var(--muted);font-size:12px;margin-top:6px}
details{margin:8px 0;border:1px solid var(--line);border-radius:8px;background:var(--card)}
summary{cursor:pointer;padding:11px 14px;font-size:14.5px;min-height:44px;display:flex;align-items:center}
details>p,details>ul{margin:0;padding:0 14px 12px}
details>ul{padding-left:32px}
details li{margin:4px 0;font-size:14.5px}
.qa{list-style:none;margin:14px 0 0;padding:0;counter-reset:qa}
.qa li{counter-increment:qa;border:1px solid var(--line);border-left-width:4px;border-radius:0 8px 8px 0;
     padding:10px 12px;margin:0 0 8px}
.qa li.mismatch{border-left-color:var(--bad);background:var(--bad-bg)}
.qa li.check{border-left-color:var(--warn);background:var(--warn-bg)}
.qa li.match{border-left-color:var(--line)}
.qa .q{margin:0;font-weight:600;font-size:15px}
.qa .q::before{content:counter(qa) ". ";color:var(--muted);font-weight:400}
.qa .a{margin:6px 0 0;font-size:15px}
.exp{display:inline-block;border:1px solid var(--line);border-radius:5px;padding:1px 7px;font-size:12.5px;
     color:var(--muted);background:var(--bg)}
.arrow{color:var(--muted);margin:0 6px}
.qa li.extra .q{color:var(--muted)}
.done{display:flex;align-items:center;gap:10px;margin:16px 0 6px;padding:12px;border:1px dashed var(--line);
     border-radius:10px;font-size:15px;min-height:48px}
.done input{width:22px;height:22px}
.top{margin:6px 0 0;font-size:14px}
.handover{border-color:var(--accent)}
.handover>ul{padding:0 14px 12px 32px}
.handover li{margin:8px 0}
code{background:var(--bg);border:1px solid var(--line);border-radius:4px;padding:0 4px;font-size:13px;word-break:break-all}
a{color:var(--accent)}
body.f-flag .qa li.match,body.f-flag .item.clean{display:none}
body.f-extra .qa li.expected{display:none}
"""

# 端末内で完結する軽い操作（絞り込みと確認済みチェック。localStorage は失敗しても無視する）
REVIEW_JS = """
(function(){
  var KEY='umigame-batch01-done';
  var done={};
  try{done=JSON.parse(localStorage.getItem(KEY)||'{}')||{}}catch(e){done={}}
  function save(){try{localStorage.setItem(KEY,JSON.stringify(done))}catch(e){}}
  document.querySelectorAll('input[data-done]').forEach(function(cb){
    var no=cb.getAttribute('data-done');
    cb.checked=!!done[no];
    mark(no);
    cb.addEventListener('change',function(){done[no]=cb.checked;save();mark(no)});
  });
  function mark(no){
    var link=document.querySelector('[data-idx="'+no+'"]');
    if(link){link.classList.toggle('done',!!done[no])}
  }
  document.querySelectorAll('.item').forEach(function(sec){
    if(!sec.querySelector('.qa li.mismatch, .qa li.check')){sec.classList.add('clean')}
  });
  document.querySelectorAll('button.f').forEach(function(btn){
    btn.addEventListener('click',function(){
      document.querySelectorAll('button.f').forEach(function(b){b.classList.remove('on')});
      btn.classList.add('on');
      var f=btn.getAttribute('data-f');
      document.body.className=(f==='all')?'':'f-'+f;
    });
  });
})();
"""

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


def handover_html() -> str:
    """STATUS.md の「人間レビューへの申し送り」節を折りたたみブロックに変換する。

    スマホ 1 ページでレビューを完結させるため、review.html の先頭に埋め込む。
    節が無い場合は空文字を返す（STATUS.md 側の見出しを変えたら黙って消える）。

    Returns:
        ``<details>`` ブロックの HTML（見つからなければ空文字）。
    """
    status_path = HERE / "STATUS.md"
    if not status_path.exists():
        return ""
    lines = status_path.read_text(encoding="utf-8").splitlines()
    body: list[str] = []
    collecting = False
    for line in lines:
        if line.startswith("## "):
            if collecting:
                break
            collecting = "申し送り" in line
            continue
        if collecting:
            body.append(line)
    items = [re.sub(r"^[-*]\s+", "", ln).strip() for ln in body if ln.strip().startswith(("-", "*"))]
    if not items:
        return ""

    def inline(text: str) -> str:
        """太字とコード記法だけを HTML へ起こす（それ以外はエスケープする）。"""
        escaped = html.escape(text)
        escaped = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", escaped)
        return re.sub(r"`(.+?)`", r"<code>\1</code>", escaped)

    return (
        "<details class='handover' open><summary>レビュー前の申し送り（STATUS.md）</summary><ul>"
        + "".join(f"<li>{inline(i)}</li>" for i in items)
        + "</ul></details>"
    )


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
    out = [
        "<!doctype html><html lang='ja'><head><meta charset='utf-8'>",
        "<meta name='viewport' content='width=device-width,initial-scale=1'>",
        "<meta name='color-scheme' content='light dark'>",
        "<title>umigame-soup-1 batch-01 プローブ結果</title>",
        f"<style>{REVIEW_CSS}</style></head><body>",
        "<header class='bar'>",
        "<div class='bar-row'><b>batch-01 プローブ結果</b>"
        f"<span class='muted'>{html.escape(model)}</span></div>",
        "<div class='bar-row filters'>"
        "<button type='button' class='f on' data-f='all'>全部</button>"
        "<button type='button' class='f' data-f='flag'>要チェックのみ</button>"
        "<button type='button' class='f' data-f='extra'>共通プローブ</button>"
        "<a class='f' href='#index'>目次</a></div>",
        "</header>",
        "<main>",
        f"<p class='note'>生成 {datetime.now(timezone.utc).astimezone().strftime('%Y-%m-%d %H:%M')}。"
        "<b class='bad'>不一致</b> = 期待した冒頭語と違う。<b class='warn'>要確認</b> = 機械判定できない。"
        "「真相の丸ごと言い当て」「感想」「意味不明」は全問共通の追加プローブ。"
        "各問の「確認済み」はこの端末のブラウザに保存される。</p>",
        handover_html(),
    ]

    index_rows = []
    for no, recs in results.items():
        it = by_no[no]
        n_mis = sum(1 for r in recs if r["judge"] == "mismatch")
        n_chk = sum(1 for r in recs if r["judge"] == "check")
        total += len(recs)
        mismatch += n_mis
        badges = f"<span class='b bad'>{n_mis}</span>" if n_mis else ""
        badges += f"<span class='b warn'>{n_chk}</span>" if n_chk else ""
        badges = badges or "<span class='b ok'>0</span>"
        index_rows.append(
            f"<a class='idx' href='#{no}' data-idx='{no}'><span class='idx-no'>{no}</span>"
            f"<span class='idx-title'>{html.escape(it['title'])}</span>"
            f"<span class='idx-badges'>{badges}<span class='b n'>{len(recs)}</span></span></a>"
        )
    out.append("<h2 id='index'>目次（10 問）</h2><nav class='index'>")
    out += index_rows
    out.append("</nav>")

    for no, recs in results.items():
        it = by_no[no]
        out.append(f"<section class='item' id='{no}' data-no='{no}'>")
        out.append(
            f"<h2 class='item-h'><span class='no'>{no}</span> {html.escape(it['title'])}"
            f"<span class='tag'>{it['puzzle_type']} / 難易度 {it['difficulty']}</span></h2>"
        )
        out.append(
            f"<p class='problem'>{html.escape(it['problem_text'])}"
            f"<span class='len'>{len(it['problem_text'])} 字</span></p>"
        )
        out.append(
            f"<details class='truth'><summary>真相を見る</summary><p>{html.escape(it['truth'])}</p></details>"
        )
        out.append("<details class='facts'><summary>確定事実シート（{}）</summary><ul>".format(len(it["fact_sheet"])))
        out += [f"<li>{html.escape(f)}</li>" for f in it["fact_sheet"]]
        out.append("</ul></details>")
        out.append("<ol class='qa'>")
        for r in recs:
            long_truth = r["kind"] == "extra" and len(r["q"]) >= 60
            q = "（真相の丸ごと言い当て）" if long_truth else r["q"]
            out.append(
                f"<li class='{r['judge']} {r['kind']}'>"
                f"<p class='q'>{html.escape(q)}</p>"
                f"<p class='a'><span class='exp'>{html.escape(r['a'])}</span>"
                f"<span class='arrow'>→</span>{html.escape(r['reply'])}</p></li>"
            )
        out.append("</ol>")
        out.append(
            f"<label class='done'><input type='checkbox' data-done='{no}'> {no} は確認済み</label>"
        )
        out.append("<p class='top'><a href='#index'>目次へ戻る</a></p>")
        out.append("</section>")
    out.append("</main>")
    out.append(f"<script>{REVIEW_JS}</script>")
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
