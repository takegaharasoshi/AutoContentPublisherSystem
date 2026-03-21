# ワークフロー実装仕様

処理フローの業務ロジックは [design/batch.md](../design/batch.md) を参照。CDK リソース定義は [specs/infrastructure.md](infrastructure.md) を参照。運用時の対応手順は [design/operation.md](../design/operation.md) を参照。

## 1. 画像生成 Step Functions ASL 定義

> **TaskDefinition の指定方式**: ASL 内の `${...TaskDefFamily}` プレースホルダには、CDK が ECS Task Definition の family 名（例: `acps-prod-image-batch`）を渡す。ECS RunTask API は family 名指定で常に ACTIVE な最新リビジョンを使用するため、デプロイ時に ASL の更新は不要。

```json
{
  "StartAt": "WaitForDbReady",
  "States": {
    "WaitForDbReady": {
      "Type": "Task",
      "Resource": "arn:aws:states:::ecs:runTask.sync",
      "Parameters": {
        "LaunchType": "FARGATE",
        "Cluster": "${EcsClusterArn}",
        "TaskDefinition": "${DbReadinessCheckTaskDefFamily}",
        "NetworkConfiguration": {
          "AwsvpcConfiguration": {
            "Subnets": ["${PublicSubnetId1}", "${PublicSubnetId2}"],
            "SecurityGroups": ["${DbReadinessCheckSgId}"],
            "AssignPublicIp": "ENABLED"
          }
        }
      },
      "Retry": [
        {
          "ErrorEquals": ["States.TaskFailed"],
          "IntervalSeconds": 30,
          "MaxAttempts": 2,
          "BackoffRate": 2.0
        }
      ],
      "Catch": [
        {
          "ErrorEquals": ["States.ALL"],
          "Next": "HandleError"
        }
      ],
      "Next": "RunImageBatchTask"
    },
    "RunImageBatchTask": {
      "Type": "Task",
      "Resource": "arn:aws:states:::ecs:runTask.sync",
      "Parameters": {
        "LaunchType": "FARGATE",
        "Cluster": "${EcsClusterArn}",
        "TaskDefinition": "${ImageBatchTaskDefFamily}",
        "NetworkConfiguration": {
          "AwsvpcConfiguration": {
            "Subnets": ["${PublicSubnetId1}", "${PublicSubnetId2}"],
            "SecurityGroups": ["${ImageBatchSgId}"],
            "AssignPublicIp": "ENABLED"
          }
        },
        "Overrides": {
          "ContainerOverrides": [
            {
              "Name": "image-batch",
              "Environment": [
                { "Name": "SET_CODE", "Value.$": "$.set_code" },
                { "Name": "EXECUTION_ARN", "Value.$": "$$.Execution.Id" },
                { "Name": "SCHEDULED_AT", "Value.$": "$.scheduled_at" }
              ]
            }
          ]
        }
      },
      "Retry": [
        {
          "ErrorEquals": ["States.TaskFailed"],
          "IntervalSeconds": 30,
          "MaxAttempts": 2,
          "BackoffRate": 2.0
        }
      ],
      "Catch": [
        {
          "ErrorEquals": ["States.ALL"],
          "Next": "HandleError"
        }
      ],
      "Next": "StartSnsPostBatch"
    },
    "StartSnsPostBatch": {
      "Type": "Task",
      "Resource": "arn:aws:states:::states:startExecution",
      "Parameters": {
        "StateMachineArn": "${SnsPostingSfnArn}",
        "Input": {
          "set_code.$": "$.set_code"
        }
      },
      "Retry": [
        {
          "ErrorEquals": ["States.TaskFailed"],
          "IntervalSeconds": 10,
          "MaxAttempts": 2,
          "BackoffRate": 2.0
        }
      ],
      "Catch": [
        {
          "ErrorEquals": ["States.ALL"],
          "Next": "NotifySnsPostStartFailure"
        }
      ],
      "End": true
    },
    "NotifySnsPostStartFailure": {
      "Type": "Task",
      "Resource": "arn:aws:states:::aws-sdk:cloudwatch:putMetricData",
      "Parameters": {
        "Namespace": "ACPS",
        "MetricData": [
          {
            "MetricName": "SnsPostStartFailureCount",
            "Value": 1,
            "Unit": "Count"
          }
        ]
      },
      "Comment": "SNS 投稿 SFN の起動失敗を CloudWatch カスタムメトリクスとして発行し、MonitoringStack のアラームで検知する",
      "Next": "ImageBatchSucceeded"
    },
    "ImageBatchSucceeded": {
      "Type": "Succeed",
      "Comment": "画像生成は成功済みのため、SNS 投稿 SFN の起動失敗時もワークフローは成功終了とする。SNS 投稿が起動されなかったことはカスタムメトリクスのアラームで検知し、手動で sns-posting-sfn を起動する"
    },
    "HandleError": {
      "Type": "Fail",
      "Error": "ImageBatchFailed",
      "Cause": "Image batch task failed after retries"
    }
  }
}
```

> **StartSnsPostBatch のエラーハンドリング**: Retry 後も起動に失敗した場合は `NotifySnsPostStartFailure` でカスタムメトリクスを発行し、`ImageBatchSucceeded` で成功終了する。画像生成 ECS タスクは既に成功しているため、SNS 投稿の起動失敗のみでワークフロー全体を失敗にはしない。

## 2. SNS 投稿 Step Functions ASL 定義

画像生成 Step Functions から `startExecution`（非同期）で起動される。画像生成 Step Functions は SNS 投稿の完了を待たずに終了する。手動での単独起動も可能。

```json
{
  "StartAt": "WaitForDbReady",
  "States": {
    "WaitForDbReady": {
      "Type": "Task",
      "Resource": "arn:aws:states:::ecs:runTask.sync",
      "Parameters": {
        "LaunchType": "FARGATE",
        "Cluster": "${EcsClusterArn}",
        "TaskDefinition": "${DbReadinessCheckTaskDefFamily}",
        "NetworkConfiguration": {
          "AwsvpcConfiguration": {
            "Subnets": ["${PublicSubnetId1}", "${PublicSubnetId2}"],
            "SecurityGroups": ["${DbReadinessCheckSgId}"],
            "AssignPublicIp": "ENABLED"
          }
        }
      },
      "Retry": [
        {
          "ErrorEquals": ["States.TaskFailed"],
          "IntervalSeconds": 30,
          "MaxAttempts": 2,
          "BackoffRate": 2.0
        }
      ],
      "Catch": [
        {
          "ErrorEquals": ["States.ALL"],
          "Next": "HandleError"
        }
      ],
      "Next": "RunSnsPostBatchTask"
    },
    "RunSnsPostBatchTask": {
      "Type": "Task",
      "Resource": "arn:aws:states:::ecs:runTask.sync",
      "Parameters": {
        "LaunchType": "FARGATE",
        "Cluster": "${EcsClusterArn}",
        "TaskDefinition": "${SnsPostBatchTaskDefFamily}",
        "NetworkConfiguration": {
          "AwsvpcConfiguration": {
            "Subnets": ["${PublicSubnetId1}", "${PublicSubnetId2}"],
            "SecurityGroups": ["${SnsPostBatchSgId}"],
            "AssignPublicIp": "ENABLED"
          }
        },
        "Overrides": {
          "ContainerOverrides": [
            {
              "Name": "sns-post-batch",
              "Environment": [
                { "Name": "SET_CODE", "Value.$": "$.set_code" },
                { "Name": "EXECUTION_ARN", "Value.$": "$$.Execution.Id" }
              ]
            }
          ]
        }
      },
      "Retry": [
        {
          "ErrorEquals": ["States.TaskFailed"],
          "IntervalSeconds": 30,
          "MaxAttempts": 2,
          "BackoffRate": 2.0
        }
      ],
      "Catch": [
        {
          "ErrorEquals": ["States.ALL"],
          "Next": "HandleError"
        }
      ],
      "End": true
    },
    "HandleError": {
      "Type": "Fail",
      "Error": "SnsPostBatchFailed",
      "Cause": "SNS post batch task failed after retries"
    }
  }
}
```

## 3. 環境変数一覧

### 3.1 画像生成バッチ

| 変数名 | 説明 | 取得元 |
|---|---|---|
| DB_SECRET_ARN | DB 接続情報の Secret ARN | CDK で設定 |
| API_SECRET_ARN | 画像生成 API キーの Secret ARN | CDK で設定 |
| S3_BUCKET_NAME | 画像保存先 S3 バケット名 | CDK で設定 |
| ENV_NAME | 環境識別子（現時点では `prod`） | CDK で設定 |
| SET_CODE | バッチセット識別コード（batch_sets.set_code に対応） | Step Functions 入力パラメータ |
| EXECUTION_ARN | Step Functions 実行 ARN（手動 RunTask 時は空） | Step Functions コンテナオーバーライド（`$$.Execution.Id`） |
| SCHEDULED_AT | スケジュール実行日時（ISO 8601、例: 2024-01-15T00:00:00Z）。DB には UTC の DATETIME として保存する（`Z` 接尾辞を除いた値） | Step Functions 入力パラメータ（EventBridge Scheduler の `<aws.scheduler.scheduled-time>` から取得） |

### 3.2 SNS 投稿バッチ

| 変数名 | 説明 | 取得元 |
|---|---|---|
| DB_SECRET_ARN | DB 接続情報の Secret ARN | CDK で設定 |
| S3_BUCKET_NAME | 画像保存元 S3 バケット名 | CDK で設定 |
| ENV_NAME | 環境識別子（現時点では `prod`） | CDK で設定 |
| SET_CODE | バッチセット識別コード（batch_sets.set_code に対応） | Step Functions 入力パラメータ |
| EXECUTION_ARN | Step Functions 実行 ARN（手動 RunTask 時は空） | Step Functions コンテナオーバーライド（`$$.Execution.Id`） |
| BATCH_SIZE_LIMIT | 1 回のバッチ実行で処理する最大投稿件数（デフォルト: 50） | CDK で設定 |

> **SNS 認証情報**: 環境変数ではなく Secrets Manager からアカウントごとに取得する。Secret 名規約は [design/security.md](../design/security.md) を参照。

## 4. Step Functions エラーハンドリング

| エラー種別 | 対応 |
|---|---|
| ECS タスク起動失敗 | Retry（最大 2 回、30 秒間隔） |
| ECS タスク異常終了 | Retry → Catch → Fail ステートへ遷移 |
| タイムアウト | Catch → Fail ステートへ遷移 |
| SNS 投稿 SFN 起動失敗 | Retry → Catch → カスタムメトリクス発行 → 画像生成ワークフローは成功終了 |

## 5. カスタムメトリクス定義

| メトリクス名 | Namespace | 発行元 | 用途 |
|---|---|---|---|
| `SnsPostStartFailureCount` | `ACPS` | image-generation-sfn（`NotifySnsPostStartFailure` ステート） | SNS 投稿 Step Functions の起動失敗を検知 |

## 6. CloudWatch Alarm 定義

| 監視対象 | メトリクス | 条件 | Period | EvaluationPeriods | DatapointsToAlarm | TreatMissingData | 通知先 |
|---|---|---|---|---|---|---|---|
| Step Functions 失敗 | 標準メトリクス `ExecutionsFailed` | >= 1 | 300 秒 | 1 | 1 | notBreaching | SNS Topic |
| SNS 投稿起動失敗 | カスタムメトリクス `ACPS/SnsPostStartFailureCount` | >= 1 | 300 秒 | 1 | 1 | notBreaching | SNS Topic |
| Aurora CPU | 標準メトリクス `CPUUtilization` | >= 80% | 300 秒 | 3 | 2 | notBreaching | SNS Topic |
| Aurora メモリ | 標準メトリクス `FreeableMemory` | <= 268435456（256 MB） | 300 秒 | 3 | 2 | notBreaching | SNS Topic |

> **閾値の設計方針**: Aurora のアラームは `notBreaching`（データ欠損時はアラームを発報しない）を使用する。Aurora Serverless v2 の自動一時停止中はメトリクスが発行されないため、`missing` や `breaching` にすると一時停止のたびにアラームが発報される。Step Functions とカスタムメトリクスのアラームも同様に `notBreaching` とする。閾値は初期値であり、実運用の負荷状況に応じて調整する。

## 7. EventBridge Rule 定義

| ルール | イベントソース | フィルタ条件 | アクション |
|---|---|---|---|
| ECS タスク異常終了検知 | ECS Task State Change | `exitCode != 0` または異常停止 | SNS Topic に通知 |

> **ECS タスク異常終了の監視**: ECS タスクの終了コードは CloudWatch の標準メトリクスとして提供されないため、CloudWatch Alarm では直接監視できない。代わりに EventBridge Rule で ECS Task State Change イベント（`detail.stoppedReason` / `detail.containers[].exitCode` でフィルタ）を捕捉し、SNS Topic に通知する。
