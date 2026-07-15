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

describe('SnsPostBatchStack の CI/CD パイプライン', () => {
  const stack = createSnsPostBatchStack();
  const template = Template.fromStack(stack);

  test('V2 パイプラインに対象ブランチとファイルパスのトリガーを設定する', () => {
    template.hasResourceProperties('AWS::CodePipeline::Pipeline', {
      Name: 'acps-prod-sns-post-batch-pipeline',
      PipelineType: 'V2',
      Triggers: [
        {
          ProviderType: 'CodeStarSourceConnection',
          GitConfiguration: {
            Push: [
              {
                Branches: { Includes: ['main'] },
                FilePaths: {
                  Includes: ['services/sns-post-batch/**', 'shared/**'],
                },
              },
            ],
          },
        },
      ],
    });
  });

  test('Docker ビルド可能な CodeBuild プロジェクトで buildspec を参照する', () => {
    template.hasResourceProperties('AWS::CodeBuild::Project', {
      Name: 'acps-prod-sns-post-batch-build',
      Source: {
        BuildSpec: 'services/sns-post-batch/buildspec.yml',
      },
      Environment: Match.objectLike({
        PrivilegedMode: true,
        ComputeType: 'BUILD_GENERAL1_SMALL',
      }),
    });
  });

  test('CodeBuild ロールにタスク定義登録と ECS タスクロールの PassRole を許可する', () => {
    const policies = Object.values(template.findResources('AWS::IAM::Policy')) as any[];
    const buildPolicy = policies.find((policy) =>
      policy.Properties.PolicyDocument.Statement.some((statement: any) =>
        statement.Action?.includes('ecs:RegisterTaskDefinition'),
      ),
    );

    expect(buildPolicy.Properties.PolicyDocument.Statement).toEqual(
      expect.arrayContaining([
        expect.objectContaining({
          Action: expect.arrayContaining(['ecs:RegisterTaskDefinition']),
          Resource: '*',
        }),
        expect.objectContaining({
          Action: 'iam:PassRole',
          Condition: {
            StringEquals: {
              'iam:PassedToService': 'ecs-tasks.amazonaws.com',
            },
          },
        }),
      ]),
    );
  });

  test('新形式 CodeConnections ARN の UseConnection をソースアクションロールに許可する', () => {
    const policies = Object.values(template.findResources('AWS::IAM::Policy')) as any[];

    expect(policies).toEqual(
      expect.arrayContaining([
        expect.objectContaining({
          Properties: expect.objectContaining({
            PolicyDocument: expect.objectContaining({
              Statement: expect.arrayContaining([
                expect.objectContaining({
                  Action: 'codeconnections:UseConnection',
                  Resource:
                    'arn:aws:codeconnections:ap-northeast-1:516964473143:connection/b671e788-6378-4296-89d9-bfe3a55e4be7',
                }),
              ]),
            }),
          }),
        }),
      ]),
    );
  });
});

describe('SnsPostBatchStack の SNS 投稿ワークフロー', () => {
  const stack = createSnsPostBatchStack();
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
          StateMachineName: 'acps-prod-sns-posting-sfn',
        }),
      }),
    );
  });

  test('ASL の置換値をすべて設定する', () => {
    expect(stateMachine.Properties.DefinitionSubstitutions).toEqual(
      expect.objectContaining({
        EcsClusterArn: expect.anything(),
        DbReadinessCheckTaskDefFamily: expect.anything(),
        SnsPostBatchTaskDefFamily: expect.anything(),
        PublicSubnetId1: expect.anything(),
        PublicSubnetId2: expect.anything(),
        DbReadinessCheckSgId: expect.anything(),
        BatchSgId: expect.anything(),
      }),
    );
  });

  test('DB 準備確認と SNS 投稿タスクを実行する ASL をインラインで保持する', () => {
    const definitionString = stateMachine.Properties.DefinitionString as string;

    expect(definitionString).toContain('WaitForDbReady');
    expect(definitionString).toContain('RunSnsPostBatchTask');
    expect(definitionString).toContain('HandleError');
    expect(definitionString).toContain('ecs:runTask.sync');
    expect(definitionString).toContain('ContainerOverrides');
    expect(definitionString).toContain('SET_CODE');
    expect(definitionString).toContain('EXECUTION_ARN');
  });

  test('ECS 同期実行に必要な最小権限をステートマシンロールに付与する', () => {
    const policies = Object.values(
      template.findResources('AWS::IAM::Policy'),
    ) as any[];
    const stateMachinePolicy = policies.find((policy) =>
      policy.Properties.PolicyDocument.Statement.some((statement: any) =>
        statement.Action?.includes('ecs:RunTask'),
      ),
    );
    const statements = stateMachinePolicy.Properties.PolicyDocument.Statement;

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
                  ':task-definition/acps-prod-sns-post-batch:*',
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
      ]),
    );

    const passRoleStatement = statements.find(
      (statement: any) => statement.Action === 'iam:PassRole',
    );
    expect(passRoleStatement.Resource).toHaveLength(4);
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

    Annotations.fromStack(stack).hasError(
      '*',
      Match.stringLikeRegexp('.*-c snsPostBatchImageTag=<tag> の指定が必要.*'),
    );
  });
});
