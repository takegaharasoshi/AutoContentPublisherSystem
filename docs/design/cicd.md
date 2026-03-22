# CI/CD 設計書

## 1. 全体フロー

```
【サービスパイプライン（image-batch / sns-post-batch）】

GitHub (push)
    │
    ▼
CodePipeline
    │
    ├── Source Stage
    │     └── GitHub リポジトリからソース取得
    │
    └── Build Stage
          └── CodeBuild
                ├── Docker イメージのビルド
                ├── ECR へ push
                └── 新しい ECS タスク定義リビジョンの登録

【インフラデプロイ（手動）】

開発者がローカルから実行:
    1. cdk diff -c env=prod <StackName>    ← 差分を目視確認
    2. cdk deploy -c env=prod <StackName>  ← 確認後にデプロイ
```

> **インフラパイプラインは構築しない**: FoundationStack に Aurora・VPC など破壊的変更のリスクが高いリソースが含まれるため、インフラ変更は `cdk diff -c env=prod` で差分を確認した上で手動デプロイとする。個人開発でインフラ変更頻度は低く、手動運用のコストも小さい。

### 1.1 GitHub 接続方式

- **CodePipeline V2** + **CodeStar Connections（GitHub App）** を使用する
- CodeStar Connections は AWS コンソールで事前に作成し、GitHub リポジトリとの接続を承認する
- パイプラインの Source Stage で CodeStar Connections をソースプロバイダーとして指定する
- トリガーフィルタ: CodePipeline V2 のトリガー設定でファイルパスフィルタ（`services/image-batch/**`、`shared/**` 等）を指定し、関連ファイルの変更時のみパイプラインを起動する

## 2. パイプライン分割

サービスごとにパイプラインを分割する。

| パイプライン | 対象サービス | CDK スタック | トリガー条件 |
|---|---|---|---|
| image-batch-pipeline | 画像生成バッチ | ImageBatchStack | `services/image-batch/**` OR `shared/**` の変更 |
| sns-post-batch-pipeline | SNS 投稿バッチ | SnsPostBatchStack | `services/sns-post-batch/**` OR `shared/**` の変更 |

> **db-readiness-check について**: db-readiness-check は FoundationStack で管理する共通ユーティリティであり、CI/CD パイプラインの対象外とする。更新時は開発者が不変タグ（例: Git コミットハッシュ）で Docker イメージを ECR へ push し、`dbReadinessCheckImageTag` の CDK Context にそのタグを渡して `cdk deploy -c env=prod -c dbReadinessCheckImageTag=<tag> FoundationStack` を実行する。FoundationStack はこのタグを使って新しい ECS Task Definition revision を登録する。

> **トリガー条件の補足**:
> - `shared/**` の変更は全サービスパイプラインをトリガーする（共通ライブラリの変更が各サービスに影響するため）
> - `infra/**` の変更に対する自動パイプラインは設けない。インフラ変更時は開発者が `cdk diff -c env=prod` → `cdk deploy -c env=prod` を手動で実行する。サービスパイプラインは最新 ACTIVE revision をベースに image URI だけを差し替えて新 revision を登録するため、後続のイメージ更新時にも CDK 変更が引き継がれる

## 3. CodeBuild 設定

CodeBuild サービスロールの権限詳細は [design/security.md](security.md) セクション 2.5 を参照。

### 3.1 バッチサービス用（image-batch / sns-post-batch）

- **buildspec.yml の配置**: サービスごとに `services/{service-name}/buildspec.yml` に配置する（例: `services/image-batch/buildspec.yml`）
- **Docker ビルドコンテキスト**: リポジトリルートをビルドコンテキストとし、サービスごとの Dockerfile を `-f` オプションで指定する（例: `docker build -f services/image-batch/Dockerfile .`）。これにより `shared/` ディレクトリを `COPY` でコンテナに含めることができる
- **`.dockerignore`**: リポジトリルートに `.dockerignore` を配置し、ビルドに不要なファイル（`docs/`, `.git/`, `infra/`, `plans/`, ルート直下の `*.md`）を除外する。ビルドコンテキストの肥大化を防ぎ、ビルド時間を短縮する

```yaml
# buildspec.yml の概要
version: 0.2
phases:
  pre_build:
    commands:
      - ECR ログイン
      - イメージタグの設定（コミットハッシュ）
  build:
    commands:
      - Docker イメージのビルド
      - ECR へ push
  post_build:
    commands:
      - family 名で最新 ACTIVE な ECS タスク定義を取得（aws ecs describe-task-definition）
      - 取得した定義のコンテナ image URI だけを新タグへ差し替える
      - 新しい ECS タスク定義リビジョンを登録（aws ecs register-task-definition）
      # Task Definition 全体の SSOT は CDK。CodeBuild は image URI の差し替えだけを担う
      # Step Functions の更新は不要（タスク定義を family 名で参照し、常に最新リビジョンを使用するため）
```

### 3.2 インフラデプロイ（手動）

インフラ変更は CI/CD パイプラインを経由せず、開発者がローカルから手動で実行する。

```bash
# 手動デプロイ手順
cd infra
cdk diff -c env=prod <StackName>            # 差分を確認
cdk deploy -c env=prod <StackName>          # 確認後にデプロイ

# db-readiness-check イメージ更新時
cdk diff -c env=prod -c dbReadinessCheckImageTag=<immutable-tag> FoundationStack
cdk deploy -c env=prod -c dbReadinessCheckImageTag=<immutable-tag> FoundationStack

# 全スタックを依存順にデプロイする場合
cdk deploy -c env=prod FoundationStack
cdk deploy -c env=prod SnsPostBatchStack
cdk deploy -c env=prod ImageBatchStack
cdk deploy -c env=prod MonitoringStack
```

> **注記**: 上記の `FoundationStack` などは CDK app 内の論理スタック ID であり、`-c env=prod` を付与した場合の CloudFormation 実スタック名は `Prod-FoundationStack` のように環境名付きとなる。

## 4. ECR リポジトリ

サービスごとに ECR リポジトリを作成する。

| リポジトリ名 | 対象サービス |
|---|---|
| auto-content-publisher/image-batch | 画像生成バッチ |
| auto-content-publisher/sns-post-batch | SNS 投稿バッチ |
| auto-content-publisher/db-readiness-check | DB 準備確認（パイプライン対象外・手動更新） |

### ライフサイクルポリシー

ECR リポジトリにはライフサイクルポリシーを設定し、古いイメージを自動削除する。

- **保持ルール**: タグ付きイメージを最新 10 個まで保持し、それ以前は自動削除する
- **設定箇所**: FoundationStack の ECR リポジトリ定義に含める

## 5. デプロイ方式

- Blue/Green デプロイは採用しない
- ECS Service は使用しない
- Docker イメージを ECR に push し、新しい ECS タスク定義リビジョンを登録する
- **タスク定義の参照方式**: Step Functions はタスク定義を family 名（例: `acps-prod-image-batch`）で参照し、ECS RunTask API が常に ACTIVE な最新リビジョンを使用する
- **Task Definition の SSOT**: Task Definition 全体（family、ロール、環境変数、ログ設定、CPU/メモリ）の正は CDK とする。CodeBuild は最新 ACTIVE revision を取得し、コンテナ image URI だけを差し替えて新 revision を登録する

### Task Definition の管理責任

| 操作 | 担当 | 説明 |
|---|---|---|
| db-readiness-check の初期作成・更新 | CDK（FoundationStack、手動） | 開発者が Docker イメージを不変タグで ECR push し、`cdk deploy -c env=prod -c dbReadinessCheckImageTag=<tag> FoundationStack` でそのタグを参照する新 revision を登録する |
| 初期作成・設定変更 | CDK（ImageBatchStack / SnsPostBatchStack） | Task Definition、IAM Role、Log Group、環境変数等を一括作成し、Task Definition 全体の正とする |
| イメージ更新時の revision 登録 | CodeBuild（post_build） | `aws ecs describe-task-definition` で latest ACTIVE revision を取得し、コンテナ image URI だけを差し替えて `aws ecs register-task-definition` で新 revision を登録する |
| インフラ変更後の確認 | 開発者 | `cdk deploy -c env=prod` 後に latest ACTIVE revision を確認し、ロール・環境変数・リソース参照が反映されていることを確認する |

> **注意**: サービスパイプライン（image-batch-pipeline / sns-post-batch-pipeline）に Deploy Stage（CDK Deploy）は含めない。インフラ変更は必ず CDK の手動デプロイで反映し、アプリ更新時の Task Definition revision 登録は CodeBuild が担う。

## 6. インフラ変更時の運用手順

CDK Deploy でタスク定義に影響する変更（ロール、環境変数、リソース参照等）を行った場合も、CDK が latest ACTIVE revision を更新する。CodeBuild は後続のイメージ更新時にこの latest ACTIVE revision をベースに image URI だけを差し替えるため、設定変更は自動的に引き継がれる。インフラ変更時は以下の手順を実施する。

### 6.1 手順

1. `cdk diff -c env=prod <StackName>` で差分を確認する
2. **db-readiness-check のイメージ更新を伴う場合**、手動で Docker イメージをビルドし、不変タグで ECR に push する
3. `cdk deploy -c env=prod <StackName>` でインフラを更新する
   - db-readiness-check の更新時は `cdk deploy -c env=prod -c dbReadinessCheckImageTag=<tag> FoundationStack` を使用する
4. **ImageBatchStack または SnsPostBatchStack に変更が含まれる場合**、latest ACTIVE revision を確認する
   - 期待するロール、環境変数、ログ設定、リソース参照が反映されていることを AWS Console または CLI で確認する
5. Step Functions が次回実行時に latest ACTIVE revision を使用することを確認する

### 6.2 パイプライン手動実行が必要なケース

| 変更内容 | パイプライン手動実行 |
|---|---|
| FoundationStack のみ（VPC、S3、Aurora 等。db-readiness-check を除く） | 不要（タスク定義に影響しない） |
| FoundationStack + db-readiness-check イメージ更新 | サービスパイプライン不要。手動で Docker ビルド・ECR push 後、`cdk deploy -c env=prod -c dbReadinessCheckImageTag=<tag> FoundationStack` を実行 |
| ImageBatchStack（ロール、環境変数等） | 不要（CDK が latest ACTIVE revision を更新する） |
| SnsPostBatchStack（ロール、環境変数等） | 不要（同上） |
| MonitoringStack のみ | 不要 |

> **注意**: インフラ変更の直後にアプリケーションコードも差し替えたい場合のみ、対応するサービスパイプラインを任意で手動実行する。設定反映だけが目的であれば、手動実行は不要である。

## 7. ブランチ戦略

| ブランチ | 用途 | デプロイ先 |
|---|---|---|
| main | 本番用 | 本番環境 |
| develop | 開発用（将来拡張。現時点では未使用） | 開発環境（将来） |
| feature/* | 機能開発 | - |

## 8. パイプラインの失敗監視

CodePipeline / CodeBuild の失敗はコンソールで手動確認する。現時点では自動通知の仕組みは構築しない。

> **将来の改善**: パイプライン失敗の検知を自動化する場合は、CodePipeline のステート変更を EventBridge Rule で検知し、SNS Topic に通知する構成を検討する。

## 9. 環境分離方針

### 9.1 現在の運用

現時点では本番環境（`main` ブランチ）のみを運用する。環境は 1 つだが、将来の複数環境対応に備えて環境名は `prod` として扱う。開発環境の分離は将来拡張とする。

### 9.2 命名規約（将来の複数環境対応に備えた方針）

将来的に開発環境を追加する際は、**同一 AWS アカウント内**で環境を分離する（アカウント分離は行わない）。以下の命名規約でリソースを区別する:

| リソース | 命名規約 | 例（本番） | 例（開発） |
|---|---|---|---|
| CDK スタック | `{EnvName}-{StackName}` | `Prod-FoundationStack` | `Dev-FoundationStack` |
| ECR リポジトリ | 環境共通（イメージタグで区別） | `auto-content-publisher/image-batch:abc123` | 同左 |
| Secrets Manager | `acps/{env}/...` | `acps/prod/db/credentials` | `acps/dev/db/credentials` |
| S3 バケット | CDK Context で環境ごとに別バケット | `acps-prod-images` | `acps-dev-images` |

- CDK Context パラメータ（`-c env=prod`）で環境名を渡し、リソース名に反映する
- 現時点の単一環境でも `env=prod` を付与して運用し、Secret 名・IAM スコープ・スタック名に反映する
- ECS Task Definition には `ENV_NAME` を環境変数として注入し、アプリケーションが Secret 名を導出できるようにする
- S3 バケット名はグローバルに一意である必要がある。CDK がバケット名に一意のサフィックスを自動付与するため、上表の例（`acps-prod-images`）は論理名であり、実際のバケット名は `acps-prod-images-xxxxxxxxxxxx` のような形式になる

> **注記**: 初期開発では単一環境で運用するが、命名規約だけは `prod` を前提に先行導入しておく。
