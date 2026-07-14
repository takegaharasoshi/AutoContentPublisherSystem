import * as cdk from 'aws-cdk-lib/core';
import { Annotations, Match, Template } from 'aws-cdk-lib/assertions';
import { FoundationStack } from '../lib/foundation-stack';
import { ImageBatchStack } from '../lib/image-batch-stack';
import { SnsPostBatchStack } from '../lib/sns-post-batch-stack';

const createImageBatchStack = (): ImageBatchStack => {
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
    snsPostBatchRepository: foundationStack.snsPostBatchRepository,
    imagesBucket: foundationStack.imagesBucket,
    auroraCluster: foundationStack.auroraCluster,
    vpc: foundationStack.vpc,
    ecsCluster: foundationStack.ecsCluster,
    batchSecurityGroup: foundationStack.batchSecurityGroup,
    dbReadinessCheckSecurityGroup: foundationStack.dbReadinessCheckSecurityGroup,
    dbReadinessCheckTaskDefinition: foundationStack.dbReadinessCheckTaskDefinition,
  });

  return new ImageBatchStack(app, 'ImageBatchStack', {
    envName: 'prod',
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
};

describe('ImageBatchStack の ECS タスク定義', () => {
  const stack = createImageBatchStack();
  const template = Template.fromStack(stack);

  test('Fargate の family・CPU・メモリが設定される', () => {
    template.hasResourceProperties('AWS::ECS::TaskDefinition', {
      Family: 'acps-prod-image-batch',
      Cpu: '256',
      Memory: '512',
      RequiresCompatibilities: ['FARGATE'],
    });
  });

  test('環境変数と awslogs 設定を持つコンテナが作成される', () => {
    template.hasResourceProperties('AWS::ECS::TaskDefinition', {
      ContainerDefinitions: [
        Match.objectLike({
          Name: 'image-batch',
          Environment: Match.arrayWith([
            Match.objectLike({ Name: 'DB_SECRET_ARN' }),
            Match.objectLike({ Name: 'API_SECRET_ARN' }),
            Match.objectLike({ Name: 'S3_BUCKET_NAME' }),
            { Name: 'ENV_NAME', Value: 'prod' },
          ]),
          Image: {
            'Fn::Join': ['', Match.arrayWith([':test-image-tag'])],
          },
          LogConfiguration: {
            LogDriver: 'awslogs',
            Options: Match.objectLike({
              'awslogs-stream-prefix': 'image-batch',
            }),
          },
        }),
      ],
    });
  });
});

describe('ImageBatchStack のタスクロール', () => {
  const stack = createImageBatchStack();
  const template = Template.fromStack(stack);

  test('DB と画像 API の Secret 読み取り、S3 読み書きを許可する', () => {
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
                          expect.arrayContaining([':secret:acps/prod/image/*']),
                        ],
                      },
                    ],
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
                expect.objectContaining({
                  Action: expect.arrayContaining(['s3:PutObject']),
                }),
              ]),
            }),
          }),
        }),
      ]),
    );
  });

  test('カスタムメトリクス発行権限を持たない', () => {
    const roles = Object.values(template.findResources('AWS::IAM::Role')) as any[];
    const taskRole = roles.find((role) =>
      role.Properties.Policies?.some(
        (policy: any) => policy.PolicyName === 'ReadSecrets',
      ),
    );
    const policies = taskRole.Properties.Policies as any[];

    expect(policies).not.toEqual(
      expect.arrayContaining([
        expect.objectContaining({ PolicyName: 'PutAcpsMetrics' }),
      ]),
    );
  });
});

describe('ImageBatchStack のロググループ', () => {
  const stack = createImageBatchStack();
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

describe('ImageBatchStack の画像生成ワークフロー', () => {
  const stack = createImageBatchStack();
  const template = Template.fromStack(stack);
  const stateMachines = Object.values(
    template.findResources('AWS::StepFunctions::StateMachine'),
  ) as any[];
  const stateMachine = stateMachines[0];

  test('明示した名前の Standard ステートマシンを作成する', () => {
    expect(stateMachines).toHaveLength(1);
    expect(stateMachine).toEqual(
      expect.objectContaining({
        Properties: expect.objectContaining({
          StateMachineName: 'acps-prod-image-generation-sfn',
        }),
      }),
    );
  });

  test('ASL の置換値をすべて設定する', () => {
    expect(stateMachine.Properties.DefinitionSubstitutions).toEqual(
      expect.objectContaining({
        EcsClusterArn: expect.anything(),
        DbReadinessCheckTaskDefFamily: expect.anything(),
        ImageBatchTaskDefFamily: expect.anything(),
        PublicSubnetId1: expect.anything(),
        PublicSubnetId2: expect.anything(),
        DbReadinessCheckSgId: expect.anything(),
        BatchSgId: expect.anything(),
        SnsPostingSfnArn: expect.anything(),
        ImageGenerationSfnName: 'acps-prod-image-generation-sfn',
      }),
    );
  });

  test('DB 準備確認、画像生成、SNS 投稿起動を行う ASL をインラインで保持する', () => {
    const definitionString = stateMachine.Properties.DefinitionString as string;

    expect(definitionString).toContain('WaitForDbReady');
    expect(definitionString).toContain('RunImageBatchTask');
    expect(definitionString).toContain('StartSnsPostBatch');
    expect(definitionString).toContain('SnsPostAlreadyStarted');
    expect(definitionString).toContain('NotifySnsPostStartFailure');
    expect(definitionString).toContain('ImageBatchSucceeded');
    expect(definitionString).toContain('HandleError');
    expect(definitionString).toContain('ecs:runTask.sync');
    expect(definitionString).toContain('ContainerOverrides');
    expect(definitionString).toContain('SET_CODE');
    expect(definitionString).toContain('EXECUTION_ARN');
    expect(definitionString).toContain('SCHEDULED_AT');
    expect(definitionString).toContain('states:startExecution');
    expect(definitionString).toContain('cloudwatch:putMetricData');
  });

  test('ECS 実行、SNS 投稿起動、カスタムメトリクス発行の最小権限をステートマシンロールに付与する', () => {
    const policies = Object.values(
      template.findResources('AWS::IAM::Policy'),
    ) as any[];
    const stateMachinePolicy = policies.find((policy) =>
      policy.Properties.PolicyDocument.Statement.some((statement: any) =>
        statement.Action?.includes('states:StartExecution'),
      ),
    );
    const statements = stateMachinePolicy.Properties.PolicyDocument.Statement;
    const snsPostingSfnArn =
      stateMachine.Properties.DefinitionSubstitutions.SnsPostingSfnArn;

    expect(statements).toEqual(
      expect.arrayContaining([
        expect.objectContaining({
          Action: 'ecs:RunTask',
          Resource: expect.arrayContaining([
            expect.objectContaining({
              'Fn::Join': [
                '',
                expect.arrayContaining([
                  ':task-definition/acps-prod-db-readiness-check:*',
                ]),
              ],
            }),
            expect.objectContaining({
              'Fn::Join': [
                '',
                expect.arrayContaining([
                  ':task-definition/acps-prod-image-batch:*',
                ]),
              ],
            }),
          ]),
        }),
        expect.objectContaining({
          Action: expect.arrayContaining([
            'ecs:StopTask',
            'ecs:DescribeTasks',
          ]),
          Resource: '*',
        }),
        expect.objectContaining({
          Action: expect.arrayContaining([
            'events:DescribeRule',
            'events:PutRule',
            'events:PutTargets',
          ]),
          Resource: expect.objectContaining({
            'Fn::Join': [
              '',
              expect.arrayContaining([
                ':rule/StepFunctionsGetEventsForECSTaskRule',
              ]),
            ],
          }),
        }),
        expect.objectContaining({
          Action: 'iam:PassRole',
          Resource: expect.arrayContaining([
            expect.anything(),
            expect.anything(),
            expect.anything(),
            expect.anything(),
          ]),
          Condition: {
            StringEquals: {
              'iam:PassedToService': 'ecs-tasks.amazonaws.com',
            },
          },
        }),
        expect.objectContaining({
          Action: 'states:StartExecution',
          Resource: expect.objectContaining({
            'Fn::ImportValue': expect.anything(),
          }),
        }),
        expect.objectContaining({
          Action: 'cloudwatch:PutMetricData',
          Resource: '*',
          Condition: {
            StringEquals: { 'cloudwatch:namespace': 'ACPS' },
          },
        }),
      ]),
    );

    expect(statements).toHaveLength(6);
    const passRoleStatement = statements.find(
      (statement: any) => statement.Action === 'iam:PassRole',
    );
    expect(passRoleStatement.Resource).toHaveLength(4);
    const startExecutionStatement = statements.find(
      (statement: any) => statement.Action === 'states:StartExecution',
    );
    expect(startExecutionStatement.Resource).toEqual(snsPostingSfnArn);
  });
});

describe('ImageBatchStack の画像生成バッチイメージタグ Context', () => {
  test('未指定時はエラーアノテーションを追加する', () => {
    const app = new cdk.App({
      context: {
        dbReadinessCheckImageTag: 'test-tag',
        snsPostBatchImageTag: 'test-sns-tag',
      },
    });
    const foundationStack = new FoundationStack(app, 'FoundationStack', {
      envName: 'prod',
    });
    const snsPostBatchStack = new SnsPostBatchStack(app, 'SnsPostBatchStack', {
      envName: 'prod',
      snsPostBatchRepository: foundationStack.snsPostBatchRepository,
      imagesBucket: foundationStack.imagesBucket,
      auroraCluster: foundationStack.auroraCluster,
      vpc: foundationStack.vpc,
      ecsCluster: foundationStack.ecsCluster,
      batchSecurityGroup: foundationStack.batchSecurityGroup,
      dbReadinessCheckSecurityGroup: foundationStack.dbReadinessCheckSecurityGroup,
      dbReadinessCheckTaskDefinition: foundationStack.dbReadinessCheckTaskDefinition,
    });
    const stack = new ImageBatchStack(app, 'ImageBatchStack', {
      envName: 'prod',
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

    Annotations.fromStack(stack).hasError(
      '*',
      Match.stringLikeRegexp('.*-c imageBatchImageTag=<tag> の指定が必要.*'),
    );
  });
});
