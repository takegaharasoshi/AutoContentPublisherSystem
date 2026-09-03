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

出力の `FunctionUrl`（Meta に設定する Webhook URL）を控える。後から見るには:

```bash
aws cloudformation describe-stacks --stack-name Prod-UmigamePocStack --region ap-northeast-1 --query "Stacks[0].Outputs" --output table
```
シークレット `umigame-poc/credentials` が空値テンプレートで作成される（`verify_token` のみランダム自動生成済み）。

### 2. テスト用 Instagram アカウント（ステージング面）

1. テスト用 Instagram アカウントを新規作成する（既存の運用アカウントは使わない）
2. 設定からプロアカウント（ビジネスまたはクリエイター）へ切り替える

### 3. テスト用 Meta アプリ

1. [developers.facebook.com](https://developers.facebook.com) でアプリを新規作成。ユースケースは「**Instagram でメッセージとコンテンツを管理**」（Instagram API with Instagram Login。Facebook ページ不要の方式）を選ぶ。ビジネスポートフォリオは「**リンクしない**」（開発モードでは不要。既存セットの資産から切り離すため）
2. **開発モードのまま**使う（App Review なしで動くかの実測が PoC の目的の一部）
3. **先にテスト用アカウントをアプリの「Instagram テスター」に追加する**（実測 2026-09-03: これをせずに接続すると `開発者の役割が不十分です` で拒否される）。ダッシュボード「アプリの役割」→「役割」→「人を追加」→ Instagram テスター → ユーザーネーム入力。次に **Instagram 側で承認**: テスト用アカウントで 設定 →「ウェブサイトのアクセス許可」→「テスター招待」タブ → 承認（Web: instagram.com/accounts/manage_access/）
4. 「ユースケース」→「Instagram でメッセージとコンテンツを管理」の「カスタマイズ」→「設定」タブ（= API setup with Instagram login）で、「1. Instagram アカウントでアクセストークンを生成」→「アカウントを追加」→ テスト用アカウントでログイン・許可 → 「トークンを生成」で長期トークン（60 日有効）を取得。必要スコープ `instagram_business_basic` + `instagram_business_manage_comments` はユースケース選択時に付与済み
5. あわせて以下を控える:
   - **Instagram app secret**（同じページの最上部、または「Instagram ビジネスログインを設定」セクション内の「Instagram アプリシークレット」→「表示」）。**署名検証の鍵がこれか Facebook 側「アプリ設定 → ベーシック」の app secret かは実測で確定する**: まず Instagram 側を入れ、ログに「Webhook 署名の検証に失敗しました」が出たら Facebook 側に入れ替える
   - **Instagram user ID**（トークン生成時に表示される。ループ防止用。出なければ `GET https://graph.instagram.com/v23.0/me?fields=id,username&access_token=<トークン>` で取得）

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

1. 「設定」タブの「3. Webhooks を設定する」で、コールバック URL に手順 1 の Function URL、「トークンを認証」にシークレットの `verify_token` を入力して「確認して保存」（Lambda の GET 検証が通れば成功。事前に `curl "<FunctionUrl>?hub.mode=subscribe&hub.verify_token=<verify_token>&hub.challenge=123"` で 123 が返ることを確認できる）
   - ⚠️ 画面に「Webhooks を受信するには、アプリの状態が公開済みである必要があります」と表示される。開発モードのままで届かなければ、「アプリ設定 → ベーシック」にプライバシーポリシー URL（テスト用なので到達可能な URL なら何でもよい）を入れて**アプリを公開（ライブ）モードに切り替えて**再試行する。標準アクセスのままなので App Review は不要の想定（実測で確認）
2. `comments` フィールドを購読（subscribe）する
3. 「アクセストークンを生成する」セクションの表にある **Webhook サブスクリプションのトグルをオン**にする（アカウント単位の購読スイッチ。オフのままだとコメントイベントが届かない）

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

- [x] Webhook 検証（GET）が通る（2026-09-03 08:00 JST）
- [x] 他アカウントのコメントイベントを受信できる（2026-09-03 09:19 JST。リール投稿へのコメント「テスト」を受信）
- [x] Graph API でコメント返信が Instagram 上に表示される（受信から約 4 秒で返信 id 取得・Instagram 上で表示を確認）
- [x] 自己返信ループが起きない（自分の返信「はい。」の Webhook が届き、ループ防止でスキップされたことをログで確認）
- [x] （AI 返信）OpenAI キー投入後、質問に「はい / いいえ / 関係ありません」系の返信が付く（返信文「はい。」= OpenAI 経路）

**→ PoC 成功（2026-09-03）。** 実測で分かったこと:

- **開発モードでは comments Webhook は一切配信されない**（設定画面の注意書きどおり）。プライバシーポリシー URL を入れてアプリを**公開（ライブ）モード**に切り替えたら即座に届いた。App Review は不要だった（標準アクセスのまま）
- 受信ペイロードの形: `entry[].changes[].value` に `id`（コメント id）・`text`・`from.{id,username}`・`media.{id,media_product_type}`。自分の返信には `parent_id` と `from.self_ig_scoped_id` が付く。`from.id` は自分の返信なら Instagram user ID（`entry[].id` と同じ）で、ループ防止の照合キーとして使える
- 受信 → 返信の所要は約 4 秒（OpenAI 呼び出し込み）。PoC 規模では Function URL 同期処理で問題なし

成功したら: アイデア記録を「待機 → 採用」にし、開発計画（新セットのフェーズ起案）・事業戦略書（セットポートフォリオ）への転記を**開発レーン**で行う。
失敗したら（権限が取れない・返信が拒否される等）: 事象をアイデア記録に残し、見送りまたはピボットの再壁打ちを行う。

## 開発メモ

- テスト: `cd poc/umigame-comment-webhook && python3 -m pytest tests/`
- 手動での動作確認（署名付き POST の再現）はテストコードの `event_with_signature` を参照
- Meta の仕様は変更が多い領域。本 README の Meta 側手順と実際の画面が食い違ったら、実測した手順でこの README を上書きする（実態の記録を優先）
