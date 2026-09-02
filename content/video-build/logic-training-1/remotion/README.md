# logic-training-1 コンポジション（Remotion）

`quiz-prebuilt` 方式の事前動画を Remotion でレンダリングするプロジェクトです。改修 R-1
（動画レンダラーの Remotion 載せ替え）の成果物で、R-1-2 時点では**プロトタイプ**（1 問だけ
作って現行版と見比べるための一式）です。運用手順の正は
[方式設計書 quiz-prebuilt.html](../../../../docs/app/generators/quiz-prebuilt.html) セクション 8、
改修の経緯は[セット計画書 logic-training-1.html](../../../../docs/plans/logic-training-1.html) の改修 R-1 です。

## 不変条件（R-1 起票時のユーザー決定）

尺 16 秒 / 3 カット / SE のタイミング（tick 8.0 秒・chime 13.0 秒）/ BGM と SE のミックス設計 /
「答えはキャプションで開示」の情報設計 / イラスト（既存の `<content_key>_illustration.png` の再利用）は
**変えません**。変えるのはレンダラー・カット内の動き・上部の余白だけです。書体も現行版と同じ
Noto Sans JP のままにしています（比較を濁らせないため）。

## ループ要件

R-1-1（2026-09-02）で平均再生時間が 16 秒を超えること = **ループ視聴が常態**であることが実証されたため、

- 周期アニメーションの周期は**すべて 480 フレーム（16 秒 × 30fps）の約数**にする
- 16 秒末尾の状態が 0 秒の状態に一致する

を必須要件にしています。周期は `src/timeline.ts` の `LOOP_PERIODS` に集約し、約数でない値を書くと
モジュール読み込み時に例外で落ちます。一覧の確認は次のコマンドです。

```bash
python scripts/check_loop_periods.py
```

継ぎ目（15.6〜16.0 秒）では誘導カット固有の要素を落とし、15.8 秒で導入カットの状態へ**スナップで**
戻します。表情や文言をクロスフェードすると二重露光に見えて不具合と区別がつかないためです
（試作 1 回目の frame 474 で確認）。

## 構成

| ファイル | 役割 |
|---|---|
| `src/layout.ts` | 版面の定数。**上部ゾーンは左右対称でカード幅を使い切り、Instagram UI の右 12% 予約は下部ゾーンだけに掛ける**（R-1 の版面変更） |
| `src/design.ts` | props から版面の実寸（帯・見出し・問題文・イラスト枠・吹き出し・バッジ）を導く |
| `src/textUtils.ts` | 禁則つきの行分割とフォントサイズの自動決定。**行ごとの段階表示のために行の配列が要る**ので自前で割る |
| `src/timeline.ts` | カット境界・段階表示・ホップ・`LOOP_PERIODS`（480 の約数を強制） |
| `src/motion.ts` | 周期モーションのヘルパーと、現行版と同じ減衰ホップ |
| `src/palette.ts` | スロット別パレット（現行レンダラーと同値） |
| `src/QuizVideo.tsx` | 版面本体 |
| `src/mockProps.ts` | Remotion Studio 用のダミー props |
| `scripts/prototype.py` | 1 問を通しでビルドする入口（下記） |
| `scripts/build_props.py` | ローカル DB と `work/illustrations/` から props JSON を作る |
| `scripts/fetch_assets.py` | コーチ立ち絵を S3 から取得し 4 表情共通の矩形でトリミング |
| `scripts/mix_audio.py` | 現行版と同じ ffmpeg フィルタで BGM + SE を載せる |
| `scripts/check_loop_periods.py` | 周期が 480 の約数であることの一覧確認 |

## 素材（`public/` は git 管理しない）

| 置き場 | 中身 | 取得元 |
|---|---|---|
| `public/fonts/` | `NotoSansJP-Regular.otf` / `NotoSansJP-Bold.otf` | `prototype.py` が pref-ranking-1 の `public/fonts/` から複製 |
| `public/coach/` | コーチ立ち絵 4 表情 | S3 `assets/logic-training-1/coach_*.png`（`fetch_assets.py`） |
| `public/illustrations/` | 問題ごとの情景イラスト | `work/illustrations/<id>.png`（`build_props.py`） |

## プロトタイプの実行

レンダリングは WSL に Chrome の共有ライブラリが無いため Docker 経由です。イメージは
pref-ranking-1 と共通の作りで、リポジトリルートを `/repo` にマウントします。

```bash
# 初回のみ（pref-ranking-1 側で作成済みならそのまま使える）
docker build -f Dockerfile.render -t remotion-render .
docker build -f ../../../../services/image-batch/Dockerfile -t image-batch:ffmpeg-check ../../../..

cd content/video-build/logic-training-1/remotion
S3_BUCKET_NAME=<bucket> python scripts/prototype.py --item <quiz_stock_items.id>
```

`work/prototype/<id>-silent.mp4`（映像のみ）と `work/prototype/<id>.mp4`（音声込み）が出ます。
現行版は `../work/videos/<id>.mp4` にあるので、並べて再生して比べます。
`--skip-assets` を付けるとコーチ立ち絵の再取得を飛ばします。

プロトタイプの間は **S3 にも DB にも書き戻しません**（読むだけ）。BGM は台帳
`../work/build_manifest.json` に記録済みの音源をそのまま使い、LRU（`audio_assets.last_used_at`）も
更新しません。ビルドツーリング（`build.py`）への畳み込みは R-1-4 で行います。
