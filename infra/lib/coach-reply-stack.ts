import * as path from 'path';
import * as cdk from 'aws-cdk-lib/core';
import * as iam from 'aws-cdk-lib/aws-iam';
import * as lambda from 'aws-cdk-lib/aws-lambda';
import * as logs from 'aws-cdk-lib/aws-logs';
import * as scheduler from 'aws-cdk-lib/aws-scheduler';
import * as schedulerTargets from 'aws-cdk-lib/aws-scheduler-targets';
import * as s3 from 'aws-cdk-lib/aws-s3';
import * as s3deploy from 'aws-cdk-lib/aws-s3-deployment';
import * as secretsmanager from 'aws-cdk-lib/aws-secretsmanager';
import * as ssm from 'aws-cdk-lib/aws-ssm';
import { Construct } from 'constructs';

export interface CoachReplyStackProps extends cdk.StackProps {
  /** 環境識別子（例: prod） */
  envName: string;
  /** 正解返信経路の本番面 / ステージング面 */
  face: 'prod' | 'staging';
  /** 問題スナップショットと判定済み状態を保存する共有バケット */
  assetsBucket: s3.IBucket;
}

/** 脳みそコーチの正解返信経路。Lambda は VPC 外で実行する。 */
export class CoachReplyStack extends cdk.Stack {
  /** 本番面の正解返信失敗を MonitoringStack で監視する Lambda */
  public readonly runFunction: lambda.Function;
  /** 週次で正解返信用トークンを更新する Lambda */
  public readonly tokenRefreshFunction: lambda.Function;

  constructor(scope: Construct, id: string, props: CoachReplyStackProps) {
    super(scope, id, props);

    const sfx = props.face === 'staging' ? '-staging' : '';
    const problemsPrefix = props.face === 'staging'
      ? 'assets/logic-training-1/staging/problems/'
      : 'assets/logic-training-1/problems/';
    const statePrefix = `coach-reply/logic-training-1${sfx}/state/`;
    const paramPrefix = `/acps/${props.envName}/coach-reply${sfx}/`;
    const runFunctionName = `acps-${props.envName}-coach-reply-run${sfx}`;
    const tokenRefreshFunctionName = `acps-${props.envName}-coach-reply-token-refresh${sfx}`;

    // 空の認証情報だけを定義し、値は作成後に手動投入する。
    const credentialsSecret = new secretsmanager.Secret(this, 'CredentialsSecret', {
      secretName: `acps/${props.envName}/logic-training-1/coach-reply${sfx}`,
      description:
        'Instagram coach reply credentials. Set ig_access_token, ig_user_id, token_expires_at and anthropic_api_key manually.',
      secretObjectValue: {
        ig_access_token: cdk.SecretValue.unsafePlainText(''),
        ig_user_id: cdk.SecretValue.unsafePlainText(''),
        token_expires_at: cdk.SecretValue.unsafePlainText(''),
        anthropic_api_key: cdk.SecretValue.unsafePlainText(''),
      },
      removalPolicy: cdk.RemovalPolicy.RETAIN,
    });

    // CloudFormation はプロパティが不変のリソースを更新しないため、CLI で変えた値は
    // 再デプロイで戻らない。この動作を保つため、テンプレートの初期値は今後変更しないこと。
    const replyEnabledParameter = new ssm.StringParameter(this, 'ReplyEnabledParameter', {
      parameterName: `${paramPrefix}reply-enabled`,
      stringValue: 'off',
      tier: ssm.ParameterTier.STANDARD,
    });
    new ssm.StringParameter(this, 'ReplyNotBeforeParameter', {
      parameterName: `${paramPrefix}reply-not-before`,
      stringValue: '2099-01-01T00:00:00Z',
      tier: ssm.ParameterTier.STANDARD,
    });

    // ランタイム同梱の boto3 を使い、配布するのは app/ のみ。
    // app/prompts/judge.md は実行時に必要なので README だけを除外する。
    const code = lambda.Code.fromAsset(
      path.join(__dirname, '../../services/coach-reply'),
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
          'README.md',
          'requirements*.txt',
          'pyproject.toml',
        ],
      },
    );

    const runLogGroup = new logs.LogGroup(this, 'RunLogGroup', {
      logGroupName: `/aws/lambda/${runFunctionName}`,
      retention: logs.RetentionDays.THREE_MONTHS,
      removalPolicy: cdk.RemovalPolicy.DESTROY,
    });
    const tokenRefreshLogGroup = new logs.LogGroup(this, 'TokenRefreshLogGroup', {
      logGroupName: `/aws/lambda/${tokenRefreshFunctionName}`,
      retention: logs.RetentionDays.THREE_MONTHS,
      removalPolicy: cdk.RemovalPolicy.DESTROY,
    });

    this.runFunction = new lambda.Function(this, 'RunFunction', {
      functionName: runFunctionName,
      runtime: lambda.Runtime.PYTHON_3_13,
      code,
      handler: 'app.run_handler.lambda_handler',
      memorySize: 256,
      timeout: cdk.Duration.seconds(300),
      reservedConcurrentExecutions: 1,
      retryAttempts: 0,
      logGroup: runLogGroup,
      environment: {
        SECRET_ARN: credentialsSecret.secretArn,
        ASSETS_BUCKET: props.assetsBucket.bucketName,
        PROBLEMS_PREFIX: problemsPrefix,
        STATE_PREFIX: statePrefix,
        PARAM_PREFIX: paramPrefix,
        GRAPH_API_BASE: 'https://graph.instagram.com/v25.0',
        JUDGE_MODEL: 'claude-haiku-5-5',
        JUDGE_EFFORT: 'high',
      },
    });
    this.runFunction.addToRolePolicy(new iam.PolicyStatement({
      actions: ['secretsmanager:GetSecretValue'],
      resources: [credentialsSecret.secretArn],
    }));
    this.runFunction.addToRolePolicy(new iam.PolicyStatement({
      actions: ['ssm:GetParameter'],
      resources: [this.formatArn({
        service: 'ssm',
        resource: 'parameter',
        resourceName: `${paramPrefix.slice(1)}*`,
        arnFormat: cdk.ArnFormat.SLASH_RESOURCE_NAME,
      })],
    }));

    // 共有バケットのポリシーを変更せず、FoundationStack への循環参照を避ける。
    // SSE-S3 のため KMS 権限は不要。ListBucket は存在しないキーを NoSuchKey として扱うために必要。
    this.runFunction.addToRolePolicy(new iam.PolicyStatement({
      actions: ['s3:GetObject'],
      resources: [
        `${props.assetsBucket.bucketArn}/${problemsPrefix}*`,
        `${props.assetsBucket.bucketArn}/${statePrefix}*`,
      ],
    }));
    this.runFunction.addToRolePolicy(new iam.PolicyStatement({
      actions: ['s3:PutObject'],
      resources: [`${props.assetsBucket.bucketArn}/${statePrefix}*`],
    }));
    this.runFunction.addToRolePolicy(new iam.PolicyStatement({
      actions: ['s3:ListBucket'],
      resources: [props.assetsBucket.bucketArn],
      conditions: {
        StringLike: { 's3:prefix': [`${problemsPrefix}*`, `${statePrefix}*`] },
      },
    }));

    this.tokenRefreshFunction = new lambda.Function(this, 'TokenRefreshFunction', {
      functionName: tokenRefreshFunctionName,
      runtime: lambda.Runtime.PYTHON_3_13,
      code,
      handler: 'app.token_refresh_handler.lambda_handler',
      memorySize: 128,
      timeout: cdk.Duration.seconds(60),
      retryAttempts: 0,
      logGroup: tokenRefreshLogGroup,
      environment: {
        SECRET_ARN: credentialsSecret.secretArn,
        REFRESH_API_BASE: 'https://graph.instagram.com',
      },
    });
    credentialsSecret.grantRead(this.tokenRefreshFunction);
    credentialsSecret.grantWrite(this.tokenRefreshFunction);

    if (props.face === 'prod') {
      new scheduler.Schedule(this, 'RunSchedule', {
        scheduleName: runFunctionName,
        schedule: scheduler.ScheduleExpression.cron({
          minute: '0',
          hour: '0,2,8,10,12,14,16,18,20,22',
          timeZone: cdk.TimeZone.ASIA_TOKYO,
        }),
        target: new schedulerTargets.LambdaInvoke(this.runFunction, {
          retryAttempts: 0,
          maxEventAge: cdk.Duration.hours(1),
        }),
      });
    }
    new scheduler.Schedule(this, 'TokenRefreshSchedule', {
      scheduleName: tokenRefreshFunctionName,
      schedule: scheduler.ScheduleExpression.cron({
        minute: '30',
        hour: '4',
        weekDay: 'MON',
        timeZone: cdk.TimeZone.ASIA_TOKYO,
      }),
      target: new schedulerTargets.LambdaInvoke(this.tokenRefreshFunction, {
        retryAttempts: 2,
        maxEventAge: cdk.Duration.hours(1),
      }),
    });

    new cdk.CfnOutput(this, 'RunFunctionName', {
      value: this.runFunction.functionName,
      description: '正解返信 Lambda の手動実行に使用する関数名',
    });
    new cdk.CfnOutput(this, 'SecretName', {
      value: credentialsSecret.secretName,
      description: '正解返信用の認証情報を設定する Secret 名',
    });
    new cdk.CfnOutput(this, 'ReplyEnabledParameterName', {
      value: replyEnabledParameter.parameterName,
      description: '正解返信の on / off を切り替える SSM パラメータ名',
    });
    new cdk.CfnOutput(this, 'TokenRefreshFunctionName', {
      value: this.tokenRefreshFunction.functionName,
      description: '正解返信用トークン更新 Lambda の手動実行に使用する関数名',
    });

    // 本番面の返信専用 Meta アプリ用。https のオブジェクト URL で公開する。
    if (props.face === 'prod') {
      const privacyPolicyBucket = new s3.Bucket(this, 'PrivacyPolicyBucket', {
        bucketName: `acps-${props.envName}-coach-reply-privacy-policy`,
        publicReadAccess: true,
        blockPublicAccess: new s3.BlockPublicAccess({
          blockPublicAcls: true,
          ignorePublicAcls: true,
          blockPublicPolicy: false,
          restrictPublicBuckets: false,
        }),
        encryption: s3.BucketEncryption.S3_MANAGED,
        removalPolicy: cdk.RemovalPolicy.RETAIN,
      });
      new s3deploy.BucketDeployment(this, 'PrivacyPolicyDeployment', {
        destinationBucket: privacyPolicyBucket,
        sources: [s3deploy.Source.asset(path.join(__dirname, '../assets/coach-reply-privacy-policy'))],
        contentType: 'text/html; charset=utf-8',
      });
      new cdk.CfnOutput(this, 'PrivacyPolicyUrl', {
        value: `https://${privacyPolicyBucket.bucketRegionalDomainName}/index.html`,
        description: '返信専用 Meta アプリの「プライバシーポリシーの URL」に設定する URL',
      });
    }
  }
}
