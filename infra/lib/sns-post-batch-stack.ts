import * as cdk from 'aws-cdk-lib/core';
import * as codebuild from 'aws-cdk-lib/aws-codebuild';
import * as codepipeline from 'aws-cdk-lib/aws-codepipeline';
import * as codepipelineActions from 'aws-cdk-lib/aws-codepipeline-actions';
import * as ec2 from 'aws-cdk-lib/aws-ec2';
import * as ecs from 'aws-cdk-lib/aws-ecs';
import * as ecr from 'aws-cdk-lib/aws-ecr';
import * as iam from 'aws-cdk-lib/aws-iam';
import * as logs from 'aws-cdk-lib/aws-logs';
import * as rds from 'aws-cdk-lib/aws-rds';
import * as s3 from 'aws-cdk-lib/aws-s3';
import * as sfn from 'aws-cdk-lib/aws-stepfunctions';
import * as fs from 'fs';
import * as path from 'path';
import { Construct } from 'constructs';

export interface SnsPostBatchStackProps extends cdk.StackProps {
  /** 環境識別子（例: prod） */
  envName: string;
  /** GitHub 接続の CodeConnections ARN */
  githubConnectionArn: string;
  /** GitHub リポジトリのオーナー */
  githubOwner: string;
  /** GitHub リポジトリ名 */
  githubRepo: string;
  /** CI/CD の対象 GitHub ブランチ */
  githubBranch: string;
  /** SNS 投稿バッチのコンテナイメージ用 ECR リポジトリ */
  snsPostBatchRepository: ecr.Repository;
  /** 生成画像を保存する共有 S3 バケット */
  imagesBucket: s3.Bucket;
  /** Aurora Serverless v2 クラスター */
  auroraCluster: rds.DatabaseCluster;
  /** Public Subnet ID を参照するための VPC */
  vpc: ec2.Vpc;
  /** SNS 投稿バッチを実行する ECS クラスター */
  ecsCluster: ecs.Cluster;
  /** SNS 投稿バッチ ECS タスク用の Security Group */
  batchSecurityGroup: ec2.SecurityGroup;
  /** DB 準備確認 ECS タスク用の Security Group */
  dbReadinessCheckSecurityGroup: ec2.SecurityGroup;
  /** DB 準備確認タスク定義 */
  dbReadinessCheckTaskDefinition: ecs.FargateTaskDefinition;
}

/**
 * SNS 投稿バッチ実行基盤スタック。
 * リソースは docs/infra/stacks.html セクション 3.3 に沿って段階的に追加する。
 */
export class SnsPostBatchStack extends cdk.Stack {
  /** SNS 投稿バッチのタスク定義。Step Functions から family 名で参照される */
  public readonly taskDefinition: ecs.FargateTaskDefinition;
  /** SNS 投稿ワークフロー。Phase 5 で ImageBatchStack が ARN を、Phase 7 で MonitoringStack が参照する */
  public readonly stateMachine: sfn.StateMachine;

  constructor(scope: Construct, id: string, props: SnsPostBatchStackProps) {
    super(scope, id, props);

    const contextImageTag = this.node.tryGetContext('snsPostBatchImageTag');
    const hasSnsPostBatchImageTag =
      typeof contextImageTag === 'string' && contextImageTag.trim().length > 0;
    const snsPostBatchImageTag =
      hasSnsPostBatchImageTag ? contextImageTag.trim() : 'MISSING';

    if (!hasSnsPostBatchImageTag) {
      // CDK はデプロイ対象外のスタックも synth するため、throw すると他スタックのデプロイも失敗する。
      cdk.Annotations.of(this).addError(
        '-c snsPostBatchImageTag=<tag> の指定が必要です。',
      );
    }

    const taskRole = new iam.Role(this, 'SnsPostBatchTaskRole', {
      assumedBy: new iam.ServicePrincipal('ecs-tasks.amazonaws.com'),
      inlinePolicies: {
        ReadSecrets: new iam.PolicyDocument({
          statements: [
            new iam.PolicyStatement({
              actions: ['secretsmanager:GetSecretValue'],
              resources: [
                `arn:aws:secretsmanager:${this.region}:${this.account}:secret:acps/${props.envName}/db/*`,
                `arn:aws:secretsmanager:${this.region}:${this.account}:secret:acps/${props.envName}/*/sns/*`,
              ],
            }),
          ],
        }),
      },
    });

    props.imagesBucket.grantRead(taskRole);

    const logGroup = new logs.LogGroup(this, 'SnsPostBatchLogGroup', {
      retention: logs.RetentionDays.THREE_MONTHS,
      removalPolicy: cdk.RemovalPolicy.DESTROY,
    });

    const dbSecretArn = props.auroraCluster.secret?.secretArn;
    if (!dbSecretArn) {
      throw new Error('Aurora クラスターの認証情報 Secret が見つかりません。');
    }

    this.taskDefinition = new ecs.FargateTaskDefinition(
      this,
      'SnsPostBatchTaskDefinition',
      {
        family: `acps-${props.envName}-sns-post-batch`,
        cpu: 256,
        memoryLimitMiB: 512,
        taskRole,
      },
    );

    this.taskDefinition.addContainer('SnsPostBatchContainer', {
      containerName: 'sns-post-batch',
      image: ecs.ContainerImage.fromEcrRepository(
        props.snsPostBatchRepository,
        snsPostBatchImageTag,
      ),
      environment: {
        DB_SECRET_ARN: dbSecretArn,
        S3_BUCKET_NAME: props.imagesBucket.bucketName,
        ENV_NAME: props.envName,
      },
      logging: ecs.LogDrivers.awsLogs({
        logGroup,
        streamPrefix: 'sns-post-batch',
      }),
    });

    // ECR イメージ + awslogs を使う両タスク定義には CDK がタスク実行ロールを自動生成している前提
    const dbReadinessCheckExecutionRole =
      props.dbReadinessCheckTaskDefinition.executionRole;
    const snsPostBatchExecutionRole = this.taskDefinition.executionRole;
    if (!dbReadinessCheckExecutionRole || !snsPostBatchExecutionRole) {
      throw new Error('ECS タスク定義のタスク実行ロールが見つかりません。');
    }

    const buildLogGroup = new logs.LogGroup(this, 'SnsPostBatchBuildLogGroup', {
      retention: logs.RetentionDays.THREE_MONTHS,
      removalPolicy: cdk.RemovalPolicy.DESTROY,
    });

    const buildProject = new codebuild.PipelineProject(this, 'SnsPostBatchBuild', {
      projectName: `acps-${props.envName}-sns-post-batch-build`,
      buildSpec: codebuild.BuildSpec.fromSourceFilename(
        'services/sns-post-batch/buildspec.yml',
      ),
      environment: {
        buildImage: codebuild.LinuxBuildImage.STANDARD_7_0,
        privileged: true,
        computeType: codebuild.ComputeType.SMALL,
      },
      environmentVariables: {
        ECR_REPO_URI: { value: props.snsPostBatchRepository.repositoryUri },
        TASK_DEF_FAMILY: { value: this.taskDefinition.family },
        CONTAINER_NAME: { value: 'sns-post-batch' },
      },
      logging: {
        cloudWatch: { logGroup: buildLogGroup },
      },
    });

    props.snsPostBatchRepository.grantPullPush(buildProject);
    buildProject.addToRolePolicy(
      new iam.PolicyStatement({
        actions: ['ecs:DescribeTaskDefinition', 'ecs:RegisterTaskDefinition'],
        resources: ['*'],
      }),
    );
    buildProject.addToRolePolicy(
      new iam.PolicyStatement({
        actions: ['iam:PassRole'],
        resources: [
          this.taskDefinition.taskRole.roleArn,
          snsPostBatchExecutionRole.roleArn,
        ],
        conditions: {
          StringEquals: {
            'iam:PassedToService': 'ecs-tasks.amazonaws.com',
          },
        },
      }),
    );

    // アクションロールはサービスではなくパイプラインロールが sts:AssumeRole するため、
    // アカウント root を信頼する（CDK 自動生成のアクションロールと同じ構造）
    const sourceActionRole = new iam.Role(this, 'SnsPostBatchSourceActionRole', {
      assumedBy: new iam.AccountRootPrincipal(),
    });
    sourceActionRole.addToPolicy(
      new iam.PolicyStatement({
        actions: ['codeconnections:UseConnection'],
        resources: [props.githubConnectionArn],
      }),
    );

    const sourceOutput = new codepipeline.Artifact();
    const sourceAction = new codepipelineActions.CodeStarConnectionsSourceAction({
      actionName: 'Source',
      connectionArn: props.githubConnectionArn,
      owner: props.githubOwner,
      repo: props.githubRepo,
      branch: props.githubBranch,
      output: sourceOutput,
      role: sourceActionRole,
      triggerOnPush: false,
    });

    new codepipeline.Pipeline(this, 'SnsPostBatchPipeline', {
      pipelineName: `acps-${props.envName}-sns-post-batch-pipeline`,
      pipelineType: codepipeline.PipelineType.V2,
      crossAccountKeys: false,
      stages: [
        {
          stageName: 'Source',
          actions: [sourceAction],
        },
        {
          stageName: 'Build',
          actions: [
            new codepipelineActions.CodeBuildAction({
              actionName: 'Build',
              project: buildProject,
              input: sourceOutput,
            }),
          ],
        },
      ],
      triggers: [
        {
          providerType: codepipeline.ProviderType.CODE_STAR_SOURCE_CONNECTION,
          gitConfiguration: {
            sourceAction,
            pushFilter: [
              {
                branchesIncludes: [props.githubBranch],
                filePathsIncludes: ['services/sns-post-batch/**', 'shared/**'],
              },
            ],
          },
        },
      ],
    });

    this.stateMachine = new sfn.StateMachine(this, 'SnsPostingStateMachine', {
      stateMachineName: `acps-${props.envName}-sns-posting-sfn`,
      definitionBody: sfn.DefinitionBody.fromString(
        fs.readFileSync(
          path.join(__dirname, 'asl', 'sns-posting.asl.json'),
          'utf-8',
        ),
      ),
      definitionSubstitutions: {
        EcsClusterArn: props.ecsCluster.clusterArn,
        DbReadinessCheckTaskDefFamily:
          props.dbReadinessCheckTaskDefinition.family,
        SnsPostBatchTaskDefFamily: this.taskDefinition.family,
        PublicSubnetId1: props.vpc.publicSubnets[0].subnetId,
        PublicSubnetId2: props.vpc.publicSubnets[1].subnetId,
        DbReadinessCheckSgId:
          props.dbReadinessCheckSecurityGroup.securityGroupId,
        BatchSgId: props.batchSecurityGroup.securityGroupId,
      },
    });

    this.stateMachine.addToRolePolicy(
      new iam.PolicyStatement({
        actions: ['ecs:RunTask'],
        resources: [
          `arn:aws:ecs:${this.region}:${this.account}:task-definition/${props.dbReadinessCheckTaskDefinition.family}:*`,
          `arn:aws:ecs:${this.region}:${this.account}:task-definition/${this.taskDefinition.family}:*`,
        ],
      }),
    );
    this.stateMachine.addToRolePolicy(
      new iam.PolicyStatement({
        actions: ['ecs:StopTask', 'ecs:DescribeTasks'],
        resources: ['*'],
      }),
    );
    this.stateMachine.addToRolePolicy(
      new iam.PolicyStatement({
        actions: ['events:PutTargets', 'events:PutRule', 'events:DescribeRule'],
        resources: [
          `arn:aws:events:${this.region}:${this.account}:rule/StepFunctionsGetEventsForECSTaskRule`,
        ],
      }),
    );
    this.stateMachine.addToRolePolicy(
      new iam.PolicyStatement({
        actions: ['iam:PassRole'],
        resources: [
          props.dbReadinessCheckTaskDefinition.taskRole.roleArn,
          dbReadinessCheckExecutionRole.roleArn,
          this.taskDefinition.taskRole.roleArn,
          snsPostBatchExecutionRole.roleArn,
        ],
        conditions: {
          StringEquals: {
            'iam:PassedToService': 'ecs-tasks.amazonaws.com',
          },
        },
      }),
    );
  }
}
