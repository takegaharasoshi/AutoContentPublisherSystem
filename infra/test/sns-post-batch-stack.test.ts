import * as cdk from 'aws-cdk-lib/core';
import { Annotations, Match, Template } from 'aws-cdk-lib/assertions';
import { FoundationStack } from '../lib/foundation-stack';
import { SnsPostBatchStack } from '../lib/sns-post-batch-stack';

const createSnsPostBatchStack = (): SnsPostBatchStack => {
  const app = new cdk.App({
    context: {
      dbReadinessCheckImageTag: 'test-tag',
      snsPostBatchImageTag: 'test-sns-tag',
    },
  });
  const foundationStack = new FoundationStack(app, 'FoundationStack', {
    envName: 'prod',
  });

  return new SnsPostBatchStack(app, 'SnsPostBatchStack', {
    envName: 'prod',
    snsPostBatchRepository: foundationStack.snsPostBatchRepository,
    imagesBucket: foundationStack.imagesBucket,
    auroraCluster: foundationStack.auroraCluster,
  });
};

describe('SnsPostBatchStack の ECS タスク定義', () => {
  const stack = createSnsPostBatchStack();
  const template = Template.fromStack(stack);

  test('Fargate の family・CPU・メモリが設定される', () => {
    template.hasResourceProperties('AWS::ECS::TaskDefinition', {
      Family: 'acps-prod-sns-post-batch',
      Cpu: '256',
      Memory: '512',
      RequiresCompatibilities: ['FARGATE'],
    });
  });

  test('環境変数と awslogs 設定を持つコンテナが作成される', () => {
    template.hasResourceProperties('AWS::ECS::TaskDefinition', {
      ContainerDefinitions: [
        Match.objectLike({
          Name: 'sns-post-batch',
          Environment: Match.arrayWith([
            Match.objectLike({ Name: 'DB_SECRET_ARN' }),
            Match.objectLike({ Name: 'S3_BUCKET_NAME' }),
            { Name: 'ENV_NAME', Value: 'prod' },
          ]),
          Image: {
            'Fn::Join': ['', Match.arrayWith([':test-sns-tag'])],
          },
          LogConfiguration: {
            LogDriver: 'awslogs',
            Options: Match.objectLike({
              'awslogs-stream-prefix': 'sns-post-batch',
            }),
          },
        }),
      ],
    });
  });
});

describe('SnsPostBatchStack のタスクロール', () => {
  const stack = createSnsPostBatchStack();
  const template = Template.fromStack(stack);

  test('DB と SNS の Secret 読み取り、S3 読み取り、カスタムメトリクス発行を許可する', () => {
    const roles = Object.values(template.findResources('AWS::IAM::Role')) as any[];
    const taskRole = roles.find((role) =>
      role.Properties.Policies?.some(
        (policy: any) => policy.PolicyName === 'ReadSecrets',
      ),
    );

    expect(taskRole).toEqual(
      expect.objectContaining({
        Properties: expect.objectContaining({
          AssumeRolePolicyDocument: expect.objectContaining({
            Statement: expect.arrayContaining([
              expect.objectContaining({
                Principal: { Service: 'ecs-tasks.amazonaws.com' },
              }),
            ]),
          }),
          Policies: expect.arrayContaining([
            expect.objectContaining({
              PolicyName: 'ReadSecrets',
              PolicyDocument: expect.objectContaining({
                Statement: expect.arrayContaining([
                  expect.objectContaining({
                    Action: 'secretsmanager:GetSecretValue',
                    Resource: [
                      {
                        'Fn::Join': [
                          '',
                          expect.arrayContaining([':secret:acps/prod/db/*']),
                        ],
                      },
                      {
                        'Fn::Join': [
                          '',
                          expect.arrayContaining([':secret:acps/prod/*/sns/*']),
                        ],
                      },
                    ],
                  }),
                ]),
              }),
            }),
            expect.objectContaining({
              PolicyName: 'PutAcpsMetrics',
              PolicyDocument: expect.objectContaining({
                Statement: expect.arrayContaining([
                  expect.objectContaining({
                    Action: 'cloudwatch:PutMetricData',
                    Resource: '*',
                    Condition: {
                      StringEquals: { 'cloudwatch:namespace': 'ACPS' },
                    },
                  }),
                ]),
              }),
            }),
          ]),
        }),
      }),
    );

    const policies = Object.values(template.findResources('AWS::IAM::Policy')) as any[];
    expect(policies).toEqual(
      expect.arrayContaining([
        expect.objectContaining({
          Properties: expect.objectContaining({
            PolicyDocument: expect.objectContaining({
              Statement: expect.arrayContaining([
                expect.objectContaining({
                  Action: expect.arrayContaining(['s3:GetObject*']),
                }),
              ]),
            }),
          }),
        }),
      ]),
    );
  });
});

describe('SnsPostBatchStack のロググループ', () => {
  const stack = createSnsPostBatchStack();
  const template = Template.fromStack(stack);

  test('90 日で削除される', () => {
    template.hasResource('AWS::Logs::LogGroup', {
      Properties: {
        RetentionInDays: 90,
      },
      DeletionPolicy: 'Delete',
    });
  });
});

describe('SnsPostBatchStack の SNS 投稿バッチイメージタグ Context', () => {
  test('未指定時はエラーアノテーションを追加する', () => {
    const app = new cdk.App({
      context: { dbReadinessCheckImageTag: 'test-tag' },
    });
    const foundationStack = new FoundationStack(app, 'FoundationStack', {
      envName: 'prod',
    });
    const stack = new SnsPostBatchStack(app, 'SnsPostBatchStack', {
      envName: 'prod',
      snsPostBatchRepository: foundationStack.snsPostBatchRepository,
      imagesBucket: foundationStack.imagesBucket,
      auroraCluster: foundationStack.auroraCluster,
    });

    Annotations.fromStack(stack).hasError(
      '*',
      Match.stringLikeRegexp('.*-c snsPostBatchImageTag=<tag> の指定が必要.*'),
    );
  });
});
