import * as cdk from 'aws-cdk-lib/core';
import { Match, Template } from 'aws-cdk-lib/assertions';
import { FoundationStack } from '../lib/foundation-stack';
import { ImageBatchStack } from '../lib/image-batch-stack';
import { MonitoringStack } from '../lib/monitoring-stack';
import { SnsPostBatchStack } from '../lib/sns-post-batch-stack';

const createMonitoringStack = (): MonitoringStack => {
  const app = new cdk.App({
    context: {
      dbReadinessCheckImageTag: 'test-tag',
      imageBatchImageTag: 'test-image-tag',
      snsPostBatchImageTag: 'test-sns-tag',
    },
  });
  const foundationStack = new FoundationStack(app, 'FoundationStack', {
    envName: 'prod',
  });
  const snsPostBatchStack = new SnsPostBatchStack(app, 'SnsPostBatchStack', {
    envName: 'prod',
    githubConnectionArn:
      'arn:aws:codeconnections:ap-northeast-1:516964473143:connection/b671e788-6378-4296-89d9-bfe3a55e4be7',
    githubOwner: 'takegaharasoshi',
    githubRepo: 'AutoContentPublisherSystem',
    githubBranch: 'main',
    snsPostBatchRepository: foundationStack.snsPostBatchRepository,
    imagesBucket: foundationStack.imagesBucket,
    auroraCluster: foundationStack.auroraCluster,
    vpc: foundationStack.vpc,
    ecsCluster: foundationStack.ecsCluster,
    batchSecurityGroup: foundationStack.batchSecurityGroup,
    dbReadinessCheckSecurityGroup: foundationStack.dbReadinessCheckSecurityGroup,
    dbReadinessCheckTaskDefinition: foundationStack.dbReadinessCheckTaskDefinition,
  });
  const imageBatchStack = new ImageBatchStack(app, 'ImageBatchStack', {
    envName: 'prod',
    githubConnectionArn:
      'arn:aws:codeconnections:ap-northeast-1:516964473143:connection/b671e788-6378-4296-89d9-bfe3a55e4be7',
    githubOwner: 'takegaharasoshi',
    githubRepo: 'AutoContentPublisherSystem',
    githubBranch: 'main',
    imageBatchRepository: foundationStack.imageBatchRepository,
    imagesBucket: foundationStack.imagesBucket,
    auroraCluster: foundationStack.auroraCluster,
    imageApiKeySecret: foundationStack.imageApiKeySecret,
    vpc: foundationStack.vpc,
    ecsCluster: foundationStack.ecsCluster,
    batchSecurityGroup: foundationStack.batchSecurityGroup,
    dbReadinessCheckSecurityGroup: foundationStack.dbReadinessCheckSecurityGroup,
    dbReadinessCheckTaskDefinition: foundationStack.dbReadinessCheckTaskDefinition,
    snsPostingStateMachine: snsPostBatchStack.stateMachine,
  });

  return new MonitoringStack(app, 'MonitoringStack', {
    envName: 'prod',
    auroraCluster: foundationStack.auroraCluster,
    ecsCluster: foundationStack.ecsCluster,
    imageGenerationStateMachine: imageBatchStack.stateMachine,
    snsPostingStateMachine: snsPostBatchStack.stateMachine,
    imageScheduleGroup: imageBatchStack.scheduleGroup,
  });
};

describe('MonitoringStack', () => {
  const stack = createMonitoringStack();
  const template = Template.fromStack(stack);

  test('アラーム通知用 SNS Topic を作成する', () => {
    template.hasResourceProperties('AWS::SNS::Topic', {
      TopicName: 'acps-prod-alarm-topic',
    });
  });

  test('CloudWatch Alarm を 11 個作成する', () => {
    template.resourceCountIs('AWS::CloudWatch::Alarm', 11);
  });

  test('画像生成 Step Functions の失敗を監視する', () => {
    template.hasResourceProperties('AWS::CloudWatch::Alarm', {
      AlarmName: 'acps-prod-image-generation-sfn-failed',
      Namespace: 'AWS/States',
      MetricName: 'ExecutionsFailed',
      Threshold: 1,
      TreatMissingData: 'notBreaching',
      AlarmActions: [{ Ref: Match.stringLikeRegexp('AlarmTopic') }],
    });
  });

  test('Aurora の CPU 使用率と空きメモリを監視する', () => {
    template.hasResourceProperties('AWS::CloudWatch::Alarm', {
      AlarmName: 'acps-prod-aurora-cpu-high',
      EvaluationPeriods: 3,
      DatapointsToAlarm: 3,
      Threshold: 80,
    });
    template.hasResourceProperties('AWS::CloudWatch::Alarm', {
      AlarmName: 'acps-prod-aurora-memory-low',
      ComparisonOperator: 'LessThanOrEqualToThreshold',
      DatapointsToAlarm: 3,
    });
  });

  test('Scheduler の 6 種類の異常を監視する', () => {
    for (const metricName of [
      'TargetErrorCount',
      'TargetErrorThrottledCount',
      'InvocationThrottleCount',
      'InvocationDroppedCount',
      'InvocationsSentToDeadLetterCount',
      'InvocationsFailedToBeSentToDeadLetterCount',
    ]) {
      template.hasResourceProperties('AWS::CloudWatch::Alarm', {
        Namespace: 'AWS/Scheduler',
        MetricName: metricName,
      });
    }
  });

  test('異常終了した ECS タスクを SNS Topic に通知する', () => {
    template.hasResourceProperties('AWS::Events::Rule', {
      Name: 'acps-prod-ecs-task-abnormal-exit',
      EventPattern: {
        source: ['aws.ecs'],
        'detail-type': ['ECS Task State Change'],
        detail: {
          lastStatus: ['STOPPED'],
          clusterArn: [Match.anyValue()],
          containers: {
            exitCode: [{ 'anything-but': [0] }],
          },
        },
      },
      Targets: [
        Match.objectLike({
          Arn: { Ref: Match.stringLikeRegexp('AlarmTopic') },
        }),
      ],
    });
  });
});
