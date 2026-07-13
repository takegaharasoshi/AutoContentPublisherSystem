import * as cdk from 'aws-cdk-lib/core';
import { Annotations, Match, Template } from 'aws-cdk-lib/assertions';
import { FoundationStack } from '../lib/foundation-stack';

const createFoundationStack = (): FoundationStack => {
  const app = new cdk.App({
    context: { dbReadinessCheckImageTag: 'test-tag' },
  });

  return new FoundationStack(app, 'FoundationStack', { envName: 'prod' });
};

describe('FoundationStack の VPC', () => {
  const stack = createFoundationStack();
  const template = Template.fromStack(stack);

  test('VPC が 1 つ作成される', () => {
    template.resourceCountIs('AWS::EC2::VPC', 1);
  });

  test('Public Subnet x2 と Isolated Subnet x2 が作成される', () => {
    template.resourceCountIs('AWS::EC2::Subnet', 4);
    const publicSubnets = template.findResources('AWS::EC2::Subnet', {
      Properties: { MapPublicIpOnLaunch: true },
    });
    const isolatedSubnets = template.findResources('AWS::EC2::Subnet', {
      Properties: { MapPublicIpOnLaunch: false },
    });
    expect(Object.keys(publicSubnets)).toHaveLength(2);
    expect(Object.keys(isolatedSubnets)).toHaveLength(2);
  });

  test('NAT Gateway が作成されない', () => {
    template.resourceCountIs('AWS::EC2::NatGateway', 0);
  });

  test('Internet Gateway が 1 つ作成される', () => {
    template.resourceCountIs('AWS::EC2::InternetGateway', 1);
  });
});

describe('FoundationStack の画像保存用 S3 バケット', () => {
  const stack = createFoundationStack();
  const template = Template.fromStack(stack);

  test('S3 バケットが 1 つ作成される', () => {
    template.resourceCountIs('AWS::S3::Bucket', 1);
  });

  test('30 日で自動削除するライフサイクルルールが設定される', () => {
    template.hasResourceProperties('AWS::S3::Bucket', {
      LifecycleConfiguration: {
        Rules: [
          {
            ExpirationInDays: 30,
            Status: 'Enabled',
          },
        ],
      },
    });
  });

  test('Block Public Access がすべて有効になる', () => {
    template.hasResourceProperties('AWS::S3::Bucket', {
      PublicAccessBlockConfiguration: {
        BlockPublicAcls: true,
        BlockPublicPolicy: true,
        IgnorePublicAcls: true,
        RestrictPublicBuckets: true,
      },
    });
  });

  test('SSL 強制のバケットポリシーが設定される', () => {
    const bucketPolicies = template.findResources('AWS::S3::BucketPolicy');
    const statements = Object.values(bucketPolicies)[0].Properties.PolicyDocument.Statement;

    expect(statements).toEqual(
      expect.arrayContaining([
        expect.objectContaining({
          Action: 's3:*',
          Condition: {
            Bool: {
              'aws:SecureTransport': 'false',
            },
          },
          Effect: 'Deny',
          Principal: {
            AWS: '*',
          },
        }),
      ]),
    );
  });

  test('サーバーサイド暗号化が設定される', () => {
    template.hasResourceProperties('AWS::S3::Bucket', {
      BucketEncryption: {
        ServerSideEncryptionConfiguration: [
          {
            ServerSideEncryptionByDefault: {
              SSEAlgorithm: 'AES256',
            },
          },
        ],
      },
    });
  });

  test('バケットの DeletionPolicy が Delete である', () => {
    template.hasResource('AWS::S3::Bucket', {
      DeletionPolicy: 'Delete',
      UpdateReplacePolicy: 'Delete',
    });
  });
});

describe('FoundationStack の Security Group', () => {
  const stack = createFoundationStack();
  const template = Template.fromStack(stack);

  test('Security Group が 3 つ作成される', () => {
    template.resourceCountIs('AWS::EC2::SecurityGroup', 3);
  });

  test('バッチ共通 SG・DB 準備確認 SG は Ingress なしで必要な Egress のみを持つ', () => {
    const securityGroups = template.findResources('AWS::EC2::SecurityGroup');
    const findSecurityGroup = (description: string): [string, any] => {
      const securityGroup = Object.entries(securityGroups).find(
        ([, resource]) => resource.Properties.GroupDescription === description,
      );

      if (!securityGroup) {
        throw new Error(`Security Group not found: ${description}`);
      }

      return securityGroup;
    };
    const [batchSecurityGroupId, batchSecurityGroup] = findSecurityGroup(
      'Security group for ECS Fargate batch tasks',
    );
    const [dbReadinessCheckSecurityGroupId, dbReadinessCheckSecurityGroup] =
      findSecurityGroup('Security group for DB readiness check ECS tasks');
    const [auroraSecurityGroupId] = findSecurityGroup(
      'Security group for Aurora Serverless v2',
    );
    const httpsEgressRule = {
      CidrIp: '0.0.0.0/0',
      Description: 'Allow HTTPS access to external services',
      FromPort: 443,
      IpProtocol: 'tcp',
      ToPort: 443,
    };

    expect(batchSecurityGroup.Properties.SecurityGroupIngress).toBeUndefined();
    expect(batchSecurityGroup.Properties.SecurityGroupEgress).toEqual([httpsEgressRule]);
    expect(dbReadinessCheckSecurityGroup.Properties.SecurityGroupIngress).toBeUndefined();
    expect(dbReadinessCheckSecurityGroup.Properties.SecurityGroupEgress).toEqual([
      httpsEgressRule,
    ]);

    template.resourceCountIs('AWS::EC2::SecurityGroupEgress', 2);
    const egressRules = Object.values(
      template.findResources('AWS::EC2::SecurityGroupEgress'),
    );
    for (const sourceSecurityGroupId of [
      batchSecurityGroupId,
      dbReadinessCheckSecurityGroupId,
    ]) {
      expect(egressRules).toEqual(
        expect.arrayContaining([
          expect.objectContaining({
            Properties: expect.objectContaining({
              DestinationSecurityGroupId: {
                'Fn::GetAtt': [auroraSecurityGroupId, 'GroupId'],
              },
              FromPort: 3306,
              GroupId: { 'Fn::GetAtt': [sourceSecurityGroupId, 'GroupId'] },
              IpProtocol: 'tcp',
              ToPort: 3306,
            }),
          }),
        ]),
      );
    }
  });

  test('Aurora SG はバッチ SG 2 つからの MySQL Ingress とダミー Egress のみを持つ', () => {
    const securityGroups = template.findResources('AWS::EC2::SecurityGroup');
    const findSecurityGroup = (description: string): [string, any] => {
      const securityGroup = Object.entries(securityGroups).find(
        ([, resource]) => resource.Properties.GroupDescription === description,
      );

      if (!securityGroup) {
        throw new Error(`Security Group not found: ${description}`);
      }

      return securityGroup;
    };
    const [batchSecurityGroupId] = findSecurityGroup(
      'Security group for ECS Fargate batch tasks',
    );
    const [dbReadinessCheckSecurityGroupId] = findSecurityGroup(
      'Security group for DB readiness check ECS tasks',
    );
    const [auroraSecurityGroupId, auroraSecurityGroup] = findSecurityGroup(
      'Security group for Aurora Serverless v2',
    );

    expect(auroraSecurityGroup.Properties.SecurityGroupIngress).toBeUndefined();
    expect(auroraSecurityGroup.Properties.SecurityGroupEgress).toEqual([
      expect.objectContaining({
        CidrIp: '255.255.255.255/32',
        Description: 'Disallow all traffic',
      }),
    ]);

    template.resourceCountIs('AWS::EC2::SecurityGroupIngress', 2);
    const ingressRules = Object.values(
      template.findResources('AWS::EC2::SecurityGroupIngress'),
    );
    for (const sourceSecurityGroupId of [
      batchSecurityGroupId,
      dbReadinessCheckSecurityGroupId,
    ]) {
      expect(ingressRules).toEqual(
        expect.arrayContaining([
          expect.objectContaining({
            Properties: expect.objectContaining({
              FromPort: 3306,
              GroupId: { 'Fn::GetAtt': [auroraSecurityGroupId, 'GroupId'] },
              IpProtocol: 'tcp',
              SourceSecurityGroupId: {
                'Fn::GetAtt': [sourceSecurityGroupId, 'GroupId'],
              },
              ToPort: 3306,
            }),
          }),
        ]),
      );
    }
  });
});

describe('FoundationStack の画像生成 API キー用 Secret', () => {
  const stack = createFoundationStack();
  const template = Template.fromStack(stack);

  test('Secrets Manager Secret が 2 つ作成される', () => {
    template.resourceCountIs('AWS::SecretsManager::Secret', 2);
  });

  test('Secret 名が設定される', () => {
    template.hasResourceProperties('AWS::SecretsManager::Secret', {
      Name: 'acps/prod/image/api-key',
    });
  });

  test('生成する値の形式が設定される', () => {
    template.hasResourceProperties('AWS::SecretsManager::Secret', {
      GenerateSecretString: {
        SecretStringTemplate: '{}',
        GenerateStringKey: 'api_key',
      },
    });
  });
});

describe('FoundationStack の Aurora Serverless v2', () => {
  const stack = createFoundationStack();
  const template = Template.fromStack(stack);

  test('Aurora MySQL クラスターが必要な設定で作成される', () => {
    const securityGroups = template.findResources('AWS::EC2::SecurityGroup', {
      Properties: {
        GroupDescription: 'Security group for Aurora Serverless v2',
      },
    });
    const auroraSecurityGroupId = Object.keys(securityGroups)[0];

    template.resourceCountIs('AWS::RDS::DBCluster', 1);
    template.hasResourceProperties('AWS::RDS::DBCluster', {
      EngineVersion: '8.0.mysql_aurora.3.08.2',
      ServerlessV2ScalingConfiguration: {
        MinCapacity: 0,
        MaxCapacity: 1,
      },
      EnableHttpEndpoint: true,
      DatabaseName: 'acps',
      StorageEncrypted: true,
      VpcSecurityGroupIds: [
        {
          'Fn::GetAtt': [auroraSecurityGroupId, 'GroupId'],
        },
      ],
    });
  });

  test('クラスターの削除・置換時にはスナップショットを保持する', () => {
    template.hasResource('AWS::RDS::DBCluster', {
      DeletionPolicy: 'Snapshot',
      UpdateReplacePolicy: 'Snapshot',
    });
  });

  test('Serverless v2 Writer インスタンスが 1 つ作成される', () => {
    template.resourceCountIs('AWS::RDS::DBInstance', 1);
    template.hasResourceProperties('AWS::RDS::DBInstance', {
      DBInstanceClass: 'db.serverless',
    });
  });

  test('DB 認証情報 Secret 名が設定される', () => {
    template.hasResourceProperties('AWS::SecretsManager::Secret', {
      Name: 'acps/prod/db/credentials',
    });
  });

  test('DB Subnet Group が Isolated Subnet 2 つを参照する', () => {
    const subnetGroups = template.findResources('AWS::RDS::DBSubnetGroup');
    const isolatedSubnets = template.findResources('AWS::EC2::Subnet', {
      Properties: { MapPublicIpOnLaunch: false },
    });

    expect(Object.keys(subnetGroups)).toHaveLength(1);
    expect(Object.values(subnetGroups)[0].Properties.SubnetIds).toEqual(
      expect.arrayContaining(
        Object.keys(isolatedSubnets).map((subnetId) => ({ Ref: subnetId })),
      ),
    );
    expect(Object.values(subnetGroups)[0].Properties.SubnetIds).toHaveLength(2);
  });
});

describe('FoundationStack の ECS Cluster', () => {
  const stack = createFoundationStack();
  const template = Template.fromStack(stack);

  test('ECS Cluster が 1 つ作成される', () => {
    template.resourceCountIs('AWS::ECS::Cluster', 1);
  });
});

describe('FoundationStack の DB 準備確認タスク定義', () => {
  const stack = createFoundationStack();
  const template = Template.fromStack(stack);

  test('Fargate の family・CPU・メモリが設定される', () => {
    template.hasResourceProperties('AWS::ECS::TaskDefinition', {
      Family: 'acps-prod-db-readiness-check',
      Cpu: '256',
      Memory: '512',
      RequiresCompatibilities: ['FARGATE'],
    });
  });

  test('DB Secret を渡すコンテナと awslogs 設定が作成される', () => {
    template.hasResourceProperties('AWS::ECS::TaskDefinition', {
      ContainerDefinitions: [
        Match.objectLike({
          Name: 'db-readiness-check',
          Environment: Match.arrayWith([
            Match.objectLike({ Name: 'DB_SECRET_ARN' }),
            { Name: 'ENV_NAME', Value: 'prod' },
          ]),
          Image: {
            'Fn::Join': ['', Match.arrayWith([':test-tag'])],
          },
          LogConfiguration: {
            LogDriver: 'awslogs',
            Options: Match.objectLike({
              'awslogs-stream-prefix': 'db-readiness-check',
            }),
          },
        }),
      ],
    });
  });

  test('タスクロールは DB Secret の読み取りだけを許可する', () => {
    template.hasResourceProperties('AWS::IAM::Role', {
      AssumeRolePolicyDocument: Match.objectLike({
        Statement: Match.arrayWith([
          Match.objectLike({
            Principal: { Service: 'ecs-tasks.amazonaws.com' },
          }),
        ]),
      }),
      Policies: Match.arrayWith([
        Match.objectLike({
          PolicyDocument: Match.objectLike({
            Statement: Match.arrayWith([
              Match.objectLike({
                Action: 'secretsmanager:GetSecretValue',
                Resource: {
                  'Fn::Join': ['', Match.arrayWith([':secret:acps/prod/db/*'])],
                },
              }),
            ]),
          }),
        }),
      ]),
    });
  });

  test('ロググループは 90 日で削除される', () => {
    template.hasResource('AWS::Logs::LogGroup', {
      Properties: {
        RetentionInDays: 90,
      },
      DeletionPolicy: 'Delete',
    });
  });
});

describe('FoundationStack の DB 準備確認イメージタグ Context', () => {
  test('未指定時はエラーアノテーションを追加する', () => {
    const app = new cdk.App();
    const stack = new FoundationStack(app, 'FoundationStack', { envName: 'prod' });

    Annotations.fromStack(stack).hasError(
      '*',
      Match.stringLikeRegexp('.*-c dbReadinessCheckImageTag=<tag> の指定が必要.*'),
    );
  });
});

describe('FoundationStack の ECR リポジトリ', () => {
  const stack = createFoundationStack();
  const template = Template.fromStack(stack);
  const repositories = template.findResources('AWS::ECR::Repository');

  const findRepository = (repositoryName: string): any => {
    const repository = Object.values(repositories).find(
      (resource: any) => resource.Properties.RepositoryName === repositoryName,
    );

    if (!repository) {
      throw new Error(`ECR repository not found: ${repositoryName}`);
    }

    return repository;
  };

  const lifecyclePolicy = (repositoryName: string): object =>
    JSON.parse(
      findRepository(repositoryName).Properties.LifecyclePolicy.LifecyclePolicyText,
    );

  test('3 つのリポジトリが正しい名前で作成される', () => {
    expect(Object.keys(repositories)).toHaveLength(3);
    expect(Object.values(repositories)).toEqual(
      expect.arrayContaining([
        expect.objectContaining({
          Properties: expect.objectContaining({
            RepositoryName: 'auto-content-publisher/image-batch',
          }),
        }),
        expect.objectContaining({
          Properties: expect.objectContaining({
            RepositoryName: 'auto-content-publisher/sns-post-batch',
          }),
        }),
        expect.objectContaining({
          Properties: expect.objectContaining({
            RepositoryName: 'auto-content-publisher/db-readiness-check',
          }),
        }),
      ]),
    );
  });

  test.each([
    'auto-content-publisher/image-batch',
    'auto-content-publisher/sns-post-batch',
  ])('%s はリリース用と通常用のライフサイクルルールを持つ', (repositoryName) => {
    expect(lifecyclePolicy(repositoryName)).toEqual({
      rules: [
        {
          rulePriority: 1,
          description: 'Retain the latest 30 release images',
          selection: {
            tagStatus: 'tagged',
            tagPrefixList: ['release-'],
            countType: 'imageCountMoreThan',
            countNumber: 30,
          },
          action: { type: 'expire' },
        },
        {
          rulePriority: 2,
          description: 'Retain the latest 10 images',
          selection: {
            tagStatus: 'any',
            countType: 'imageCountMoreThan',
            countNumber: 10,
          },
          action: { type: 'expire' },
        },
      ],
    });
  });

  test('DB 準備確認リポジトリは最新 30 個を保持するライフサイクルルールを持つ', () => {
    expect(
      lifecyclePolicy('auto-content-publisher/db-readiness-check'),
    ).toEqual({
      rules: [
        {
          rulePriority: 1,
          description: 'Retain the latest 30 images',
          selection: {
            tagStatus: 'any',
            countType: 'imageCountMoreThan',
            countNumber: 30,
          },
          action: { type: 'expire' },
        },
      ],
    });
  });

  test('スタック削除時にリポジトリとイメージが削除される', () => {
    for (const repository of Object.values(repositories) as any[]) {
      expect(repository.Properties.EmptyOnDelete).toBe(true);
      expect(repository.DeletionPolicy).toBe('Delete');
      expect(repository.UpdateReplacePolicy).toBe('Delete');
    }
  });
});

describe('FoundationStack の VPC Endpoint', () => {
  const stack = createFoundationStack();
  const template = Template.fromStack(stack);

  test('S3 Gateway VPC Endpoint が 1 つ作成される', () => {
    template.resourceCountIs('AWS::EC2::VPCEndpoint', 1);
  });

  test('Gateway 型で S3 サービスを参照する', () => {
    template.hasResourceProperties('AWS::EC2::VPCEndpoint', {
      VpcEndpointType: 'Gateway',
      ServiceName: Match.objectLike({
        'Fn::Join': [
          '',
          Match.arrayWith(['com.amazonaws.', '.s3']),
        ],
      }),
    });
  });

  test('Public Subnet のルートテーブル 2 つだけに関連付けられる', () => {
    const endpoints = Object.values(template.findResources('AWS::EC2::VPCEndpoint'));

    expect(endpoints[0].Properties.RouteTableIds).toHaveLength(2);
  });
});
