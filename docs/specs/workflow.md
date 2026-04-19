# ワークフロー実装仕様

処理フローの業務ロジックは [design/batch.md](../design/batch.md) を参照。CDK リソース定義は [specs/infrastructure.md](infrastructure.md) を参照。運用時の対応手順は [design/operation.md](../design/operation.md) を参照。

## 1. 画像生成 Step Functions ASL 定義

> **TaskDefinition の指定方式**: ASL 内の `${...TaskDefFamily}` プレースホルダには、CDK が ECS Task Definition の family 名（例: `acps-prod-image-batch`）を渡す。ECS RunTask API は family 名指定で常に ACTIVE な最新リビジョンを使用するため、デプロイ時に ASL の更新は不要。

> **SecurityGroup の指定方式**: `${BatchSgId}` は FoundationStack で定義される「ECS Fargate 用（バッチ共通）」Security Group を指す。画像生成バッチと SNS 投稿バッチは同一の Security Group を共有する。DB 準備確認タスクには専用の `${DbReadinessCheckSgId}` を使用する。

> **WaitForDbReady の retry 方針**: DB 準備確認の再試行は db-readiness-check コンテナ内部で完結させる。`WaitForDbReady` ステート自体には Step Functions Retry を設定せず、総待機時間を ECS タスク内部の約 510 秒に固定する。

> **Task ステートのタイムアウト**: ハング時にワークフローが長時間ぶら下がらないよう、`WaitForDbReady=900` 秒、`RunImageBatchTask=3600` 秒、`StartSnsPostBatch=60` 秒、`RunSnsPostBatchTask=3600` 秒の明示タイムアウトを設定する。`WaitForDbReady` の 900 秒は、ECS Fargate 起動（約 60 秒）+ DB 接続リトライ（最大約 510 秒）+ バッファ（約 330 秒）を考慮した値である。

> **StartSnsPostBatch の呼び出し方式**: `StartSnsPostBatch` で使用する `arn:aws:states:::states:startExecution`（`.sync` サフィックスなし）は非同期呼び出しであり、子実行（sns-posting-sfn）の完了を待たずに即座に成功を返す。画像生成ワークフローは SNS 投稿の起動のみを行い、投稿処理の完了は待機しない。

> **StartSnsPostBatch の冪等性**: `StartExecution.Name` には親ワークフローの `$$.Execution.Name` を渡す。これにより Retry 時も同一要求として扱われ、SNS 投稿 Step Functions の二重起動リスクを抑制できる。

> **実行名の文字数制限**: Step Functions の実行名（`Name`）は最大 80 文字に制限されている。本システムでは `$$.Execution.Name` を子実行の Name として使用する。EventBridge Scheduler がデフォルトで生成する実行名は UUID ベース（36 文字）のため通常は問題ないが、カスタム名を使用する場合は 80 文字制限に注意すること。

> **ResultPath の設定**: `WaitForDbReady` と `RunImageBatchTask` には `"ResultPath": null` を設定し、ECS RunTask.sync の出力（DescribeTasks レスポンス）で入力パラメータ（`$.set_code` 等）が上書きされるのを防ぐ。

> **EventBridge Scheduler の Input テンプレート**: Scheduler は以下の形式で画像生成 Step Functions を起動する。`<aws.scheduler.scheduled-time>` は EventBridge Scheduler が実行時刻（UTC、ISO 8601）に自動置換する。
>
> ```json
> {
>   "set_code": "fashion-set-1",
>   "scheduled_at": "<aws.scheduler.scheduled-time>"
> }
> ```

> **EventBridge Scheduler の Retry / DLQ**: Scheduler には RetryPolicy と SQS DLQ を設定する。RetryPolicy は `MaximumRetryAttempts=3`、`MaximumEventAgeInSeconds=3600` を初期値とする。リトライを使い切っても画像生成 Step Functions を起動できない場合は、失敗イベントを Scheduler DLQ に送信し、MonitoringStack の CloudWatch Alarm で検知する。

```json
{
  "StartAt": "WaitForDbReady",
  "States": {
    "WaitForDbReady": {
      "Type": "Task",
      "Resource": "arn:aws:states:::ecs:runTask.sync",
      "TimeoutSeconds": 900,
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
      "ResultPath": null,
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
      "TimeoutSeconds": 3600,
      "Parameters": {
        "LaunchType": "FARGATE",
        "Cluster": "${EcsClusterArn}",
        "TaskDefinition": "${ImageBatchTaskDefFamily}",
        "NetworkConfiguration": {
          "AwsvpcConfiguration": {
            "Subnets": ["${PublicSubnetId1}", "${PublicSubnetId2}"],
            "SecurityGroups": ["${BatchSgId}"],
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
          "ErrorEquals": ["States.TaskFailed", "States.Timeout"],
          "IntervalSeconds": 30,
          "MaxAttempts": 2,
          "BackoffRate": 2.0
        }
      ],
      "ResultPath": null,
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
      "TimeoutSeconds": 60,
      "Parameters": {
        "StateMachineArn": "${SnsPostingSfnArn}",
        "Name.$": "$$.Execution.Name",
        "Input": {
          "set_code.$": "$.set_code"
        }
      },
      "Retry": [
        {
          "ErrorEquals": ["States.ALL"],
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
            "Dimensions": [
              {
                "Name": "StateMachineName",
                "Value": "${ImageGenerationSfnName}"
              }
            ],
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
      "TimeoutSeconds": 900,
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
      "ResultPath": null,
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
      "TimeoutSeconds": 3600,
      "Parameters": {
        "LaunchType": "FARGATE",
        "Cluster": "${EcsClusterArn}",
        "TaskDefinition": "${SnsPostBatchTaskDefFamily}",
        "NetworkConfiguration": {
          "AwsvpcConfiguration": {
            "Subnets": ["${PublicSubnetId1}", "${PublicSubnetId2}"],
            "SecurityGroups": ["${BatchSgId}"],
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
          "ErrorEquals": ["States.TaskFailed", "States.Timeout"],
          "IntervalSeconds": 30,
          "MaxAttempts": 2,
          "BackoffRate": 2.0
        }
      ],
      "ResultPath": null,
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
| EXECUTION_ARN | Step Functions 実行 ARN（手動 RunTask 時は空）。`$$.Execution.Id` は名前に反して実行 ARN（`arn:aws:states:...` 形式）を返す | Step Functions コンテナオーバーライド（`$$.Execution.Id`） |
| SCHEDULED_AT | スケジュール実行日時（ISO 8601、例: 2024-01-15T00:00:00Z）。DB には UTC の DATETIME として保存する（`Z` 接尾辞を除いた値） | Step Functions 入力パラメータ（EventBridge Scheduler の `<aws.scheduler.scheduled-time>` から取得） |

### 3.2 SNS 投稿バッチ

| 変数名 | 説明 | 取得元 |
|---|---|---|
| DB_SECRET_ARN | DB 接続情報の Secret ARN | CDK で設定 |
| S3_BUCKET_NAME | 画像保存元 S3 バケット名 | CDK で設定 |
| ENV_NAME | 環境識別子（現時点では `prod`） | CDK で設定 |
| SET_CODE | バッチセット識別コード（batch_sets.set_code に対応） | Step Functions 入力パラメータ |
| EXECUTION_ARN | Step Functions 実行 ARN（手動 RunTask 時は空）。`$$.Execution.Id` は名前に反して実行 ARN（`arn:aws:states:...` 形式）を返す | Step Functions コンテナオーバーライド（`$$.Execution.Id`） |
| BATCH_SIZE_LIMIT | 1 回のバッチ実行で処理する最大投稿件数（デフォルト: 50） | CDK で設定 |

> **SNS 認証情報**: 環境変数ではなく Secrets Manager からアカウントごとに取得する。Secret 名規約は [design/security.md](../design/security.md) を参照。

### 3.3 DB 準備確認タスク

| 変数名 | 説明 | 取得元 |
|---|---|---|
| DB_SECRET_ARN | DB 接続情報の Secret ARN | CDK で設定 |
| ENV_NAME | 環境識別子（現時点では `prod`） | CDK で設定 |

> **注記**: DB 準備確認タスクの環境変数はすべて CDK で Task Definition に静的設定する。Step Functions からのコンテナオーバーライドはない。

## 4. Step Functions エラーハンドリング

| エラー種別 | 対応 |
|---|---|
| DB 準備確認失敗 | db-readiness-check コンテナ内部で最大 8 回 retry 後、Catch → Fail ステートへ遷移 |
| 画像生成 / SNS 投稿 ECS タスク起動失敗 | Retry（最大 2 回、30 秒間隔） |
| 画像生成 / SNS 投稿 ECS タスク異常終了 | Retry → Catch → Fail ステートへ遷移 |
| タイムアウト | Retry（`States.Timeout` を Retry 対象に含む。一時的なネットワーク遅延等を考慮）→ Catch → Fail ステートへ遷移 |
| SNS 投稿 SFN 起動失敗 | `Name=$$.Execution.Name` で冪等化した上で Retry（`States.ALL`、最大 2 回、10 秒間隔）→ Catch → カスタムメトリクス発行 → 画像生成ワークフローは成功終了 |
| EventBridge Scheduler の画像生成 SFN 起動失敗 | Scheduler Retry（最大 3 回、イベント有効期間 3600 秒）→ Scheduler DLQ 送信 → CloudWatch Alarm で通知 |

## 5. カスタムメトリクス定義

| メトリクス名 | Namespace | Dimensions | 発行元 | 用途 |
|---|---|---|---|---|
| `SnsPostStartFailureCount` | `ACPS` | `StateMachineName=${ImageGenerationSfnName}` | image-generation-sfn（`NotifySnsPostStartFailure` ステート） | SNS 投稿 Step Functions の起動失敗を検知 |

## 6. CloudWatch Alarm 定義

| 監視対象 | Namespace | メトリクス | Dimensions | 条件 | Period | EvaluationPeriods | DatapointsToAlarm | TreatMissingData | 通知先 |
|---|---|---|---|---|---|---|---|---|---|
| image-generation-sfn 失敗 | `AWS/States` | `ExecutionsFailed` | `StateMachineArn=${ImageGenerationSfnArn}` | >= 1 | 300 秒 | 1 | 1 | notBreaching | SNS Topic |
| sns-posting-sfn 失敗 | `AWS/States` | `ExecutionsFailed` | `StateMachineArn=${SnsPostingSfnArn}` | >= 1 | 300 秒 | 1 | 1 | notBreaching | SNS Topic |
| SNS 投稿起動失敗 | `ACPS` | `SnsPostStartFailureCount` | `StateMachineName=${ImageGenerationSfnName}` | >= 1 | 300 秒 | 1 | 1 | notBreaching | SNS Topic |
| Scheduler ターゲット起動失敗 | `AWS/Scheduler` | `TargetErrorCount` | `ScheduleGroup=${ImageScheduleGroupName}` | >= 1 | 300 秒 | 1 | 1 | notBreaching | SNS Topic |
| Scheduler ターゲット API スロットル | `AWS/Scheduler` | `TargetErrorThrottledCount` | `ScheduleGroup=${ImageScheduleGroupName}` | >= 1 | 300 秒 | 1 | 1 | notBreaching | SNS Topic |
| Scheduler 呼び出しスロットル | `AWS/Scheduler` | `InvocationThrottleCount` | `ScheduleGroup=${ImageScheduleGroupName}` | >= 1 | 300 秒 | 1 | 1 | notBreaching | SNS Topic |
| Scheduler リトライ枯渇 | `AWS/Scheduler` | `InvocationDroppedCount` | `ScheduleGroup=${ImageScheduleGroupName}` | >= 1 | 300 秒 | 1 | 1 | notBreaching | SNS Topic |
| Scheduler DLQ 送信 | `AWS/Scheduler` | `InvocationsSentToDeadLetterCount` | `ScheduleGroup=${ImageScheduleGroupName}` | >= 1 | 300 秒 | 1 | 1 | notBreaching | SNS Topic |
| Scheduler DLQ 送信失敗 | `AWS/Scheduler` | `InvocationsFailedToBeSentToDeadLetterCount` | `ScheduleGroup=${ImageScheduleGroupName}` | >= 1 | 300 秒 | 1 | 1 | notBreaching | SNS Topic |
| Aurora CPU | `AWS/RDS` | `CPUUtilization` | `DBClusterIdentifier=${AuroraClusterIdentifier}` | >= 80% | 300 秒 | 3 | 2 | notBreaching | SNS Topic |
| Aurora メモリ | `AWS/RDS` | `FreeableMemory` | `DBClusterIdentifier=${AuroraClusterIdentifier}` | <= 268435456（256 MB） | 300 秒 | 3 | 2 | notBreaching | SNS Topic |

> **閾値の設計方針**: Aurora のアラームは `notBreaching`（データ欠損時はアラームを発報しない）を使用する。Aurora Serverless v2 の自動一時停止中はメトリクスが発行されないため、`missing` や `breaching` にすると一時停止のたびにアラームが発報される。Step Functions とカスタムメトリクスのアラームも同様に `notBreaching` とする。閾値は初期値であり、実運用の負荷状況に応じて調整する。

## 7. EventBridge Rule 定義

| ルール | イベントソース | フィルタ条件 | アクション |
|---|---|---|---|
| ECS タスク異常終了検知 | ECS Task State Change | `lastStatus=STOPPED` かつ `clusterArn=${EcsClusterArn}` かつ `containers[].exitCode != 0` | SNS Topic に通知 |

```json
{
  "source": ["aws.ecs"],
  "detail-type": ["ECS Task State Change"],
  "detail": {
    "lastStatus": ["STOPPED"],
    "clusterArn": ["${EcsClusterArn}"],
    "containers": {
      "exitCode": [
        {
          "anything-but": 0
        }
      ]
    }
  }
}
```

> **ECS タスク異常終了の監視**: ECS タスクの終了コードは CloudWatch の標準メトリクスとして提供されないため、CloudWatch Alarm では直接監視できない。代わりに EventBridge Rule で ECS Task State Change イベントを捕捉し、SNS Topic に通知する。コンテナ起動前に ECS API レベルで失敗したケースは Step Functions 側の `ExecutionsFailed` アラームで補完する。

## 8. Scheduler DLQ 定義

ImageBatchStack で EventBridge Scheduler 専用の SQS DLQ を作成し、画像生成スケジュールの DeadLetterConfig に設定する。

| 項目 | 値 |
|---|---|
| Queue 名 | `acps-prod-image-scheduler-dlq` |
| 用途 | Scheduler が画像生成 Step Functions を起動できなかったイベントの退避 |
| Message retention | 14 日 |
| 監視 | `AWS/Scheduler` の `InvocationDroppedCount`、`InvocationsSentToDeadLetterCount`、`InvocationsFailedToBeSentToDeadLetterCount` を MonitoringStack で監視 |

DLQ にメッセージが入った場合は、対象 `set_code` と `scheduled_at` を確認し、必要に応じて画像生成 Step Functions を手動実行する。
