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
| `src/japanPaths.ts` | 日本地図のパスデータ（**現行はプロトの GFDL 由来。17-4b で PD 素材へ差し替える**） |
| `src/prefCentroids.ts` | 各県の重心（確定県名の飛翔の起点）。`scripts/gen_centroids.py` で自動生成 |
| `src/mockProps.ts` | 版面確認用のサンプル props（第 1 バッチ 001 ぎょうざ） |

## 素材（`public/` は git 管理しない）

レンダリング前に以下を配置します。ビルドツーリング（17-4e）が自動化するまでは手動です。

| 置き場 | 中身 | 取得元 |
|---|---|---|
| `public/fonts/` | `NotoSansJP-Regular.otf` / `NotoSansJP-Bold.otf` | Google Fonts（OFL）。書体の選定は 17-4b |
| `public/char/` | 表彰台五郎のポーズ 3 種（透過 PNG） | S3 `assets/pref-ranking-1/goro_*.png`（正式化は 17-4b） |
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
地図 SVG を差し替えたら `python scripts/gen_centroids.py` で重心を再生成します。
