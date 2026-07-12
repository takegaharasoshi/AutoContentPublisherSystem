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
