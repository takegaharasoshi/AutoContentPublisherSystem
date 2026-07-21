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
import * as scheduler from 'aws-cdk-lib/aws-scheduler';
import * as schedulerTargets from 'aws-cdk-lib/aws-scheduler-targets';
import * as secretsmanager from 'aws-cdk-lib/aws-secretsmanager';
import * as sfn from 'aws-cdk-lib/aws-stepfunctions';
import * as sqs from 'aws-cdk-lib/aws-sqs';
import * as fs from 'fs';
import * as path from 'path';
import { Construct } from 'constructs';

export interface ImageBatchStackProps extends cdk.StackProps {
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
  /** 画像生成バッチのコンテナイメージ用 ECR リポジトリ */
  imageBatchRepository: ecr.Repository;
  /** 生成画像を保存する共有 S3 バケット */
  imagesBucket: s3.Bucket;
  /** Aurora Serverless v2 クラスター */
  auroraCluster: rds.DatabaseCluster;
  /** 画像生成 API キー用の Secret */
  imageApiKeySecret: secretsmanager.Secret;
  /** Public Subnet ID を参照するための VPC */
  vpc: ec2.Vpc;
  /** 画像生成バッチを実行する ECS クラスター */
  ecsCluster: ecs.Cluster;
  /** 画像生成バッチ ECS タスク用の Security Group */
  batchSecurityGroup: ec2.SecurityGroup;
  /** DB 準備確認 ECS タスク用の Security Group */
  dbReadinessCheckSecurityGroup: ec2.SecurityGroup;
  /** DB 準備確認タスク定義 */
  dbReadinessCheckTaskDefinition: ecs.FargateTaskDefinition;
  /** SNS 投稿ワークフロー。ARN を非同期起動先として参照する */
  snsPostingStateMachine: sfn.StateMachine;
}

/**
 * 画像生成バッチ実行基盤スタック。
 * リソースは docs/infra/stacks.html セクション 3.2 に沿って段階的に追加する。
 */
export class ImageBatchStack extends cdk.Stack {
  /** 画像生成バッチのタスク定義。Step Functions から family 名で参照される */
  public readonly taskDefinition: ecs.FargateTaskDefinition;
  /** 画像生成ワークフロー。Phase 5-6 の EventBridge Scheduler と Phase 7 の MonitoringStack が参照する */
  public readonly stateMachine: sfn.StateMachine;
  /** Phase 7 の MonitoringStack が参照する Scheduler 用 DLQ */
  public readonly schedulerDlq: sqs.Queue;
  /** Phase 7 の AWS/Scheduler メトリクス Dimension で参照する ScheduleGroup */
  public readonly scheduleGroup: scheduler.ScheduleGroup;

  constructor(scope: Construct, id: string, props: ImageBatchStackProps) {
    super(scope, id, props);

    const contextImageTag = this.node.tryGetContext('imageBatchImageTag');
    const hasImageBatchImageTag =
      typeof contextImageTag === 'string' && contextImageTag.trim().length > 0;
    const imageBatchImageTag =
      hasImageBatchImageTag ? contextImageTag.trim() : 'MISSING';

    if (!hasImageBatchImageTag) {
      // CDK はデプロイ対象外のスタックも synth するため、throw すると他スタックのデプロイも失敗する。
      cdk.Annotations.of(this).addError(
        '-c imageBatchImageTag=<tag> の指定が必要です。',
      );
    }

    const taskRole = new iam.Role(this, 'ImageBatchTaskRole', {
      assumedBy: new iam.ServicePrincipal('ecs-tasks.amazonaws.com'),
      inlinePolicies: {
        ReadSecrets: new iam.PolicyDocument({
          statements: [
            new iam.PolicyStatement({
              actions: ['secretsmanager:GetSecretValue'],
              resources: [
                `arn:aws:secretsmanager:${this.region}:${this.account}:secret:acps/${props.envName}/db/*`,
                `arn:aws:secretsmanager:${this.region}:${this.account}:secret:acps/${props.envName}/image/*`,
              ],
            }),
          ],
        }),
      },
    });

    props.imagesBucket.grantReadWrite(taskRole);

    const logGroup = new logs.LogGroup(this, 'ImageBatchLogGroup', {
      retention: logs.RetentionDays.THREE_MONTHS,
      removalPolicy: cdk.RemovalPolicy.DESTROY,
    });

    const dbSecretArn = props.auroraCluster.secret?.secretArn;
    if (!dbSecretArn) {
      throw new Error('Aurora クラスターの認証情報 Secret が見つかりません。');
    }

    this.schedulerDlq = new sqs.Queue(this, 'ImageSchedulerDlq', {
      queueName: `acps-${props.envName}-image-scheduler-dlq`,
      retentionPeriod: cdk.Duration.days(14),
    });

    this.scheduleGroup = new scheduler.ScheduleGroup(
      this,
      'ImageScheduleGroup',
      {
        scheduleGroupName: `acps-${props.envName}-image-schedule-group`,
      },
    );

    this.taskDefinition = new ecs.FargateTaskDefinition(
      this,
      'ImageBatchTaskDefinition',
      {
        family: `acps-${props.envName}-image-batch`,
        cpu: 256,
        memoryLimitMiB: 512,
        taskRole,
      },
    );

    this.taskDefinition.addContainer('ImageBatchContainer', {
      containerName: 'image-batch',
      image: ecs.ContainerImage.fromEcrRepository(
        props.imageBatchRepository,
        imageBatchImageTag,
      ),
      environment: {
        DB_SECRET_ARN: dbSecretArn,
        API_SECRET_ARN: props.imageApiKeySecret.secretArn,
        S3_BUCKET_NAME: props.imagesBucket.bucketName,
        ENV_NAME: props.envName,
      },
      logging: ecs.LogDrivers.awsLogs({
        logGroup,
        streamPrefix: 'image-batch',
      }),
    });

    // ECR イメージ + awslogs を使う両タスク定義には CDK がタスク実行ロールを自動生成している前提
    const dbReadinessCheckExecutionRole =
      props.dbReadinessCheckTaskDefinition.executionRole;
    const imageBatchExecutionRole = this.taskDefinition.executionRole;
    if (!dbReadinessCheckExecutionRole || !imageBatchExecutionRole) {
      throw new Error('ECS タスク定義のタスク実行ロールが見つかりません。');
    }

    const buildLogGroup = new logs.LogGroup(this, 'ImageBatchBuildLogGroup', {
      retention: logs.RetentionDays.THREE_MONTHS,
      removalPolicy: cdk.RemovalPolicy.DESTROY,
    });

    const buildProject = new codebuild.PipelineProject(this, 'ImageBatchBuild', {
      projectName: `acps-${props.envName}-image-batch-build`,
      buildSpec: codebuild.BuildSpec.fromSourceFilename(
        'services/image-batch/buildspec.yml',
      ),
      environment: {
        buildImage: codebuild.LinuxBuildImage.STANDARD_7_0,
        privileged: true,
        computeType: codebuild.ComputeType.SMALL,
      },
      environmentVariables: {
        ECR_REPO_URI: { value: props.imageBatchRepository.repositoryUri },
        TASK_DEF_FAMILY: { value: this.taskDefinition.family },
        CONTAINER_NAME: { value: 'image-batch' },
      },
      logging: {
        cloudWatch: { logGroup: buildLogGroup },
      },
    });

    props.imageBatchRepository.grantPullPush(buildProject);
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
          imageBatchExecutionRole.roleArn,
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
    const sourceActionRole = new iam.Role(this, 'ImageBatchSourceActionRole', {
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

    new codepipeline.Pipeline(this, 'ImageBatchPipeline', {
      pipelineName: `acps-${props.envName}-image-batch-pipeline`,
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
                filePathsIncludes: ['services/image-batch/**', 'shared/**'],
              },
            ],
          },
        },
      ],
    });

    const stateMachineName = `acps-${props.envName}-image-generation-sfn`;
    this.stateMachine = new sfn.StateMachine(this, 'ImageGenerationStateMachine', {
      stateMachineName,
      definitionBody: sfn.DefinitionBody.fromString(
        fs.readFileSync(
          path.join(__dirname, 'asl', 'image-generation.asl.json'),
          'utf-8',
        ),
      ),
      definitionSubstitutions: {
        EcsClusterArn: props.ecsCluster.clusterArn,
        DbReadinessCheckTaskDefFamily:
          props.dbReadinessCheckTaskDefinition.family,
        ImageBatchTaskDefFamily: this.taskDefinition.family,
        PublicSubnetId1: props.vpc.publicSubnets[0].subnetId,
        PublicSubnetId2: props.vpc.publicSubnets[1].subnetId,
        DbReadinessCheckSgId:
          props.dbReadinessCheckSecurityGroup.securityGroupId,
        BatchSgId: props.batchSecurityGroup.securityGroupId,
        SnsPostingSfnArn: props.snsPostingStateMachine.stateMachineArn,
        ImageGenerationSfnName: stateMachineName,
      },
    });

    // 本番スケジュール: 1 日 3 回（7:00 / 12:00 / 21:00 JST）で全チェーンを起動する
    // （Phase 13-1 で本番化。workflow.html セクション 1.5）。
    new scheduler.Schedule(this, 'ImageGenerationSchedule', {
      scheduleName: `acps-${props.envName}-image-generation-schedule`,
      scheduleGroup: this.scheduleGroup,
      schedule: scheduler.ScheduleExpression.cron({
        minute: '0',
        hour: '7,12,21',
        timeZone: cdk.TimeZone.ASIA_TOKYO,
      }),
      enabled: true,
      target: new schedulerTargets.StepFunctionsStartExecution(this.stateMachine, {
        input: scheduler.ScheduleTargetInput.fromObject({
          set_code: 'fantasy-animals-1',
          scheduled_at: scheduler.ContextAttribute.scheduledTime,
        }),
        deadLetterQueue: this.schedulerDlq,
        retryAttempts: 3,
        maxEventAge: cdk.Duration.hours(1),
      }),
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
          imageBatchExecutionRole.roleArn,
        ],
        conditions: {
          StringEquals: {
            'iam:PassedToService': 'ecs-tasks.amazonaws.com',
          },
        },
      }),
    );
    this.stateMachine.addToRolePolicy(
      new iam.PolicyStatement({
        actions: ['states:StartExecution'],
        resources: [props.snsPostingStateMachine.stateMachineArn],
      }),
    );
    this.stateMachine.addToRolePolicy(
      new iam.PolicyStatement({
        actions: ['cloudwatch:PutMetricData'],
        resources: ['*'],
        conditions: {
          StringEquals: { 'cloudwatch:namespace': 'ACPS' },
        },
      }),
    );
  }
}
