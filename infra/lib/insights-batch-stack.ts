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
import * as scheduler from 'aws-cdk-lib/aws-scheduler';
import * as schedulerTargets from 'aws-cdk-lib/aws-scheduler-targets';
import * as sfn from 'aws-cdk-lib/aws-stepfunctions';
import * as sqs from 'aws-cdk-lib/aws-sqs';
import * as fs from 'fs';
import * as path from 'path';
import { Construct } from 'constructs';

export interface InsightsBatchStackProps extends cdk.StackProps {
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
  /** インサイト収集バッチのコンテナイメージ用 ECR リポジトリ */
  insightsBatchRepository: ecr.Repository;
  /** Aurora Serverless v2 クラスター */
  auroraCluster: rds.DatabaseCluster;
  /** Public Subnet ID を参照するための VPC */
  vpc: ec2.Vpc;
  /** インサイト収集バッチを実行する ECS クラスター */
  ecsCluster: ecs.Cluster;
  /** インサイト収集バッチ ECS タスク用の Security Group */
  batchSecurityGroup: ec2.SecurityGroup;
  /** DB 準備確認 ECS タスク用の Security Group */
  dbReadinessCheckSecurityGroup: ec2.SecurityGroup;
  /** DB 準備確認タスク定義 */
  dbReadinessCheckTaskDefinition: ecs.FargateTaskDefinition;
}

/** インサイト収集バッチ実行基盤スタック。 */
export class InsightsBatchStack extends cdk.Stack {
  /** インサイト収集バッチのタスク定義。Step Functions から family 名で参照される */
  public readonly taskDefinition: ecs.FargateTaskDefinition;
  /** インサイト収集ワークフロー。MonitoringStack が参照する */
  public readonly stateMachine: sfn.StateMachine;
  /** Scheduler 用 DLQ */
  public readonly schedulerDlq: sqs.Queue;
  /** MonitoringStack の AWS/Scheduler メトリクス Dimension で参照する ScheduleGroup */
  public readonly scheduleGroup: scheduler.ScheduleGroup;

  constructor(scope: Construct, id: string, props: InsightsBatchStackProps) {
    super(scope, id, props);

    const contextImageTag = this.node.tryGetContext('insightsBatchImageTag');
    const hasInsightsBatchImageTag =
      typeof contextImageTag === 'string' && contextImageTag.trim().length > 0;
    const insightsBatchImageTag =
      hasInsightsBatchImageTag ? contextImageTag.trim() : 'MISSING';

    if (!hasInsightsBatchImageTag) {
      // CDK はデプロイ対象外のスタックも synth するため、throw すると他スタックのデプロイも失敗する。
      cdk.Annotations.of(this).addError(
        '-c insightsBatchImageTag=<tag> の指定が必要です。',
      );
    }

    const taskRole = new iam.Role(this, 'InsightsBatchTaskRole', {
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

    const logGroup = new logs.LogGroup(this, 'InsightsBatchLogGroup', {
      retention: logs.RetentionDays.THREE_MONTHS,
      removalPolicy: cdk.RemovalPolicy.DESTROY,
    });

    const dbSecretArn = props.auroraCluster.secret?.secretArn;
    if (!dbSecretArn) {
      throw new Error('Aurora クラスターの認証情報 Secret が見つかりません。');
    }

    this.schedulerDlq = new sqs.Queue(this, 'InsightsSchedulerDlq', {
      queueName: `acps-${props.envName}-insights-scheduler-dlq`,
      retentionPeriod: cdk.Duration.days(14),
    });

    this.scheduleGroup = new scheduler.ScheduleGroup(this, 'InsightsScheduleGroup', {
      scheduleGroupName: `acps-${props.envName}-insights-schedule-group`,
    });

    this.taskDefinition = new ecs.FargateTaskDefinition(
      this,
      'InsightsBatchTaskDefinition',
      {
        family: `acps-${props.envName}-insights-batch`,
        cpu: 256,
        memoryLimitMiB: 512,
        taskRole,
      },
    );

    this.taskDefinition.addContainer('InsightsBatchContainer', {
      containerName: 'insights-batch',
      image: ecs.ContainerImage.fromEcrRepository(
        props.insightsBatchRepository,
        insightsBatchImageTag,
      ),
      environment: {
        DB_SECRET_ARN: dbSecretArn,
        ENV_NAME: props.envName,
      },
      logging: ecs.LogDrivers.awsLogs({
        logGroup,
        streamPrefix: 'insights-batch',
      }),
    });

    const dbReadinessCheckExecutionRole =
      props.dbReadinessCheckTaskDefinition.executionRole;
    const insightsBatchExecutionRole = this.taskDefinition.executionRole;
    if (!dbReadinessCheckExecutionRole || !insightsBatchExecutionRole) {
      throw new Error('ECS タスク定義のタスク実行ロールが見つかりません。');
    }

    const buildLogGroup = new logs.LogGroup(this, 'InsightsBatchBuildLogGroup', {
      retention: logs.RetentionDays.THREE_MONTHS,
      removalPolicy: cdk.RemovalPolicy.DESTROY,
    });

    const buildProject = new codebuild.PipelineProject(this, 'InsightsBatchBuild', {
      projectName: `acps-${props.envName}-insights-batch-build`,
      buildSpec: codebuild.BuildSpec.fromSourceFilename(
        'services/insights-batch/buildspec.yml',
      ),
      environment: {
        buildImage: codebuild.LinuxBuildImage.STANDARD_7_0,
        privileged: true,
        computeType: codebuild.ComputeType.SMALL,
      },
      environmentVariables: {
        ECR_REPO_URI: { value: props.insightsBatchRepository.repositoryUri },
        TASK_DEF_FAMILY: { value: this.taskDefinition.family },
        CONTAINER_NAME: { value: 'insights-batch' },
      },
      logging: { cloudWatch: { logGroup: buildLogGroup } },
    });

    props.insightsBatchRepository.grantPullPush(buildProject);
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
          insightsBatchExecutionRole.roleArn,
        ],
        conditions: { StringEquals: { 'iam:PassedToService': 'ecs-tasks.amazonaws.com' } },
      }),
    );

    const sourceActionRole = new iam.Role(this, 'InsightsBatchSourceActionRole', {
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

    new codepipeline.Pipeline(this, 'InsightsBatchPipeline', {
      pipelineName: `acps-${props.envName}-insights-batch-pipeline`,
      pipelineType: codepipeline.PipelineType.V2,
      crossAccountKeys: false,
      stages: [
        { stageName: 'Source', actions: [sourceAction] },
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
                filePathsIncludes: ['services/insights-batch/**', 'shared/**'],
              },
            ],
          },
        },
      ],
    });

    this.stateMachine = new sfn.StateMachine(this, 'InsightsCollectionStateMachine', {
      stateMachineName: `acps-${props.envName}-insights-collection-sfn`,
      definitionBody: sfn.DefinitionBody.fromString(
        fs.readFileSync(
          path.join(__dirname, 'asl', 'insights-collection.asl.json'),
          'utf-8',
        ),
      ),
      definitionSubstitutions: {
        EcsClusterArn: props.ecsCluster.clusterArn,
        DbReadinessCheckTaskDefFamily:
          props.dbReadinessCheckTaskDefinition.family,
        InsightsBatchTaskDefFamily: this.taskDefinition.family,
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
          insightsBatchExecutionRole.roleArn,
        ],
        conditions: { StringEquals: { 'iam:PassedToService': 'ecs-tasks.amazonaws.com' } },
      }),
    );

    // 命名規約: acps-{env}-insights-collection-{set_code}-{morning|evening}。
    // 全セット共通で 1 日 2 回（06:00 / 18:00 JST）実行する。
    //
    // 16-10 のデプロイから 16-11 の instagram_manage_insights 再認可までは
    // false にして停止していた（未再認可のまま定時実行すると権限エラーで
    // 失敗アラームが鳴り続けるため）。2026-08-10 に再認可と両セットの疎通確認・
    // バックフィルが完了したため true へ戻した。長期停止が必要になった場合も
    // 手動 DISABLE ではなく本フラグで止める（Scheduler は CDK を単一の正とする。
    // docs/infra/workflow.html セクション 1.5 の decision）。
    const insightsCollectionSchedulesEnabled = true;

    const insightsCollectionSchedules = [
      { setCode: 'fantasy-animals-1', slot: 'morning', minute: '0', hour: '6' },
      { setCode: 'fantasy-animals-1', slot: 'evening', minute: '0', hour: '18' },
      { setCode: 'logic-training-1', slot: 'morning', minute: '0', hour: '6' },
      { setCode: 'logic-training-1', slot: 'evening', minute: '0', hour: '18' },
      // pref-ranking-1: 17-5c（2026-08-26）の稼働開始で追加
      { setCode: 'pref-ranking-1', slot: 'morning', minute: '0', hour: '6' },
      { setCode: 'pref-ranking-1', slot: 'evening', minute: '0', hour: '18' },
    ];

    for (const entry of insightsCollectionSchedules) {
      new scheduler.Schedule(
        this,
        `InsightsCollectionSchedule-${entry.setCode}-${entry.slot}`,
        {
          scheduleName: `acps-${props.envName}-insights-collection-${entry.setCode}-${entry.slot}`,
          scheduleGroup: this.scheduleGroup,
          schedule: scheduler.ScheduleExpression.cron({
            minute: entry.minute,
            hour: entry.hour,
            timeZone: cdk.TimeZone.ASIA_TOKYO,
          }),
          enabled: insightsCollectionSchedulesEnabled,
          target: new schedulerTargets.StepFunctionsStartExecution(
            this.stateMachine,
            {
              input: scheduler.ScheduleTargetInput.fromObject({
                set_code: entry.setCode,
                scheduled_at: scheduler.ContextAttribute.scheduledTime,
                media_lookback_days: '14',
              }),
              deadLetterQueue: this.schedulerDlq,
              retryAttempts: 3,
              maxEventAge: cdk.Duration.hours(1),
            },
          ),
        },
      );
    }
  }
}
