import * as cdk from 'aws-cdk-lib/core';
import * as ec2 from 'aws-cdk-lib/aws-ec2';
import { Construct } from 'constructs';

/**
 * 共通基盤スタック。
 * リソースは docs/infra/stacks.html セクション 3.1 に沿って段階的に追加する。
 */
export class FoundationStack extends cdk.Stack {
  /** 全サービス共有の VPC。後続の ImageBatchStack / SnsPostBatchStack から参照される */
  public readonly vpc: ec2.Vpc;

  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
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
  }
}
