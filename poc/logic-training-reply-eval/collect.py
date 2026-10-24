"""脳みそコーチ（logic-training-1）の正解自動返信のオフライン評価用データを集める（Phase 31-1）。

返信専用 Meta アプリ（Instagram ログイン方式）のトークンでコメントと運用者の返信を読み出し、
本番 Aurora の出題スナップショット（quiz_items）と突き合わせて、運用者の返信をラベルにした評価用データを作る。
読み取り専用: Graph API は GET だけ、Aurora は SELECT だけ（RDS Data API 経由）。

使い方:
    python3 collect.py me                  # トークンごとに /me を叩いて疎通確認（test / coach）
    python3 collect.py comments            # coach の全リールのコメント + 返信を data/comments.json へ
    python3 collect.py answers             # Aurora から投稿ごとの問題・答えを data/answers.json へ
    python3 collect.py label               # 上の 2 つを突き合わせて data/eval.jsonl + 内訳を表示

トークンは ~/.config/acps/lt-reply-tokens.json（{"test": "...", "coach": "..."}・chmod 600）に置く。
リポジトリには入れない。data/ は個人の名前を含むため git 管理外（.gitignore）。
"""

from __future__ import annotations

import argparse
import collections
import json
import os
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
DATA = HERE / "data"
TOKEN_FILE = Path(os.environ.get("LT_REPLY_TOKEN_FILE", "~/.config/acps/lt-reply-tokens.json")).expanduser()
GRAPH = "https://graph.instagram.com/v25.0"
DB = "acps"
SET_CODE = "logic-training-1"

COMMENT_FIELDS = "id,text,username,timestamp,like_count,replies{id,text,username,timestamp}"

# 運用者の返信文からラベルを決める語。返信が複数あるときは最後の 1 本（訂正）で決める。
# 別解の言い回しを先に見る（「別解として正解」を correct にしない）→ 外れ → 正解の順。
ALT_WORDS = ("別解", "これも正解", "として正解", "正解としても", "正解にした", "どちらも正解")
WRONG_WORDS = ("不正解", "惜しい", "おしい", "残念", "ハズレ", "はずれ", "本当は動かせない")
CORRECT_WORDS = ("正解", "お見事", "その通り", "そのとおり", "ご名答")
# 正解と言いつつ想定外の答えを認めたときの言い回し（correct ではなく alt に寄せる）
ALT_HINT_WORDS = ("なるほど", "ナイス発想", "捉えた", "とは違う", "確かに", "見方によっては", "着眼点", "書いてない")


def load_tokens() -> dict[str, str]:
    """トークンファイルを読む。"""
    if not TOKEN_FILE.exists():
        raise SystemExit(f"token file not found: {TOKEN_FILE}")
    return json.loads(TOKEN_FILE.read_text())


def graph_get(path: str, token: str, **params: str) -> dict:
    """Graph API に GET する（エラー本文はトークンを含まないのでそのまま出す）。"""
    query = urllib.parse.urlencode({**params, "access_token": token})
    url = path if path.startswith("https://") else f"{GRAPH}/{path}?{query}"
    if path.startswith("https://") and "access_token=" not in path:
        url = f"{path}&access_token={token}"
    for attempt in range(3):
        try:
            with urllib.request.urlopen(url, timeout=30) as res:
                return json.loads(res.read())
        except urllib.error.HTTPError as e:
            body = e.read().decode()
            if e.code >= 500 and attempt < 2:
                time.sleep(3)
                continue
            shown = path.split("?")[0]  # paging.next はトークンを含むので問い合わせ部を落とす
            raise SystemExit(f"HTTP {e.code} {shown}: {body}")
    raise SystemExit("unreachable")


def paged(path: str, token: str, **params: str) -> list[dict]:
    """paging.next をたどって data を全部集める。"""
    out: list[dict] = []
    page = graph_get(path, token, **params)
    while True:
        out.extend(page.get("data", []))
        nxt = page.get("paging", {}).get("next")
        if not nxt:
            return out
        page = graph_get(nxt, token)


def cmd_me(_: argparse.Namespace) -> None:
    """各トークンで /me と最新メディア 1 件のコメント数を出す（疎通確認）。"""
    for name, token in load_tokens().items():
        me = graph_get("me", token, fields="user_id,username,account_type,media_count")
        print(f"[{name}] /me -> {json.dumps(me, ensure_ascii=False)}")
        media = graph_get("me/media", token, fields="id,timestamp,comments_count", limit="1").get("data", [])
        if not media:
            print(f"[{name}] media: none")
            continue
        m = media[0]
        comments = graph_get(f"{m['id']}/comments", token, fields="id,timestamp", limit="5").get("data", [])
        print(f"[{name}] latest media {m['id']} {m['timestamp']} comments_count={m.get('comments_count')} "
              f"-> /comments returned {len(comments)} (first ids: {[c['id'] for c in comments[:3]]})")


def cmd_comments(_: argparse.Namespace) -> None:
    """coach の全メディアのコメントと返信を保存する。"""
    token = load_tokens()["coach"]
    me = graph_get("me", token, fields="user_id,username")
    media = paged("me/media", token, fields="id,timestamp,media_type,comments_count,permalink", limit="50")
    # 投稿済みでも /me/media に出ないメディアがある（2026-10-24 実測: DB 367 件中 215 件）。
    # answers.json があれば、そのメディア ID も直接読む（読めないものは件数だけ数える）
    listed = {m["id"] for m in media}
    unreachable = 0
    answers_file = DATA / "answers.json"
    extra = [r["media_id"] for r in json.loads(answers_file.read_text())] if answers_file.exists() else []
    for media_id in (i for i in extra if i not in listed):
        try:
            m = graph_get(media_id, token, fields="id,timestamp,media_type,comments_count,permalink")
        except SystemExit:
            unreachable += 1
            continue
        m["listed"] = False
        media.append(m)
    print(f"media: {len(media)} (listed {len(listed)}, unreachable {unreachable})", file=sys.stderr)
    for i, m in enumerate(media):
        m["comments"] = paged(f"{m['id']}/comments", token, fields=COMMENT_FIELDS, limit="50") \
            if m.get("comments_count") else []
        if i % 20 == 0:
            print(f"  {i}/{len(media)}", file=sys.stderr)
    DATA.mkdir(exist_ok=True)
    (DATA / "comments.json").write_text(json.dumps({"me": me, "media": media}, ensure_ascii=False, indent=1))
    total = sum(len(m["comments"]) for m in media)
    print(f"saved data/comments.json: media={len(media)} (listed {len(listed)}, by DB id {len(media) - len(listed)},"
          f" unreachable {unreachable}) top-level comments={total}")


def aurora_execute(sql: str) -> list[dict]:
    """Data API で SELECT を 1 文流す（content/insights-analysis/run_queries.py と同じ方式）。"""
    def discover(cmd: list[str]) -> str:
        return subprocess.run(cmd, capture_output=True, text=True, timeout=60, check=True).stdout.split()[0]
    cluster = os.environ.get("AURORA_CLUSTER_ARN") or discover(
        ["aws", "rds", "describe-db-clusters", "--query", "DBClusters[0].DBClusterArn", "--output", "text"])
    secret = os.environ.get("AURORA_SECRET_ARN") or discover(
        ["aws", "secretsmanager", "list-secrets", "--query",
         "SecretList[?contains(Name,'db/credentials')].ARN", "--output", "text"])
    cmd = ["aws", "rds-data", "execute-statement", "--resource-arn", cluster, "--secret-arn", secret,
           "--database", DB, "--sql", sql, "--format-records-as", "JSON", "--output", "json"]
    for attempt in range(8):
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=180)
        if r.returncode == 0:
            return json.loads(json.loads(r.stdout).get("formattedRecords", "[]"))
        if "DatabaseResumingException" in r.stderr or "Communications link failure" in r.stderr:
            print(f"  (DB resuming, retry {attempt + 1})", file=sys.stderr)
            time.sleep(20)
            continue
        raise SystemExit(r.stderr.strip())
    raise SystemExit("DB did not resume")


def cmd_answers(_: argparse.Namespace) -> None:
    """投稿済みリールの問題・答えのスナップショットを保存する。"""
    rows = aurora_execute(f"""
SELECT p.platform_post_id AS media_id, p.posted_at, q.quiz_type, q.difficulty,
       q.question_text, q.answer_text, q.content_fields
FROM posts p
JOIN batch_sets b ON b.id = p.set_id
JOIN quiz_items q ON q.set_id = p.set_id AND q.generation_run_id = p.generation_run_id
WHERE b.set_code = '{SET_CODE}' AND p.status = 'success' AND p.platform_post_id IS NOT NULL
ORDER BY p.posted_at""")
    DATA.mkdir(exist_ok=True)
    (DATA / "answers.json").write_text(json.dumps(rows, ensure_ascii=False, indent=1))
    print(f"saved data/answers.json: posts={len(rows)}")


def label_of(replies: list[str]) -> str:
    """運用者の返信文からラベルを決める。

    返信が無ければ unanswered、正解とも外れとも言っていない返信（ねぎらい・ヒント・雑談）は other。
    """
    if not replies:
        return "unanswered"
    text = replies[-1]
    if any(w in text for w in ALT_WORDS):
        return "alt"
    if any(w in text for w in WRONG_WORDS):
        return "wrong"
    if any(w in text for w in CORRECT_WORDS):
        return "alt" if any(w in text for w in ALT_HINT_WORDS) else "correct"
    return "other"


def cmd_label(args: argparse.Namespace) -> None:
    """コメントと答えを突き合わせて評価用データを書き、内訳を出す。"""
    raw = json.loads((DATA / "comments.json").read_text())
    own = raw["me"]["username"]
    answers = {r["media_id"]: r for r in json.loads((DATA / "answers.json").read_text())}
    # replies{} の各行には username が返らない。返信はトップレベルの一覧にも重ねて出るので、
    # 運用者の返信 = 「運用者のトップレベル行と同じ ID の返信」で見分け、返信の行はコメントとして数えない
    every = [c for m in raw["media"] for c in m["comments"]]
    own_ids = {c["id"] for c in every if c.get("username") == own}
    reply_ids = {r["id"] for c in every for r in c.get("replies", {}).get("data", [])}
    counts: collections.Counter[str] = collections.Counter()
    unmatched_media = 0
    samples: dict[str, list[str]] = collections.defaultdict(list)
    with (DATA / "eval.jsonl").open("w") as f:
        for m in raw["media"]:
            ans = answers.get(m["id"])
            if ans is None:
                unmatched_media += 1 if m["comments"] else 0
                continue
            for c in m["comments"]:
                # 運用者の行・他人の返信の行・本文のない行（削除・制限済みと見られる）は飛ばす
                if c.get("username") == own or c["id"] in reply_ids or "text" not in c:
                    continue
                replies = [r["text"] for r in c.get("replies", {}).get("data", []) if r["id"] in own_ids]
                label = label_of(replies)
                counts[label] += 1
                if len(samples[label]) < args.samples:
                    samples[label].append(f"{c['text'][:40]!r} -> {' / '.join(replies)[:60]!r}")
                f.write(json.dumps({
                    "media_id": m["id"], "posted_at": ans["posted_at"], "quiz_type": ans["quiz_type"],
                    "question_text": ans["question_text"], "answer_text": ans["answer_text"],
                    "comment_id": c["id"], "comment_text": c["text"], "comment_at": c["timestamp"],
                    "commenter": c.get("username"), "operator_replies": replies, "label": label,
                }, ensure_ascii=False) + "\n")
    print(f"media with comments but no DB match: {unmatched_media}")
    print(f"total comments: {sum(counts.values())}")
    for k in ("correct", "alt", "wrong", "other", "unanswered"):
        print(f"  {k}: {counts[k]}")
    for k, lines in samples.items():
        print(f"\n## samples: {k}")
        print("\n".join(lines))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="cmd", required=True)
    sub.add_parser("me").set_defaults(func=cmd_me)
    sub.add_parser("comments").set_defaults(func=cmd_comments)
    sub.add_parser("answers").set_defaults(func=cmd_answers)
    p = sub.add_parser("label")
    p.add_argument("--samples", type=int, default=5, help="ラベルごとに表示する例の数（コメント本文は伏せずに出る）")
    p.set_defaults(func=cmd_label)
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
