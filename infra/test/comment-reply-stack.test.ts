import * as fs from 'fs';
import * as path from 'path';
import * as cdk from 'aws-cdk-lib/core';
import * as secretsmanager from 'aws-cdk-lib/aws-secretsmanager';
import { Match, Template } from 'aws-cdk-lib/assertions';
import { CommentReplyStack, CommentReplyStackProps } from '../lib/comment-reply-stack';
import { FoundationStack } from '../lib/foundation-stack';

const createCommentReplyStack = (face: CommentReplyStackProps['face']) => {
  const app = new cdk.App({
    context: { dbReadinessCheckImageTag: 'test-tag' },
  });
  const foundationStack = new FoundationStack(app, 'FoundationStack', {
    envName: 'prod',
  });
  const stack = new CommentReplyStack(app, 'CommentReplyStack', {
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
    problemsPrefix: 'assets/umigame-soup-1/problems/',
    setCode: 'umigame-soup-1',
  },
  {
    face: 'staging' as const,
    sfx: '-staging',
    problemsPrefix: 'assets/umigame-soup-1/staging/problems/',
    setCode: 'umigame-soup-1-staging',
  },
])('CommentReplyStack ($face)', ({ face, sfx, problemsPrefix, setCode }) => {
  const { stack, foundationStack } = createCommentReplyStack(face);
  const template = Template.fromStack(stack);
  const webhookName = `acps-prod-comment-reply-webhook${sfx}`;
  const replyName = `acps-prod-comment-reply-reply${sfx}`;
  const [secretId] = Object.keys(template.findResources('AWS::SecretsManager::Secret'));
  const [queueId] = Object.keys(template.findResources('AWS::SQS::Queue', {
    Properties: { QueueName: `acps-prod-comment-reply${sfx}.fifo` },
  }));
  const [webhookId] = Object.keys(template.findResources('AWS::Lambda::Function', {
    Properties: { FunctionName: webhookName },
  }));
  const [replyId] = Object.keys(template.findResources('AWS::Lambda::Function', {
    Properties: { FunctionName: replyName },
  }));
  const [webhookLogGroupId] = Object.keys(template.findResources('AWS::Logs::LogGroup', {
    Properties: { LogGroupName: `/aws/lambda/${webhookName}` },
  }));
  const [replyLogGroupId] = Object.keys(template.findResources('AWS::Logs::LogGroup', {
    Properties: { LogGroupName: `/aws/lambda/${replyName}` },
  }));

  const roleStatements = (functionId: string): any[] => {
    const functions = template.findResources('AWS::Lambda::Function');
    const roleId = functions[functionId].Properties.Role['Fn::GetAtt'][0];
    return Object.values(template.findResources('AWS::IAM::Policy'))
      .filter((policy) => policy.Properties.Roles.some(
        (role: { Ref: string }) => role.Ref === roleId,
      ))
      .flatMap((policy) => policy.Properties.PolicyDocument.Statement);
  };

  test('認証情報の空値テンプレートを作成し、Secret を保持する', () => {
    template.resourceCountIs('AWS::SecretsManager::Secret', 1);
    template.hasResource('AWS::SecretsManager::Secret', {
      Properties: {
        Name: `acps/prod/umigame-soup-1/comment-reply${sfx}`,
        GenerateSecretString: {
          GenerateStringKey: 'verify_token',
          ExcludePunctuation: true,
          SecretStringTemplate: JSON.stringify({
            app_secret: '',
            ig_access_token: '',
            ig_user_id: '',
            token_expires_at: '',
            openai_api_key: '',
            typesafe_api_key: '',
            anthropic_api_key: '',
          }),
        },
      },
      DeletionPolicy: 'Retain',
      UpdateReplacePolicy: 'Retain',
    });
  });

  test('SSE-SQS 暗号化した FIFO キューと 14 日保持の DLQ を作成する', () => {
    template.resourceCountIs('AWS::SQS::Queue', 2);
    template.hasResourceProperties('AWS::SQS::Queue', {
      QueueName: `acps-prod-comment-reply-dlq${sfx}.fifo`,
      FifoQueue: true,
      MessageRetentionPeriod: 1209600,
      SqsManagedSseEnabled: true,
    });
    template.hasResourceProperties('AWS::SQS::Queue', {
      QueueName: `acps-prod-comment-reply${sfx}.fifo`,
      FifoQueue: true,
      ContentBasedDeduplication: false,
      MessageRetentionPeriod: 345600,
      VisibilityTimeout: 720,
      SqsManagedSseEnabled: true,
      RedrivePolicy: {
        deadLetterTargetArn: stack.resolve(stack.replyDlq.queueArn),
        maxReceiveCount: 3,
      },
    });
  });

  test('Webhook Lambda に認証情報と送信先キューを設定する', () => {
    template.hasResourceProperties('AWS::Lambda::Function', {
      FunctionName: webhookName,
      Runtime: 'python3.13',
      Handler: 'app.webhook_handler.lambda_handler',
      MemorySize: 128,
      Timeout: 10,
      Environment: {
        Variables: Match.objectEquals({
          SECRET_ARN: { Ref: secretId },
          QUEUE_URL: { Ref: queueId },
        }),
      },
      LoggingConfig: { LogGroup: { Ref: webhookLogGroupId } },
    });
  });

  test('Reply Lambda に面別プレフィックスと判定・返信の既定値を設定する', () => {
    const bucketName = stack.resolve(foundationStack.imagesBucket.bucketName);
    template.hasResourceProperties('AWS::Lambda::Function', {
      FunctionName: replyName,
      Runtime: 'python3.13',
      Handler: 'app.reply_handler.lambda_handler',
      MemorySize: 256,
      Timeout: 120,
      ReservedConcurrentExecutions: 2,
      Environment: {
        Variables: Match.objectEquals({
          SECRET_ARN: { Ref: secretId },
          ASSETS_BUCKET: bucketName,
          COMMENT_LOG_BUCKET: bucketName,
          PROBLEMS_PREFIX: problemsPrefix,
          SET_CODE: setCode,
          GRAPH_API_BASE: 'https://graph.instagram.com/v23.0',
          JUDGE_MODE: 'haiku',
          REPLY_VARIANT: '1b-haiku',
          HAIKU_EFFORT: 'high',
          LUNA_EFFORT: 'xhigh',
          LUNA_MODEL: 'gpt-6-luna',
        }),
      },
      LoggingConfig: { LogGroup: { Ref: replyLogGroupId } },
    });
  });

  test('両 Lambda は VPC 外で実行する', () => {
    template.resourceCountIs('AWS::Lambda::Function', 2);
    for (const fn of Object.values(template.findResources('AWS::Lambda::Function'))) {
      expect(fn.Properties).not.toHaveProperty('VpcConfig');
    }
  });

  test('Webhook の Function URL は認証なしで公開する', () => {
    template.resourceCountIs('AWS::Lambda::Url', 1);
    template.hasResourceProperties('AWS::Lambda::Url', {
      AuthType: 'NONE',
      TargetFunctionArn: { 'Fn::GetAtt': [webhookId, 'Arn'] },
    });
  });

  test('SQS を 1 件ずつ消費し、部分失敗を通知する', () => {
    template.resourceCountIs('AWS::Lambda::EventSourceMapping', 1);
    template.hasResourceProperties('AWS::Lambda::EventSourceMapping', {
      EventSourceArn: { 'Fn::GetAtt': [queueId, 'Arn'] },
      FunctionName: { Ref: replyId },
      BatchSize: 1,
      FunctionResponseTypes: ['ReportBatchItemFailures'],
    });
  });

  test('両 Lambda は Secret を読み取り、Webhook だけがキューに送信する', () => {
    for (const functionId of [webhookId, replyId]) {
      const actions = roleStatements(functionId).flatMap((statement) => statement.Action);
      expect(actions).toContain('secretsmanager:GetSecretValue');
      expect(actions).not.toContain('secretsmanager:PutSecretValue');
    }
    const webhookActions = roleStatements(webhookId).flatMap((statement) => statement.Action);
    const replyActions = roleStatements(replyId).flatMap((statement) => statement.Action);
    expect(webhookActions).toContain('sqs:SendMessage');
    expect(webhookActions).not.toContain('sqs:ReceiveMessage');
    expect(webhookActions.some((action: string) => action.startsWith('s3:'))).toBe(false);
    expect(replyActions).toContain('sqs:ReceiveMessage');
    expect(replyActions).toContain('sqs:DeleteMessage');
    expect(replyActions).not.toContain('sqs:SendMessage');
  });

  test('Reply の S3 権限を面別の問題読み取りとコメント記録書き込みに限定する', () => {
    const statements = roleStatements(replyId);
    const s3Statements = statements.filter((statement) =>
      [statement.Action].flat().some((action: string) => action.startsWith('s3:')),
    );
    expect(s3Statements).toEqual([
      {
        Action: 's3:GetObject',
        Effect: 'Allow',
        Resource: stack.resolve(`${foundationStack.imagesBucket.bucketArn}/${problemsPrefix}*`),
      },
      {
        Action: 's3:PutObject',
        Effect: 'Allow',
        Resource: stack.resolve(`${foundationStack.imagesBucket.bucketArn}/comment-log/${setCode}/*`),
      },
    ]);
    expect(statements.flatMap((statement) => statement.Action)).not.toContain('*');
    expect(statements.flatMap((statement) => statement.Action).some(
      (action: string) => action.startsWith('kms:'),
    )).toBe(false);
    template.resourceCountIs('AWS::S3::BucketPolicy', 0);
    expect(foundationStack.dependencies).not.toContain(stack);
  });

  test('ロググループを明示し、保持期間を 90 日にする', () => {
    template.resourceCountIs('AWS::Logs::LogGroup', 2);
    for (const name of [webhookName, replyName]) {
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

  test('配布 asset は app/ だけを含み、キャッシュを含まない', () => {
    const assets = stack.node.findAll().filter(
      (node): node is cdk.AssetStaging => node instanceof cdk.AssetStaging,
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
      expect(fs.existsSync(path.join(asset.absoluteStagedPath, 'app/webhook_handler.py'))).toBe(true);
      expect(fs.existsSync(path.join(asset.absoluteStagedPath, 'app/reply_handler.py'))).toBe(true);
      expect(fs.existsSync(path.join(asset.absoluteStagedPath, 'app/prompts/haiku_judge.txt'))).toBe(true);
      checkContents(asset.absoluteStagedPath);
    }
  });

  test('接続先 URL と Secret 名を出力する', () => {
    const secret = stack.node.findChild('CredentialsSecret') as secretsmanager.Secret;
    template.hasOutput('FunctionUrl', { Value: stack.resolve(stack.functionUrl.url) });
    template.hasOutput('SecretName', { Value: stack.resolve(secret.secretName) });
    template.hasOutput('DlqUrl', { Value: stack.resolve(stack.replyDlq.queueUrl) });
    template.hasOutput('QueueUrl', { Value: { Ref: queueId } });
  });
});
