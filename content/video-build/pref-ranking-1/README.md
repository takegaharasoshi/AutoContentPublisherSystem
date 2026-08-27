# pref-ranking-1 事前動画ビルド

`ranking-prebuilt` 用のローカル運用ツールです。技術設計は `docs/app/generators/ranking-prebuilt.html` セクション 8、運用手順とレビュー基準は `docs/app/operation.html` セクション 3 手順 6 を正とします。生成物はすべて `work/` に置かれ、git 管理しません。

スクリプトは WSL ホストの Python 3.12 で実行します。ホストに必要な Python パッケージは `pymysql` / `boto3` / `pytest` です。画像処理に PIL が必要な `intake.py` だけは `image-batch:ffmpeg-check` 内で実行します。ローカル MySQL は既定で `127.0.0.1:3306 / app / password / acps` を使用し、必要なら `LOCAL_DB_HOST`、`LOCAL_DB_PORT`、`LOCAL_DB_USER`、`LOCAL_DB_PASSWORD`、`LOCAL_DB_NAME` で上書きします。

## 事前準備

リポジトリルートでレンダリング用と ffmpeg 用のイメージを作ります。

```bash
docker build -f content/video-build/pref-ranking-1/remotion/Dockerfile.render \
  -t remotion-render content/video-build/pref-ranking-1/remotion
docker build -f services/image-batch/Dockerfile -t image-batch:ffmpeg-check .
```

Remotion が使うフォントと正式キャラクター素材を配置します。バケット名は環境に合わせて置き換えてください。

```bash
cd content/video-build/pref-ranking-1
mkdir -p remotion/public/fonts remotion/public/char
for w in Black Bold Medium; do
  curl -sSLo "remotion/public/fonts/ZenKakuGothicNew-$w.ttf" \
    "https://raw.githubusercontent.com/google/fonts/main/ofl/zenkakugothicnew/ZenKakuGothicNew-$w.ttf"
done
aws s3 cp s3://your-bucket/assets/pref-ranking-1/goro_base.png remotion/public/char/goro_base.png
aws s3 cp s3://your-bucket/assets/pref-ranking-1/goro_suspense.png remotion/public/char/goro_suspense.png
aws s3 cp s3://your-bucket/assets/pref-ranking-1/goro_gunbai.png remotion/public/char/goro_gunbai.png
```

VOICEVOX Engine は別ターミナルで起動したままにします。既定の接続先は `http://127.0.0.1:50021`、話者は白上虎太郎（ID 12）です。

```bash
docker run --rm -p 50021:50021 voicevox/voicevox_engine:cpu-ubuntu20.04-latest
```

## BGM の調達・前処理（セット立ち上げ時と曲の追加時だけ）

`prepare_bgm.py` が「切り出し → 2 パス loudnorm → AAC 化 → 登録 SQL の生成」を行います。前処理の仕様（30 秒ちょうど・フェードは焼かない・I=-14 LUFS）とその理由はスクリプトの docstring、運用ルールは `docs/app/operation.html` セクション 3 を参照してください。

```bash
cd content/video-build/pref-ranking-1
python prepare_bgm.py --init          # work/bgm/tracks.json の雛形
# work/bgm/source/ に原曲を置き、tracks.json に file / start / 証跡 3 点を書く
python prepare_bgm.py                 # work/bgm/out/trackNN.m4a + 登録 SQL
```

`start` は曲のサビ・盛り上がりの開始位置（秒）です。出力の実測ラウドネスと尺が 1 曲ずつ表示されるので、`I` が -14 LUFS 付近か、尺が 30.00s かを確認します。登録 SQL は `content/ranking-stock/pref-ranking-1/set-registration/03_audio_assets.sql` に書き出され、証跡 3 点（出典 URL・ライセンス種別・取得日）はこの SQL 経由で `audio_assets` に入ります。試聴後に S3 の `audio/pref-ranking-1/` へ配置し、SQL を両環境へ適用してください（コマンドは実行後に表示されます）。

## 工程 1: 対象抽出

未ビルド尺を一覧します。`20s` / `30s` のうち DB の S3 キーが NULL の尺だけが表示されます。

```bash
cd content/video-build/pref-ranking-1
python build.py --list
python build.py --list --durations 20s
python build.py --list --content-key 001-gyoza-spend
```

版面・タイムライン・キャラクター等の変更をビルド済み動画へ反映するときだけ `--rebuild` を使います。ビルド済み尺が対象となり、記録済み BGM を引き継いで選曲 LRU を消費しません。

```bash
python build.py --list --rebuild
```

## 工程 2: 背景生成と取り込み

対象行の `content_fields.bg_motif` にセット固定の画風・9:16・文字禁止指定を加えた imagegen プロンプトを書き出します。

```bash
python export_prompts.py
# 個別または再ビルド時:
python export_prompts.py --content-key 001-gyoza-spend
python export_prompts.py --rebuild --content-key 001-gyoza-spend
```

`work/prompts/<content_key>.txt` を imagegen に渡し、生成した PNG または JPG を `work/backgrounds_raw/<content_key>.png`（または `.jpg`）へ置きます。次に、PIL を含む image-batch イメージ内で中央クロップ・リサイズ・JPEG 化を行います。

```bash
cd ../../..
docker run --rm -u $(id -u):$(id -g) -v "$PWD:/repo" \
  -w /repo/content/video-build/pref-ranking-1 \
  --entrypoint python image-batch:ffmpeg-check intake.py
cd content/video-build/pref-ranking-1
```

原本は `work/backgrounds/<content_key>.png`、レンダリング用 JPEG は `remotion/public/bg/<content_key>.jpg` に作られます。9:16 でない画像には切り捨て率の WARNING が出るため、被写体の見切れを確認してください。

## 工程 3: TTS・レンダリング・ラウドネス正規化

通常ビルドは BGM を LRU で 1 曲選び、2 尺で共用します。ただし片方の尺が publish 済みで `video_audio_asset_id` が記録されている行は、その曲を引き継いで LRU を消費しません。BGM は `S3_BUCKET_NAME` のバケットから取得されます。`build.py` 自体は WSL ホストで動き、Remotion と ffmpeg だけを Docker で実行します。

```bash
export S3_BUCKET_NAME=your-bucket
python build.py
```

対象や尺を限定するときは次のように実行します。props と VOICEVOX 合成・予算検査だけを確認する場合は `--dry-run` を使います。

```bash
python build.py --durations 20s --content-key 001-gyoza-spend
python build.py --content-key 001-gyoza-spend --dry-run
python build.py --rebuild --content-key 001-gyoza-spend
python build.py --engine http://127.0.0.1:50021
```

`--no-bgm` はツーリング検証専用です。動画と manifest の `audio_asset_id: null` は作られますが、音源記録のない動画を本番へ出さないため `publish.py` が拒否します。

```bash
python build.py --no-bgm --content-key 001-gyoza-spend
```

完成動画は `work/videos/<content_key>_<duration>.mp4`、props は `work/props/`、マージ更新される台帳は `work/build_manifest.json` です。ナレーションの予算超過やストック不備は全件処理後に一覧表示され、終了コード 1 になります。

## 工程 4: 全数レビュー

```bash
python review_sheet.py
```

`work/review.html` をブラウザで開き、ネタごとに 20 秒版・30 秒版、背景、版面文言、TOP5、cue 台本、BGM、実測ラウドネスを確認します。観点は ①背景イラストの品質（文字・数字・記号の混入、和モダン調、可読性）②版面（県名・数値・地図・見切れ）③音（同期・語尾切れ・BGM バランス）です。NG は背景・DB の文言・ナレーションを修正して再ビルドし、解消するまで承認しません。

承認したネタの `content_key` を 1 行ずつ `work/approved.txt` に書きます。空行と `#` から始まる行は無視されます。**承認はネタ単位（2 尺まとめて）** です（ユーザー Fix 2026-08-12。片方の尺だけ NG なら両尺とも保留し、直して再ビルドする）。

```text
# 2026-08 第1回承認
001-gyoza-spend
002-ramen-out
```

## 工程 5: S3・DB へ配置

最初に dry run でアップロード先と更新尺を確認します。承認対象の manifest、MP4、背景 PNG、BGM ID のどれかが欠けていれば、S3・DB に触れる前に全体を中断します。

```bash
python publish.py --bucket your-bucket --dry-run
python publish.py --bucket your-bucket
```

MP4 は `assets/pref-ranking-1/prebuilt/<content_key>_20s.mp4` / `_30s.mp4`、背景原本は `assets/pref-ranking-1/prebuilt/<content_key>_bg.png` へアップロードされます。ローカル MySQL はビルドした尺の列だけを 1 トランザクションで更新します。

Aurora へは **既定で Data API 経由の自動適用**まで行います（S3 とローカル MySQL だけ更新されて Aurora が取り残される片肺状態を作らないため。ユーザー Fix 2026-08-12）。Aurora 用 SQL は常に `work/update_prebuilt.sql` に生成されるので、適用を分けたいときだけ `--no-aurora` を使い、後から手動で適用します。

```bash
python publish.py --bucket your-bucket --no-aurora
python ../../ranking-stock/pref-ranking-1/common/apply_aurora.py work/update_prebuilt.sql
```

S3 キーと両環境の UPDATE は環境非依存の `content_key` を使います。ローカルの `ranking_stock_items.id` は AUTO_INCREMENT で Aurora と一致しないため、識別には使いません。

## アカウントのプロフィール画像（アカウント開設時と作り直しのときだけ）

`account/build_profile_icon.py` が Instagram のプロフィール画像（1080x1080）を生成します。採用案・作画上の制約は `docs/app/sets/pref-ranking-1.html` セクション 2 の decision（2026-08-27）が正です。入力は `remotion/public/char/goro_base.png` なので、事前準備のキャラクター素材の配置が済んでいる必要があります。PIL が要るためコンテナで実行します（リポジトリルートから）。

```bash
docker run --rm -v "$PWD:/work" -w /work --user "$(id -u)" \
  --entrypoint python image-batch:ffmpeg-check \
  content/video-build/pref-ranking-1/account/build_profile_icon.py
```

採用案が `account/profile_icon.png` に上書き出力されます。不採用案の再現は `--variant dark|gunbai`、円クロップ + 実表示サイズ（320 / 110 / 40px）の比較シートは `--compare`（出力先は `work/profile/`）です。
