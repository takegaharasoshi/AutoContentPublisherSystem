# umigame-soup-1 ストック資材（ウミガメのスープ参加型セット）

`umigame_stock_items`（V012）へ投入する問題ストックのバッチ別ソースと整備ツーリング。仕様の正は
[セット別設計書](../../../docs/app/sets/umigame-soup-1.html) セクション 4（素材 18 項目）、投入手順の正は
[運用設計](../../../docs/app/operation.html)。**作問の手順（コア宣言・動線・現実性の自己検査）の正はスキル `.claude/skills/umigame-problem-writer/SKILL.md`**。

```
umigame-soup-1/
├── common/umigame_common.py # セット既定文、イラスト / キャプションの組み立て、素材項目のキー一覧
├── set-registration/        # セット登録 SQL 4 本・ローカル dry-run・稼働開始の手順書（STATUS.md。21-7）
├── tools/                   # write_snapshot.py（スナップショットの手動再出力。21-7）+ プローブ用ツール（21-8c）+ tests/（21-8c2）
├── pyproject.toml           # tools/tests の pytest 設定（21-8c2）
├── .venv/ · work/           # 実行環境とツールの出力（gitignore。21-8c2）
└── batch-01/                # 第 1 バッチ（全 14 問 = story 7 / misdirection 7）
    ├── stock_items.py       #   単一ソース（素材 18 項目〔判定・出力ガード用の 4 項目は JUDGE_POINTS〕+ 管理項目）
    ├── validate.py          #   素材の機械検証
    ├── review_sheet.py      #   素材レビューシート生成（API キー不要）
    ├── generate.py          #   insert_umigame_stock.sql の生成 + ローカル MySQL でのドライラン
    ├── research.md          #   リサーチ台帳
    ├── STATUS.md            #   進行状況（引き継ぎメモ）
    └── work/review.html     #   review_sheet.py が生成する素材レビューシート（gitignore）
```

## 素材の確認と投入準備

```bash
cd content/umigame-stock/umigame-soup-1/batch-01
python3 validate.py
python3 review_sheet.py       # work/review.html を生成。API キー不要
python3 generate.py --dry-run # SQL を生成し、ローカル MySQL でトランザクション内に流して ROLLBACK
```

本番経路の機械プローブは `tools/probe_run.py` を使う（21-8c で `services/comment-reply/tools/` から移し、21-8c2 でテスト・実行環境・出力先もこのディレクトリへ寄せた）。評価ケースは
`judge-trial/data/eval_problems.json` に追加してから `--problems <no>` を指定する。手順は下の「評価プローブ」。

## ローカル試行・評価プローブの実行環境

ツールは Python 3.10 以上が要ります（WSL の `python3` は 3.8 のため `~/.local/bin/python3.12` を使う）。標準ライブラリだけで動き、boto3 は本番の S3 書き込みでだけ遅延 import するため、`.venv` に入れるのは pytest だけです（`tools/requirements-dev.txt`）。`.venv/` と `work/` は git 管理外です。

```bash
cd content/umigame-stock/umigame-soup-1
python3.12 -m venv .venv
.venv/bin/pip install -r tools/requirements-dev.txt
.venv/bin/python -m pytest -q   # tools/tests（プローブ用ツールと write_snapshot.py）
```

## ローカル試行

```bash
cd content/umigame-stock/umigame-soup-1

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

`--snapshot path.json` で公開スナップショットを読み込めます。`--comment` は繰り返し指定可、`--comments-file` は 1 行 1 コメント、指定なしは対話入力です。`--out` の既定はセットのディレクトリの `work/local_trial/` です（`probe_run.py`・`contradiction_sweep.py` も同じ `work/` を使う。git 管理外。21-8c2 で `services/comment-reply/` から移した）。stub 時の書き手は 2b 定型に切り替えます。

`--patterns` は下表の番号 `1 2 5 7 9 10` を受け付け、`--modes` と `--reply-variant` より優先します。記録は `p<番号>-<モード>-<案>/` に保存します。`--haiku-effort` / `--luna-effort` の既定は Config の値です。複数指定すると、その方式で判定するか対応する書き手を使うパターンを effort ごとに実行します。サブにだけ使う方式には最初の指定値を使います。判定・返信の所要秒数も表示します。

2b の正解返信は `CORRECT_PREFIX + reveal_text` です。その他の返信種別は各 3 通り以上の定型文を持ち、`sha1(comment_id)` で選びます。語だけの q_open は 3 通りの専用定型文です。

## 評価プローブ

実行はこのディレクトリから、上の `.venv` で行います（判定・書き手は `services/comment-reply/app` を読み込む）。

`probe_run.py` は本番の判定・書き手・コメント記録を通し、`results.json` と `metrics.json` を出します。ケースごとに方式・effort 単位で判定を共有し、`judge_cache.json` / `writer_cache.json` で再開できます。メイン成功時にはサブを呼びません。独立したケースと書き手は `--workers`（既定 4）で並列に実行します。

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

`probe_sweep.py --probe <results.json のあるディレクトリ>` は Jev の段 B / B2 から閾値を掃引し、`sweep.json` に書きます。Jev は過去の `jev-2b` と現在の `jev-2c` / `jev-1b-haiku` を読めます。`--fill-b2` は不足する B2 だけを Jev API で取得し、`sweep_b2_cache.json` に保存します。合意ルールの参考集計では、旧結果の Decisions の判定も読めます。新しい Decisions の判定・B2 取得は行いません。
