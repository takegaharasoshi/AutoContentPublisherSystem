# 17-5a 第 2 バッチ（4 件）の状態

| 項目 | 状態 |
|---|---|
| 対象 | `pref-ranking-1` 追加ストック 第 2 バッチ 4 件（011〜014）。**尺は 30 秒のみ**（17-5a の単尺確定後、最初のバッチ） |
| データ検証 | 完了（2026-08-24）。証跡は [research.md](research.md) |
| 文言・ナレーション執筆 | 完了（30 秒版のみ）。`validate.py` 全項目パス |
| 人間レビュー | **完了（2026-08-25）— 全 4 件承認（指摘なし）**。一次スクリーニングの申し送りは [research.md](research.md) の「順位確定性の注記」 |
| DB 投入 | **完了（2026-08-25）**。ローカル MySQL（ロールバック・ドライラン → 本適用）/ Aurora（Data API）の両環境へ 4 件。セット計 14 行の `(title, content_fields, ranking_data, narration, source_note)` MD5 が両環境で全行一致・`CHAR_LENGTH` 正常を確認済み |
| 動画ビルド | 17-5c（背景 imagegen → 30 秒版ビルド → 全数レビュー） |

## 構成

第 1 バッチ（[../2026-08-initial/STATUS.md](../2026-08-initial/STATUS.md)）と同じ構成。差分のみ:

| ファイル | 役割 |
|---|---|
| `extract_walking.py` | 社会生活基本調査 rank21.xlsx → `data/walking.json` の機械抽出（入力ファイルは引数で渡す） |
| `extract_myhome.py` | 住宅・土地統計調査 概要 PDF 付表 → `data/myhome.json` の機械抽出（同上） |
| `validate.py` | 第 1 バッチ版に「20 秒版 cue の任意化」（17-5a）+「バッチ先頭番号からの連番検査」を加えたコピー |
| `generate.py` | 第 1 バッチ版のコピー（タイトル文言のみ第 2 バッチ表記） |

- `no` はセット通し番号（011〜014）。`narration` に `"20s"` キーは無い（新規執筆は 30 秒版のみ。
  [../WRITING-NOTES.md](../WRITING-NOTES.md) の 2026-08-24 前提を参照）
- 再生成: `python3 validate.py && python3 generate.py`
