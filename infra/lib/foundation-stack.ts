import * as cdk from 'aws-cdk-lib/core';
import * as ec2 from 'aws-cdk-lib/aws-ec2';
import * as ecs from 'aws-cdk-lib/aws-ecs';
import * as ecr from 'aws-cdk-lib/aws-ecr';
import * as iam from 'aws-cdk-lib/aws-iam';
import * as logs from 'aws-cdk-lib/aws-logs';
import * as rds from 'aws-cdk-lib/aws-rds';
import * as s3 from 'aws-cdk-lib/aws-s3';
import * as secretsmanager from 'aws-cdk-lib/aws-secretsmanager';
import { Construct } from 'constructs';

export interface FoundationStackProps extends cdk.StackProps {
  /** 環境識別子（例: prod） */
  envName: string;
}

/**
 * 共通基盤スタック。
 * リソースは docs/infra/stacks.html セクション 3.1 に沿って段階的に追加する。
 */
export class FoundationStack extends cdk.Stack {
  /** 全サービス共有の VPC。後続の ImageBatchStack / SnsPostBatchStack から参照される */
  public readonly vpc: ec2.Vpc;
  /** 生成画像を保存する共有 S3 バケット。後続の ImageBatchStack / SnsPostBatchStack から参照される */
  public readonly imagesBucket: s3.Bucket;
  /** ECS Fargate バッチ共通の Security Group。後続の ImageBatchStack / SnsPostBatchStack から参照される */
  public readonly batchSecurityGroup: ec2.SecurityGroup;
  /** DB 準備確認 ECS タスク用の Security Group。後続の ImageBatchStack / SnsPostBatchStack から参照される */
  public readonly dbReadinessCheckSecurityGroup: ec2.SecurityGroup;
  /** Aurora Serverless v2 用の Security Group。Phase 3-1 の Aurora 作成時に同一スタック内で参照される */
  public readonly auroraSecurityGroup: ec2.SecurityGroup;
  /** Aurora Serverless v2 クラスター。後続の ImageBatchStack / SnsPostBatchStack から参照される */
  public readonly auroraCluster: rds.DatabaseCluster;
  /** 画像生成 API キー用の Secret。後続の ImageBatchStack から参照される */
  public readonly imageApiKeySecret: secretsmanager.Secret;
  /** 全バッチ共通の ECS Cluster。後続の ImageBatchStack / SnsPostBatchStack から参照される */
  public readonly ecsCluster: ecs.Cluster;
  /** 画像生成バッチのコンテナイメージ用 ECR リポジトリ。後続の ImageBatchStack から参照される */
  public readonly imageBatchRepository: ecr.Repository;
  /** SNS 投稿バッチのコンテナイメージ用 ECR リポジトリ。後続の SnsPostBatchStack から参照される */
  public readonly snsPostBatchRepository: ecr.Repository;
  /** DB 準備確認バッチのコンテナイメージ用 ECR リポジトリ。Phase 3-3 で同一スタック内から参照される */
  public readonly dbReadinessCheckRepository: ecr.Repository;
  /** DB 準備確認タスク定義。Phase 5・6 で ImageBatchStack / SnsPostBatchStack の Step Functions から family 名で参照される */
  public readonly dbReadinessCheckTaskDefinition: ecs.FargateTaskDefinition;

  constructor(scope: Construct, id: string, props: FoundationStackProps) {
    super(scope, id, props);

    const contextImageTag = this.node.tryGetContext('dbReadinessCheckImageTag');
    const hasDbReadinessCheckImageTag =
      typeof contextImageTag === 'string' && contextImageTag.trim().length > 0;
    const dbReadinessCheckImageTag =
      hasDbReadinessCheckImageTag ? contextImageTag.trim() : 'MISSING';

    if (!hasDbReadinessCheckImageTag) {
      // CDK はデプロイ対象外のスタックも synth するため、throw すると他スタックのデプロイも失敗する。
      cdk.Annotations.of(this).addError(
        '-c dbReadinessCheckImageTag=<tag> の指定が必要です。',
      );
    }

    // NAT Gateway は使用しない（ECS Fargate はパブリック IP で外部 API にアクセスする。
    // docs/infra/architecture.html セクション 2.1）
    this.vpc = new ec2.Vpc(this, 'Vpc', {
      maxAzs: 2,
      natGateways: 0,
      subnetConfiguration: [
        { name: 'Public', subnetType: ec2.SubnetType.PUBLIC },
        { name: 'Isolated', subnetType: ec2.SubnetType.PRIVATE_ISOLATED },
      ],
    });

    this.imagesBucket = new s3.Bucket(this, 'ImagesBucket', {
      bucketName: `acps-${props.envName}-images-${this.account}`,
      lifecycleRules: [
        {
          expiration: cdk.Duration.days(30),
        },
      ],
      blockPublicAccess: s3.BlockPublicAccess.BLOCK_ALL,
      encryption: s3.BucketEncryption.S3_MANAGED,
      enforceSSL: true,
      removalPolicy: cdk.RemovalPolicy.DESTROY,
      autoDeleteObjects: true,
    });

    this.batchSecurityGroup = new ec2.SecurityGroup(this, 'BatchSecurityGroup', {
      vpc: this.vpc,
      description: 'Security group for ECS Fargate batch tasks',
      allowAllOutbound: false,
    });

    this.dbReadinessCheckSecurityGroup = new ec2.SecurityGroup(
      this,
      'DbReadinessCheckSecurityGroup',
      {
        vpc: this.vpc,
        description: 'Security group for DB readiness check ECS tasks',
        allowAllOutbound: false,
      },
    );

    this.auroraSecurityGroup = new ec2.SecurityGroup(this, 'AuroraSecurityGroup', {
      vpc: this.vpc,
      description: 'Security group for Aurora Serverless v2',
      allowAllOutbound: false,
    });

    const batchSecurityGroups = [
      this.batchSecurityGroup,
      this.dbReadinessCheckSecurityGroup,
    ];

    for (const securityGroup of batchSecurityGroups) {
      securityGroup.addEgressRule(
        ec2.Peer.anyIpv4(),
        ec2.Port.tcp(443),
        'Allow HTTPS access to external services',
      );
      securityGroup.addEgressRule(
        this.auroraSecurityGroup,
        ec2.Port.tcp(3306),
        'Allow MySQL access to Aurora',
      );
      this.auroraSecurityGroup.addIngressRule(
        securityGroup,
        ec2.Port.tcp(3306),
        'Allow MySQL access from ECS tasks',
      );
    }

    // DB は正式な記録を担うため、RemovalPolicy はデフォルトの SNAPSHOT を使用する。
    this.auroraCluster = new rds.DatabaseCluster(this, 'AuroraCluster', {
      engine: rds.DatabaseClusterEngine.auroraMysql({
        version: rds.AuroraMysqlEngineVersion.VER_3_08_2,
      }),
      vpc: this.vpc,
      vpcSubnets: { subnetType: ec2.SubnetType.PRIVATE_ISOLATED },
      securityGroups: [this.auroraSecurityGroup],
      writer: rds.ClusterInstance.serverlessV2('Writer'),
      serverlessV2MinCapacity: 0,
      serverlessV2MaxCapacity: 1.0,
      credentials: rds.Credentials.fromGeneratedSecret('admin', {
        secretName: `acps/${props.envName}/db/credentials`,
      }),
      defaultDatabaseName: 'acps',
      enableDataApi: true,
      storageEncrypted: true,
    });

    this.imageApiKeySecret = new secretsmanager.Secret(this, 'ImageApiKeySecret', {
      secretName: `acps/${props.envName}/image/api-key`,
      description:
        'API key for the image generation service (placeholder; set the actual value manually via AWS Console)',
      generateSecretString: {
        secretStringTemplate: '{}',
        generateStringKey: 'api_key',
      },
    });

    // 既存 VPC を使用し、Cluster 作成時の VPC 自動作成を防ぐ
    this.ecsCluster = new ecs.Cluster(this, 'EcsCluster', {
      vpc: this.vpc,
    });

    const batchRepositoryProps = {
      lifecycleRules: [
        {
          rulePriority: 1,
          description: 'Retain the latest 30 release images',
          tagPrefixList: ['release-'],
          maxImageCount: 30,
        },
        {
          rulePriority: 2,
          description: 'Retain the latest 10 images',
          tagStatus: ecr.TagStatus.ANY,
          maxImageCount: 10,
        },
      ],
      removalPolicy: cdk.RemovalPolicy.DESTROY,
      emptyOnDelete: true,
    };

    this.imageBatchRepository = new ecr.Repository(this, 'ImageBatchRepository', {
      repositoryName: 'auto-content-publisher/image-batch',
      ...batchRepositoryProps,
    });

    this.snsPostBatchRepository = new ecr.Repository(this, 'SnsPostBatchRepository', {
      repositoryName: 'auto-content-publisher/sns-post-batch',
      ...batchRepositoryProps,
    });

    this.dbReadinessCheckRepository = new ecr.Repository(
      this,
      'DbReadinessCheckRepository',
      {
        repositoryName: 'auto-content-publisher/db-readiness-check',
        lifecycleRules: [
          {
            description: 'Retain the latest 30 images',
            tagStatus: ecr.TagStatus.ANY,
            maxImageCount: 30,
          },
        ],
        removalPolicy: cdk.RemovalPolicy.DESTROY,
        emptyOnDelete: true,
      },
    );

    // ECS Fargate から S3 への通信を AWS 網内に閉じる（Gateway 型は無料。
    // docs/infra/architecture.html セクション 2.1）
    this.vpc.addGatewayEndpoint('S3GatewayEndpoint', {
      service: ec2.GatewayVpcEndpointAwsService.S3,
      subnets: [{ subnetType: ec2.SubnetType.PUBLIC }],
    });

    const dbReadinessCheckTaskRole = new iam.Role(this, 'DbReadinessCheckTaskRole', {
      assumedBy: new iam.ServicePrincipal('ecs-tasks.amazonaws.com'),
      inlinePolicies: {
        ReadDbSecret: new iam.PolicyDocument({
          statements: [
            new iam.PolicyStatement({
              actions: ['secretsmanager:GetSecretValue'],
              resources: [
                `arn:aws:secretsmanager:${this.region}:${this.account}:secret:acps/${props.envName}/db/*`,
              ],
            }),
          ],
        }),
      },
    });

    const dbReadinessCheckLogGroup = new logs.LogGroup(
      this,
      'DbReadinessCheckLogGroup',
      {
        retention: logs.RetentionDays.THREE_MONTHS,
        removalPolicy: cdk.RemovalPolicy.DESTROY,
      },
    );

    const dbSecretArn = this.auroraCluster.secret?.secretArn;
    if (!dbSecretArn) {
      throw new Error('Aurora クラスターの認証情報 Secret が見つかりません。');
    }

    this.dbReadinessCheckTaskDefinition = new ecs.FargateTaskDefinition(
      this,
      'DbReadinessCheckTaskDefinition',
      {
        family: `acps-${props.envName}-db-readiness-check`,
        cpu: 256,
        memoryLimitMiB: 512,
        taskRole: dbReadinessCheckTaskRole,
      },
    );

    this.dbReadinessCheckTaskDefinition.addContainer('DbReadinessCheckContainer', {
      containerName: 'db-readiness-check',
      image: ecs.ContainerImage.fromEcrRepository(
        this.dbReadinessCheckRepository,
        dbReadinessCheckImageTag,
      ),
      environment: {
        DB_SECRET_ARN: dbSecretArn,
        ENV_NAME: props.envName,
      },
      logging: ecs.LogDrivers.awsLogs({
        logGroup: dbReadinessCheckLogGroup,
        streamPrefix: 'db-readiness-check',
      }),
    });
  }
}
