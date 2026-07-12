import * as cdk from 'aws-cdk-lib/core';
import * as ec2 from 'aws-cdk-lib/aws-ec2';
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
  /** 画像生成 API キー用の Secret。後続の ImageBatchStack から参照される */
  public readonly imageApiKeySecret: secretsmanager.Secret;

  constructor(scope: Construct, id: string, props: FoundationStackProps) {
    super(scope, id, props);

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

    this.imageApiKeySecret = new secretsmanager.Secret(this, 'ImageApiKeySecret', {
      secretName: `acps/${props.envName}/image/api-key`,
      description:
        'API key for the image generation service (placeholder; set the actual value manually via AWS Console)',
      generateSecretString: {
        secretStringTemplate: '{}',
        generateStringKey: 'api_key',
      },
    });
  }
}
