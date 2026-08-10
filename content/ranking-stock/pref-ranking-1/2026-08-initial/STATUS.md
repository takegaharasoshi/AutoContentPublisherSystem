# 17-3 第 1 バッチ（10 件）の状態

| 項目 | 状態 |
|---|---|
| 対象 | `pref-ranking-1` 初期ストック 第 1 バッチ 10 件（001〜010） |
| データ検証 | 完了（2026-08-10）。証跡は [research.md](research.md) |
| 文言・ナレーション執筆 | 完了。`validate.py` 全項目パス |
| 人間レビュー | **未実施**（[review.md](review.md) をユーザーが確認する） |
| DB 投入 | **未実施**（レビュー承認後に `insert_ranking_stock.sql` をローカル MySQL と Aurora へ適用） |
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
| `research.md` | データ検証の証跡・採否の判断記録 |

再生成: `python3 validate.py && python3 generate.py`

## 投入前の前提（重要）

`insert_ranking_stock.sql` は `set_id` を
`(SELECT id FROM batch_sets WHERE set_code = 'pref-ranking-1')` で解決する。
**`batch_sets` に `pref-ranking-1` の行が無い状態では投入できない**（`set_id` が NULL になり
NOT NULL 制約で落ちる）。セット登録は本来 17-5 の手順（operation.html セクション 2.1）だが、
ストック投入がそれに先行するため、最小構成の行
（`set_code` / `name` / `generator_name='ranking-prebuilt'` / `stories_enabled=1` / `is_active=0`）
を先に登録する必要がある。`is_active=0` の間は両バッチがスキップして正常終了するため安全で、
17-5 でアカウント・プロンプト・キャプション・BGM を揃えたうえで `is_active=1` にする。

## 残作業（第 2・第 3 バッチ）

初期ストックは 30 件が目標（operation.html セクション 3）。残り 20 件は同じ手順
（リサーチ → データ検証 → 執筆 → レビュー → 投入）で `2026-08-initial-2` 等の別バッチとして進める。
第 1 バッチで確立した採否ルール（TOP6 に同値があるネタは不採用 / 時刻・時分の指標は現行の
データモデルに載らない）は [research.md](research.md) を参照。
