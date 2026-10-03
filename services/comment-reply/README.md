# comment-reply

Instagram コメントの Webhook 受信と返信を、2 本の Lambda に分けたサービスです。Webhook は署名検証後に SQS FIFO に入れ、Reply は投稿時の問題スナップショットを S3 から読みます。Reply は Aurora を参照しません。

## 構成

| パス | 役割 |
|---|---|
| `app.webhook_handler.lambda_handler` | Function URL の GET 検証、POST 署名検証、SQS 送信 |
| `app.reply_handler.lambda_handler` | SQS 部分失敗、問題取得、判定、返信、記録 |
| `app/judge/luna.py`, `jev.py`, `combiner.py` | 独立した 2 方式と 3 モードの組み合わせ |
| `app/reply/templates.py`, `writer.py` | 定型文と 4 案の返信文 |
| `app/comment_log.py` | S3 / ローカル共通のコメント記録 |
| `tools/local_trial.py` | AWS・Instagram を使わない試行 CLI |

Python 3.10 以上が必要です。Lambda 実行時の依存は標準ライブラリとランタイム同梱の boto3 のみです。`boto3` はハンドラ内で遅延 import するため、ローカル試行ツールは boto3 なしでも動きます。

## 環境変数

| 名前 | 既定値 | 用途 |
|---|---|---|
| `SECRET_ARN` | なし | 両 Lambda が読む JSON Secret の ARN |
| `QUEUE_URL` | なし | Webhook の送信先 SQS FIFO URL |
| `ASSETS_BUCKET` | なし | 問題スナップショットの S3 バケット |
| `PROBLEMS_PREFIX` | `assets/umigame-soup-1/problems/` | `media_id.json` の前につけるキー。ステージングは `assets/umigame-soup-1/staging/problems/` |
| `COMMENT_LOG_BUCKET` | `ASSETS_BUCKET` | コメント記録のバケット |
| `SET_CODE` | `umigame-soup-1` | 問題が見つからない場合の記録上のセット |
| `GRAPH_API_BASE` | `https://graph.instagram.com/v23.0` | Graph API ベース URL |
| `JUDGE_MODE` | `hybrid` | `luna` / `jev` / `hybrid` |
| `JUDGE_SHADOW` | `on` | hybrid の見張り役。`on/off`、`true/false`、`1/0` を受け付ける |
| `JUDGE_CONSENSUS` | `on` | hybrid の正解合意制。上と同じ真偽値 |
| `REPLY_VARIANT` | `1d-luna` | `1b` / `1d-luna` / `2b` / `2c-luna` |
| `LUNA_MODEL` | `gpt-6-luna` | 判定・書き手の OpenAI モデル名。日付付き ID を指定可 |

Secret の必須キーは、Webhook が `verify_token`, `app_secret`, `ig_user_id`、Reply が `ig_access_token`, `ig_user_id`, `openai_api_key`, `typesafe_api_key` です。ステージングと本番は Secret と環境変数で切り替えます。

`hybrid` では luna と Jev を並列に呼びます。`JUDGE_SHADOW` と `JUDGE_CONSENSUS` は独立です。合意制が on なら Jev を呼び、両方 off なら Jev を呼びません。luna の失敗は SQS 再試行に回し、Jev の失敗は luna 単体へ進めます。`jev` モードで Jev が失敗した場合も luna にフォールバックします。合意制の split は真相を開示しません。`JUDGE_SHADOW_MISMATCH` と `JUDGE_CONSENSUS_SPLIT` は WARNING ログの固定マーカーです。

`1d-luna` と `2c-luna` は試走時の判定元だけが異なり、本番では同じ書き手実装の別名です。`1b` だけ真相を渡し、正解開示も LLM に書かせます。それ以外の案は `正解！` と `reveal_text` を連結します。spam / personal_info は返信せず、troll / abuse は定型文です。LLM 書き手の失敗や判定語違反は 2b 定型へ戻します。80 字超は警告のみで、200 字の切り詰めは Graph API 送信直前に行います。

## コメント記録 JSON（schema_version 1）

キーは `comment-log/{set_code}/dt=YYYY-MM-DD/{comment_id}.json` です。日付は Webhook 受信時刻の UTC 日付です。書き込み失敗は WARNING にして返信処理を続けます。問題スナップショットがないコメントも `problem_not_found` を記録して成功扱いにします。

項目の定義（キーと型）の正はセット別設計書 `docs/app/sets/umigame-soup-1.html` の 10.6「コメント記録 JSON」です（ここには重複して書きません）。実装は `app/comment_log.py`。

## ローカル試行

```bash
cd services/comment-reply
python3.12 -m venv .venv
.venv/bin/pip install -r requirements-dev.txt
.venv/bin/python -m pytest -q

# 同梱 stub はキーやネットワークを使わず、6 コメント × 3 モードを試せる
.venv/bin/python tools/local_trial.py --problem U01 \
  --stub-judgements tools/sample_stub_U01.json --reply-variant 2b

# 実 API を使う試行。キーは環境変数からだけ読む（Secrets Manager は読まない）
OPENAI_API_KEY=... TYPESAFE_API_KEY=... .venv/bin/python tools/local_trial.py \
  --problem U01 --comment '男は病院に行ったの？' --modes luna jev hybrid
```

`--snapshot path.json` で公開スナップショットを読み込めます。`--comment` は繰り返し指定可、`--comments-file` は 1 行 1 コメント、指定なしは対話入力です。`--shadow/--no-shadow` と `--consensus/--no-consensus` で hybrid のスイッチを切り替えます。`--out` の既定値は `work/local_trial/` で、モード別に本番と同じ形式の記録を保存します。stub 時に LLM 書き手が選択されていた場合、外部呼び出しを避けるため 2b 定型に切り替えます。

`guess_correct` の 2b 返信は `CORRECT_PREFIX + reveal_text` の固定形式です。その他の返信種別は各 3 通り以上の定型文を持ち、`sha1(comment_id)` で選びます。語だけの q_open と合意制 split にはそれぞれ 3 通りの専用定型文があります。

## コメント返信の評価プローブ

`tools/probe_run.py` は評価ケースを本番の判定合成・書き手・コメント記録に通し、`results.json` と `metrics.json` を出します。判定結果はケース単位でパターン間共有し、`judge_cache.json` と `writer_cache.json` で中断後も再開できます。実行には `OPENAI_API_KEY` と `TYPESAFE_API_KEY` を環境変数で指定します。Instagram への送信は行いません。

```bash
cd services/comment-reply
OPENAI_API_KEY=... TYPESAFE_API_KEY=... .venv/bin/python tools/probe_run.py \
  --problems U01 U13 --out work/probe/sample
.venv/bin/python tools/build_probe_page.py \
  --results work/probe/sample/results.json --out /tmp/comment-reply-probe.html
```

`--patterns` で 5 パターンから選択、`--workers` で並列数を変更、`--refresh-judge` / `--refresh-writer` でキャッシュを更新できます。ページ生成器は `--out` を省くと `docs/app/sets/umigame-soup-1-probe.html`（サマリー = 合否表・グラフ・評価・問題の目次）に出力し、同名ディレクトリに問題ごとのページ（`U01.html` 等。パターンごとのコメント一覧）と生データの JS（開いたときに遅延読み込み）を置きます（21-6d3 で分割）。判定キャッシュのキーに Jev の閾値は入らないため、閾値を変えたら `--refresh-judge` で取り直してください。並列数を上げすぎると OpenAI の 429 が判定・書き手の記録に残るので、全件は `--workers 4` 程度で回します。
