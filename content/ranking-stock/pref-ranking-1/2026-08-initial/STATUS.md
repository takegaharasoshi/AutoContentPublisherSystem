# 17-3 第 1 バッチ（10 件）の状態

| 項目 | 状態 |
|---|---|
| 対象 | `pref-ranking-1` 初期ストック 第 1 バッチ 10 件（001〜010） |
| データ検証 | 完了（2026-08-10）。証跡は [research.md](research.md) |
| 文言・ナレーション執筆 | 完了。`validate.py` 全項目パス |
| 人間レビュー | **完了（2026-08-11）— 全 10 件承認**。指摘の反映内容は下記「1 巡目の反映」 |
| DB 投入 | **完了（2026-08-11）**。ローカル MySQL / Aurora の両環境へ 10 件。`(title, content_fields, ranking_data, narration, source_note)` の MD5 が全行一致することを確認済み |
| 追補 | **`content_fields.value_prefix` を追記（2026-08-11 / 17-4b）**。下記「投入後の追補」 |
| 動画ビルド | 17-4 のツーリング完成後（17-5） |

## 構成

| ファイル | 役割 |
|---|---|
| `stock_items.py` | 表示文言とナレーション台本の単一ソース（数値は持たない） |
| `data/*.json` | ネタごとの検証済みデータ（`ranking_data` / `full_ranking` / `source_note_text` / `meta`）。`common/convert.py` の出力、または一次情報から機械抽出したもの |
| `validate.py` | 機械検証（`--report` で全 cue のモーラ数一覧、`--selftest` でモーラ推定の自己確認） |
| `generate.py` | `review.md` と `insert_ranking_stock.sql` を生成（実行前に validate を通す） |
| `review.md` | 人間レビュー用シート（生成物） |
| `insert_ranking_stock.sql` | 両環境投入用 SQL（生成物） |
| `update_value_prefix.sql` | 投入済み 10 件へ `value_prefix` を追記する適用済み SQL（17-4b。冪等） |
| `research.md` | データ検証の証跡・採否の判断記録 |

再生成: `python3 validate.py && python3 generate.py`

## 1 巡目の反映（2026-08-11）

| # | 指摘 | 反映内容 |
|---|---|---|
| ① | 家計調査の値が「二人以上世帯・1 世帯あたり年間支出」だと画面のどこにも出ない | `SRC_KAKEI` を `総務省 家計調査 2023〜25年平均／二人以上世帯の年間支出（政令市等を世帯数加重で県換算）` に変更（8 件）。**`subtitle` は 30 秒版の導入 3.5s にしか出ない**ため、両尺の出典行帯とキャプションの双方に出る `source_display` を置き場所にした |
| ② | タイトルが「〜にお金を使う県」でそのまますぎる | 全件「〜大好き都道府県」へ改訂（009 温泉のみ据え置き）。006 は 008 喫茶代と紛らわしいため **`おうちコーヒー大好き都道府県`**、あわせて trivia を「喫茶文化」ではなく家庭内購入の説明に修正 |
| ③ | `intro` の後に予想を促す煽りが欲しい | ナレーションに **`teaser` cue を新設**（全 20 件 = 10 ネタ × 2 尺）。原資は 5〜2 位の呼び込みと県名の cue 統合。総尺・1 位シーン・結果総覧・締めは不変 |
| ④ | 各フィールドの使われ方はレビューの前提 | レビューシートの冒頭に「表示文言フィールドの使われ方」表を常設（`generate.py`） |
| ⑤ | 010 の hook「8人に1人」は 12.2%（= 8.2 人に 1 人）をわずかに盛っている | 「約8人に1人」に是正 |
| ⑥ | 締めのセリフに中身がない | 20 秒版の `outro` を **「みんなはわかったかな？」で全ネタ共通**に（`teaser` の答え合わせ）。30 秒版は県名を並べるだけの `recap` を廃止し、`recap` + `outro` を **`closing` 1 本**（結果総覧 3.0s + 締め 2.0s をまたぐ）へ統合して、ネタの含意を口語で言い切る形にした |
| ⑦ | trivia の文体がキャラクター表現になっていない | `hook` / `trivia` を **表彰台五郎の一人称（タメ口の実況調）** に統一（10 件）。キャプションだけ中立の解説調だと書き手が入れ替わって見えるため。数値・単位・出典は原文どおり。**文体規定が設計書に無かった**のが原因なので、セット別設計書セクション 5 に規定として明記した |

タイムライン・cue 体系の変更は方式設計書
（`docs/app/generators/ranking-prebuilt.html` セクション 8.2 / 8.3 の decision）に反映済み。
17-4 への実装制約（アンカーの後ろ合わせ・吹き出しの表示開始）も同 decision に記載。

## 投入後の追補: `value_prefix`（2026-08-11 / 17-4b）

17-4a の版面 Fix で `content_fields.value_prefix`（順位行の数値の前置き。例「年間◯◯円」）を
新設したが、第 1 バッチ 10 件は**このフィールドを持たない状態で投入済み**だったため、
17-4b の頭で両環境へ追記した（17-4e のビルドツーリングが初期ビルドをかける前に済ませる必要があった）。

- 値の決め方: **家計調査の 8 件が `"年間"`**（ランキング表の値が「1 世帯当たり年間支出金額」のため）。
  **009 温泉（源泉総数）・010 釣り（社会生活基本調査の行動者率）は `null`**（前置きが要らない指標）
- 単一ソース化: `common/convert.py` が `meta.prefix` を出力するようにし（家計調査は既定 `年間` /
  `--prefix ""` で無効化）、`generate.py` が `data/*.json` の `meta.prefix` を
  `content_fields.value_prefix` へ機械転記する。**手書きしない**（`result_list` / `value_suffix` と同じ扱い）
- 適用: `update_value_prefix.sql`（`JSON_SET` で該当キーのみ更新。冪等）をローカル MySQL と
  Aurora（`common/apply_aurora.py`）の両方へ適用。適用後、**10 行の MD5 が両環境で一致**し、
  かつ**DB の `content_fields` が生成元（`generate.py` の出力）と完全一致**することを確認済み

## 投入時に見つかった不具合（2026-08-11・修正済み）

先行登録した `batch_sets` の `pref-ranking-1` 行の `name` が、**ローカル MySQL 側だけ
二重エンコードで文字化けしていた**（`CHAR_LENGTH` = 45 = 15 文字 × 3）。原因は
`docker exec ... mysql` に `--default-character-set=utf8mb4` を付けずに INSERT したこと
（`docs/plans/development-plan.html` の 2026-07-29 / 15-10 に記録済みの既知の落とし穴）。
正しい値で UPDATE して解消済み（Aurora 側は Data API 経由のため元から正常）。

**同じ原因で `fantasy-animals-1` の `name` もローカルだけ文字化けしている**
（`CHAR_LENGTH` = 33 = 11 文字 × 3）。旧セットのため本ステップでは触っていない。

## 投入前の前提（重要）

`insert_ranking_stock.sql` は `set_id` を
`(SELECT id FROM batch_sets WHERE set_code = 'pref-ranking-1')` で解決する。
**`batch_sets` に `pref-ranking-1` の行が無い状態では投入できない**（`set_id` が NULL になり
NOT NULL 制約で落ちる）。セット登録は本来 17-5 の手順（operation.html セクション 2.1）だが、
ストック投入がそれに先行するため、最小構成の行
（`set_code` / `name` / `generator_name='ranking-prebuilt'` / `stories_enabled=1` / `is_active=0`）
を先に登録する必要がある。`is_active=0` の間は両バッチがスキップして正常終了するため安全で、
17-5 でアカウント・プロンプト・キャプション・BGM を揃えたうえで `is_active=1` にする。

## プレビュー動画（2026-08-10）

ネタ判断の材料として 001 / 002 / 009 の 20 秒版プレビューを
`plans/ranking-set-research/remotion-proto/`（git 管理外）でビルドした
（`PrefRankingPreview` コンポジション + `scripts/build_preview.py`）。
実データ + VOICEVOX ナレーション + imagegen 背景つきで、**ナレーションは全 cue が実測で予算内**。

**このプレビューは 17-3 のレビュー対象ではない**（17-3 のレビュー観点はデータの正しさ・表現・重複・
フォーマット適合の 4 点で、対象は `review.html` のテキスト）。版面の品位は 17-4 の作り込みで扱う。
プレビューから出た版面の課題と実行環境の知見は `docs/plans/development-plan.html` の 17-4 に申し送り済み。

## 残作業（第 2・第 3 バッチ）

初期ストックは 30 件が目標（operation.html セクション 3）。残り 20 件は同じ手順
（リサーチ → データ検証 → 執筆 → レビュー → 投入）で `2026-08-initial-2` 等の別バッチとして進める。
第 1 バッチで確立した採否ルール（TOP6 に同値があるネタは不採用 / 時刻・時分の指標は現行の
データモデルに載らない）は [research.md](research.md) を参照。
