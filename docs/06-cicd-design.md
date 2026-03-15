# CI/CD 設計書

## 1. 全体フロー

```
GitHub (push)
    │
    ▼
CodePipeline（サービスごと）
    │
    ├── Source Stage
    │     └── GitHub リポジトリからソース取得
    │
    ├── Build Stage
    │     └── CodeBuild
    │           ├── Docker イメージのビルド
    │           ├── ECR へ push
    │           └── 新しい ECS タスク定義リビジョンの登録
    │
    └── Deploy Stage
          └── CDK Deploy（対象スタック）
```

## 2. パイプライン分割

サービスごとにパイプラインを分割する。

| パイプライン | 対象サービス | トリガー条件 |
|---|---|---|
| image-batch-pipeline | 画像生成バッチ | `services/image-batch/**` の変更 |
| sns-post-batch-pipeline | SNS 投稿バッチ | `services/sns-post-batch/**` の変更 |
| foundation-pipeline | 共通基盤 | `infra/foundation/**` の変更 |
| monitoring-pipeline | 監視 | `infra/monitoring/**` の変更 |

## 3. CodeBuild 設定

### 3.1 バッチサービス用（image-batch / sns-post-batch）

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
      - 新しい ECS タスク定義リビジョンの登録
      - Step Functions の定義更新（必要に応じて）
```

### 3.2 インフラ用（CDK Deploy）

```yaml
# buildspec.yml の概要
version: 0.2
phases:
  install:
    commands:
      - npm install（CDK 依存パッケージ）
  build:
    commands:
      - cdk deploy <StackName> --require-approval never
```

## 4. ECR リポジトリ

サービスごとに ECR リポジトリを作成する。

| リポジトリ名 | 対象サービス |
|---|---|
| auto-content-publisher/image-batch | 画像生成バッチ |
| auto-content-publisher/sns-post-batch | SNS 投稿バッチ |

## 5. デプロイ方式

- Blue/Green デプロイは採用しない
- ECS Service は使用しない
- Docker イメージを ECR に push し、新しい ECS タスク定義リビジョンを登録する
- Step Functions は最新のタスク定義を参照して Fargate タスクを起動する

## 6. ブランチ戦略

| ブランチ | 用途 | デプロイ先 |
|---|---|---|
| main | 本番用 | 本番環境 |
| develop | 開発用 | 開発環境（将来） |
| feature/* | 機能開発 | - |
