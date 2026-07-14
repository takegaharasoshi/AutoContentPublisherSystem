import * as cdk from 'aws-cdk-lib/core';
import * as ecs from 'aws-cdk-lib/aws-ecs';
import * as ecr from 'aws-cdk-lib/aws-ecr';
import * as iam from 'aws-cdk-lib/aws-iam';
import * as logs from 'aws-cdk-lib/aws-logs';
import * as rds from 'aws-cdk-lib/aws-rds';
import * as s3 from 'aws-cdk-lib/aws-s3';
import * as secretsmanager from 'aws-cdk-lib/aws-secretsmanager';
import { Construct } from 'constructs';

export interface ImageBatchStackProps extends cdk.StackProps {
  /** 環境識別子（例: prod） */
  envName: string;
  /** 画像生成バッチのコンテナイメージ用 ECR リポジトリ */
  imageBatchRepository: ecr.Repository;
  /** 生成画像を保存する共有 S3 バケット */
  imagesBucket: s3.Bucket;
  /** Aurora Serverless v2 クラスター */
  auroraCluster: rds.DatabaseCluster;
  /** 画像生成 API キー用の Secret */
  imageApiKeySecret: secretsmanager.Secret;
}

/**
 * 画像生成バッチ実行基盤スタック。
 * リソースは docs/infra/stacks.html セクション 3.2 に沿って段階的に追加する。
 */
export class ImageBatchStack extends cdk.Stack {
  /** 画像生成バッチのタスク定義。Step Functions から family 名で参照される */
  public readonly taskDefinition: ecs.FargateTaskDefinition;

  constructor(scope: Construct, id: string, props: ImageBatchStackProps) {
    super(scope, id, props);

    const contextImageTag = this.node.tryGetContext('imageBatchImageTag');
    const hasImageBatchImageTag =
      typeof contextImageTag === 'string' && contextImageTag.trim().length > 0;
    const imageBatchImageTag =
      hasImageBatchImageTag ? contextImageTag.trim() : 'MISSING';

    if (!hasImageBatchImageTag) {
      // CDK はデプロイ対象外のスタックも synth するため、throw すると他スタックのデプロイも失敗する。
      cdk.Annotations.of(this).addError(
        '-c imageBatchImageTag=<tag> の指定が必要です。',
      );
    }

    const taskRole = new iam.Role(this, 'ImageBatchTaskRole', {
      assumedBy: new iam.ServicePrincipal('ecs-tasks.amazonaws.com'),
      inlinePolicies: {
        ReadSecrets: new iam.PolicyDocument({
          statements: [
            new iam.PolicyStatement({
              actions: ['secretsmanager:GetSecretValue'],
              resources: [
                `arn:aws:secretsmanager:${this.region}:${this.account}:secret:acps/${props.envName}/db/*`,
                `arn:aws:secretsmanager:${this.region}:${this.account}:secret:acps/${props.envName}/image/*`,
              ],
            }),
          ],
        }),
      },
    });

    props.imagesBucket.grantReadWrite(taskRole);

    const logGroup = new logs.LogGroup(this, 'ImageBatchLogGroup', {
      retention: logs.RetentionDays.THREE_MONTHS,
      removalPolicy: cdk.RemovalPolicy.DESTROY,
    });

    const dbSecretArn = props.auroraCluster.secret?.secretArn;
    if (!dbSecretArn) {
      throw new Error('Aurora クラスターの認証情報 Secret が見つかりません。');
    }

    this.taskDefinition = new ecs.FargateTaskDefinition(
      this,
      'ImageBatchTaskDefinition',
      {
        family: `acps-${props.envName}-image-batch`,
        cpu: 256,
        memoryLimitMiB: 512,
        taskRole,
      },
    );

    this.taskDefinition.addContainer('ImageBatchContainer', {
      containerName: 'image-batch',
      image: ecs.ContainerImage.fromEcrRepository(
        props.imageBatchRepository,
        imageBatchImageTag,
      ),
      environment: {
        DB_SECRET_ARN: dbSecretArn,
        API_SECRET_ARN: props.imageApiKeySecret.secretArn,
        S3_BUCKET_NAME: props.imagesBucket.bucketName,
        ENV_NAME: props.envName,
      },
      logging: ecs.LogDrivers.awsLogs({
        logGroup,
        streamPrefix: 'image-batch',
      }),
    });
  }
}
