# 17-7 第 3 バッチ（16 件）の状態

| 項目 | 状態 |
|---|---|
| 対象 | `pref-ranking-1` 追加ストック 第 3 バッチ 16 件（015〜030）。初期 30 ネタの最終バッチ。スキル `/ranking-stock-replenish` の実地テスト |
| データ検証 | 完了（2026-08-27）。証跡は [research.md](research.md)。不採用: 卵・料理・DIY（TOP6 同値）・バナナ（TOP5 が 35 円幅の団子） |
| 文言・ナレーション執筆 | 完了（30 秒版のみ）。`validate.py` 全項目パス（上限到達 cue は執筆時に短縮済み） |
| 人間レビュー | **未実施**。一次スクリーニングの申し送りは [research.md](research.md) の「申し送り」 |
| DB 投入 | 未実施（レビュー承認後） |
| 動画ビルド | 未実施（投入後。背景 imagegen 16 枚 → 30 秒版ビルド → 全数レビュー → S3 / 両環境 DB） |

## 構成

第 2 バッチ（[../2026-08-initial-2/STATUS.md](../2026-08-initial-2/STATUS.md)）と同じ構成。差分のみ:

| ファイル | 役割 |
|---|---|
| `extract_shakai.py` | 社会生活基本調査 rank25 / 27 / 28 → `data/{gardening,manga,basketball}.json` の機械抽出（1 シート 2 表の列オフセット対応。入力ディレクトリは引数で渡す） |
| `validate.py` / `generate.py` | 第 2 バッチ版のコピー（表記のみ第 3 バッチへ更新） |

- 家計調査 13 件の `data/*.json` は `common/convert.py` の出力（`--json`）。抽出スクリプトは持たない
- `no` はセット通し番号（015〜030）。`narration` に `"20s"` キーは無い
- 再生成: `python3 validate.py && python3 generate.py`（common/ の venv を使う: `../common/.venv/bin/python`）
