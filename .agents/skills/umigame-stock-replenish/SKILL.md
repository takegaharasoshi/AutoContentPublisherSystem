---
name: umigame-stock-replenish
description: umigame-soup-1（探偵カメロックのウミガメのスープ）の問題ストック(umigame_stock_items)を補充する運用ラッパー。起動時の照合(確認待ち・課題表)と在庫確認 → 作問(1 問ずつ umigame-problem-writer に委ねる) → 4 問そろったら機械検証・プローブ・素材の人間レビュー(週 1 回 × 4 問) → 核心語辞書の追記(開発レーン) → 投入 → 動画ビルド(umigame-prebuilt) → 動画レビュー → 配置 → 記録。週 4 問・在庫水位 8 問以上。「ウミガメの週次補充」「umigame の在庫を足す」「第 N バッチを投入・ビルドする」で使う。作問そのものは扱わない。
---
> **Claude Code 専用(Codex は起動しない)**。Codex 直接セッションの対象スキルは idea / issue / quiz-stock-replenish の 3 本(Phase 23-2・AGENTS.md「直接セッションのルール」)。

# ウミガメストック補充スキル（umigame-stock-replenish）

umigame-soup-1 の問題ストック（`umigame_stock_items`）を、第 1 バッチ（Phase 21・14 問）で確立した手順で補充するための**運用ラッパー**（21-8a〔2026-10-12〕で新設）。**作問（コア宣言から素材化まで）は `/umigame-problem-writer` に委ね**、本スキルは在庫確認・照合・ゴールの切り方・投入・ビルド・配置・記録だけを持つ。

正の所在: 素材 17 項目の仕様・補充とレビューのペース = `docs/app/sets/umigame-soup-1.html` セクション 4、作問の手順 = `.claude/skills/umigame-problem-writer/SKILL.md`（型別の分冊 story.md / misdirection.md）、素材ツールの使い方 = `content/umigame-stock/umigame-soup-1/README.md`、動画ビルドのコマンド = `content/video-build/umigame-soup-1/README.md`、計画と記録 = `docs/plans/umigame-soup-1.html` / `umigame-soup-1-log.html`。矛盾したら設計書・ツール > 本スキル。

**前提**: 投稿は夜 20:00 JST の**週 4 回（日・火・木・土）**で、消費は**週 4 問**（21-6i）。**レビューは週 1 回 × 4 問**。バッチの型構成は**両型同数**（4 問なら story 2 / misdirection 2。2026-09-20 ユーザー決定）。**在庫水位の目安は未使用ビルド済み 8 問（2 週間分）以上**。

**資材の置き場**: `content/umigame-stock/umigame-soup-1/<バッチ名>/`（`batch-02` から連番。git 管理）。直前のバッチから `stock_items.py`（問題は空にする）・`validate.py`・`review_sheet.py`・`generate.py` をコピーし、`research.md`・`STATUS.md` は新しく書く。**`content_key` の 3 桁連番は全バッチ通しで重ならないようにする**（`validate.py` はバッチ内の連番と欠番の再利用を検査する。新バッチの先頭は既存の最大番号 + 1。第 1 バッチの欠番 002 は再利用しない）。コピーしたツールの `batch-01` 固定の参照（パス・既定値）は新バッチに合わせて直す。

## 起動時（工程に入る前に必ず）

1. **確認待ちリストの照合**（ルールは `docs/plans/index.html` セクション 5.2）: `docs/plans/umigame-soup-1.html` の「確認待ちリスト」を読み、トリガー列が「次の週次補充」または日付型で期日を過ぎた行があれば、今回の補充で確認して結果列に日付 + 結果を書く（OK なら行を `umigame-soup-1-log.html` へ移す。NG なら「NG 時の扱い」列に従う）。該当なしなら「確認待ち: 該当なし」と一言宣言する
2. **課題表の照合（セット名）**（ルールは `docs/issues/index.html` セクション 4.8）: `grep -n "umigame" docs/issues/index.html` で live 表（umigame-soup-1 の節 + 開発レーンの節でセット名・`services/comment-reply/` を含む行）を引き、トリガー列が「umigame-soup-1 の次の週次補充」「第 N バッチ」の行を拾う。該当行があれば「同梱する / トリガーを更新して据え置き継続 / 受容」を決めて表を更新する（黙って通り過ぎない）。該当なしなら「課題表: 該当なし」と宣言する
3. **在庫確認**（下のクエリ。**Aurora の値が正**。ローカル MySQL は投入のドライラン用）。`unused_built` が 8 問を下回る、または下回る見込みなら今週の 4 問を補充する。`unbuilt` が 0 以外なら投入済みのビルド漏れなので、補充より先に工程 6〜7 を終わらせる。在庫が尽きると LRU で再利用になる（投稿は止まらないが、前回の真相ブロックで答えが公開済みの問題を再び出すことになる）

```sql
SELECT COUNT(*) AS active_total,
       SUM(s.last_used_at IS NULL AND s.video_s3_key IS NOT NULL) AS unused_built,
       SUM(s.video_s3_key IS NULL) AS unbuilt,
       MAX(s.last_used_at) AS last_used_at
FROM umigame_stock_items s JOIN batch_sets b ON b.id = s.set_id
WHERE b.set_code = 'umigame-soup-1' AND s.is_active = 1;
```

Aurora は `python3 content/ranking-stock/pref-ranking-1/common/apply_aurora.py <sql ファイル>`（Data API。自動一時停止からの復帰リトライ内蔵）で流す。型の内訳は DB に列がないため `validate.py` の集計行で見る。

## ゴールの切り方

人間の判断（コア宣言の承認・素材レビュー・動画レビュー）の前後でゴールを切る。`/goal` はスキルからは起動できないので、各ゴールの行をコードブロックで提示し、ユーザーが打つ。**goal が立つまで工程に入らない**。Aurora 更新・S3 配置を含むゴールは auto mode で走らせない（許可プロンプトがゲートを兼ねる）。

| ゴール | 中身 | 終わり（= 人間の判断を始められる状態） |
|---|---|---|
| 作問 A / B × 4 問 | `/umigame-problem-writer` のゴール A（コア宣言の提示）・ゴール B（素材化・機械検査・コミット）を 1 問ずつ | 作問スキルの定義どおり。**4 問そろうまで次へ進まない** |
| G1 素材の仕上げ | 4 問の `validate.py` 全パス・`review_sheet.py`・評価データへのケース追加と `probe_run.py`・核心語の追記案 | 素材シートとプローブ結果を提示（素材の人間レビュー = 週 1 回 × 4 問） |
| 核心語辞書（開発レーン） | 承認した 4 問の語を `services/comment-reply/app/reply/leak_words.json` に追記 → push → `CommentReplyStack` の deploy（ユーザー） | **開発レーンの作業**（下の工程 5） |
| G2 投入とビルド | 投入（工程 6）→ 背景生成 → ビルド → `review_sheet.py` | 動画レビュー用の `work/review.html` を提示 |
| G3 配置と記録 | `publish.py`（dry-run → 本実行）→ 在庫確認で `unbuilt = 0` → 記録 → コミット・push | ゴール到達で補充完了 |

G1 の行の例（N・バッチ名を埋めて提示する）:

```
/goal セットレーン umigame-soup-1・週次補充 G1（素材の仕上げ）<バッチ名>。完了条件: 作問済み 4 問について validate.py が全パス（出力を貼る）、review_sheet.py で work/review.html を生成、judge-trial/data/eval_problems.json に 4 問のケースを足して probe_run.py --problems <no...> を回し結果の要約を貼る、核心語の追記案（content_key ごとの語）を提示する。素材の人間レビューは開始しない。Aurora・S3・services/ には触らない。or stop after 20 turns
```

## 1〜3. 作問（umigame-problem-writer）

- 型は在庫の偏りから決める（`validate.py` の集計行。週 4 問なら各型 2 問）。1 問ずつ `/umigame-problem-writer` を起動し、そのスキルの工程・自己検査・2 ゴールの切り方に従う
- 作問ログ・判定と取り下げの経緯はバッチの `STATUS.md` に残す（作問スキルの定め）。スキルの修正（同じ失敗を次の問でも起こす手順の穴）は作問スキル側へ反映する

## 4. 機械検証・プローブ・素材の人間レビュー（G1）

```bash
cd content/umigame-stock/umigame-soup-1/<バッチ名>
python3 validate.py
python3 review_sheet.py        # work/review.html（API キー不要）
python3 generate.py --dry-run  # insert SQL の生成 + ローカル MySQL でのトランザクション内ドライラン
```

- **プローブ**: 評価データ `content/umigame-stock/umigame-soup-1/judge-trial/data/eval_problems.json` にケースを足し（**正解ラベルは人が確認する**）、`services/comment-reply/tools/probe_run.py --problems <no...>` を回す（ツールの実行だけなら `services/` への書き込みはない）。判定の不一致は確定事実シートの穴か正解ラベルの誤りとして直す。API キーは `~/.bashrc` の `ANTHROPIC_API_KEY`
- **Claude が先に一次スクリーニングしてから出す**: ①問題文と真相の語・時制の一致 ②`title` が真相の手がかりになっていないか ③`truth` が公開して自然な文か（翌回のキャプションで全文公開）④既存問題とモチーフ・仕掛けが近接していないか（近い場合は投稿順を離す申し送り）⑤プローブの不一致の原因
- レビューは**週 1 回 × 4 問**。指摘は `stock_items.py`（全問共通なら `../common/umigame_common.py`）へその場で反映 → `validate.py` → `review_sheet.py` を回し直して再提示。全問承認まで投入しない

## 5. 核心語辞書の追記（開発レーン）

- 核心語辞書 `services/comment-reply/app/reply/leak_words.json`（P1 漏れ候補と本番の出力ガードの正）に、承認した問題の `content_key` と語を足す。**`services/` のパスなので開発レーン**で行い、本番に効かせるには `CommentReplyStack`（本番面）の `cdk deploy`（ユーザー）が要る。comment-reply には CodePipeline が無いので、パイプライン完走の `/goal` は出さない
- **投稿前に deploy を終える**: 辞書に語が無い問題は、出力ガードが真相の語を含む返信を止められない。投入（工程 6）より先、遅くとも配置（工程 7）までに済ませる
- 補充のたびに開発レーンを挟むこの構造は課題 `I-038` で扱う（対応方針が決まったら本節を直す）

## 6. 投入（G2 の前半。素材の全問承認後）

- ローカル MySQL: `generate.py --dry-run` で ROLLBACK を確かめた後、`insert_umigame_stock.sql` を `--default-character-set=utf8mb4` 付きで流す（落とすと日本語が二重エンコードで壊れる）
- Aurora: `apply_aurora.py insert_umigame_stock.sql`
- 投入後に両環境で 4 問の内容（`problem_text`・`truth`・`fact_sheet`・`judge_criteria`）の MD5 が一致することを確かめ、出力を貼る

## 7. 動画ビルド・レビュー・配置（G2 の後半 + G3）

コマンドの正は `content/video-build/umigame-soup-1/README.md`。**`--batch <バッチ名>` を付けて、そのバッチの問題だけを対象にする**。

1. `export_prompts.py --batch <バッチ名>` → `scripts/gen_backgrounds.sh`（背景生成）→ `intake.py` → `background_sheet.py`（背景の一覧で文字混入・構図を Claude が先に全数目視）
2. `build.py --batch <バッチ名>`（Irodori-TTS・ローカル GPU。読み間違い・予算超過は `--retake-tts --content-key <key>`、1 問 3 回まで）→ `review_sheet.py`
3. **動画の全数レビュー**（人間）。承認した `content_key` を `work/approved.txt` に追記する
4. G3: `publish.py --batch <バッチ名> --dry-run` で**対象件数 = 今回の承認件数**を確かめてから本実行（S3 + ローカル MySQL + Aurora）。承認ファイルに過去の配置済み分が含まれる場合は、そのバッチ分だけを列挙したファイルを `--approved` で渡す
5. 締め: 在庫確認クエリで両環境 `unbuilt = 0` を確認（出力を貼る）→ バッチ資材・台帳の変更をコミットし `pull --rebase` → push → セット記録 `docs/plans/umigame-soup-1-log.html` の「週次補充の記録」に表 1 行を追記し、セット計画書 `docs/plans/umigame-soup-1.html` のステータス欄の在庫を更新する。計画書を書き換えたら**コミット前に `python3 tools/docs_check.py --plan-only` を実行し出力を貼る**（計画書は新様式で構造検査の対象。記録ファイルは対象外）

## 実行環境の要点

- WSL に ffmpeg / Chrome は無い。Remotion のレンダリング・ffmpeg・PIL は Docker 経由（README の形）。TTS は `~/tools/Irodori-TTS`（BF16 必須）
- Codex 委譲: 背景生成は imagegen（`scripts/gen_backgrounds.sh`）。類題の Web 照合は `codex --search exec`（作問スキル工程 7）。作問・レビュー・投入判断・コミットは Claude
- 稼働初期（2026-10-12 から 2 週間）はコメント欄の目視をユーザーが毎日行う（セット別設計書）。問題があればストックを `is_active=0` にする
