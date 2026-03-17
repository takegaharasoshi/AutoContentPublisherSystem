# システム概要設計書

## 1. システムの目的

AWS 上のマネージドサービスを活用し、画像生成から SNS 投稿までを自動化するバッチシステムを構築する。

## 2. システム構成

### 2.1 画像生成バッチ

1. EventBridge Scheduler が定期的に Step Functions を起動
2. Step Functions が DB 準備確認 ECS タスクを起動し、Aurora の利用可能を確認
3. Step Functions が画像生成 ECS Fargate タスクを起動
4. Fargate タスクが Nano Banana Pro（Gemini 3 Pro 画像 API）を呼び出し、画像を生成
5. 生成した画像を S3 に保存
6. メタ情報を Aurora Serverless v2 に登録

### 2.2 SNS 投稿バッチ

1. EventBridge Scheduler が定期的に Step Functions を起動（または画像生成 Step Functions から自動起動）
2. Step Functions が DB 準備確認 ECS タスクを起動し、Aurora の利用可能を確認
3. Step Functions が SNS 投稿 ECS Fargate タスクを起動
4. Fargate タスクが DB から投稿対象を取得
5. S3 の画像に対して Presigned URL を発行（Instagram Graph API は公開到達可能な URL を要求するため）
6. Instagram Graph API に Presigned URL を渡して投稿
7. 投稿結果を DB に記録

## 3. アーキテクチャ構成図

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│   EventBridge   │────▶│  Step Functions   │────▶│  ECS Fargate    │
│   Scheduler     │     │  (Standard)       │     │  RunTask        │
└─────────────────┘     └──────────────────┘     └────────┬────────┘
                                                          │
                         ┌────────────────────────────────┼────────────────────┐
                         │                                │                    │
                         ▼                                ▼                    ▼
                ┌─────────────────┐             ┌─────────────────┐  ┌─────────────────┐
                │  External API   │             │      S3         │  │ Aurora Serverless│
                │  (画像生成/SNS) │             │  (画像保存)     │  │  v2 (MySQL)     │
                └─────────────────┘             └─────────────────┘  └─────────────────┘
```

## 4. 技術選定

| 要素 | 技術 | 選定理由 |
|---|---|---|
| 開発言語 | Python | AI/ML ライブラリの充実、API 連携の容易さ |
| DB | Aurora Serverless v2（MySQL） | 自動一時停止によるコスト最適化、サーバーレス運用 |
| バッチ実行 | ECS Fargate RunTask | サーバー管理不要、タスク単位の課金 |
| ワークフロー | Step Functions Standard | エラーハンドリング（Retry/Catch）、可視化 |
| スケジューラ | EventBridge Scheduler | cron 式による柔軟なスケジュール設定 |
| インフラ定義 | AWS CDK | TypeScript による型安全なインフラ定義 |
| CI/CD | CodePipeline + CodeBuild | AWS ネイティブ、ECR 連携の容易さ |

## 5. 開発環境

| 項目 | 詳細 |
|---|---|
| 開発端末 | Windows |
| エディタ | VS Code ベースのエディタ |
| 開発環境 | WSL2（Ubuntu） |
| コンテナ | Docker Desktop |

## 6. 開発方針

- **モノリポジトリ**を採用し、全サービスを単一リポジトリで管理する
- **機能単位（サービス単位）**でコンテナイメージを分割する
- CodePipeline / CodeBuild はサービスごとに分ける
- CDK Deploy はサービスごとに分ける
- 共通インフラと各サービスは CDK スタックを分離する

## 7. 拡張計画

- 画像生成バッチと SNS 投稿バッチを 1 セットとし、将来的に複数セットを運用する
  - 複数セット運用時は、Step Functions ステートマシンを共有し、EventBridge Scheduler をセットごとに追加する方式を採る
  - スケジュール定義のマスタは IaC（CDK）とする
- 管理画面（オンラインシステム）を追加し、設定・履歴・バッチ管理を GUI で行えるようにする
