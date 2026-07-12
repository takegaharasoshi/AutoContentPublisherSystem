import * as cdk from 'aws-cdk-lib/core';
import * as ec2 from 'aws-cdk-lib/aws-ec2';
import * as s3 from 'aws-cdk-lib/aws-s3';
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
  }
}
