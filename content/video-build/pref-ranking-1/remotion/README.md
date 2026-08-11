# pref-ranking-1 コンポジション（Remotion）

`ranking-prebuilt` 方式の事前動画をレンダリングする Remotion プロジェクトです。版面・タイムラインの仕様は
[方式設計書 ranking-prebuilt.html](../../../../docs/app/generators/ranking-prebuilt.html) セクション 8 と
[セット別設計書 pref-ranking-1.html](../../../../docs/app/sets/pref-ranking-1.html) セクション 7〜8 が正です。

## 構成

| ファイル | 役割 |
|---|---|
| `src/layout.ts` | 版面のジオメトリ（セーフ域・地図ボックス・順位行スタック・出典行帯・キャラ位置） |
| `src/theme.ts` | カラートークン（生成り × 淡墨茶 × 金。17-4a で Fix） |
| `src/timeline.ts` | 尺別のタイムライン定数（シーン境界・スピン・行の出現フレーム） |
| `src/PrefRankingVideo.tsx` | 版面本体。画面に出る文言はすべて props（英語圏展開の再利用要件②） |
| `src/japanPaths.ts` | 日本地図のパスデータ（**Natural Earth = PD 由来。自動生成物なので手で編集しない**） |
| `src/prefCentroids.ts` | 各県のラベル起点（確定県名の飛翔の起点）。japanPaths.ts と同時に自動生成 |
| `scripts/build_japan_paths.py` | 上記 2 ファイルの生成（素材の取得・投影・インセット移設・県割当の検査） |
| `src/mockProps.ts` | 版面確認用のサンプル props（第 1 バッチ 001 ぎょうざ） |

## 素材（`public/` は git 管理しない）

レンダリング前に以下を配置します。ビルドツーリング（17-4e）が自動化するまでは手動です。

| 置き場 | 中身 | 取得元 |
|---|---|---|
| `public/fonts/` | `ZenKakuGothicNew-Black.ttf` / `-Bold.ttf` / `-Medium.ttf` | 下記「フォント」 |
| `public/char/` | 表彰台五郎のポーズ 3 種（`goro_base.png` / `goro_suspense.png` / `goro_gunbai.png`） | S3 `assets/pref-ranking-1/goro_*.png`（**17-4b で正規化済みの正式アセット**） |
| `public/bg/` | ネタごとの背景イラスト（JPEG） | S3 `assets/pref-ranking-1/prebuilt/{content_key}_bg.png` を JPEG 化して置く |

背景を 2MB 級の PNG のまま置くとフォント読み込みが `delayRender` タイムアウトするため、**JPEG 化**してから置きます（17-3 の知見）。

## レンダリング

WSL には Chrome の共有ライブラリが無いため、**Docker 経由で実行**します。

```bash
cd content/video-build/pref-ranking-1/remotion
docker build -f Dockerfile.render -t remotion-render .

# 静止画（版面確認）
docker run --rm -v "$PWD:/work" -w /work -e HOME=/tmp --user $(id -u):$(id -g) remotion-render \
  npx remotion still src/index.ts PrefRanking20s work/out/main_0.png --frame=0 --props=work/props/main.json

# 通し（20 秒）
docker run --rm -v "$PWD:/work" -w /work -e HOME=/tmp --user $(id -u):$(id -g) remotion-render \
  npx remotion render src/index.ts PrefRanking20s work/out/main_20s.mp4 --props=work/props/main.json \
  --concurrency=3 --timeout=120000
```

版面レビュー用の HTML は `python scripts/design_review_sheet.py`（`work/design-review.html` を生成）。

## フォント（17-4b で Fix）

**Zen Kaku Gothic New**（SIL OFL 1.1。証跡は [../LICENSES.md](../LICENSES.md) セクション 5）。
見出し = Black / 本文 = Medium・Bold の 2 役で、対応は `src/fonts.ts` が正です。

```bash
cd public/fonts
for w in Black Bold Medium; do
  curl -sSLO "https://raw.githubusercontent.com/google/fonts/main/ofl/zenkakugothicnew/ZenKakuGothicNew-$w.ttf"
done
```

`src/fonts.ts` の `FONT_SETS` には 17-4b で比較した 4 案（`noto` / `zenKaku` / `dela` / `mincho`）が
残してあり、`REMOTION_FONT_SET=<key>` を渡すと切り替えて比較レンダリングできます
（採用案以外のファイルは `public/fonts/` に別途落とす必要があります）。

## 表彰台五郎アセットの正規化（17-4b）

ポーズ 3 種は **1160x1220 の共通キャンバス・共通倍率**へ正規化した正式アセットです
（生成 AI の出力そのままだとポーズごとにキャラの寸法・立ち位置が違い、切り替えで伸縮・跳躍して見えるため。
logic-training-1 の 15-13 と同じ手法）。基準はボディ前面の**「1」の字の高さ**（倍率と左右位置）と
**足元**（上下）で、`src/layout.ts` の `CHARACTER` はこのキャンバス前提の値です。

生成 AI で作った元ポーズ（S3 `assets/pref-ranking-1/source/goro_*_raw.png`）を差し替えたら再実行します。

```bash
aws s3 cp s3://acps-prod-images-516964473143/assets/pref-ranking-1/source/ work/char-src/ --recursive
docker run --rm -u $(id -u):$(id -g) -v "$PWD:/work" -w /work \
  --entrypoint python image-batch:ffmpeg-check scripts/normalize_character.py \
  --source work/char-src --dest public/char
```

## 日本地図の再生成

```bash
python scripts/build_japan_paths.py           # japanPaths.ts + prefCentroids.ts を生成
python scripts/build_japan_paths.py --report  # 生成せず診断（頂点数・bbox・インセット枠）のみ
```

素材は Natural Earth 10m admin-1（**パブリックドメイン**。証跡は [../LICENSES.md](../LICENSES.md) セクション 4）。
初回実行時に `.cache/naturalearth/` へダウンロードします（`.gitignore` 対象。約 15MB）。
**Natural Earth は奄美群島を沖縄県に割り当てている誤りがある**ため、スクリプトが鹿児島県へ付け替えたうえで、
目印の島 21 件の県割当を毎回検査します（不一致なら失敗）。投影・インセットの定数はスクリプト冒頭が正です。
