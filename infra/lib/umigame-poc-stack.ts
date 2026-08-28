import * as path from 'path';
import * as cdk from 'aws-cdk-lib/core';
import * as lambda from 'aws-cdk-lib/aws-lambda';
import * as secretsmanager from 'aws-cdk-lib/aws-secretsmanager';
import { Construct } from 'constructs';

export interface UmigamePocStackProps extends cdk.StackProps {
  /** 環境識別子（例: prod） */
  envName: string;
}

/**
 * ウミガメのスープ Instagram コメント Webhook PoC スタック。
 * VPC を介さず、Lambda Function URL で Meta Webhook を直接受信する。
 */
export class UmigamePocStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props: UmigamePocStackProps) {
    super(scope, id, props);

    // 値は作成後に AWS Console または CLI から手動で設定する。
    const credentialsSecret = new secretsmanager.Secret(this, 'CredentialsSecret', {
      secretName: 'umigame-poc/credentials',
      description:
        'Instagram comment webhook PoC credentials. verify_token is auto-generated. Set app_secret, ig_access_token, ig_user_id and optional openai_api_key manually.',
      generateSecretString: {
        // verify_token のみランダム自動生成し、そのまま Meta 側の Webhook 検証トークンに使う
        secretStringTemplate:
          '{"app_secret":"","ig_access_token":"","ig_user_id":"","openai_api_key":""}',
        generateStringKey: 'verify_token',
        excludePunctuation: true,
      },
      removalPolicy: cdk.RemovalPolicy.DESTROY,
    });

    const webhookFunction = new lambda.Function(this, 'WebhookFunction', {
      functionName: `acps-${props.envName}-umigame-comment-webhook`,
      runtime: lambda.Runtime.PYTHON_3_13,
      code: lambda.Code.fromAsset(
        path.join(__dirname, '../../poc/umigame-comment-webhook/lambda'),
      ),
      handler: 'handler.lambda_handler',
      timeout: cdk.Duration.seconds(30),
      memorySize: 256,
      environment: {
        SECRET_ARN: credentialsSecret.secretArn,
        GRAPH_API_BASE: 'https://graph.instagram.com/v23.0',
      },
    });
    credentialsSecret.grantRead(webhookFunction);

    const functionUrl = webhookFunction.addFunctionUrl({
      authType: lambda.FunctionUrlAuthType.NONE,
    });

    new cdk.CfnOutput(this, 'FunctionUrl', {
      value: functionUrl.url,
      description: 'Meta Webhook に設定する Lambda Function URL',
    });
    new cdk.CfnOutput(this, 'CredentialsSecretName', {
      value: credentialsSecret.secretName,
      description: 'PoC 認証情報を設定する Secrets Manager シークレット名',
    });
  }
}
