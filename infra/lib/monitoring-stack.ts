import * as cdk from 'aws-cdk-lib/core';
import * as cloudwatch from 'aws-cdk-lib/aws-cloudwatch';
import * as cloudwatchActions from 'aws-cdk-lib/aws-cloudwatch-actions';
import * as ecs from 'aws-cdk-lib/aws-ecs';
import * as events from 'aws-cdk-lib/aws-events';
import * as eventsTargets from 'aws-cdk-lib/aws-events-targets';
import * as rds from 'aws-cdk-lib/aws-rds';
import * as scheduler from 'aws-cdk-lib/aws-scheduler';
import * as sfn from 'aws-cdk-lib/aws-stepfunctions';
import * as sns from 'aws-cdk-lib/aws-sns';
import { Construct } from 'constructs';

export interface MonitoringStackProps extends cdk.StackProps {
  /** 環境識別子（例: prod） */
  envName: string;
  /** Aurora メトリクスの監視対象クラスター */
  auroraCluster: rds.DatabaseCluster;
  /** ECS タスク異常終了イベントの clusterArn フィルタ用クラスター */
  ecsCluster: ecs.Cluster;
  /** 画像生成ワークフロー */
  imageGenerationStateMachine: sfn.StateMachine;
  /** SNS 投稿ワークフロー */
  snsPostingStateMachine: sfn.StateMachine;
  /** AWS/Scheduler メトリクスの Dimension に使用する ScheduleGroup */
  imageScheduleGroup: scheduler.ScheduleGroup;
}

/**
 * 運用監視スタック。
 * リソースは docs/infra/stacks.html の監視設計に沿って定義する。
 */
export class MonitoringStack extends cdk.Stack {
  /** CloudWatch Alarm と ECS タスク異常終了通知の送信先 SNS Topic */
  public readonly alarmTopic: sns.Topic;

  constructor(scope: Construct, id: string, props: MonitoringStackProps) {
    super(scope, id, props);

    this.alarmTopic = new sns.Topic(this, 'AlarmTopic', {
      topicName: `acps-${props.envName}-alarm-topic`,
    });

    const createAlarm = (
      id: string,
      alarmName: string,
      metric: cloudwatch.IMetric,
      threshold: number,
      comparisonOperator: cloudwatch.ComparisonOperator,
      evaluationPeriods: number,
      datapointsToAlarm: number,
      alarmDescription: string,
    ): cloudwatch.Alarm => {
      const alarm = new cloudwatch.Alarm(this, id, {
        alarmName,
        metric,
        threshold,
        comparisonOperator,
        evaluationPeriods,
        datapointsToAlarm,
        treatMissingData: cloudwatch.TreatMissingData.NOT_BREACHING,
        alarmDescription,
      });
      alarm.addAlarmAction(new cloudwatchActions.SnsAction(this.alarmTopic));
      return alarm;
    };

    createAlarm(
      'ImageGenerationSfnFailedAlarm',
      `acps-${props.envName}-image-generation-sfn-failed`,
      props.imageGenerationStateMachine.metricFailed({
        statistic: 'Sum',
        period: cdk.Duration.minutes(5),
      }),
      1,
      cloudwatch.ComparisonOperator.GREATER_THAN_OR_EQUAL_TO_THRESHOLD,
      1,
      1,
      '画像生成 Step Functions の実行失敗を検知。CloudWatch Logs で原因を確認し、必要に応じて手動再実行する',
    );

    createAlarm(
      'SnsPostingSfnFailedAlarm',
      `acps-${props.envName}-sns-posting-sfn-failed`,
      props.snsPostingStateMachine.metricFailed({
        statistic: 'Sum',
        period: cdk.Duration.minutes(5),
      }),
      1,
      cloudwatch.ComparisonOperator.GREATER_THAN_OR_EQUAL_TO_THRESHOLD,
      1,
      1,
      'SNS 投稿 Step Functions の実行失敗を検知。CloudWatch Logs で原因を確認し、必要に応じて手動再実行する',
    );

    createAlarm(
      'SnsPostStartFailureAlarm',
      `acps-${props.envName}-sns-post-start-failure`,
      new cloudwatch.Metric({
        namespace: 'ACPS',
        metricName: 'SnsPostStartFailureCount',
        dimensionsMap: {
          StateMachineName: props.imageGenerationStateMachine.stateMachineName,
        },
        statistic: 'Sum',
        period: cdk.Duration.minutes(5),
      }),
      1,
      cloudwatch.ComparisonOperator.GREATER_THAN_OR_EQUAL_TO_THRESHOLD,
      1,
      1,
      'SNS 投稿ワークフローの起動失敗を検知。原因を確認し、手動で SNS 投稿 Step Functions を起動する',
    );

    createAlarm(
      'AuroraCpuHighAlarm',
      `acps-${props.envName}-aurora-cpu-high`,
      props.auroraCluster.metricCPUUtilization({
        statistic: 'Average',
        period: cdk.Duration.minutes(5),
      }),
      80,
      cloudwatch.ComparisonOperator.GREATER_THAN_OR_EQUAL_TO_THRESHOLD,
      3,
      2,
      'Aurora の CPU 使用率高騰を検知。Performance Insights と CloudWatch Logs で負荷要因を確認する',
    );

    createAlarm(
      'AuroraMemoryLowAlarm',
      `acps-${props.envName}-aurora-memory-low`,
      props.auroraCluster.metricFreeableMemory({
        statistic: 'Average',
        period: cdk.Duration.minutes(5),
      }),
      268435456,
      cloudwatch.ComparisonOperator.LESS_THAN_OR_EQUAL_TO_THRESHOLD,
      3,
      2,
      'Aurora の空きメモリ不足を検知。Performance Insights で負荷要因を確認し、必要に応じて容量を見直す',
    );

    const schedulerAlarms = [
      ['TargetErrorCount', 'image-scheduler-target-error'],
      ['TargetErrorThrottledCount', 'image-scheduler-target-error-throttled'],
      ['InvocationThrottleCount', 'image-scheduler-invocation-throttle'],
      ['InvocationDroppedCount', 'image-scheduler-invocation-dropped'],
      ['InvocationsSentToDeadLetterCount', 'image-scheduler-dlq-sent'],
      [
        'InvocationsFailedToBeSentToDeadLetterCount',
        'image-scheduler-dlq-send-failed',
      ],
    ];

    for (const [metricName, alarmNameSuffix] of schedulerAlarms) {
      createAlarm(
        `${metricName}Alarm`,
        `acps-${props.envName}-${alarmNameSuffix}`,
        new cloudwatch.Metric({
          namespace: 'AWS/Scheduler',
          metricName,
          dimensionsMap: {
            ScheduleGroup: props.imageScheduleGroup.scheduleGroupName,
          },
          statistic: 'Sum',
          period: cdk.Duration.minutes(5),
        }),
        1,
        cloudwatch.ComparisonOperator.GREATER_THAN_OR_EQUAL_TO_THRESHOLD,
        1,
        1,
        'Scheduler の異常を検知。Scheduler DLQ のメッセージを確認し、対象 set_code と scheduled_at で画像生成 Step Functions を手動実行する',
      );
    }

    new events.Rule(this, 'EcsTaskAbnormalExitRule', {
      ruleName: `acps-${props.envName}-ecs-task-abnormal-exit`,
      eventPattern: {
        source: ['aws.ecs'],
        detailType: ['ECS Task State Change'],
        detail: {
          lastStatus: ['STOPPED'],
          clusterArn: [props.ecsCluster.clusterArn],
          containers: {
            // Match.anythingBut は配列にレンダリングされるため、配列で包むと不正なネスト配列になる
            exitCode: events.Match.anythingBut(0),
          },
        },
      },
      targets: [new eventsTargets.SnsTopic(this.alarmTopic)],
    });
  }
}
