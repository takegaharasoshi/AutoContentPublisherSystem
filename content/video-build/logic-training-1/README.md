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

ビルドツールはホスト（WSL）で実行し、Remotion レンダリングと ffmpeg 処理だけを
Docker に委譲します。リポジトリルートで次のイメージビルドを済ませておきます。

```bash
docker build -f content/video-build/logic-training-1/remotion/Dockerfile.render \
  -t remotion-render content/video-build/logic-training-1/remotion
docker build -f services/image-batch/Dockerfile -t image-batch:ffmpeg-check .

cd content/video-build/logic-training-1
S3_BUCKET_NAME=<bucket> python build.py
python review_sheet.py
```

対象を限定する場合は `--item <id>`（複数指定可）、ビルド済み動画を既存 BGM のまま
作り直す場合は `--rebuild` を付けます。`--list` は対象一覧だけを表示し、`--dry-run` は
props 生成まで、`--skip-assets` はコーチ立ち絵の再取得を省略します。

ビルドツールのテストは `python -m pytest` で実行します（DB・Docker・ネットワークは不要）。

`work/review.html` で動画、ループ継ぎ目を含む 5 枚のスチル、イラストを全数確認します。
承認済み ID を 1 行ずつ `work/approved.txt` に記載してから、まず dry run を行います。

```bash
python publish.py --approved-file work/approved.txt --bucket your-bucket --dry-run
python publish.py --approved-file work/approved.txt --bucket your-bucket
```

`publish.py` は S3 への MP4 とイラストのアップロード後、`video_s3_key` / `video_audio_asset_id` / `video_built_at` をローカル MySQL へ同時更新します。`work/update_prebuilt.sql` は Aurora へ運用者が適用するために残します。

S3 のファイル名は `content_key`（`morning-001` など。V007 で導入）で組みます。ローカルの `quiz_stock_items.id` は環境ローカルな AUTO_INCREMENT で Aurora と一致しないため、S3 キーには使いません（`work/` 配下の中間生成物のファイル名だけがローカル id です）。
