# pref-ranking-1 県換算ツーリング（common/）

家計調査（**県庁所在市・政令指定都市** 52 市）の品目別ランキングを、
**47 都道府県のランキング**へ換算するローカル専用ツール。バッチ（`../<バッチ名>/`）をまたいで使う
共通資材のため `common/` に置く（置き場のルールは
[docs/app/operation.html](../../../../docs/app/operation.html) セクション 3）。

換算方針（Phase 17 決定）は `docs/plans/development-plan.html` の Phase 17 冒頭②と
[docs/app/sets/pref-ranking-1.html](../../../../docs/app/sets/pref-ranking-1.html) セクション 1 が正。

## 換算ルール

1. 家計調査の公表対象は 52 市 = 47 県庁所在市（東京は「東京都区部」）+ 県庁所在市でない政令市 5
   （川崎・相模原・浜松・堺・北九州）
2. 同一県に複数市がある **4 県は世帯数による加重平均**で合算する（支出額は「1 世帯あたり平均」のため
   単純平均・単純合計は不可）
   - 神奈川県 = 横浜 + 川崎 + 相模原 / 静岡県 = 静岡 + 浜松 / 大阪府 = 大阪 + 堺 / 福岡県 = 福岡 + 北九州
3. 残り 43 県は県庁所在市の値をそのまま県値として採用する
4. **注記義務は残る**: 合算後も母集団は「県庁所在市・政令市の世帯」のみ。動画の出典行とキャプションに
   「※家計調査（県庁所在市・政令市の世帯数加重平均）」の類の注記を必ず入れる
   （`content_fields.source_display`）

## 世帯数ウェイト（households.csv）

| 項目 | 内容 |
|---|---|
| 出典 | 令和2年国勢調査 人口等基本集計 **第6-3表**（世帯人員の人数別一般世帯数－全国，都道府県，市区町村） |
| e-Stat 統計表 | 統計表 ID `0003445278` — https://www.e-stat.go.jp/dbview?sid=0003445278 |
| ダウンロード | https://www.e-stat.go.jp/stat-search/file-download?fileKind=0&statInfId=000032142483 （xlsx） |
| データ年 | 2020 年（令和 2 年） |
| 値の定義 | **二人以上の一般世帯数 = 一般世帯数（総数） − 世帯人員が 1 人の一般世帯数** |
| 取得日・検証 | 2026-08-10。上記 xlsx を直接パースして 52 市分を機械生成し、9 市（加重平均対象）は個別に突合済み |

家計調査の調査対象が「二人以上の世帯」であるため、ウェイトも**二人以上の一般世帯数**を使う
（総世帯数には施設等の世帯が含まれ、単独世帯を含む一般世帯数は大都市ほど過大になる）。
実際に加重平均へ効くのは上記 4 県の 9 市だけだが、透明性のため 52 市すべてを保持している。

**更新タイミング**: 国勢調査は 5 年ごと。令和 7 年（2025 年）国勢調査は 2026-05-29 に人口速報集計が
公表済みだが、**世帯人員別の一般世帯数を含む「人口等基本集計」は 2026 年 9 月までの公表予定**
（https://www.stat.go.jp/data/kokusei/2025/kekka.html ）。公表後に本 CSV を令和 7 年ベースへ更新し、
`data_year` / `source_name` / `source_url` を差し替える。更新しても既存ストックの
`ranking_data` は再計算しない（投入時点の出典・データ年を `source_note` で保持しているため。
再計算する場合は動画の再ビルドを伴う）。

## 使い方

```bash
# 初回のみ（ローカル専用の venv）
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt

# 品目の一覧（rank01〜14 をダウンロードしてキャッシュ。系列と単位まで表示）
.venv/bin/python convert.py list
.venv/bin/python convert.py list --rank 10

# 都道府県ランキングへ換算（既定は金額系列）
.venv/bin/python convert.py convert --item "ぎょうざ"
.venv/bin/python convert.py convert --item "米" --measure 数量        # 単位は kg が自動で付く
.venv/bin/python convert.py convert --item "ぎょうざ" --json out.json  # ストック投入用の JSON
```

出力 JSON の `meta.prefix` / `meta.suffix` は `content_fields.value_prefix` / `value_suffix`
（版面の順位行の「**年間** 3,478 **円**」）になる。家計調査の値は 1 世帯当たり**年間**支出金額 /
年間購入数量のため `prefix` の既定は `年間`。前置きが不要なネタ（一次情報から手で作る JSON を含む）は
`--prefix ""` または `meta.prefix = null` にする。

出力は 4 点:

1. 47 都道府県の降順一覧（目視確認用）
2. `ranking_data` の JSON（`ranking_stock_items.ranking_data` にそのまま入る形。
   **都道府県コードと数値のみで言語文字列を含まない** = 英語圏展開の再利用要件④）
3. `source_note` 用の加重平均の計算過程（4 県分。`ranking_stock_items.source_note` へ貼る）
4. 出典行の素材（調査名・データ年ラベル・取得日・URL）

ダウンロードした xlsx は `.cache/` に置かれ git 管理外。最新版へ更新したいときは `.cache/` を消す。

## 構成

| ファイル | 役割 |
|---|---|
| `prefectures.py` | 47 都道府県マスタ（JIS X 0401 コード）と家計調査 52 市 → 県コードの対応 |
| `kakei.py` | 家計調査 rank01〜14.xlsx のダウンロードとパース（金額 / 数量の 2 系列・単位の抽出・52 市の網羅検査） |
| `convert.py` | 換算 CLI（`list` / `convert`）。加重平均は `Decimal` + `ROUND_HALF_UP` |
| `households.csv` | 世帯数ウェイトの静的テーブル（上記） |
| `tests/` | pytest（`.venv/bin/python -m pytest`） |

## 注意

- 家計調査のランキング表は **品目ごとに独立して降順ソート済み**で、行の並びは品目間で一致しない
  （パーサは市名と値のペアで読む）。
- 品目によっては「金額」と「数量」の 2 系列がある（例: 米・パン・麺類）。`--measure` で選ぶ。
  既定は金額。
- **本ツールは家計調査（出典 A）専用**。人口動態統計・社会生活基本調査など都道府県単位で公表される
  統計（出典 B〜I）は換算不要で、ネタ資材側で直接 `ranking_data` を作る。
