import * as cdk from 'aws-cdk-lib/core';
import { Annotations, Match, Template } from 'aws-cdk-lib/assertions';
import { FoundationStack } from '../lib/foundation-stack';
import { InsightsBatchStack } from '../lib/insights-batch-stack';

const createInsightsBatchStack = (
  context: Record<string, string> = {
    dbReadinessCheckImageTag: 'test-tag',
    insightsBatchImageTag: 'test-insights-tag',
  },
): InsightsBatchStack => {
  const app = new cdk.App({ context });
  const foundationStack = new FoundationStack(app, 'FoundationStack', {
    envName: 'prod',
  });
  return new InsightsBatchStack(app, 'InsightsBatchStack', {
    envName: 'prod',
    githubConnectionArn:
      'arn:aws:codeconnections:ap-northeast-1:516964473143:connection/b671e788-6378-4296-89d9-bfe3a55e4be7',
    githubOwner: 'takegaharasoshi',
    githubRepo: 'AutoContentPublisherSystem',
    githubBranch: 'main',
    insightsBatchRepository: foundationStack.insightsBatchRepository,
    auroraCluster: foundationStack.auroraCluster,
    vpc: foundationStack.vpc,
    ecsCluster: foundationStack.ecsCluster,
    batchSecurityGroup: foundationStack.batchSecurityGroup,
    dbReadinessCheckSecurityGroup: foundationStack.dbReadinessCheckSecurityGroup,
    dbReadinessCheckTaskDefinition: foundationStack.dbReadinessCheckTaskDefinition,
    assetsBucket: foundationStack.imagesBucket,
  });
};

describe('InsightsBatchStack', () => {
  const stack = createInsightsBatchStack();
  const template = Template.fromStack(stack);

  test('タスク定義はコメント記録バケットと指定した family・CPU・メモリを持つ', () => {
    const taskDefinitions = Object.values(
      template.findResources('AWS::ECS::TaskDefinition'),
    ) as any[];
    expect(taskDefinitions).toHaveLength(1);
    expect(taskDefinitions[0].Properties).toEqual(
      expect.objectContaining({
        Family: 'acps-prod-insights-batch',
        Cpu: '256',
        Memory: '512',
        ContainerDefinitions: [
          expect.objectContaining({
            Name: 'insights-batch',
            Environment: expect.arrayContaining([
              expect.objectContaining({ Name: 'DB_SECRET_ARN' }),
              { Name: 'ENV_NAME', Value: 'prod' },
              expect.objectContaining({ Name: 'COMMENT_LOG_BUCKET' }),
            ]),
          }),
        ],
      }),
    );
    expect(taskDefinitions[0].Properties.ContainerDefinitions[0].Environment).toHaveLength(3);
    expect(JSON.stringify(taskDefinitions[0])).not.toContain('S3_BUCKET_NAME');
  });

  test('タスクロールはコメント記録の一覧・取得だけを許可する', () => {
    const roles = Object.values(template.findResources('AWS::IAM::Role')) as any[];
    const taskRole = roles.find((role) =>
      JSON.stringify(role.Properties.Policies).includes('s3:GetObject'),
    );
    expect(taskRole).toBeDefined();
    const statements = taskRole.Properties.Policies.flatMap(
      (policy: any) => policy.PolicyDocument.Statement,
    );
    expect(statements).toEqual(
      expect.arrayContaining([
        expect.objectContaining({
          Action: 's3:ListBucket',
          Condition: { StringLike: { 's3:prefix': 'comment-log/*' } },
        }),
        expect.objectContaining({ Action: 's3:GetObject' }),
      ]),
    );
    expect(JSON.stringify(statements)).not.toMatch(/s3:(PutObject|DeleteObject)/);
  });

  test('インサイト収集 State Machine と 4 変数のコンテナオーバーライドを作成する', () => {
    const stateMachine = Object.values(
      template.findResources('AWS::StepFunctions::StateMachine'),
    )[0] as any;
    expect(stateMachine.Properties.StateMachineName).toBe(
      'acps-prod-insights-collection-sfn',
    );
    const definition = stateMachine.Properties.DefinitionString as string;
    expect(definition).toContain('insights-batch');
    for (const name of [
      'SET_CODE',
      'SCHEDULED_AT',
      'MEDIA_LOOKBACK_DAYS',
      'EXECUTION_ARN',
    ]) {
      expect(definition).toContain(name);
    }
  });

  test('3 セットの朝夕用 Scheduler、ScheduleGroup、DLQ を作成する', () => {
    const schedules = Object.values(
      template.findResources('AWS::Scheduler::Schedule'),
    ) as any[];
    expect(schedules).toHaveLength(6);
    for (const [setCode, slot, hour] of [
      // fantasy-animals-1 は Phase 20-1（2026-09-03）の停止でスケジュールごと削除
      ['logic-training-1', 'morning', '6'],
      ['logic-training-1', 'evening', '18'],
      // pref-ranking-1 は 17-5c（2026-08-26）の稼働開始で追加
      ['pref-ranking-1', 'morning', '6'],
      ['pref-ranking-1', 'evening', '18'],
      // umigame-soup-1 は 21-7 で追加
      ['umigame-soup-1', 'morning', '6'],
      ['umigame-soup-1', 'evening', '18'],
    ]) {
      expect(schedules).toEqual(
        expect.arrayContaining([
          expect.objectContaining({
            Properties: expect.objectContaining({
              Name: `acps-prod-insights-collection-${setCode}-${slot}`,
              ScheduleExpression: `cron(0 ${hour} * * ? *)`,
              Target: expect.objectContaining({
                Input: expect.stringContaining('"media_lookback_days":"14"'),
              }),
            }),
          }),
        ]),
      );
    }
    // 16-11 完了で定常運用へ復帰済み。長期停止する場合は
    // insights-batch-stack.ts の insightsCollectionSchedulesEnabled を false にし、
    // この期待値も DISABLED へ揃えること。
    for (const schedule of schedules) {
      expect(schedule.Properties.State).toBe('ENABLED');
    }
    template.hasResourceProperties('AWS::Scheduler::ScheduleGroup', {
      Name: 'acps-prod-insights-schedule-group',
    });
    template.hasResourceProperties('AWS::SQS::Queue', {
      QueueName: 'acps-prod-insights-scheduler-dlq',
      MessageRetentionPeriod: 1209600,
    });
  });

  test('CodePipeline と CodeBuild にインサイト収集バッチ用の名前・パスフィルタを設定する', () => {
    template.hasResourceProperties('AWS::CodePipeline::Pipeline', {
      Name: 'acps-prod-insights-batch-pipeline',
      Triggers: [
        {
          ProviderType: 'CodeStarSourceConnection',
          GitConfiguration: {
            Push: [
              {
                FilePaths: {
                  Includes: ['services/insights-batch/**', 'shared/**'],
                },
              },
            ],
          },
        },
      ],
    });
    template.hasResourceProperties('AWS::CodeBuild::Project', {
      Name: 'acps-prod-insights-batch-build',
      Source: { BuildSpec: 'services/insights-batch/buildspec.yml' },
    });
  });

  test('イメージタグ未指定時にアノテーションエラーを出す', () => {
    const stackWithoutTag = createInsightsBatchStack({
      dbReadinessCheckImageTag: 'test-tag',
    });
    Annotations.fromStack(stackWithoutTag).hasError(
      '*',
      Match.stringLikeRegexp(
        '.*-c insightsBatchImageTag=<tag> の指定が必要.*',
      ),
    );
  });
});
