import * as cdk from 'aws-cdk-lib/core';
import { Template } from 'aws-cdk-lib/assertions';
import { FoundationStack } from '../lib/foundation-stack';

test('FoundationStack が synth できる', () => {
  const app = new cdk.App();
  const stack = new FoundationStack(app, 'FoundationStack');
  const template = Template.fromStack(stack);

  // 1-1 時点ではリソースを定義していない（VPC は 1-2 で追加する）
  expect(template.toJSON().Resources ?? {}).toEqual({});
});
