import * as cdk from 'aws-cdk-lib/core';
import { Template } from 'aws-cdk-lib/assertions';
import { FoundationStack } from '../lib/foundation-stack';

describe('FoundationStack の VPC', () => {
  const app = new cdk.App();
  const stack = new FoundationStack(app, 'FoundationStack', { envName: 'prod' });
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
  const app = new cdk.App();
  const stack = new FoundationStack(app, 'FoundationStack', { envName: 'prod' });
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
  const app = new cdk.App();
  const stack = new FoundationStack(app, 'FoundationStack', { envName: 'prod' });
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
  const app = new cdk.App();
  const stack = new FoundationStack(app, 'FoundationStack', { envName: 'prod' });
  const template = Template.fromStack(stack);

  test('Secrets Manager Secret が 1 つ作成される', () => {
    template.resourceCountIs('AWS::SecretsManager::Secret', 1);
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

describe('FoundationStack の ECS Cluster', () => {
  const app = new cdk.App();
  const stack = new FoundationStack(app, 'FoundationStack', { envName: 'prod' });
  const template = Template.fromStack(stack);

  test('ECS Cluster が 1 つ作成される', () => {
    template.resourceCountIs('AWS::ECS::Cluster', 1);
  });
});
