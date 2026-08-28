---
name: ranking-stock-replenish
description: pref-ranking-1 のランキングストック(ranking_stock_items)を補充する。ネタ選定→一次データの機械パース検証→文言・ナレーション執筆→機械検証→人間レビュー→両環境投入→動画ビルド(ranking-prebuilt)の共通パイプラインと、17-3〜17-5c で確立した執筆・レビューの勘所への導線。週次補充(7 ネタ目安・在庫水位 14 件以上)・追加バッチ整備のどちらにも使う。
---

# ランキングストック補充スキル(ranking-stock-replenish)

pref-ranking-1 セットのランキングストック(`ranking_stock_items`)を、17-3〜17-5c で確立した品質・手順で補充するためのスキル。
正の所在: 運用手順 = `docs/app/operation.html` セクション 3(ランキングストックの節)、フィールド仕様・cue 体系 = `docs/app/generators/ranking-prebuilt.html` セクション 8.3 + `docs/app/data-model.html` セクション 4.13、**執筆・レビュー・投入の実務の勘所 = `content/ranking-stock/pref-ranking-1/WRITING-NOTES.md`(作業前に必読)**。本スキルはパイプラインの流れと迷いやすい分岐だけを持ち、矛盾したら設計書 > WRITING-NOTES > 本スキルの順で勝つ。

**前提(2026-08-24 尺確定)**: 新規執筆は **30 秒版の cue のみ**(`narration` に `"20s"` キーを作らない)。投稿は夜 20:00 JST の 1 日 1 回で**消費は週 7 ネタ**。

**資材の置き場**: `content/ranking-stock/pref-ranking-1/<バッチ名>/`(git 管理)。バッチごとに自己完結の一式 — 単一ソース `stock_items.py`(表示文言とナレーションだけ。**数値は書かない**)・機械抽出 `extract_*.py` と出力 `data/*.json`・検証 `validate.py`・生成 `generate.py`(review.html + insert SQL)・リサーチ証跡 `research.md`・状態 `STATUS.md` — を置く。補充時は**最新バッチの一式を新しいバッチディレクトリ(`2026-09-w1` 等)へコピー**して回し、投入完了時にディレクトリごとコミットする(`data/*.json` は検証済みデータの単一ソースとしてコミットする。`review.md` / `review.html` はルートの `.gitignore` で除外済みの派生物)。県換算・Aurora 適用の共通ツールは `../common/`(`convert.py` = 家計調査 52 市→47 県の世帯数加重換算、`apply_aurora.py` = Data API 適用)。

## 0. 在庫確認(入口)

operation.html セクション 3 の在庫確認クエリで `unused_built_30s`(未使用かつ 30 秒版ビルド済み = 投稿可能在庫)を確認し、**14 件(2 週間分)を下回っていたら 7 ネタ(1 週間分)を目安に補充**する。`unbuilt_30s` が 0 以外なら投入済みのビルド漏れなので、補充より先にセクション 7 のビルドを終わらせる。`*_20s` 列は監視対象外(20 秒版はビルドしない)。再利用 WARNING がログに出ていたら補充遅延のサイン・優先対応。

## 1. ネタ選定・リサーチ

- 供給源は ①ネタ帳 `plans/ranking-set-research/neta-30.md`(git 管理外・17-1 検証の 31 件。各バッチの `research.md` に採用済み・不採用の消し込みがある)②枯れたら家計調査の品目別ランキング(約 500 品目。食べ物系だけで数十本追加採掘可能)や官公庁統計の新規リサーチ
- **ネタ選定基準は「下位の県の人が笑って自虐できるか」**(事業戦略書セクション 6)。× = 所得・離婚率・学力・肥満・犯罪率。△ 判定(出生率・家事育児など)は**上位のみ発表**構成が条件 — TOP5 版面はもともと下位を晒さないが、hook / trivia / closing でも下位・「最下位」に触れない
- **既投入分とのテーマ・出典の重複を避ける**。同一出典ファイル(例: rank13 外食)・近いテーマ(食べ物系の連発)は不採用理由にはならないが、レビューで申し送り「投稿日を離す判断材料」として記録する
- 新規リサーチを Codex に委譲する場合は **MCP 不可・`codex --search exec` 直接実行**(Web 検索が要るため)。出典の再検証も同様。成果物は「出典 URL・データ年・TOP5 の生値」まで。**採用判断と数値の正は必ず手順 2 の機械パースで取り直す**(Codex の報告値をそのまま使わない)

## 2. データ検証・県換算(機械パース必須)

- **数値は必ず一次情報のファイル(e-Stat / 官公庁の xlsx・PDF)を機械パースして得る**。まとめ記事・ランキングサイトは使わない。抽出スクリプト `extract_*.py` は入力ファイルを引数で受け、公表値 2〜3 点のクロスチェックをスクリプト内に書く(第 2 バッチ `extract_myhome.py` が例)
- 家計調査は `common/convert.py`(xlsx ダウンロード → 52 市 → 47 県の世帯数加重換算。`meta.prefix` = 「年間」も出力)。出力は `data/*.json` に置き、`stock_items.py` には数値を書かない
- **採否ルール(17-3 確立)**:
  - **TOP6 に同値があるネタは不採用**(5 位と 6 位が同値だと 5 位だけ載せる根拠がなくなる。validate.py も検査する)
  - **時刻・時分の指標(平均就寝時刻・「1時間45分」)は現行データモデルに載らない**ため見送り(計画書の設計課題リスト。分換算の採否は未決)
  - データ年が古い統計(国民健康・栄養調査の都道府県別 = 2016 年等)を使う場合はデータ年の明記が条件
- 僅差(数円差・0.1pt 差)は同値でなければ採用可だが、`research.md` に「順位確定性の注記」として残しレビューへ申し送る
- 検証の経緯(出典・取得方法・取得日・不採用とその理由)を `research.md` に記録する。**不採用の記録は次バッチの重複検証を省く資産**なので省かない

## 3. 執筆

フィールドごとの「出る場所」と書き方の正は **WRITING-NOTES.md セクション 0〜4**(取り違えると必ず手戻りする)。ここでは落とし穴だけ:

- タイトルは「〜大好き都道府県」に統一(上限 30 字・タイトル帯 1 行制約)。同じ食材で 2 ネタあるときは語を足して区別(「おうちコーヒー」)
- `hook` / `trivia` / ナレーションは**表彰台五郎の一人称・タメ口実況調**。数値・単位・出典は原文どおり。誇張の禁止線(12.2% を「8人に1人」としない)
- 単位・前提(「二人以上世帯の年間支出」等)は `source_display` に置く(`subtitle` は序盤で消えキャプションに出ない)
- `value_prefix` / `value_suffix` / `result_list` は手書きしない(ツーリングが `data/*.json` の meta から転記・整形)
- ナレーション cue(30 秒版のみ): `teaser` 必須・数値は読み上げない・**各 cue は上限の 2 割減を目安に短く**(話速はすでに上限 1.2。超過の対処はセリフ短縮しか無い)・`closing` は trivia の核を 1 文に凝縮。モーラ推定の癖と節約テク(ひらがなに開く)は WRITING-NOTES セクション 4
- **吹き出しの行またぎを目で見る**: 熟語の途中で折れないか(「日 / 本海側」の実例)。validate.py は検出しない。読点の位置・語順で直す

## 4. 機械検証(執筆後に必ず)

```bash
cd content/ranking-stock/pref-ranking-1/<バッチ名>
python3 validate.py && python3 generate.py
```

- `validate.py`: フィールド上限・TOP6 同値・rank 1〜5 の一意性・cue の存在(30s 必須)・モーラ予算・連番。**バッチ先頭番号からの連番検査があるため、コピー元の開始番号を新バッチの先頭 `no` に合わせて直す**
- `generate.py`: レビューシート(`review.html` / `review.md`)と `insert_ranking_stock.sql` を生成。SQL の `content_key` は `{3 桁連番}-{slug}`・`set_id` は `set_code` サブクエリ解決で両環境共通
- 修正を入れたら validate → generate を回し直してから次へ

## 5. 人間レビュー

- **`review.html` をブラウザ / Live Preview で見てもらう**(ファイル書き換え後は再読み込み。「直っていない」の大半はキャッシュ)
- **Claude が先に一次スクリーニングして blocker 候補 + 申し送りを出す**。観点: ①単位・前提が画面に出るか ②同一出典・近テーマの近接(投稿日を離す材料)③順位の僅差・確定性 ④誇張が数字を超えていないか ⑤下位への言及ゼロ ⑥吹き出しの行またぎ
- ユーザーのレビュー観点の正は operation.html セクション 3 手順 4(データの正しさ・表現・重複・フォーマット適合)。指摘反映 → validate/generate → 再提示。全件承認まで投入しない

## 6. 投入(レビュー全件承認後)

コマンド・確認 SQL の正は **WRITING-NOTES.md セクション 6**。要点: ローカル MySQL は `--default-character-set=utf8mb4` 必須(落とすと日本語が二重エンコードで壊れる)+ `START TRANSACTION;`…`ROLLBACK;` のドライラン → 本適用。Aurora は `common/apply_aurora.py`(Data API。自動一時停止からの復帰リトライ内蔵)。投入後に**両環境のコンテンツ MD5 全行一致 + `CHAR_LENGTH` 正常**を確認する。

## 7. 動画ビルド・レビュー・配置(ranking-prebuilt。投入後に必ず)

投入しただけの行(`video_s3_key_30s IS NULL`)は投稿候補にならない。**実行コマンドの正は `content/video-build/pref-ranking-1/README.md`**(事前準備 = render/ffmpeg イメージ・フォント・五郎素材・VOICEVOX 起動、を含む)。工程: `build.py --list` → `export_prompts.py` → 背景生成 → `intake.py` → `build.py` → `review_sheet.py` → `publish.py`。運用ルール・レビュー観点の正は operation.html セクション 3 手順 6。スキル側の勘所:

1. **背景生成(Codex imagegen 委譲)**: `work/prompts/<content_key>.txt` の全文を渡す(画風固定・9:16・文字禁止の行はツーリングが付与済み)。指示に「**文字・数字・記号の混入を Codex 自身に確認させ、混入時は再生成**」「**941×1672(9:16)で保存し、サイズを確認させる**」を含める(17-5c 実績: 14 枚で自己確認による再生成 5 回)。保存先は `work/backgrounds_raw/<content_key>.png`。取り込み後も Claude が全数目視(文字混入・和モダン画風・中央の版面域が空いているか)
2. **ビルド**: `build.py --dry-run` で全 cue 予算内を先に確認してから本ビルド(1 本約 90 秒)。予算超過はセリフ短縮で直す(話速の引き上げ余地なし)
3. **全数人間レビュー**: `work/review.html`。観点は README 工程 4(背景・版面・音)。NG は背景再生成 / `bg_motif`・セリフ・文言の DB 修正 → 再ビルドで解消するまで承認しない
4. **配置**: 承認 `content_key` を `work/approved.txt` へ → `publish.py --dry-run` → 本実行(S3 + ローカル MySQL + **既定で Aurora まで自動適用**)。S3 キー・UPDATE は環境非依存の `content_key` 解決(id を使わない)
5. **締め**: 在庫確認クエリで両環境 `unbuilt_30s = 0` を確認 → バッチ資材・台帳の変更をコミット + push → `docs/development-log.md` の「定常運用: ランキングストック補充の記録」へ要約を追記

## 委譲・実行環境の要点

- WSL に ffmpeg / Chrome は無い。Remotion レンダリング・ffmpeg・PIL(`intake.py`)は Docker 経由(README の docker run 例が動作確認済みの形)
- Codex 委譲の使い分け: 背景 = imagegen / 実データ検証の突合 = terra/high / Web リサーチ・出典再検証 = `codex --search exec`(MCP 不可。バックグラウンド実行時は `< /dev/null` で stdin を閉じないとハングする)。執筆・レビュー・投入判断・コミットは Claude
- Aurora の Data API が auto mode classifier にブロックされる場合はユーザーに許可を求める
