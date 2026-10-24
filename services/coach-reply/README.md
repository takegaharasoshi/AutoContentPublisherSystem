# 脳みそコーチの正解返信

`logic-training-1` の投稿を定時に走査し、未判定コメントのうち
`correct` かつ `high` のものにだけ定型文で返信する Lambda。
詳細仕様は `docs/app/sets/logic-training-1-coach-reply.html` 1〜6章、
AWS の構成・権限は `docs/infra/stacks.html` 3.7 に従う。

## 構成

- `app/run_handler.py`: SSM → Secret → 投稿一覧 → コメント数の差分 →
  スナップショット → 除外 → 判定 → 返信 → S3 状態保存。
- `app/selection.py`, `first_correct.py`, `reply_text.py`: 副作用のない選別・一番乗り・定型文。
- `app/judge.py`, `prompts/judge.md`, `anthropic_util.py`: 最大20件ずつの判定。
- `app/graph_api.py`, `http_util.py`, `secrets.py`: 外部接続。
- `app/state_store.py`, `snapshot_store.py`, `switch.py`: S3 / SSM の読み書き。
- `app/token_refresh_handler.py`: 週次のトークン更新。
- `tools/backfill_snapshots.py`: 過去の投稿のスナップショット作成。
- `tools/offline_eval.py`: 保存済みの評価データを使う判定評価。
- `tests/`: 単体・結合テスト。HTTP・boto3・AWS CLI はすべてスタブ。

`services/comment-reply/` の transport、Secret、トークン更新、テスト構成を
複製して削った独立サービス。他サービスや `shared/` は import しない。
実行時の依存は標準ライブラリと Lambda 同梱の boto3 のみ。

## 環境変数

| 変数 | 用途・既定値 |
|---|---|
| `SECRET_ARN` | 正解返信・トークン更新で必須。面ごとの Secret ARN |
| `ASSETS_BUCKET` | 正解返信で必須。画像バケット |
| `PROBLEMS_PREFIX` | `assets/logic-training-1/problems/` |
| `STATE_PREFIX` | `coach-reply/logic-training-1/state/` |
| `PARAM_PREFIX` | `/acps/prod/coach-reply/` |
| `GRAPH_API_BASE` | `https://graph.instagram.com/v25.0` |
| `JUDGE_MODEL` | `claude-haiku-5-5` |
| `JUDGE_EFFORT` | `high`（`low / medium / high / xhigh / max`） |

ステージングでは `PROBLEMS_PREFIX=assets/logic-training-1/staging/problems/`、
`STATE_PREFIX=coach-reply/logic-training-1-staging/state/`、
`PARAM_PREFIX=/acps/prod/coach-reply-staging/` とし、Secret も分ける。
S3 のプレフィックスは先頭 `/` なし・末尾 `/` あり。

Secret は `ig_access_token`, `ig_user_id`, `token_expires_at`,
`anthropic_api_key` を持つ。正解返信は起動ごとに Secret を読み直し、
ユーザー名は毎回 Graph API の `/me` から取る。
トークン更新は他の Secret フィールドを保ったまま
`ig_access_token` と `token_expires_at` だけ更新する。
未投入の空トークンは正常終了。
複製元と同じ `REFRESH_API_BASE` の任意の上書きも使える
（既定 `https://graph.instagram.com`、バージョンなし）。

## 状態と再試行

`{STATE_PREFIX}media-counts.json` と `{STATE_PREFIX}judged/{media_id}.json`
に状態を保存する。コメント本文・ユーザー名は保存しない。
`NoSuchKey` は初回・スナップショットなしとして扱い、権限不足・壊れた JSON は例外にする。

SSM は `GetParameter` で `reply-enabled`（`on / off`）と
`reply-not-before`（UTC の ISO 8601 日時）を毎回読む。不正・取得失敗時は返信前に例外。
`off` でも判定を確定し `switch: "off", replied: false` を記録する。
後で `on` にしても、それらのコメントには返さない。

判定失敗の1〜2回目は `fail_count`・日時・スイッチ・返信なしを保存し、`verdict` のない記録は
未判定として再試行する。3回目は `judge_failed` で確定する。
失敗が未確定で残る投稿のコメント数は進めない。
返信成功ごとに状態を保存し、Graph / S3 エラーは Lambda に伝播させる。
スイッチ・Secret の値やトークン付き URL はログに出さない。

残り30秒未満なら次の投稿・判定バッチ・返信を次回に回す。
Anthropic の1回の通信は既定60秒、残り時間から保存用10秒を引いた値でさらに制限し、
呼び出し内の再試行はせず次の定時に再判定する。
古いコメントから20件ずつ判定・返信・保存を済ませ、投稿の全処理が済んだ場合だけコメント数を進める。
終了時は完了済みのコメント数を保存し、`coach_reply_summary` を INFO で1行出す。
Lambda の同時実行数1はインフラ側の設定が前提。

一番乗りは、運用者の返信なし・一番乗り返信歴なし・それより前のコメントが
すべて `wrong` の場合だけ。開始前・別解・判断保留・判定失敗・本文なしなどは
一番乗りの根拠にしない。同時刻の場合は処理順の最初の返信のみが一番乗りになる。
`off` では実際に返信していないため `first_correct_replied` は進めない。

## ローカルテスト

Lambda の対象は Python 3.13。開発用には pytest と boto3 を入れる。

```sh
cd services/coach-reply
python3.13 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements-dev.txt
python -m pytest -q
```

テストは実 API を呼ばない。評価ツールのテストも集計関数のみ。

## オフライン評価

以下はリポジトリのルートで実行する。Anthropic API を呼ぶため、
環境変数 `ANTHROPIC_API_KEY` を設定してから流す。AWS 認証は不要。
モデルと effort は上記の環境変数で切り替えられる。

```sh
python services/coach-reply/tools/offline_eval.py \
  --eval poc/logic-training-reply-eval/data/eval.jsonl \
  --answers poc/logic-training-reply-eval/data/answers.json \
  --limit-media 3 \
  --out /tmp/coach-reply-eval.jsonl
```

`--limit-media` を外すと全投稿、最大4投稿を並列に評価する。
既定の出力先は `poc/logic-training-reply-eval/data/eval_result.jsonl`。
入力1コメントにつき1行、元のラベルと `prediction`、`would_reply` を保存する。
`prediction: null` は判定失敗。
標準出力にはラベル×返信可否、誤返信（`wrong / other` のみ）の件数と本文・答え・理由、
正解を拾えた割合、判定失敗件数を出す。別解・未回答は誤返信件数には含めない。
`answers.json` の `content_fields` は JSON 文字列・オブジェクトの両方を受け付ける。

## バックフィル

実行は本番開始前のユーザー作業。AWS CLI と boto3 が必要。
DB には `collect.py answers` と同じ SELECT だけを行う。
ARN は `AURORA_CLUSTER_ARN` / `AURORA_SECRET_ARN` を優先し、未設定なら
同じ `describe-db-clusters` / `list-secrets` の問い合わせで解決する。
DB 名は `acps`。既定の dry-run でも DB と S3 を読む。

```sh
python services/coach-reply/tools/backfill_snapshots.py --bucket BUCKET --dry-run
python services/coach-reply/tools/backfill_snapshots.py --bucket BUCKET --apply
```

`--bucket` は `ASSETS_BUCKET`、`--prefix` は `PROBLEMS_PREFIX` でも指定できる。
既存キーは飛ばし、作成時も `If-None-Match: *` を使って上書きを防ぐ。
書くスナップショットは `schema_version: 1, kind: "quiz", source: "backfill"`。
`content_fields` の `explanation / hint` を取り出し、投稿日時を UTC にそろえる。
