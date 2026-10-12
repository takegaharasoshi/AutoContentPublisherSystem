# comment-reply

水平思考クイズの Instagram コメントへ返信する Lambda と、同じ判定・書き手を使うローカル評価ツールです。

| モジュール | 役割 |
|---|---|
| `app/webhook_handler.py` | 署名検証、自己コメント除外、SQS FIFO への送信 |
| `app/reply_handler.py` | 問題取得、判定、返信、コメント記録、SQS の部分失敗通知 |
| `app/judge/luna.py`, `jev.py`, `haiku.py`, `combiner.py` | 3 方式の判定と、失敗時のサブ判定への切り替え |
| `app/reply/templates.py`, `writer.py` | 定型文と LLM の返信文 |
| `app/comment_log.py` | S3 / ローカル共通のコメント記録 |
| `content/umigame-stock/umigame-soup-1/tools/` の `local_trial.py`, `probe_run.py` ほか | AWS・Instagram を使わない試行と評価。21-8c でセットの資材側へ移し、21-8c2 でテスト・実行環境・出力先も移した（`app/` を読み込むだけで、Lambda には含めない） |

Python 3.10 以上が必要です。Lambda の依存は標準ライブラリとランタイム同梱の boto3 のみです。boto3 はハンドラ内で遅延 import するため、ローカル試行ツールは boto3 なしでも動きます。

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
| `JUDGE_MODE` | `haiku` | `luna` / `jev` / `haiku` |
| `REPLY_VARIANT` | `1b-haiku` | `1b` / `1d-luna` / `2b` / `2c-luna` / `1b-haiku` / `1d-haiku` |
| `HAIKU_EFFORT` | `high` | Haiku 判定・1b-haiku 書き手。`low` / `medium` / `high` / `xhigh` / `max` |
| `LUNA_EFFORT` | `xhigh` | luna 判定・1b 書き手。許容値は `HAIKU_EFFORT` と同じ |
| `LUNA_MODEL` | `gpt-6-luna` | 判定・書き手の OpenAI モデル名。日付付き ID を指定可 |

Secret の必須キーは、Webhook が `verify_token`, `app_secret`, `ig_user_id`、Reply が `ig_access_token`, `ig_user_id`, `openai_api_key`, `typesafe_api_key` です。Haiku を使うときは `anthropic_api_key` も指定します。ステージングと本番は Secret と環境変数で切り替えます。ローカルツールは `OPENAI_API_KEY`, `TYPESAFE_API_KEY`, `ANTHROPIC_API_KEY` を読みます。

`hybrid` / `decisions` は使用できません。`JUDGE_SHADOW` / `JUDGE_CONSENSUS` は廃止しました。

## 判定とフォールバック

| メイン | 失敗時のサブ | サブ成功時の `final.decision` |
|---|---|---|
| haiku | luna | `haiku_fallback_luna` |
| luna | haiku | `luna_fallback_haiku` |
| jev | haiku | `jev_fallback_haiku` |

メインが成功すれば `final.decision` はメインの名前です。例外または `Judgement.error` がある場合だけサブを呼びます。メインとサブは順番に実行し、サブにも同じ effort 設定を使います。サブ成功時はメインのエラーを `errors` に残し、両方式の結果を `judgements` に記録します。両方が失敗すると例外を投げ、Reply Lambda が該当メッセージを `batchItemFailures` に入れて SQS 再試行に回します。各方式の判定ロジックは単一の実装を使います。

Jev のコア判定は `T_POINT=0.6`、惜しい判定は `T_CLOSE=0.40` です。

書き手は判定モードと独立です。`1b` と `1b-haiku` は真相を受け取り、正解開示も LLM が書きます。`1d-luna` / `2c-luna` は同じ書き手の別名で、effort は `low` のままです。`1d-haiku` も `low` です。真相を渡さない案の正解返信は `正解！` と `reveal_text` の連結です。spam / personal_info は返信せず、troll / abuse は定型文です。

LLM 書き手の失敗・拒否や判定語違反は 2b 定型へ戻し、`fallback_template` を記録します。Anthropic が利用できないときも、判定済みの結果で定型返信を作ります。コア語の漏れは共通の漏れ止めで処理します。80 字超は警告のみで、200 字の切り詰めは Graph API 送信直前に行います。

## コメント記録 JSON（schema_version 1）

キーは `comment-log/{set_code}/dt=YYYY-MM-DD/{comment_id}.json`、日付は Webhook 受信時刻の UTC 日付です。書き込み失敗はログに残して返信処理を続けます。問題スナップショットがないコメントは `problem_not_found` を記録して成功扱いにします。

項目の定義（キーと型）の正はセット別設計書 `docs/app/sets/umigame-soup-1.html` の「コメント記録 JSON」です（ここには重複して書きません）。実装は `app/comment_log.py`。過去のキー（`shadow`・`consensus`・`shadow_mismatch`・`decisions`）や判定ラベルを含む JSON も、評価ページ・集計・掃引ツールで引き続き読めます。

## テスト

```bash
cd services/comment-reply
python3.12 -m venv .venv
.venv/bin/pip install -r requirements-dev.txt
.venv/bin/python -m pytest -q
```

本体のテストはプローブ用ツールを読みません（`problem` フィクスチャは `tests/fixtures/u01_judge_points.json` から組み立てる。21-8c2）。

## ローカル試行・評価プローブ

ツール・テスト・実行環境・出力先（`work/`）はセットの資材側にあります。手順は [content/umigame-stock/umigame-soup-1/README.md](../../content/umigame-stock/umigame-soup-1/README.md)「ローカル試行」「評価プローブ」を参照してください（21-8c2 で移した）。
