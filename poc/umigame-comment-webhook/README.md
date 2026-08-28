# ウミガメのスープ: Instagram コメント Webhook PoC

アイデア「ウミガメのスープ参加型アカウント」（[docs/ideas/umigame-soup-set.md](../../docs/ideas/umigame-soup-set.md)）の採用条件である
**「自アカウントのリールに付いたコメントを Meta Webhook で受信し、Graph API で AI 自動返信できる」** ことを実証する最小構成。

- 本 PoC 資材は使い捨てにせず、**採用後もコメント自動返信経路専用のステージング面として恒久利用する**（開発計画の設計課題リスト 2026-08-28 の decision）
- 本番設計（API Gateway + SQS + Webhook/Reply Lambda 分離）はアイデア詳細 HTML を参照。PoC は単一 Lambda + Function URL に簡略化している

## 構成

```
Instagram コメント → Meta Webhook → Lambda Function URL（署名検証）
  → 返信文言生成（OpenAI。キー未設定なら固定文言）
  → Graph API POST /{comment_id}/replies
```

- スタック: `Prod-UmigamePocStack`（`infra/lib/umigame-poc-stack.ts`。他スタック依存なし・VPC 外）
- Lambda: `acps-prod-umigame-comment-webhook`（Python 3.13・外部依存ゼロ・`lambda/handler.py`）
- 認証情報: Secrets Manager `umigame-poc/credentials`
- **無限ループ防止**: 自分の返信コメントにも Webhook が飛ぶため、`from.id == ig_user_id` のコメントはスキップする。**`ig_user_id` を設定しないままコメントが来ると自分の返信に返信し続けるので、値の投入を最優先で行うこと**

## セットアップ手順

### 1. AWS 側のデプロイ

```bash
cd infra && cdk deploy -c env=prod UmigamePocStack
```

出力の `FunctionUrl`（Meta に設定する Webhook URL）を控える。シークレット `umigame-poc/credentials` が空値テンプレートで作成される（`verify_token` のみランダム自動生成済み）。

### 2. テスト用 Instagram アカウント（ステージング面）

1. テスト用 Instagram アカウントを新規作成する（既存の運用アカウントは使わない）
2. 設定からプロアカウント（ビジネスまたはクリエイター）へ切り替える

### 3. テスト用 Meta アプリ

1. [developers.facebook.com](https://developers.facebook.com) でアプリを新規作成。ユースケースは Instagram（**Instagram API with Instagram Login**。Facebook ページ不要の方式）を選ぶ
2. **開発モードのまま**使う（App Review なしで動くかの実測が PoC の目的の一部）
3. Instagram プロダクトの「API setup with Instagram login」でテスト用アカウントを接続し、アクセストークンを生成する。必要スコープ: `instagram_business_basic` + `instagram_business_manage_comments`（長期トークン・60 日有効）
4. あわせて以下を控える:
   - **Instagram app secret**（Instagram プロダクト設定内。Webhook 署名検証の鍵）
   - **Instagram user ID**（トークン生成時に表示される。ループ防止用）

### 4. シークレットへの値投入

Secrets Manager `umigame-poc/credentials` の JSON を AWS コンソールで編集:

| キー | 値 |
|---|---|
| `verify_token` | 自動生成済み。**変更せず、この値を手順 5 で Meta 側に貼る** |
| `app_secret` | Instagram app secret |
| `ig_access_token` | 手順 3 のアクセストークン |
| `ig_user_id` | テスト用アカウントの Instagram user ID |
| `openai_api_key` | OpenAI API キー（空なら固定文言返信。まず空で疎通確認 → 後から投入が安全） |

※ Lambda はシークレットをコールドスタート時にキャッシュするため、値を変更したら Lambda の設定を触るか十数分待って新コンテナに入れ替わってから試す（確実にやるなら Lambda コンソールで環境変数を一度保存し直すと全コンテナが入れ替わる）。

### 5. Meta 側の Webhook 設定

1. アプリの Instagram プロダクト内 Webhooks 設定で、Callback URL に手順 1 の Function URL、Verify token にシークレットの `verify_token` を入力して検証（Lambda の GET 検証が通れば成功）
2. `comments` フィールドを購読（subscribe）する

## 実証テスト

1. テスト用アカウントからリール（なければ通常投稿でも可）を 1 本投稿する
2. **別アカウントから**コメントする（例: 「男は店員ですか？」）
   - ⚠️ 開発モードのアプリは、アプリにロールを持つアカウントのイベントしか届かない可能性がある（ここが実測ポイント）。コメントが届かない場合は、コメントする側のアカウントをアプリのテスターとして追加して再試行し、結果を記録する
3. 確認:
   - CloudWatch Logs `/aws/lambda/acps-prod-umigame-comment-webhook` に受信ペイロード全文と Graph API 返信結果が出ている
   - Instagram 上でコメントに返信が付いている
   - 自分の返信に対する Webhook が「自分の返信コメントをスキップしました」でループしていない

### 成功判定（採用条件）

以下がすべて満たされたら PoC 成功 = 企画採用:

- [ ] Webhook 検証（GET）が通る
- [ ] 他アカウントのコメントイベントを受信できる
- [ ] Graph API でコメント返信が Instagram 上に表示される
- [ ] 自己返信ループが起きない
- [ ] （AI 返信）OpenAI キー投入後、質問に「はい / いいえ / 関係ありません」系の返信が付く

成功したら: アイデア記録を「待機 → 採用」にし、開発計画（新セットのフェーズ起案）・事業戦略書（セットポートフォリオ）への転記を**開発レーン**で行う。
失敗したら（権限が取れない・返信が拒否される等）: 事象をアイデア記録に残し、見送りまたはピボットの再壁打ちを行う。

## 開発メモ

- テスト: `cd poc/umigame-comment-webhook && python3 -m pytest tests/`
- 手動での動作確認（署名付き POST の再現）はテストコードの `event_with_signature` を参照
- Meta の仕様は変更が多い領域。本 README の Meta 側手順と実際の画面が食い違ったら、実測した手順でこの README を上書きする（実態の記録を優先）
