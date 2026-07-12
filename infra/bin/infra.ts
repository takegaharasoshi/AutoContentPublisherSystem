#!/usr/bin/env node
import * as cdk from 'aws-cdk-lib/core';
import { FoundationStack } from '../lib/foundation-stack';

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

new FoundationStack(app, 'FoundationStack', {
  envName,
  stackName: `${stackNamePrefix}-FoundationStack`,
  env: { account: process.env.CDK_DEFAULT_ACCOUNT, region: 'ap-northeast-1' },
});
