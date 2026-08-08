# logic-training-1 事前動画ビルド

`quiz-prebuilt` 用のローカル運用ツールです。運用ルールは `docs/app/operation.html` セクション 3 手順 5、技術仕様は `docs/app/generators/quiz-prebuilt.html` セクション 8 を正とします。生成物はすべて `work/` に置かれ、git 管理しません。

ローカル MySQL は既定で `127.0.0.1:3306 / app / password / acps` を使用します。必要なら `LOCAL_DB_HOST`、`LOCAL_DB_PORT`、`LOCAL_DB_USER`、`LOCAL_DB_PASSWORD`、`LOCAL_DB_NAME` を指定します。

```bash
cd content/video-build/logic-training-1
python export_prompts.py
# work/prompts/<stock_item_id>.txt を imagegen に渡し、生成 PNG を
# work/illustrations_raw/<stock_item_id>.png に置く
python intake.py
```

ffmpeg を含む image-batch イメージ内で、リポジトリをマウントして組版・動画ビルドを実行します。リポジトリルートで次のイメージビルドを済ませておきます。

```bash
docker build -f services/image-batch/Dockerfile -t image-batch:ffmpeg-check .
docker run --rm -v "$PWD:/repo" -v "$HOME/.aws:/aws-config:ro" -w /repo/content/video-build/logic-training-1 \
  -e PYTHONPATH=/repo/services/image-batch:/repo/shared \
  -e S3_BUCKET_NAME=<bucket> \
  -e LOCAL_DB_HOST=host.docker.internal \
  -e AWS_SHARED_CREDENTIALS_FILE=/aws-config/credentials \
  -e AWS_CONFIG_FILE=/aws-config/config \
  -e AWS_DEFAULT_REGION=ap-northeast-1 \
  --user $(id -u):$(id -g) --entrypoint python image-batch:ffmpeg-check build.py
python review_sheet.py
```

`work/review.html` で動画・イラスト・4 カット代表を全数確認します。承認済み ID を 1 行ずつ `work/approved.txt` に記載してから、まず dry run を行います。

```bash
python publish.py --approved-file work/approved.txt --bucket your-bucket --dry-run
python publish.py --approved-file work/approved.txt --bucket your-bucket
```

`publish.py` は S3 への MP4 とイラストのアップロード後、`video_s3_key` / `video_audio_asset_id` / `video_built_at` をローカル MySQL へ同時更新します。`work/update_prebuilt.sql` は Aurora へ運用者が適用するために残します。
