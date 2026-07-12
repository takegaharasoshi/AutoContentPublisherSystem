import * as cdk from 'aws-cdk-lib/core';
import { Construct } from 'constructs';

/**
 * 共通基盤スタック。
 * リソースは docs/infra/stacks.html セクション 3.1 に沿って段階的に追加する。
 */
export class FoundationStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);
  }
}
