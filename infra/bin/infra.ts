#!/usr/bin/env node
import * as cdk from 'aws-cdk-lib/core';
import { FoundationStack } from '../lib/foundation-stack';
import { SnsPostBatchStack } from '../lib/sns-post-batch-stack';
import { ImageBatchStack } from '../lib/image-batch-stack';

// 環境識別子は現時点で prod のみ（docs/infra/security.html を参照）
const SUPPORTED_ENVS = ['prod'];

const app = new cdk.App();

const envName: unknown = app.node.tryGetContext('env');
if (typeof envName !== 'string' || !SUPPORTED_ENVS.includes(envName)) {
  throw new Error(
    `Context "env" が必要です。-c env=prod のように指定してください（対応環境: ${SUPPORTED_ENVS.join(', ')}）`,
  );
}

// CloudFormation 上の実スタック名は環境名プレフィックス付き（例: Prod-FoundationStack）。
// CDK コマンドでは論理スタック ID（FoundationStack など）を指定する
const stackNamePrefix = envName.charAt(0).toUpperCase() + envName.slice(1);

const foundationStack = new FoundationStack(app, 'FoundationStack', {
  envName,
  stackName: `${stackNamePrefix}-FoundationStack`,
  env: { account: process.env.CDK_DEFAULT_ACCOUNT, region: 'ap-northeast-1' },
});

const snsPostBatchStack = new SnsPostBatchStack(app, 'SnsPostBatchStack', {
  envName,
  snsPostBatchRepository: foundationStack.snsPostBatchRepository,
  imagesBucket: foundationStack.imagesBucket,
  auroraCluster: foundationStack.auroraCluster,
  vpc: foundationStack.vpc,
  ecsCluster: foundationStack.ecsCluster,
  batchSecurityGroup: foundationStack.batchSecurityGroup,
  dbReadinessCheckSecurityGroup: foundationStack.dbReadinessCheckSecurityGroup,
  dbReadinessCheckTaskDefinition: foundationStack.dbReadinessCheckTaskDefinition,
  stackName: `${stackNamePrefix}-SnsPostBatchStack`,
  env: { account: process.env.CDK_DEFAULT_ACCOUNT, region: 'ap-northeast-1' },
});

new ImageBatchStack(app, 'ImageBatchStack', {
  envName,
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
  stackName: `${stackNamePrefix}-ImageBatchStack`,
  env: { account: process.env.CDK_DEFAULT_ACCOUNT, region: 'ap-northeast-1' },
});
