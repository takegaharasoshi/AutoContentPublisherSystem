#!/usr/bin/env node
import * as cdk from 'aws-cdk-lib/core';
import { FoundationStack } from '../lib/foundation-stack';
import { SnsPostBatchStack } from '../lib/sns-post-batch-stack';
import { ImageBatchStack } from '../lib/image-batch-stack';
import { MonitoringStack } from '../lib/monitoring-stack';

// 環境識別子は現時点で prod のみ（docs/infra/security.html を参照）
const SUPPORTED_ENVS = ['prod'];

// Phase 8-2 の SNS 投稿バッチ CI/CD でも同じ GitHub 接続情報を使用する。
const GITHUB_CONNECTION_ARN =
  'arn:aws:codeconnections:ap-northeast-1:516964473143:connection/b671e788-6378-4296-89d9-bfe3a55e4be7';
const GITHUB_OWNER = 'takegaharasoshi';
const GITHUB_REPO = 'AutoContentPublisherSystem';
const GITHUB_BRANCH = 'main';

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

const imageBatchStack = new ImageBatchStack(app, 'ImageBatchStack', {
  envName,
  githubConnectionArn: GITHUB_CONNECTION_ARN,
  githubOwner: GITHUB_OWNER,
  githubRepo: GITHUB_REPO,
  githubBranch: GITHUB_BRANCH,
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

new MonitoringStack(app, 'MonitoringStack', {
  envName,
  auroraCluster: foundationStack.auroraCluster,
  ecsCluster: foundationStack.ecsCluster,
  imageGenerationStateMachine: imageBatchStack.stateMachine,
  snsPostingStateMachine: snsPostBatchStack.stateMachine,
  imageScheduleGroup: imageBatchStack.scheduleGroup,
  stackName: `${stackNamePrefix}-MonitoringStack`,
  env: { account: process.env.CDK_DEFAULT_ACCOUNT, region: 'ap-northeast-1' },
});
