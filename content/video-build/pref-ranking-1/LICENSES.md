# pref-ranking-1 ライセンス・利用規約の証跡

表彰台五郎の都道府県ランキング（`set_code = pref-ranking-1`）の動画ビルドで使う外部資材について、
確認日・参照 URL・許諾範囲を記録する。設計上の位置づけは
[docs/app/sets/pref-ranking-1.html](../../../docs/app/sets/pref-ranking-1.html) セクション 7 と
[docs/app/operation.html](../../../docs/app/operation.html) セクション 3（証跡ルール）。

BGM・SE のライセンス証跡はこのファイルではなく `audio_assets` のカラムに記録する（証跡一元管理の原則。
operation.html セクション 3「音源の調達・前処理・登録」）。本ファイルは **DB レコードにならない資材**
（合成音声・地図 SVG・フォント等）の証跡を担う。

---

## 1. VOICEVOX（ソフトウェア本体）

| 項目 | 内容 |
|---|---|
| 確認日 | 2026-08-10 |
| 参照 URL | https://voicevox.hiroshiba.jp/term/ |
| 許諾範囲 | 「**商用・非商用問わず利用することができます**」 |
| クレジット | 「ご利用の際は **VOICEVOX を利用したことがわかるクレジット表記が必要**です。」（本体規約に文字列の指定はなく、音声ライブラリ側の指定形式で満たす = 下記 2） |
| 生成音声の扱い | 生成した音声の利用条件は**各音声ライブラリ（キャラクター）の規約に従う**。本セットは白上虎太郎のみを使用する |
| 禁止事項（抜粋） | 本ソフトウェアの全部または一部の無断再配布、リバースエンジニアリング、第三者等への不利益、公序良俗違反 |
| 実行形態 | ローカル Docker（`voicevox/voicevox_engine`）で合成し、生成音声は動画へベイクする。**音声ファイル単体では配布・保存しない**（ビルド中間物） |

## 2. 白上虎太郎（VOICEVOX 音声ライブラリ / キャラクター）

| 項目 | 内容 |
|---|---|
| 確認日 | 2026-08-10 |
| 権利者・提供元 | **VirVox Project**（規約上の「甲」）。CV（音声提供者）: **可愛ユウ**（https://www.virvoxproject.com/白上虎太郎） |
| 規約 URL | https://www.virvoxproject.com/voicevoxの利用規約 （VirVox Project「VOICEVOX の利用規約」） |
| 商用利用 | **可**（「乙は音源を商用・非商用問わず使用することができるものとします」）。事前申請が必要なのは同プロジェクトの**青山龍星のみ**で、白上虎太郎は対象外 |
| クレジット表記（必須） | 「動画内、概要欄など**任意の場所**」に表記する。VOICEVOX 公式のキャラクター別記載は「**VOICEVOX:白上虎太郎**」。本セットは **Instagram キャプションに常設**する（sets/pref-ranking-1.html セクション 5） |
| クレジット省略 | VirVox Project への問い合わせと許可が必要（本セットでは省略しない） |
| 禁止事項（本セットに関係するもの） | ①犯罪助長 ②音声提供者・キャラクターの信用・品位を著しく損なう公開 ③権利侵害 ④公序良俗に著しく反する使用 ⑤著作情報の偽装 ⑥**特定の政治団体の宣伝・過度な称賛・毀損** ⑦**特定の宗教の過度な称賛・毀損** ⑧**特定の個人・集団・国家・民族・思想を毀損する目的**での利用 ⑨出力音声をベースにした機械学習・転移学習等による新たな音響モデルの生成 ⑩VOICEVOX で合成したことを表記せずに利用すること |
| 二次配布 | 出力音声を音声素材として配布する場合は同等の規約を利用者へ義務づける必要がある（本セットは**音声単体を配布しない**ため非該当） |

### 本セットの運用上の遵守事項

- キャプションの「VOICEVOX:白上虎太郎」は**常設要素**であり、テンプレートから外さない（sets/pref-ranking-1.html セクション 5 の必須 3 点の 1 つ）。
  ストーリーズはキャプションを付けられない（Graph API 制約）ため、クレジットはリール本体のキャプションで担保する。
- ネタ選定基準「下位の県の人が笑って自虐できるか」（事業戦略書セクション 6）と TOP5 のみを扱う版面設計は、
  上記禁止事項⑧「特定の集団を毀損する目的での利用」に抵触しないための構造的なガードでもある。
- 政治・宗教をテーマにしたランキングは扱わない（禁止事項⑥⑦）。
- 合成音声を素材として切り出して配布・販売しない。

## 3. VOICEVOX ENGINE のバージョン（2026-08-10 時点の調査）

| 項目 | 内容 |
|---|---|
| 安定版 | VOICEVOX ENGINE **0.25.2**（https://github.com/VOICEVOX/voicevox_engine/releases の Latest。0.26.0-dev は Pre-release） |
| Docker イメージ | `voicevox/voicevox_engine`（https://hub.docker.com/r/voicevox/voicevox_engine ）。公式の取得例は `cpu-latest` / `nvidia-latest`。タグは CPU/GPU・アーキテクチャ・Ubuntu 版・バージョンの組み合わせ |
| 本セットでの固定 | **17-4 のビルドツーリングで具体的なタグへピン留めする**（`latest` 系は使わない。話者のスタイル ID もツーリング設定を正とする = sets/pref-ranking-1.html セクション 7） |

## 4. 日本地図（17-4b で PD 素材へ差し替え済み）

| 項目 | 内容 |
|---|---|
| 素材名 | **Natural Earth 10m Cultural Vectors — Admin 1 – States, Provinces**（`ne_10m_admin_1_states_provinces`。バージョン **5.1.1**） |
| 配布元 URL | https://www.naturalearthdata.com/downloads/10m-cultural-vectors/ （実ダウンロード: https://naciscdn.org/naturalearth/10m/cultural/ne_10m_admin_1_states_provinces.zip ） |
| ライセンス | **パブリックドメイン**。規約 https://www.naturalearthdata.com/about/terms-of-use/ の原文: 「All versions of Natural Earth raster + vector map data found on this website are **in the public domain**. You may use the maps in any manner, including **modifying the content and design**, electronic dissemination, and offset printing.」「**No permission is needed** to use Natural Earth. **Crediting the authors is unnecessary.**」 |
| クレジット | **不要**（上記のとおり）。任意表記の推奨文は "Made with Natural Earth."。動画の版面には出さず、本証跡と生成物のヘッダコメントで出所を記録する |
| 確認日・取得日 | 2026-08-11 |
| 加工内容 | `content/video-build/pref-ranking-1/remotion/scripts/build_japan_paths.py` が ①47 都道府県のポリゴン抽出（`adm0_a3 = JPN` / `iso_3166_2` の JIS コード）②**奄美群島の県割当の補正**（下記）③ランベルト正角円錐図法（標準緯線 30N/45N・中央経線 137E）で投影 ④本土を viewBox 0 0 1000 1000 へフィット ⑤南西諸島（沖縄県 + 鹿児島県のトカラ・奄美）を同一投影のまま**群としてまとめて相似変換で関東沖へ移設**（インセット）⑥座標の量子化（0.25）と頂点の間引き ⑦`src/japanPaths.ts` / `src/prefCentroids.ts` を生成。**シェープファイル本体は git 管理せず** `remotion/.cache/`（`.gitignore` 済み）へキャッシュし、スクリプトが未取得なら再ダウンロードする |

**素材側の誤りと補正（重要）**: Natural Earth 10m は **奄美群島（奄美大島・喜界島・徳之島・沖永良部島・与論島）を沖縄県（JP-47）に割り当てている**。
実際は鹿児島県のため、生成スクリプトが緯度 27.0N 以北かつ経度 128.3E 以東のリングを鹿児島県へ付け替える
（与論島 128.4E と沖縄県最北の伊平屋島 127.75E は経度で分離できる）。補正しないと「鹿児島県が 1 位のときに
奄美群島が塗られない / 沖縄県が 1 位のときに奄美群島まで塗られる」という**内容の誤り**になる。
退行検出のため、生成スクリプトは**目印の島 21 件の県割当を毎回検査**して不一致なら失敗する（`check_landmarks`）。

版面に載せない離島（伊豆諸島・小笠原諸島・硫黄島・南鳥島・大東諸島）と、面積が約 12km² 未満の島は落としている
（17-4a で Fix した版面の再現。地図ボックスの外に大きく外れる / 点にしかならないため）。素材要件
（県単位パス分割・鹿児島離島の飛び地サブパス・南西諸島インセットの再現）は
[docs/app/generators/ranking-prebuilt.html](../../../docs/app/generators/ranking-prebuilt.html) セクション 8.2 の warn が正。

## 5. フォント（17-4b で確定）

| 項目 | 内容 |
|---|---|
| 書体 | **Zen Kaku Gothic New**（見出し = Black / 本文 = Medium・Bold）。デザイナー: 大平善道（Yoshimichi Ohira） |
| 配布元 | Google Fonts（https://fonts.google.com/specimen/Zen+Kaku+Gothic+New ）。実ファイルは https://github.com/google/fonts の `ofl/zenkakugothicnew/` |
| ライセンス | **SIL Open Font License 1.1**（`ofl/zenkakugothicnew/OFL.txt`。"Copyright 2022 The Zen Kaku Gothic Project Authors"）。商用利用可・**動画への埋め込み（レンダリング結果の配布）可**・改変可。禁止は「フォントファイル単体の販売」と、OFL 由来物の再配布時にライセンスを外すこと |
| 本セットでの扱い | **フォントファイルは git 管理せず**（`public/` は `.gitignore` 対象）、ビルド時に Google Fonts のリポジトリから取得する（取得コマンドは remotion/README.md）。**フォントファイルそのものは再配布しない**（S3 にも置かない）。動画へのラスタライズ結果の配布は OFL の制限外 |
| 確認日 | 2026-08-11 |
| 選定の経緯 | 17-4b で 4 案（Noto Sans JP / Zen Kaku Gothic New / Dela Gothic One 見出し / Zen Old Mincho Black 見出し）を実データでレンダリングして比較し、**ユーザー判断で Zen Kaku Gothic New に決定**（和モダンの配色と相性がよく、リールの小さい表示でも県名が読みやすい） |
