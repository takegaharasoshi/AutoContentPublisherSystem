import * as cdk from 'aws-cdk-lib/core';
import { Template } from 'aws-cdk-lib/assertions';
import { FoundationStack } from '../lib/foundation-stack';

describe('FoundationStack の VPC', () => {
  const app = new cdk.App();
  const stack = new FoundationStack(app, 'FoundationStack');
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
