# comment-reply

水平思考クイズの Instagram コメントへ返信する Lambda と、同じ判定・書き手を使うローカル評価ツールです。

| モジュール | 役割 |
|---|---|
| `app/webhook_handler.py` | 署名検証、自己コメント除外、SQS FIFO への送信 |
| `app/reply_handler.py` | 問題取得、判定、返信、コメント記録、SQS の部分失敗通知 |
| `app/judge/luna.py`, `jev.py`, `haiku.py`, `combiner.py` | 3 方式の判定と、失敗時のサブ判定への切り替え |
| `app/reply/templates.py`, `writer.py` | 定型文と LLM の返信文 |
| `app/comment_log.py` | S3 / ローカル共通のコメント記録 |
| `tools/local_trial.py`, `probe_run.py` | AWS・Instagram を使わない試行と評価 |

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

## ローカル試行

```bash
cd services/comment-reply
python3.12 -m venv .venv
.venv/bin/pip install -r requirements-dev.txt
.venv/bin/python -m pytest -q

# 同梱 stub: キーやネットワークを使わず、6 コメント × 3 モードを試す
.venv/bin/python tools/local_trial.py --problem U01 \
  --stub-judgements tools/sample_stub_U01.json --reply-variant 2b

# 実 API: --modes の既定は luna jev haiku
OPENAI_API_KEY=... TYPESAFE_API_KEY=... ANTHROPIC_API_KEY=... \
  .venv/bin/python tools/local_trial.py --problem U01 \
  --comment '男は病院に行ったの？' --modes luna jev haiku

# パターンを番号で比較。判定結果は方式・effort ごとに再利用する
OPENAI_API_KEY=... TYPESAFE_API_KEY=... ANTHROPIC_API_KEY=... \
  .venv/bin/python tools/local_trial.py --problem U01 \
  --patterns 7 9 10 --haiku-effort high --luna-effort xhigh
```

`--snapshot path.json` で公開スナップショットを読み込めます。`--comment` は繰り返し指定可、`--comments-file` は 1 行 1 コメント、指定なしは対話入力です。`--out` の既定は `work/local_trial/` です。stub 時の書き手は 2b 定型に切り替えます。

`--patterns` は下表の番号 `1 2 5 7 9 10` を受け付け、`--modes` と `--reply-variant` より優先します。記録は `p<番号>-<モード>-<案>/` に保存します。`--haiku-effort` / `--luna-effort` の既定は Config の値です。複数指定すると、その方式で判定するか対応する書き手を使うパターンを effort ごとに実行します。サブにだけ使う方式には最初の指定値を使います。判定・返信の所要秒数も表示します。

2b の正解返信は `CORRECT_PREFIX + reveal_text` です。その他の返信種別は各 3 通り以上の定型文を持ち、`sha1(comment_id)` で選びます。語だけの q_open は 3 通りの専用定型文です。

## 評価プローブ

`tools/probe_run.py` は本番の判定・書き手・コメント記録を通し、`results.json` と `metrics.json` を出します。ケースごとに方式・effort 単位で判定を共有し、`judge_cache.json` / `writer_cache.json` で再開できます。メイン成功時にはサブを呼びません。独立したケースと書き手は `--workers`（既定 4）で並列に実行します。

| 番号 | プローブ ID | 判定 + 返信文 |
|---|---|---|
| ① | `luna-1b` | luna + 1b |
| ② | `luna-1d` | luna + 1d-luna |
| ⑤ | `jev-2c` | jev + 2c-luna |
| ⑦ | `haiku-1b-max` / `haiku-1b-xhigh` / `haiku-1b-high` | haiku + 1b-haiku（3 effort） |
| ⑨ | `luna-1b-haiku` | luna + 1b-haiku（Haiku effort high） |
| ⑩ | `jev-1b-haiku` | jev + 1b-haiku（Haiku effort high） |

CLI で `--patterns` を省くと ⑦ high・⑨・⑩ を選びます。Python の `run_probe()` で省略した場合の `LEGACY_PATTERN_IDS` は ①・②・⑤ です。全 8 パターンを実行するには `patterns=list(PATTERN_IDS)` を渡します。

```bash
OPENAI_API_KEY=... TYPESAFE_API_KEY=... ANTHROPIC_API_KEY=... \
  .venv/bin/python tools/probe_run.py --problems U01 U13 \
  --patterns haiku-1b-high luna-1b-haiku jev-1b-haiku --out work/probe/sample
.venv/bin/python tools/build_probe_page.py \
  --results work/probe/sample/results.json --out /tmp/comment-reply-probe.html
```

パターンの `luna_effort` は省略時に `LUNA_EFFORT`（既定 xhigh）、`haiku_effort` は省略時に `HAIKU_EFFORT`（既定 high）を使います。⑦・⑨・⑩ の Haiku effort はパターンで指定します。luna 判定・1b 書き手のキャッシュキーに luna effort、Haiku 判定・書き手には Haiku effort とプロンプト内容を含めます。Jev のキーには変更した `T_POINT` / `T_CLOSE` を含め、旧閾値の結果を再利用しません。`--refresh-judge` / `--refresh-writer` で取り直せます。

Haiku のモデルは `claude-haiku-5-5`、判定・1b-haiku の `max_tokens` は 32000、1d-haiku は 4000 です。HTTP は標準ライブラリの urllib を使い、system の末尾に 5 分のキャッシュ指定を付けます。実行ログは Anthropic の入力・出力・キャッシュ書き込み・読み出しトークンと拒否件数を、effort ごとに合計 / 新規呼び出し分で表示します。

metrics の `reference.api_usage` は判定 / 書き手ごとのトークン・費用・応答時間・拒否・打ち切り・空応答を集計します。`judge_fallbacks` は `*_fallback_*` 全体の件数、`fallback_decisions` はラベルごとの件数です。過去の `decisions_fallback_luna`, `jev_fallback_luna`, `consensus_ok`, `consensus_split`, `shadow_mismatch` も表示・集計できます。旧記録に書き手の debug がなければ usage は 0 扱いです。単価は `probe_metrics.py` の定数で、Jev は単価未設定です。判定を共有した分も各パターンに計上するため、パターン費用の和は実請求額と異なります。

ページ生成器は問題ごとのページと生データの JS を出し、過去のパターンも結果に含まれるものを表示します。`--out` 省略時は `docs/app/sets/umigame-soup-1-probe.html` に出力します。

`tools/probe_sweep.py --probe <results.json のあるディレクトリ>` は Jev の段 B / B2 から閾値を掃引し、`sweep.json` に書きます。Jev は過去の `jev-2b` と現在の `jev-2c` / `jev-1b-haiku` を読めます。`--fill-b2` は不足する B2 だけを Jev API で取得し、`sweep_b2_cache.json` に保存します。合意ルールの参考集計では、旧結果の Decisions の判定も読めます。新しい Decisions の判定・B2 取得は行いません。
