import * as fs from 'fs';
import * as path from 'path';
import * as cdk from 'aws-cdk-lib/core';
import * as s3 from 'aws-cdk-lib/aws-s3';
import * as secretsmanager from 'aws-cdk-lib/aws-secretsmanager';
import * as ssm from 'aws-cdk-lib/aws-ssm';
import { Match, Template } from 'aws-cdk-lib/assertions';
import { CoachReplyStack, CoachReplyStackProps } from '../lib/coach-reply-stack';
import { FoundationStack } from '../lib/foundation-stack';

const createCoachReplyStack = (face: CoachReplyStackProps['face']) => {
  const app = new cdk.App({
    context: { dbReadinessCheckImageTag: 'test-tag' },
  });
  const foundationStack = new FoundationStack(app, 'FoundationStack', {
    envName: 'prod',
  });
  const stack = new CoachReplyStack(app, 'CoachReplyStack', {
    envName: 'prod',
    face,
    assetsBucket: foundationStack.imagesBucket,
  });
  return { stack, foundationStack };
};

describe.each([
  {
    face: 'prod' as const,
    sfx: '',
    problemsPrefix: 'assets/logic-training-1/problems/',
    statePrefix: 'coach-reply/logic-training-1/state/',
  },
  {
    face: 'staging' as const,
    sfx: '-staging',
    problemsPrefix: 'assets/logic-training-1/staging/problems/',
    statePrefix: 'coach-reply/logic-training-1-staging/state/',
  },
])('CoachReplyStack ($face)', ({ face, sfx, problemsPrefix, statePrefix }) => {
  const { stack, foundationStack } = createCoachReplyStack(face);
  const template = Template.fromStack(stack);
  const runName = `acps-prod-coach-reply-run${sfx}`;
  const tokenRefreshName = `acps-prod-coach-reply-token-refresh${sfx}`;
  const paramPrefix = `/acps/prod/coach-reply${sfx}/`;
  const [secretId] = Object.keys(template.findResources('AWS::SecretsManager::Secret'));
  const [runId] = Object.keys(template.findResources('AWS::Lambda::Function', {
    Properties: { FunctionName: runName },
  }));
  const [tokenRefreshId] = Object.keys(template.findResources('AWS::Lambda::Function', {
    Properties: { FunctionName: tokenRefreshName },
  }));

  const roleStatements = (roleId: string): any[] => Object.values(
    template.findResources('AWS::IAM::Policy'),
  )
    .filter((policy) => policy.Properties.Roles.some(
      (role: { Ref: string }) => role.Ref === roleId,
    ))
    .flatMap((policy) => policy.Properties.PolicyDocument.Statement);

  const functionStatements = (functionId: string): any[] => {
    const fn = template.findResources('AWS::Lambda::Function')[functionId];
    return roleStatements(fn.Properties.Role['Fn::GetAtt'][0]);
  };

  test('4 キーが空の Secret を面別に作成し、削除・置換時も保持する', () => {
    template.resourceCountIs('AWS::SecretsManager::Secret', 1);
    template.hasResource('AWS::SecretsManager::Secret', {
      Properties: {
        Name: `acps/prod/logic-training-1/coach-reply${sfx}`,
        SecretString: JSON.stringify({
          ig_access_token: '',
          ig_user_id: '',
          token_expires_at: '',
          anthropic_api_key: '',
        }),
        GenerateSecretString: Match.absent(),
      },
      DeletionPolicy: 'Retain',
      UpdateReplacePolicy: 'Retain',
    });
  });

  test('SSM の返信スイッチと開始日時を安全な固定初期値で作成する', () => {
    template.resourceCountIs('AWS::SSM::Parameter', 2);
    for (const [name, value] of [
      ['reply-enabled', 'off'],
      ['reply-not-before', '2099-01-01T00:00:00Z'],
    ]) {
      template.hasResourceProperties('AWS::SSM::Parameter', {
        Name: `${paramPrefix}${name}`,
        Type: 'String',
        Tier: 'Standard',
        Value: value,
      });
    }
    // 更新ごとに CLI の設定値を書き戻すカスタムリソースは置かない。
    template.resourceCountIs('Custom::AWS', 0);
  });

  test('正解返信 Lambda に面別の接続先・判定設定と同時実行数 1 を設定する', () => {
    const [logGroupId] = Object.keys(template.findResources('AWS::Logs::LogGroup', {
      Properties: { LogGroupName: `/aws/lambda/${runName}` },
    }));
    template.hasResourceProperties('AWS::Lambda::Function', {
      FunctionName: runName,
      Runtime: 'python3.13',
      Handler: 'app.run_handler.lambda_handler',
      MemorySize: 256,
      Timeout: 300,
      ReservedConcurrentExecutions: 1,
      Environment: {
        Variables: Match.objectEquals({
          SECRET_ARN: { Ref: secretId },
          ASSETS_BUCKET: stack.resolve(foundationStack.imagesBucket.bucketName),
          PROBLEMS_PREFIX: problemsPrefix,
          STATE_PREFIX: statePrefix,
          PARAM_PREFIX: paramPrefix,
          GRAPH_API_BASE: 'https://graph.instagram.com/v25.0',
          JUDGE_MODEL: 'claude-haiku-5-5',
          JUDGE_EFFORT: 'high',
        }),
      },
      LoggingConfig: { LogGroup: { Ref: logGroupId } },
    });
    expect(stack.resolve(stack.runFunction.functionName)).toEqual({ Ref: runId });
  });

  test('トークン更新 Lambda は専用 Secret とバージョンなしの更新 API を使う', () => {
    const [logGroupId] = Object.keys(template.findResources('AWS::Logs::LogGroup', {
      Properties: { LogGroupName: `/aws/lambda/${tokenRefreshName}` },
    }));
    template.hasResourceProperties('AWS::Lambda::Function', {
      FunctionName: tokenRefreshName,
      Runtime: 'python3.13',
      Handler: 'app.token_refresh_handler.lambda_handler',
      MemorySize: 128,
      Timeout: 60,
      Environment: {
        Variables: Match.objectEquals({
          SECRET_ARN: { Ref: secretId },
          REFRESH_API_BASE: 'https://graph.instagram.com',
        }),
      },
      LoggingConfig: { LogGroup: { Ref: logGroupId } },
    });
    expect(stack.resolve(stack.tokenRefreshFunction.functionName)).toEqual({ Ref: tokenRefreshId });
  });

  test('両 Lambda の非同期再試行を無効にする', () => {
    template.resourceCountIs('AWS::Lambda::EventInvokeConfig', 2);
    for (const functionId of [runId, tokenRefreshId]) {
      template.hasResourceProperties('AWS::Lambda::EventInvokeConfig', {
        FunctionName: { Ref: functionId },
        MaximumRetryAttempts: 0,
      });
    }
  });

  test('VPC・Webhook・SQS を使わず、2 本の専用実行ロールを分離する', () => {
    const functions = template.findResources('AWS::Lambda::Function');
    template.resourceCountIs('AWS::Lambda::Function', face === 'prod' ? 3 : 2);
    for (const fn of Object.values(functions)) {
      expect(fn.Properties).not.toHaveProperty('VpcConfig');
    }
    expect(functions[runId].Properties.Role).not.toEqual(functions[tokenRefreshId].Properties.Role);
    for (const type of [
      'AWS::Lambda::Url',
      'AWS::Lambda::EventSourceMapping',
      'AWS::SQS::Queue',
      'AWS::EC2::VPC',
      'AWS::RDS::DBCluster',
      'AWS::CodePipeline::Pipeline',
    ]) {
      template.resourceCountIs(type, 0);
    }
  });

  test('正解返信は当該 Secret の読み取りと面別 SSM 階層の GetParameter だけを許可する', () => {
    const statements = functionStatements(runId);
    expect(statements.filter((statement) => [statement.Action].flat().some(
      (action: string) => action.startsWith('secretsmanager:'),
    ))).toEqual([{
      Action: 'secretsmanager:GetSecretValue',
      Effect: 'Allow',
      Resource: { Ref: secretId },
    }]);
    expect(statements.filter((statement) => [statement.Action].flat().some(
      (action: string) => action.startsWith('ssm:'),
    ))).toEqual([{
      Action: 'ssm:GetParameter',
      Effect: 'Allow',
      Resource: stack.resolve(stack.formatArn({
        service: 'ssm',
        resource: 'parameter',
        resourceName: `acps/prod/coach-reply${sfx}/*`,
        arnFormat: cdk.ArnFormat.SLASH_RESOURCE_NAME,
      })),
    }]);
  });

  test('S3 は問題・状態の読み取り、状態の書き込み、条件付き ListBucket に限定する', () => {
    const statements = functionStatements(runId);
    expect(statements.filter((statement) => [statement.Action].flat().some(
      (action: string) => action.startsWith('s3:'),
    ))).toEqual([
      {
        Action: 's3:GetObject',
        Effect: 'Allow',
        Resource: [
          stack.resolve(`${foundationStack.imagesBucket.bucketArn}/${problemsPrefix}*`),
          stack.resolve(`${foundationStack.imagesBucket.bucketArn}/${statePrefix}*`),
        ],
      },
      {
        Action: 's3:PutObject',
        Effect: 'Allow',
        Resource: stack.resolve(`${foundationStack.imagesBucket.bucketArn}/${statePrefix}*`),
      },
      {
        Action: 's3:ListBucket',
        Effect: 'Allow',
        Resource: stack.resolve(foundationStack.imagesBucket.bucketArn),
        Condition: {
          StringLike: { 's3:prefix': [`${problemsPrefix}*`, `${statePrefix}*`] },
        },
      },
    ]);
    expect(statements.flatMap((statement) => statement.Action).some(
      (action: string) => action === '*' || action.startsWith('kms:') || action.startsWith('ec2:'),
    )).toBe(false);
    // 共有バケットにはポリシーを足さず、FoundationStack からの逆参照を作らない。
    const bucketPolicies = Object.values(template.findResources('AWS::S3::BucketPolicy'));
    expect(bucketPolicies).toHaveLength(face === 'prod' ? 1 : 0);
    for (const policy of bucketPolicies) {
      expect(policy.Properties.Bucket.Ref).toMatch(/^PrivacyPolicyBucket/);
    }
    expect(foundationStack.dependencies).not.toContain(stack);
  });

  test('トークン更新は当該 Secret だけを読み書きし、S3・SSM 権限を持たない', () => {
    const statements = functionStatements(tokenRefreshId);
    expect(statements).toHaveLength(2);
    const actions = statements.flatMap((statement) => statement.Action);
    expect(actions).toContain('secretsmanager:GetSecretValue');
    expect(actions).toContain('secretsmanager:PutSecretValue');
    expect(actions.every((action: string) => action.startsWith('secretsmanager:'))).toBe(true);
    for (const statement of statements) {
      expect(statement.Resource).toEqual({ Ref: secretId });
    }
  });

  test('定時の正解返信 Scheduler は本番面にだけ作成する', () => {
    template.resourceCountIs('AWS::Scheduler::Schedule', face === 'prod' ? 2 : 1);
    if (face === 'prod') {
      template.hasResourceProperties('AWS::Scheduler::Schedule', {
        Name: runName,
        ScheduleExpression: 'cron(0 0,2,8,10,12,14,16,18,20,22 * * ? *)',
        ScheduleExpressionTimezone: 'Asia/Tokyo',
        FlexibleTimeWindow: { Mode: 'OFF' },
        Target: {
          Arn: { 'Fn::GetAtt': [runId, 'Arn'] },
          RetryPolicy: {
            MaximumRetryAttempts: 0,
            MaximumEventAgeInSeconds: 3600,
          },
        },
      });
    } else {
      expect(Object.values(template.findResources('AWS::Scheduler::Schedule')).some(
        (schedule) => schedule.Properties.Target.Arn['Fn::GetAtt'][0] === runId,
      )).toBe(false);
    }
    for (const schedule of Object.values(template.findResources('AWS::Scheduler::Schedule'))) {
      expect(schedule.Properties.GroupName ?? 'default').toBe('default');
    }
  });

  test('トークン更新 Scheduler は月曜 04:30 JST に実行する', () => {
    template.hasResourceProperties('AWS::Scheduler::Schedule', {
      Name: tokenRefreshName,
      ScheduleExpression: 'cron(30 4 ? * MON *)',
      ScheduleExpressionTimezone: 'Asia/Tokyo',
      FlexibleTimeWindow: { Mode: 'OFF' },
      Target: {
        Arn: { 'Fn::GetAtt': [tokenRefreshId, 'Arn'] },
        RetryPolicy: {
          MaximumRetryAttempts: 2,
          MaximumEventAgeInSeconds: 3600,
        },
      },
    });
  });

  test('Scheduler の専用実行ロールは対象の Lambda だけを起動できる', () => {
    for (const schedule of Object.values(template.findResources('AWS::Scheduler::Schedule'))) {
      const target = schedule.Properties.Target;
      const roleId = target.RoleArn['Fn::GetAtt'][0];
      const role = template.findResources('AWS::IAM::Role')[roleId];
      expect(role.Properties.AssumeRolePolicyDocument.Statement).toEqual([
        expect.objectContaining({
          Action: 'sts:AssumeRole',
          Effect: 'Allow',
          Principal: { Service: 'scheduler.amazonaws.com' },
        }),
      ]);
      const targetFunction = target.Arn['Fn::GetAtt'][0] === runId
        ? stack.runFunction : stack.tokenRefreshFunction;
      expect(roleStatements(roleId)).toEqual([{
        Action: 'lambda:InvokeFunction',
        Effect: 'Allow',
        Resource: [target.Arn, stack.resolve(`${targetFunction.functionArn}:*`)],
      }]);
    }
  });

  test('2 本のロググループを 90 日保持し、スタック削除時は削除する', () => {
    template.resourceCountIs('AWS::Logs::LogGroup', 2);
    for (const name of [runName, tokenRefreshName]) {
      template.hasResource('AWS::Logs::LogGroup', {
        Properties: {
          LogGroupName: `/aws/lambda/${name}`,
          RetentionInDays: 90,
        },
        DeletionPolicy: 'Delete',
        UpdateReplacePolicy: 'Delete',
      });
    }
  });

  test('配布 asset は app/ だけを含み、判定用 Markdown を残しキャッシュを除外する', () => {
    const assets = stack.node.findAll().filter(
      (node): node is cdk.AssetStaging => node instanceof cdk.AssetStaging
        && node.sourcePath.includes(path.join('services', 'coach-reply')),
    );
    expect(assets.length).toBeGreaterThan(0);
    const checkContents = (directory: string): void => {
      for (const entry of fs.readdirSync(directory, { withFileTypes: true })) {
        expect(entry.name).not.toBe('__pycache__');
        expect(entry.name).not.toMatch(/\.pyc$/);
        if (entry.isDirectory()) {
          checkContents(path.join(directory, entry.name));
        }
      }
    };
    for (const asset of assets) {
      expect(fs.readdirSync(asset.absoluteStagedPath)).toEqual(['app']);
      for (const file of ['run_handler.py', 'token_refresh_handler.py', 'prompts/judge.md']) {
        expect(fs.existsSync(path.join(asset.absoluteStagedPath, 'app', file))).toBe(true);
      }
      checkContents(asset.absoluteStagedPath);
    }
  });

  test('手動起動用の関数名・Secret 名・返信スイッチ名を出力する', () => {
    const secret = stack.node.findChild('CredentialsSecret') as secretsmanager.Secret;
    const replyEnabled = stack.node.findChild('ReplyEnabledParameter') as ssm.StringParameter;
    template.hasOutput('RunFunctionName', { Value: { Ref: runId } });
    template.hasOutput('TokenRefreshFunctionName', { Value: { Ref: tokenRefreshId } });
    template.hasOutput('SecretName', { Value: stack.resolve(secret.secretName) });
    template.hasOutput('ReplyEnabledParameterName', { Value: stack.resolve(replyEnabled.parameterName) });
  });
});

describe('CoachReplyStack のプライバシーポリシー', () => {
  test('本番面は専用の SSE-S3 バケットを公開読み取りにして HTML を配置する', () => {
    const { stack } = createCoachReplyStack('prod');
    const template = Template.fromStack(stack);
    const bucket = stack.node.findChild('PrivacyPolicyBucket') as s3.Bucket;
    template.resourceCountIs('AWS::S3::Bucket', 1);
    template.hasResource('AWS::S3::Bucket', {
      Properties: {
        BucketName: 'acps-prod-coach-reply-privacy-policy',
        BucketEncryption: {
          ServerSideEncryptionConfiguration: [{ ServerSideEncryptionByDefault: { SSEAlgorithm: 'AES256' } }],
        },
        PublicAccessBlockConfiguration: {
          BlockPublicAcls: true,
          IgnorePublicAcls: true,
          BlockPublicPolicy: false,
          RestrictPublicBuckets: false,
        },
      },
      DeletionPolicy: 'Retain',
      UpdateReplacePolicy: 'Retain',
    });
    template.hasResourceProperties('AWS::S3::BucketPolicy', {
      PolicyDocument: {
        Statement: [{
          Action: 's3:GetObject',
          Effect: 'Allow',
          Principal: { AWS: '*' },
          Resource: stack.resolve(`${bucket.bucketArn}/*`),
        }],
      },
    });
    template.resourceCountIs('Custom::CDKBucketDeployment', 1);
    template.hasResourceProperties('Custom::CDKBucketDeployment', {
      DestinationBucketName: stack.resolve(bucket.bucketName),
      SystemMetadata: { 'content-type': 'text/html; charset=utf-8' },
    });
    template.hasOutput('PrivacyPolicyUrl', {
      Value: stack.resolve(`https://${bucket.bucketRegionalDomainName}/index.html`),
    });
    expect(fs.existsSync(path.join(__dirname, '../assets/coach-reply-privacy-policy/index.html'))).toBe(true);
  });

  test('ステージング面はプライバシーポリシーを作成しない', () => {
    const { stack } = createCoachReplyStack('staging');
    const template = Template.fromStack(stack);
    template.resourceCountIs('AWS::S3::Bucket', 0);
    template.resourceCountIs('AWS::S3::BucketPolicy', 0);
    template.resourceCountIs('Custom::CDKBucketDeployment', 0);
    expect(Object.keys(template.findOutputs('PrivacyPolicyUrl'))).toHaveLength(0);
  });
});
