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
    1. cdk diff <StackName>    ← 差分を目視確認
    2. cdk deploy <StackName>  ← 確認後にデプロイ
```

> **インフラパイプラインは構築しない**: FoundationStack に Aurora・VPC など破壊的変更のリスクが高いリソースが含まれるため、インフラ変更は `cdk diff` で差分を確認した上で手動デプロイとする。個人開発でインフラ変更頻度は低く、手動運用のコストも小さい。

## 2. パイプライン分割

サービスごとにパイプラインを分割する。

| パイプライン | 対象サービス | トリガー条件 |
|---|---|---|
| image-batch-pipeline | 画像生成バッチ | `services/image-batch/**` OR `shared/**` の変更 |
| sns-post-batch-pipeline | SNS 投稿バッチ | `services/sns-post-batch/**` OR `shared/**` の変更 |

> **db-readiness-check について**: db-readiness-check は FoundationStack で管理する共通ユーティリティであり、CI/CD パイプラインの対象外とする。更新時は手動で Docker ビルド・ECR push を行い、`cdk deploy FoundationStack` でタスク定義を更新する。

> **トリガー条件の補足**:
> - `shared/**` の変更は全サービスパイプラインをトリガーする（共通ライブラリの変更が各サービスに影響するため）
> - `infra/**` の変更に対する自動パイプラインは設けない。インフラ変更時は開発者が `cdk diff` → `cdk deploy` を手動で実行する。CDK Deploy によりタスク定義の revision が更新された場合は、サービスパイプラインを手動で起動して最新イメージで revision を再登録すること

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
      - 新しい ECS タスク定義リビジョンの登録（aws ecs register-task-definition）
      # Step Functions の更新は不要（タスク定義を family 名で参照し、常に最新リビジョンを使用するため）
      # CDK Deploy も不要（Task Definition の更新は本ステージで完結する）
```

### 3.2 インフラデプロイ（手動）

インフラ変更は CI/CD パイプラインを経由せず、開発者がローカルから手動で実行する。

```bash
# 手動デプロイ手順
cd infra
cdk diff <StackName>            # 差分を確認
cdk deploy <StackName>          # 確認後にデプロイ

# 全スタックを依存順にデプロイする場合
cdk deploy FoundationStack
cdk deploy SnsPostBatchStack
cdk deploy ImageBatchStack
cdk deploy MonitoringStack
```

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

### Task Definition の管理責任

| 操作 | 担当 | 説明 |
|---|---|---|
| db-readiness-check の初期作成・更新 | CDK（FoundationStack、手動） | 開発者が Docker イメージを手動で ECR push し、`cdk deploy FoundationStack` で新 revision を登録する |
| 初期作成 | CDK（ImageBatchStack / SnsPostBatchStack） | Task Definition、IAM Role、Log Group 等を一括作成 |
| イメージ更新時の revision 登録 | CodeBuild（post_build） | `aws ecs register-task-definition` で新 revision を登録 |
| インフラ変更（ロール、環境変数等） | CDK（手動デプロイ） | 開発者が `cdk diff` で差分確認後、`cdk deploy` を手動実行。CDK が管理する revision と CodeBuild が登録した最新 revision が乖離する可能性があるため、インフラ変更後はサービスパイプラインを手動実行して最新イメージで revision を再登録すること |

> **注意**: サービスパイプライン（image-batch-pipeline / sns-post-batch-pipeline）に Deploy Stage（CDK Deploy）は含めない。Task Definition の更新は CodeBuild の post_build で完結する。CDK Deploy はパイプラインに含めず、開発者が手動で実行する。

## 6. インフラ変更時の運用手順

CDK Deploy でタスク定義に影響する変更（ロール、環境変数、リソース参照等）を行った場合、CodeBuild が管理する最新 revision と CDK が作成した revision が乖離する。この乖離を防ぐため、インフラ変更時は以下の手順を必ず実施する。

### 6.1 手順

1. `cdk diff <StackName>` で差分を確認する
2. **db-readiness-check のイメージ更新を伴う場合**、手動で Docker ビルド・ECR push を行う
3. `cdk deploy <StackName>` でインフラを更新する
4. **ImageBatchStack または SnsPostBatchStack に変更が含まれる場合**、対応するサービスパイプラインを手動実行する
   - AWS Console → CodePipeline → 該当パイプラインの「変更をリリースする」を実行
   - CodeBuild が最新イメージで新 revision を登録し、CDK で変更されたロール・環境変数が反映される
5. Step Functions が次回実行時に最新 revision を使用することを確認する

### 6.2 パイプライン手動実行が必要なケース

| 変更内容 | パイプライン手動実行 |
|---|---|
| FoundationStack のみ（VPC、S3、Aurora 等。db-readiness-check を除く） | 不要（タスク定義に影響しない） |
| FoundationStack + db-readiness-check イメージ更新 | サービスパイプライン不要。手動で Docker ビルド・ECR push 後、`cdk deploy FoundationStack` を実行 |
| ImageBatchStack（ロール、環境変数等） | **image-batch-pipeline を手動実行** |
| SnsPostBatchStack（ロール、環境変数等） | **sns-post-batch-pipeline を手動実行** |
| MonitoringStack のみ | 不要 |

> **注意**: パイプラインの手動実行を忘れた場合、CDK が登録した revision（古いイメージ）が使用される可能性がある。運用設計書（[design/operation.md](operation.md)）の CDK デプロイ後チェックリストも併せて参照すること。

## 7. ブランチ戦略

| ブランチ | 用途 | デプロイ先 |
|---|---|---|
| main | 本番用 | 本番環境 |
| develop | 開発用（将来拡張。現時点では未使用） | 開発環境（将来） |
| feature/* | 機能開発 | - |

## 8. 環境分離方針

### 8.1 現在の運用

現時点では本番環境（`main` ブランチ）のみを運用する。環境は 1 つだが、将来の複数環境対応に備えて環境名は `prod` として扱う。開発環境の分離は将来拡張とする。

### 8.2 命名規約（将来の複数環境対応に備えた方針）

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

> **注記**: 初期開発では単一環境で運用するが、命名規約だけは `prod` を前提に先行導入しておく。
