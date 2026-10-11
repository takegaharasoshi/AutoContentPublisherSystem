# umigame-soup-1 セット登録と稼働開始の手順（21-7 で準備）

手順の正は [docs/app/operation.html](../../../../docs/app/operation.html) セクション 2.1（セット追加手順）、
値の正は [docs/app/sets/umigame-soup-1.html](../../../../docs/app/sets/umigame-soup-1.html)。
21-7 では SQL・CDK・手順書を用意しただけで、**下の作業はすべてユーザー作業（人間ゲート）**。
`batch_sets` 行は 21-4 系で登録済み（ローカル `set_id=209`。`is_active=0` のまま）。ストック 14 問はビルド・配置済み。

## 用意したもの

| # | 対象 | ファイル | 状態 |
|---|---|---|---|
| 1 | `prompt_configs` + `caption_templates` | [01_prompt_caption.sql](01_prompt_caption.sql) | 未適用（ローカル dry-run OK・2026-10-12） |
| 2 | `sns_accounts` | [02_sns_account.sql](02_sns_account.sql) | 未適用（**投稿用 Secret を作ってから**） |
| 3 | `audio_assets`（BGM 1 曲） | [03_audio_assets.sql](03_audio_assets.sql) | ローカル適用済み（21-5a）。Aurora は適用後の確認クエリで有無を見る |
| 4 | `batch_sets` の有効化 | [04_activate.sql](04_activate.sql) | 未適用（**cdk deploy の後・1 本目の直前**） |
| 5 | 正解基準の再適用 | [../batch-01/update_judge_criteria.sql](../batch-01/update_judge_criteria.sql) | 21-6d8 以降の修正分（U01・U27・U18・U22・U25 ほか）。両環境へ再適用が必要 |
| 6 | Scheduler（画像生成 1 + インサイト 2）・スナップショット PUT 権限 | `infra/lib/{image,insights,sns-post}-batch-stack.ts` | 未 deploy |
| 7 | プライバシーポリシー | `infra/assets/umigame-privacy-policy/index.html` + `CommentReplyStack`（本番面） | 未 deploy |
| 8 | スナップショットの手動再出力 | [../tools/write_snapshot.py](../tools/write_snapshot.py) | 必要時のみ（下の「困ったとき」） |

ローカルの dry-run（01・02・04 を 1 トランザクションで流して ROLLBACK）:

```bash
cd content/umigame-stock/umigame-soup-1/set-registration
python3 dry_run.py
```

## 稼働開始の順番

**Scheduler は CDK で有効のまま deploy する。`batch_sets.is_active=0` の間は画像生成・投稿・インサイト収集とも
何もせず正常終了するので、稼働の切り替えは手順 9 の `04_activate.sql` で行う**（21-7 の決定）。

1. **Instagram アカウント開設**: `umigame.soup.jp` を取得し、プロアカウント（クリエイター or ビジネス）へ切り替える。
   名前欄は「コメントで推理！探偵カメロックのウミガメのスープ」（14 日で 2 回までしか変えられない）。
2. **投稿用の連携（既存 Meta アプリ）**: Facebook ページを新規作成して `umigame.soup.jp` と連携し、
   [operation.html セクション 5.1](../../../../docs/app/operation.html) の通常手順で長期トークンを取得する。
3. **投稿用 Secret を作成して検証する**（operation.html 2.1 手順 1・5.1 手順 7。DB 登録より先）:
   ```bash
   aws secretsmanager create-secret \
     --name acps/prod/umigame-soup-1/sns/instagram/main-account \
     --secret-string '{"access_token":"...","ig_user_id":"...","token_expires_at":"YYYY-MM-DDTHH:MM:SSZ"}'
   ```
   `ig_user_id` が **umigame.soup.jp を指していること**（pref-ranking-1 の開設時に既存セットのアカウントを指していた事故あり）と、
   スコープに `instagram_manage_insights` があることを 5.1 手順 7 の方法で確かめる。
4. **DB 登録（両環境）**: 01 → 02 → 正解基準の再適用（# 5）の順。
   ```bash
   cd content/umigame-stock/umigame-soup-1
   for f in set-registration/01_prompt_caption.sql set-registration/02_sns_account.sql batch-01/update_judge_criteria.sql; do
     docker exec -i acps-mysql mysql --default-character-set=utf8mb4 -uroot -proot acps < "$f"
     python3 ../../ranking-stock/pref-ranking-1/common/apply_aurora.py "$f"
   done
   ```
   Aurora に BGM 行が無ければ `set-registration/03_audio_assets.sql` も同じく流す（下の確認クエリで判定）。
5. **push → deploy**（`infra/` の変更はパイプラインを起動しない。イメージタグ 3 つの Context 指定が必須。
   現行タグの確認方法は [cicd.html セクション 3.2](../../../../docs/infra/cicd.html)）:
   ```bash
   cd infra
   npx cdk deploy -c env=prod -c imageBatchImageTag=<tag> -c snsPostBatchImageTag=<tag> -c insightsBatchImageTag=<tag> \
     --exclusively SnsPostBatchStack ImageBatchStack InsightsBatchStack CommentReplyStack
   ```
   出力 `CommentReplyStack.PrivacyPolicyUrl`（https のオブジェクト URL）をブラウザで開けることを確かめる。
6. **本番用 Meta アプリを作る**（コメント返信用。下の「本番 Meta アプリの作成」）。
7. **コメント返信用 Secret に値を入れる**（下の「コメント返信用 Secret」）。
8. **Webhook を接続する**（下の「本番 Meta アプリの作成」手順 6〜8）。
9. **有効化**: バックログ 0 件を確認してから `04_activate.sql` を両環境へ。
   ```sql
   SELECT COUNT(*) FROM generation_runs gr JOIN batch_sets b ON b.id = gr.set_id
   WHERE b.set_code = 'umigame-soup-1'
     AND NOT EXISTS (SELECT 1 FROM posts p WHERE p.generation_run_id = gr.id
                     AND p.status IN ('success','failed','published_unconfirmed'));
   ```
   ```bash
   python3 ../../ranking-stock/pref-ranking-1/common/apply_aurora.py set-registration/04_activate.sql
   ```
   **この時点から 20:00 の定時実行も動く**。当日の 20:00 より前に手順 10 を終えるか、20:00 の 1 本目を初回確認に使う。
10. **1 本目の投稿**: 画像生成 SFN を `{"set_code":"umigame-soup-1","scheduled_at":"<今の UTC 時刻>"}` で手動実行し
    （[infra/operation.html セクション 1.2](../../../../docs/infra/operation.html)）、リール投稿・`umigame_items.snapshot_s3_key` の記録・
    S3 `assets/umigame-soup-1/problems/{media_id}.json` の出力を確かめる。
11. **自分で 1 コメントして返信を確認する**（別アカウントから「男は店員ですか？」等）。CloudWatch Logs
    `/aws/lambda/acps-prod-comment-reply-reply` と S3 `comment-log/umigame-soup-1/` に記録が出ること。
12. 翌日の 2 本目で、前回の真相ブロックがキャプション末尾に入ることを確認する（開発計画の確認待ちリスト「21-6h 前回の真相ブロック」）。

## 本番 Meta アプリの作成（コメント返信用）

PoC の手順（[poc/umigame-comment-webhook/README.md](../../../../poc/umigame-comment-webhook/README.md)）を本番向けにしたもの。
投稿用の既存アプリとは別に作る（理由はセット別設計書 2 の付録）。画面の文言が違っていたら、実際の手順でここを上書きする。

1. [developers.facebook.com](https://developers.facebook.com) でアプリを新規作成。ユースケースは
   「**Instagram でメッセージとコンテンツを管理**」（Instagram API with Instagram Login。Facebook ページ不要の方式）。
   アプリ名は例「探偵カメロック コメント返信」。
2. **umigame.soup.jp を「Instagram テスター」に追加して Instagram 側で承認する**（PoC 実測: これをしないと
   開発モードでの接続が `開発者の役割が不十分です` で拒否される）。Instagram 側の承認は instagram.com/accounts/manage_access/ の「テスター招待」。
3. ユースケースの「カスタマイズ」→「設定」で「アカウントを追加」→ umigame.soup.jp でログイン・許可 →「トークンを生成」で
   長期トークン（60 日）を取得。スコープ `instagram_business_basic` + `instagram_business_manage_comments`。
   あわせて **Instagram アプリシークレット**（Facebook 側「アプリ設定 → ベーシック」の app secret ではない）と
   **Instagram user ID** を控える（出なければ `GET https://graph.instagram.com/v23.0/me?fields=id,username&access_token=<トークン>`）。
4. 「アプリ設定 → ベーシック」に **プライバシーポリシーの URL** = 手順 5 の `PrivacyPolicyUrl` を入れる。
   データ削除の項目を求められたら「データ削除の手順の URL」に `<PrivacyPolicyUrl>#data-deletion` を入れる。
   カテゴリ・アイコン等の必須欄も埋める。
5. **アプリを公開（ライブ）モードに切り替える**（開発モードでは comments Webhook が一切届かない。App Review は不要 = PoC 実測）。
6. コメント返信用 Secret に値を入れた後（下）、「Webhooks を設定する」でコールバック URL = 出力 `CommentReplyStack.FunctionUrl`、
   「トークンを認証」= Secret の `verify_token` を入れて「確認して保存」。事前確認:
   `curl "<FunctionUrl>?hub.mode=subscribe&hub.verify_token=<verify_token>&hub.challenge=123"` で `123` が返る。
7. `comments` フィールドを購読する。
8. 「アクセストークンを生成する」の表の **Webhook サブスクリプションのトグルをオン**にする（オフだと届かない）。

## コメント返信用 Secret

`acps/prod/umigame-soup-1/comment-reply`（CDK 作成済み・`verify_token` だけ自動生成）をコンソールで編集する。
スキーマの正は [security.html セクション 1.3](../../../../docs/infra/security.html)。

| キー | 値 |
|---|---|
| `verify_token` | 変更しない（Meta の Webhook 設定に貼る） |
| `app_secret` | 本番アプリの Instagram アプリシークレット |
| `ig_access_token` | 手順 3 の長期トークン（以後は週 1 回の更新 Lambda が書き戻す） |
| `ig_user_id` | umigame.soup.jp の Instagram user ID（**自己返信ループ防止。最優先で入れる**） |
| `token_expires_at` | 発行日時 + 60 日（UTC・末尾 Z） |
| `openai_api_key` / `anthropic_api_key` / `typesafe_api_key` | 各 API キー（ステージング面と同じでよい。OpenAI はプロジェクト単位の月額上限を設定したもの） |

Lambda はコールドスタート時に Secret を読むので、入れ替え後は Lambda の環境変数を一度保存し直すと確実に反映される。
投入後、トークン更新 Lambda を一度手動実行して成功することも確かめてよい（発行から 24 時間以上たってから）。

## 適用後の確認クエリ（両環境で同じ結果になること）

```sql
SELECT b.is_active, b.problem_snapshot_enabled, p.parameters, c.template_text,
       s.account_code, COUNT(DISTINCT a.id) AS bgm, COUNT(DISTINCT u.id) AS built_stock
FROM batch_sets b
LEFT JOIN prompt_configs p ON p.set_id = b.id AND p.is_active = 1
LEFT JOIN caption_templates c ON c.set_id = b.id AND c.is_active = 1
LEFT JOIN sns_accounts s ON s.set_id = b.id
LEFT JOIN audio_assets a ON a.set_id = b.id AND a.asset_type = 'bgm' AND a.is_active = 1
LEFT JOIN umigame_stock_items u ON u.set_id = b.id AND u.is_active = 1 AND u.video_s3_key IS NOT NULL
WHERE b.set_code = 'umigame-soup-1'
GROUP BY b.is_active, b.problem_snapshot_enabled, p.parameters, c.template_text, s.account_code;
```

期待値: `parameters` = `{"duration_seconds": 24}`・`template_text` = `{{caption}}{{prev_truth_block}}`・`account_code` = `main-account`・`bgm` ≥ 1・`built_stock` = 14。

## 困ったとき

- **スナップショットが欠けた**（`umigame_items.snapshot_s3_key IS NULL` の成功投稿がある。投稿は成功のまま・
  その投稿へのコメントには返信が付かない）: `python3 ../tools/write_snapshot.py` で対象を一覧し、`--apply` で再出力する。
- **20:00 の自動投稿を止めたい**: `UPDATE batch_sets SET is_active = 0 WHERE set_code = 'umigame-soup-1';`（両環境）。
  長期停止なら CDK 側の Scheduler も外す（Scheduler は CDK が正 = 課題 I-018 の決定）。
- **返信が付かない**: [/incident](../../../../.agents/skills/incident/SKILL.md) から入る。まず Webhook のトグル・アプリの公開モード・Secret の `ig_user_id` を疑う。
