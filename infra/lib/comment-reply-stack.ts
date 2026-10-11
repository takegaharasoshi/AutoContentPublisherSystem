import * as path from 'path';
import * as cdk from 'aws-cdk-lib/core';
import * as iam from 'aws-cdk-lib/aws-iam';
import * as lambda from 'aws-cdk-lib/aws-lambda';
import * as lambdaEventSources from 'aws-cdk-lib/aws-lambda-event-sources';
import * as logs from 'aws-cdk-lib/aws-logs';
import * as s3 from 'aws-cdk-lib/aws-s3';
import * as secretsmanager from 'aws-cdk-lib/aws-secretsmanager';
import * as sqs from 'aws-cdk-lib/aws-sqs';
import { Construct } from 'constructs';

export interface CommentReplyStackProps extends cdk.StackProps {
  /** 環境識別子（例: prod） */
  envName: string;
  /** コメント返信経路の本番面 / ステージング面 */
  face: 'prod' | 'staging';
  /** 問題スナップショットとコメント記録を保存する共有バケット */
  assetsBucket: s3.IBucket;
}

/** ウミガメのスープのコメント自動返信経路。Lambda は VPC 外で実行する。 */
export class CommentReplyStack extends cdk.Stack {
  /** 本番面の返信失敗を MonitoringStack で監視する DLQ */
  public readonly replyDlq: sqs.Queue;
  /** Meta Webhook の受信先 */
  public readonly functionUrl: lambda.FunctionUrl;

  constructor(scope: Construct, id: string, props: CommentReplyStackProps) {
    super(scope, id, props);

    const sfx = props.face === 'staging' ? '-staging' : '';
    const problemsPrefix = props.face === 'staging'
      ? 'assets/umigame-soup-1/staging/problems/'
      : 'assets/umigame-soup-1/problems/';
    const setCode = `umigame-soup-1${sfx}`;
    const webhookFunctionName = `acps-${props.envName}-comment-reply-webhook${sfx}`;
    const replyFunctionName = `acps-${props.envName}-comment-reply-reply${sfx}`;

    // verify_token だけを自動生成し、認証情報は作成後に手動投入する。
    const credentialsSecret = new secretsmanager.Secret(this, 'CredentialsSecret', {
      secretName: `acps/${props.envName}/umigame-soup-1/comment-reply${sfx}`,
      description:
        'Instagram comment reply credentials. verify_token is auto-generated. Set app_secret, ig_access_token, ig_user_id, token_expires_at, openai_api_key, typesafe_api_key and anthropic_api_key manually.',
      generateSecretString: {
        secretStringTemplate: JSON.stringify({
          app_secret: '',
          ig_access_token: '',
          ig_user_id: '',
          token_expires_at: '',
          openai_api_key: '',
          typesafe_api_key: '',
          anthropic_api_key: '',
        }),
        generateStringKey: 'verify_token',
        excludePunctuation: true,
      },
      removalPolicy: cdk.RemovalPolicy.RETAIN,
    });

    this.replyDlq = new sqs.Queue(this, 'ReplyDlq', {
      queueName: `acps-${props.envName}-comment-reply-dlq${sfx}.fifo`,
      fifo: true,
      retentionPeriod: cdk.Duration.days(14),
      encryption: sqs.QueueEncryption.SQS_MANAGED,
    });

    const replyQueue = new sqs.Queue(this, 'ReplyQueue', {
      queueName: `acps-${props.envName}-comment-reply${sfx}.fifo`,
      fifo: true,
      // 送信側が comment_id を MessageDeduplicationId に指定する。
      contentBasedDeduplication: false,
      retentionPeriod: cdk.Duration.days(4),
      // AWS 推奨に従い Reply Lambda のタイムアウト 120 秒の 6 倍にする。
      visibilityTimeout: cdk.Duration.seconds(720),
      deadLetterQueue: { queue: this.replyDlq, maxReceiveCount: 3 },
      encryption: sqs.QueueEncryption.SQS_MANAGED,
    });

    // ランタイム同梱の boto3 を使用するため、配布するのは app/ のみ。
    const code = lambda.Code.fromAsset(
      path.join(__dirname, '../../services/comment-reply'),
      {
        exclude: [
          '.gitignore',
          '.venv',
          'tests',
          'tools',
          'work',
          '.pytest_cache',
          '**/__pycache__',
          '**/*.pyc',
          '*.md',
          'requirements*.txt',
          'pyproject.toml',
        ],
      },
    );

    const webhookLogGroup = new logs.LogGroup(this, 'WebhookLogGroup', {
      logGroupName: `/aws/lambda/${webhookFunctionName}`,
      retention: logs.RetentionDays.THREE_MONTHS,
      removalPolicy: cdk.RemovalPolicy.DESTROY,
    });
    const replyLogGroup = new logs.LogGroup(this, 'ReplyLogGroup', {
      logGroupName: `/aws/lambda/${replyFunctionName}`,
      retention: logs.RetentionDays.THREE_MONTHS,
      removalPolicy: cdk.RemovalPolicy.DESTROY,
    });

    const webhookFunction = new lambda.Function(this, 'WebhookFunction', {
      functionName: webhookFunctionName,
      runtime: lambda.Runtime.PYTHON_3_13,
      code,
      handler: 'app.webhook_handler.lambda_handler',
      memorySize: 128,
      timeout: cdk.Duration.seconds(10),
      logGroup: webhookLogGroup,
      environment: {
        SECRET_ARN: credentialsSecret.secretArn,
        QUEUE_URL: replyQueue.queueUrl,
      },
    });
    credentialsSecret.grantRead(webhookFunction);
    replyQueue.grantSendMessages(webhookFunction);

    this.functionUrl = webhookFunction.addFunctionUrl({
      authType: lambda.FunctionUrlAuthType.NONE,
    });

    const replyFunction = new lambda.Function(this, 'ReplyFunction', {
      functionName: replyFunctionName,
      runtime: lambda.Runtime.PYTHON_3_13,
      code,
      handler: 'app.reply_handler.lambda_handler',
      memorySize: 256,
      timeout: cdk.Duration.seconds(120),
      reservedConcurrentExecutions: 2,
      logGroup: replyLogGroup,
      environment: {
        SECRET_ARN: credentialsSecret.secretArn,
        ASSETS_BUCKET: props.assetsBucket.bucketName,
        COMMENT_LOG_BUCKET: props.assetsBucket.bucketName,
        PROBLEMS_PREFIX: problemsPrefix,
        SET_CODE: setCode,
        GRAPH_API_BASE: 'https://graph.instagram.com/v23.0',
        JUDGE_MODE: 'haiku',
        REPLY_VARIANT: '1b-haiku',
        HAIKU_EFFORT: 'high',
        LUNA_EFFORT: 'xhigh',
        LUNA_MODEL: 'gpt-6-luna',
      },
    });
    credentialsSecret.grantRead(replyFunction);
    replyFunction.addEventSource(new lambdaEventSources.SqsEventSource(replyQueue, {
      batchSize: 1,
      reportBatchItemFailures: true,
    }));

    // バケットポリシーを変更せず、FoundationStack への循環参照を避ける。
    // 共有バケットは SSE-S3 のため KMS 権限は不要。
    replyFunction.addToRolePolicy(new iam.PolicyStatement({
      actions: ['s3:GetObject'],
      resources: [`${props.assetsBucket.bucketArn}/${problemsPrefix}*`],
    }));
    replyFunction.addToRolePolicy(new iam.PolicyStatement({
      actions: ['s3:PutObject'],
      resources: [`${props.assetsBucket.bucketArn}/comment-log/${setCode}/*`],
    }));

    new cdk.CfnOutput(this, 'FunctionUrl', {
      value: this.functionUrl.url,
      description: 'Meta Webhook に設定する Lambda Function URL',
    });
    new cdk.CfnOutput(this, 'SecretName', {
      value: credentialsSecret.secretName,
      description: 'コメント返信用の認証情報を設定する Secret 名',
    });
    new cdk.CfnOutput(this, 'DlqUrl', {
      value: this.replyDlq.queueUrl,
      description: '返信失敗メッセージを確認する DLQ URL',
    });
    new cdk.CfnOutput(this, 'QueueUrl', {
      value: replyQueue.queueUrl,
      description: 'コメント返信メッセージの送信先 FIFO キュー URL',
    });
  }
}
