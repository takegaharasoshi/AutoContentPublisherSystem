---
name: umigame-stock-replenish
description: umigame-soup-1（探偵カメロックのウミガメのスープ）の問題ストック(umigame_stock_items)を補充する運用スキル。照合と在庫確認 → G1a 候補(目標の 2 倍のコア宣言を一括)→ 人間の一括選別(OK / NG / 保留)→ G1b 素材の仕上げ → 素材のまとめレビュー → G2 プローブ用コメントの準備 → コメントレビュー → G3 機械プローブ → 結果確認・人間プローブ(必要時)・GO → G4 動画ビルド → 動画レビュー → G5 本番へ一括アップロード(投入 + 配置 + 記録)。週 4 問・在庫水位 8 問以上。「ウミガメの週次補充」「umigame の在庫を足す」「第 N バッチ」で使う。1 問だけの書き直しは umigame-problem-writer を直接使う。
---
> **Claude Code 専用(Codex は起動しない)**。Codex 直接セッションの対象スキルは idea / issue / quiz-stock-replenish の 3 本(Phase 23-2・AGENTS.md「直接セッションのルール」)。

# ウミガメストック補充スキル（umigame-stock-replenish）

umigame-soup-1 の問題ストック（`umigame_stock_items`）を補充するための運用スキル（21-8a〔2026-10-12〕で新設、同日の認識合わせで流れを全面改訂）。作り方は logic-training-1 の補充（`quiz-stock-replenish`）に倣い、**候補を目標の 2 倍まとめて出して人が一括で選ぶ**。作問の中身（コア宣言の型別の様式・工程 4〜9 の検査）は `/umigame-problem-writer` が正で、本スキルはゴールの切り方・資材の置き場・レビュー用ページ・投入と配置を持つ。

正の所在: 素材 18 項目（#18 核心語 `core_words` を含む）の仕様 = `docs/app/sets/umigame-soup-1.html` セクション 4、補充とレビューのペース・作り方の規定・事前ビルド = `docs/production/umigame-soup-1.html`(生産の詳細設計)、作問の手順 = `.claude/skills/umigame-problem-writer/SKILL.md`（候補段階はセクション 1.5、型別の分冊 story.md / misdirection.md）、素材ツール = `content/umigame-stock/umigame-soup-1/README.md`、動画ビルド = `content/video-build/umigame-soup-1/README.md`、計画と記録 = `docs/plans/umigame-soup-1.html` / `umigame-soup-1-log.html`。矛盾したら設計書・ツール > 本スキル。

**前提**: 投稿は夜 20:00 JST の**週 4 回（日・火・木・土）**で消費は**週 4 問**。**型は両型同数**（4 問なら story 2 / misdirection 2）。**在庫水位の目安は未使用ビルド済み 8 問（2 週間分）以上**。

**ツールと核心語の置き場**: プローブ用ツール（`probe_run.py`・`build_probe_page.py`・`local_trial.py` ほか）とそのテスト・実行環境・出力先は `content/umigame-stock/umigame-soup-1/`（実行はセットのディレクトリの `.venv` から、出力の既定は `work/`〔git 管理外〕。手順はセットの `README.md`「ローカル試行・評価プローブの実行環境」「評価プローブ」）。核心語は素材 #18 `core_words`（`stock_items.py` → DB 列〔V017〕→ スナップショット v4 → 返信 Lambda）で、補充に `services/` の変更・deploy は要らない（21-8c〜21-8d2 で移行済み。2026-10-13 に本番切替）。

## 資材の置き場

- **候補**: `content/umigame-stock/umigame-soup-1/candidates/<バッチ名>/`。1 候補 1 ファイル（`s01.md …` = story、`m01.md …` = misdirection）。形式・状態・集計は同ディレクトリの `README.md`・`_template.md`・`tally.py`（**初回〔第 2 バッチの G1a〕で logic-training-1 の `candidates/` を雛形に作る**。状態の名前は logic-training-1 と同じ: `unreviewed` / `ok` / `ng` / `hold` / `drafting` / `approved` / `final_ng` / `withdrawn`）。`INDEX.md` は `tally.py` の生成物
- **素材**: `content/umigame-stock/umigame-soup-1/<バッチ名>/`（`batch-02` から連番）。直前のバッチから `stock_items.py`（問題は空にする）・`validate.py`・`review_sheet.py`・`generate.py` をコピーし、`batch-01` 固定の参照を直す。`research.md`・`STATUS.md` は新しく書く。**`content_key` の 3 桁連番は全バッチ通しで重ねない**（先頭は既存の最大 + 1。第 1 バッチの欠番 002 は再利用しない）
- **プローブのページ**: バッチごとに `docs/app/sets/umigame-soup-1-probe-<バッチ名>.html`（サマリー + 末尾にコメントレビュー節）と `docs/app/sets/umigame-soup-1-probe-<バッチ名>/UXX.html`（問題別）。入口は `docs/app/sets/umigame-soup-1-probe-index.html`（全バッチと第 1 バッチ・6d17 のページへのリンク。30-6b〔2026-10-18〕で作成済み。**バッチのページを作ったら表の一番上に 1 行足す**）
- **再開地点**: バッチの `STATUS.md` に「いまどのゴールか・人の判断待ちか・型別の OK 数と不足・次に何をするか」を書く。候補側は `INDEX.md` と各ファイルの `state` が正

## 起動時（工程に入る前に必ず）

1. **確認待ちリストの照合**（ルールは `docs/plans/index.html` セクション 5.2）: `docs/plans/umigame-soup-1.html` の「確認待ちリスト」で、トリガー列が「次の週次補充」または期日を過ぎた日付型の行を拾い、該当するゴールの完了条件に足す。確認したら結果列に日付 + 結果を書く（OK なら `umigame-soup-1-log.html` へ移す。NG なら「NG 時の扱い」列に従う）。該当なしなら「確認待ち: 該当なし」と宣言する
2. **課題表の照合（セット名）**（ルールは `docs/issues/index.html` セクション 4.8）: `grep -n "umigame" docs/issues/index.html` で live 表を引き、トリガー列が「umigame-soup-1 の次の週次補充」「第 N バッチ」の行を拾って「同梱 / トリガー更新で据え置き継続 / 受容」を決めて表を更新する。該当なしなら「課題表: 該当なし」と宣言する
3. **在庫確認**（**Aurora の値が正**）。`unused_built` が 8 問を下回る、または下回る見込みなら今週の 4 問を補充する。`unbuilt` が 0 以外なら投入済みのビルド漏れなので、補充より先に G4・G5 を終わらせる。在庫が尽きると LRU で再利用になる（前回の真相ブロックで答えを公開済みの問題を再び出すことになる）

```sql
SELECT COUNT(*) AS active_total,
       SUM(s.last_used_at IS NULL AND s.video_s3_key IS NOT NULL) AS unused_built,
       SUM(s.video_s3_key IS NULL) AS unbuilt,
       MAX(s.last_used_at) AS last_used_at
FROM umigame_stock_items s JOIN batch_sets b ON b.id = s.set_id
WHERE b.set_code = 'umigame-soup-1' AND s.is_active = 1;
```

Aurora へは `python3 content/ranking-stock/pref-ranking-1/common/apply_aurora.py <sql ファイル>`（Data API・自動一時停止からの復帰リトライ内蔵）で流す。型の内訳は DB に列がないため `validate.py` の集計行で見る。

## ゴールの切り方（ゴール 6 本・人の判断 5 か所）

`/goal` はスキルから起動できないので、各ゴールの行をコードブロックで提示してユーザーが打つ。**goal が立つまで工程に入らない**。**人の判断はゴールに含めない**（ゴール到達 = 判断を始められる状態）。G5 は Aurora・S3 を更新するため auto mode で走らせない（許可プロンプトがゲートを兼ねる）。証跡（検証・集計・件数クエリの出力）は省略せず会話に貼る。

1. **G1a 候補の準備** → 【人】**選別**（OK / NG / 保留）
2. **G1b 素材の仕上げ** → 【人】**素材のまとめレビュー**（素材シート `work/review.html`）
3. **G2 プローブ用コメントの準備** → 【人】**コメントのレビュー**（バッチのプローブページ末尾）
4. **G3 機械プローブ** → 【人】**結果の確認・人間プローブ（必要時）・GO 判定**
5. **G4 動画ビルド** → 【人】**動画レビュー**（動画のレビューシート。インデックス `work/review.html` → 今回のシート `work/review/<バッチ名>.html`）
6. **G5 本番へ一括アップロード**（投入 + 配置 + 記録）

ゴール行の例（`<バッチ名>`・数を埋めて提示する。各 `or stop after 20 turns`）:

```
/goal セットレーン umigame-soup-1・週次補充 G1a（候補の準備）<バッチ名>。完了条件: 在庫確認クエリの出力を貼って目標（型別）を確認し、目標の 2 倍の候補（story と misdirection を同数）を umigame-problem-writer セクション 1.5 の候補段階で書いて candidates/<バッチ名>/ に置き、tally.py の集計（出力を貼る）と候補一覧（1 案 3 行）を提示できる状態。素材は書かない。人間の選別は開始しない。Aurora・S3・services/ には触らない。or stop after 20 turns
```

```
/goal セットレーン umigame-soup-1・週次補充 G1b（素材の仕上げ）<バッチ名>。完了条件: tally.py で型別の不足 0 を確認し（出力を貼る）、OK のうち目標数だけを umigame-problem-writer の工程 4〜9 で 1 問ずつ素材にして stock_items.py に書き（候補の state を drafting に更新）、validate.py 全パス（出力を貼る）・review_sheet.py で work/review.html を生成し、自己検査 10 行を問題ごとに会話に書いた状態。素材の人間レビューは開始しない。or stop after 20 turns
```

```
/goal セットレーン umigame-soup-1・週次補充 G2（プローブ用コメントの準備）<バッチ名>。完了条件: 承認済み N 問について問題ごとのプローブ用コメントと正解ラベルを作り、docs/app/sets/umigame-soup-1-probe-<バッチ名>.html の末尾のコメントレビュー節に載せて（インデックスにもリンク）、docs_check のリンク検査が OK（出力を貼る）。プローブは実行しない。コメントの人間レビューは開始しない。or stop after 20 turns
```

```
/goal セットレーン umigame-soup-1・週次補充 G3（機械プローブ）<バッチ名>。完了条件: 承認済みコメントを評価データに入れて probe_run.py を回し（要約を貼る）、バッチのサマリーページと問題別 UXX.html を生成してインデックスを更新し、不一致の一次分析（確定事実シートの穴 / 正解ラベルの誤り / 判定の揺れ）を提示した状態。素材の修正・GO 判定はしない。or stop after 20 turns
```

```
/goal セットレーン umigame-soup-1・週次補充 G4（動画ビルド）<バッチ名>。完了条件: GO の N 問について export_prompts → 背景生成 → intake → background_sheet（背景を全数目視して所見を書く）→ build.py --batch <バッチ名>（予算超過・読み間違いの取り直し込み）→ review_sheet.py --batch <バッチ名> で動画のインデックス work/review.html と今回のシート work/review/<バッチ名>.html を更新した状態（出力を貼る）。DB 投入・S3 配置は行わない。or stop after 20 turns
```

```
/goal セットレーン umigame-soup-1・週次補充 G5（本番へ一括アップロード）<バッチ名>。完了条件: 承認 N 問をローカル MySQL（ドライラン → 本適用）と Aurora へ投入し内容の MD5 が両環境で一致（出力を貼る）、publish.py --batch <バッチ名> を dry-run（対象 = N 件）→ 本実行、在庫確認クエリで両環境の unbuilt = 0（出力を貼る）、セット記録に 1 行・セット計画書の在庫を更新して docs_check --plan-only（出力を貼る）、日本語でコミットし pull --rebase → push。or stop after 20 turns
```

## G1a 候補の準備 → 選別

1. **目標と候補数**: 型別の目標（週 4 問なら story 2 / misdirection 2）の 2 倍を書く。**前バッチの余剰 OK（`state: ok` のまま残った候補）を先に数える**
2. **候補を書く**: `/umigame-problem-writer` のセクション 1.5（候補段階）で、型ごとにモチーフ → 連想 → コア宣言までを複数案まとめて行う。**1 案 = 3 行**:
   - コア宣言（型の様式どおり・1 文）
   - 問題文の案（骨子でよい）
   - 正解判定（何を言われたら「正解です！」か・1 文）
   既存問題（全バッチの `stock_items.py`）・台帳との照合（作問スキル工程 7 の Web 照合を含む）は候補段階で済ませ、重複は `withdrawn` にする。素材の項目（確定事実シート・想定質問など）は書かない
3. **提示**: 型ごとに 1 案 3 行で一覧にし、**OK / NG / 保留 だけ**を求める。**理由は任意。書かれなかった理由を推測で埋めない**
4. **記録**: 返答を各候補ファイルの判定欄と `state` に反映し（原案は書き換えない）、`tally.py <バッチ dir> --write-index` の出力を貼る
5. **判定**: 型別に「不足 = 目標 − OK・追加 = 不足 × 2」。**両型とも不足 0 になるまで G1b へ進まない**。不足があれば G1a のゴールを再度立てて追加する
6. NG・保留は消さずに残す（後で振り返りに使う）

## G1b 素材の仕上げ → 素材のまとめレビュー

- OK のうち**目標数だけ**を、`/umigame-problem-writer` の工程 4〜9（不思議にする・手がかりの棚卸し・動線・現実性・照合・素材化）で 1 問ずつ素材にする（候補の `state` を `drafting`・`stock_no` を記録）。**余剰 OK は仕上げない**（次回へ持ち越す）。自己検査 10 行は問題ごとに会話へ書く
- 核心語も素材の 1 項目（#18 `core_words`）として `JUDGE_POINTS` に書く（書き方は `/umigame-problem-writer` 工程 9。`validate.py` が検査し、投入 SQL に入る。`services/` の push は要らない）
- `validate.py` → `review_sheet.py`（`work/review.html`。API キー不要）→ `generate.py --dry-run`
- **素材シートのインデックス**（30-6b で追加）: バッチの `review_sheet.py` は素材シートを書くたびに、セット直下のインデックス `content/umigame-stock/umigame-soup-1/work/review.html`（全バッチの一覧）も更新する（`tools/review_index.py`。単独でも回せる）。新しいバッチの `review_sheet.py` は直前のバッチからコピーするので、末尾のインデックス更新の呼び出しを消さない。ユーザーにはインデックスと今回の素材シートのパスを伝える
- **Claude が先に一次スクリーニングしてから出す**: ①問題文と真相の語・時制の一致 ②`title` が真相の手がかりになっていないか ③`truth` が公開して自然な文か（次回のキャプションで全文公開）④既存問題とモチーフ・仕掛けが近接していないか（近い場合は投稿順を離す申し送り）
- **素材レビュー**: ユーザーが素材シートでまとめて見る（ブラウザーで開くときは `/docs-mobile-view` の要領で HTTP 配信したものでもよい）。指摘は `stock_items.py`（全問共通なら `../common/umigame_common.py`）へ反映 → `validate.py` → `review_sheet.py` → 再提示。指摘のうち手順の穴は作問スキルへ反映する
- 素材で NG になった問題は `stock_items.py` から外し、候補ファイルに「段階: 素材 / 判定: NG」を追記して `state: final_ng`。目標に足りなくなったら余剰 OK を先に使い、それでも足りなければ G1a に戻る

## G2 プローブ用コメントの準備 → コメントのレビュー

- 問題ごとに、プローブで流すコメント（質問・回答の試み）と**正解ラベル**（期待する判定の種類）を作る。観点: 確定事実シートの「はい / いいえ」の境目・正解と惜しいの境目・否定形 / 限定つきの質問・ネタバレを誘う質問・関係ない質問
- コメントはバッチのプローブページ（`umigame-soup-1-probe-<バッチ名>.html`）の**末尾のコメントレビュー節**に問題ごとに載せる。インデックスにバッチのページへのリンクを足す
- **コメントのレビュー**: ユーザーがページで見て、追加・削除・ラベルの修正を指示する。承認後に評価データ `content/umigame-stock/umigame-soup-1/judge-trial/data/eval_problems.json` へ入れる（G3 の最初でもよい）

## G3 機械プローブ → 結果確認・人間プローブ・GO

- `probe_run.py --problems <no...>` で本番と同じ判定・返信文の経路に通す（API キーは `~/.bashrc` の `ANTHROPIC_API_KEY`）。`build_probe_page.py` でバッチのサマリーページと問題別 `UXX.html` を作り、インデックスを更新する
- **不一致の一次分析**を付けて出す: 確定事実シートの穴（→ 素材を直す）/ 正解ラベルの誤り（→ ラベルを直す）/ 判定の揺れ（→ 再実行で確かめる）
- **結果の確認**はユーザー。**人間プローブ**が要るとユーザーが判断した問題は、ユーザーが `local_trial.py --problem <no> --comment ...` で自由にコメントを試す
- 素材を直した問題は G1b の検証（`validate.py`・素材シート）からやり直し、必要なら G2・G3 に戻る。**GO が出た問題だけを G4 へ進める**

## G4 動画ビルド → 動画レビュー

コマンドの正は `content/video-build/umigame-soup-1/README.md`。**`--batch <バッチ名>` を付けて、そのバッチの問題だけを対象にする**。動画ビルドは `stock_items.py` を読むので、DB 投入より前にできる。

1. `export_prompts.py --batch <バッチ名>` → `scripts/gen_backgrounds.sh`（背景生成）→ `intake.py` → `background_sheet.py`（Claude が背景を全数目視: 文字の混入・構図）
2. `build.py --batch <バッチ名>`（Irodori-TTS・ローカル GPU。読み間違い・予算超過は `--retake-tts --content-key <key>`、1 問 3 回まで）→ `review_sheet.py --batch <バッチ名>`
   - **レビューシートはインデックス + バッチ別**（30-6b〔2026-10-18〕で変更）: `review_sheet.py` は実行のたびに `work/manifest.json` を累積の台帳 `work/review_archive.json` へ足し、**インデックス `work/review.html`**（全バッチの一覧・`--batch` のバッチに今回の印）と**バッチ別のシート `work/review/<バッチ名>.html`**（14 本超は `-2.html` …）を書き直す。問題の中身は全バッチの `stock_items.py` から引き、どれにも無い問題は「未分類」に入る（`build.py` の最後にも自動で回る）
   - **補充のたびにインデックスを更新する**: ビルド後に必ず `review_sheet.py --batch <バッチ名>` を回し、**レビューの指摘で作り直したときも、その都度回してから出し直す**。出力の「インデックス: … 件」「シート: <バッチ名>.html（N 件）」の行を会話に貼り、ユーザーにはインデックスと今回のシートのパスを伝える。`work/review_archive.json` は消さない（過去分のシートの元）
3. **動画レビュー**: ユーザーがインデックスから今回のシート（`work/review/<バッチ名>.html`）を開いて全数を見る。承認した `content_key` を `work/approved.txt` に追記する

## G5 本番へ一括アップロード

1. **投入**: `generate.py --dry-run` で ROLLBACK を確かめた後、`insert_umigame_stock.sql` をローカル MySQL へ `--default-character-set=utf8mb4` 付きで流す（落とすと日本語が二重エンコードで壊れる）。Aurora は `apply_aurora.py insert_umigame_stock.sql`。両環境で `problem_text`・`truth`・`fact_sheet`・`judge_criteria`・核心語の MD5 が一致することを確かめる
2. **配置**: `publish.py --batch <バッチ名> --dry-run` で**対象件数 = 今回の承認件数**を確かめてから本実行（S3 + ローカル MySQL + Aurora）。承認ファイルに過去の配置済み分が含まれる場合は、そのバッチ分だけを列挙したファイルを `--approved` で渡す
3. **締め**: 在庫確認クエリで両環境 `unbuilt = 0`（出力を貼る）→ 候補の `state` を `approved` に更新 → セット記録 `docs/plans/umigame-soup-1-log.html` の「週次補充の記録」に表 1 行、セット計画書 `docs/plans/umigame-soup-1.html` のステータス欄の在庫を更新 → `python3 tools/docs_check.py --plan-only`（出力を貼る）→ 資材・台帳・ページの変更をコミットし `pull --rebase` → push

## 実行環境の要点

- WSL に ffmpeg / Chrome は無い。Remotion のレンダリング・ffmpeg・PIL は Docker 経由（README の形）。TTS は `~/tools/Irodori-TTS`（BF16 必須）
- Codex 委譲: 背景生成は imagegen（`scripts/gen_backgrounds.sh`）。類題の Web 照合は `codex --search exec`（作問スキル工程 7）。作問・レビュー・投入判断・コミットは Claude
- 稼働初期（2026-10-12 から 2 週間）はコメント欄の目視をユーザーが毎日行う（セット別設計書）。問題があればストックを `is_active=0` にする
