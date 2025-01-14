#!/usr/bin/env python
import os

import aws_cdk as cdk

from parkerhazel_cdk.parkerhazel_cdk_stack import ParkerHazelSiteStack


app = cdk.App()

DEPLOY_TARGET = app.node.try_get_context("deploy_target") or "dev"

print(f"DEPLOY_TARGET: {DEPLOY_TARGET}")

ParkerHazelSiteStack(app, f"ParkerHazelSiteStack-{DEPLOY_TARGET}",
    # If you don't specify 'env', this stack will be environment-agnostic.
    # Account/Region-dependent features and context lookups will not work,
    # but a single synthesized template can be deployed anywhere.

    # Uncomment the next line to specialize this stack for the AWS Account
    # and Region that are implied by the current CLI configuration.

    #env=cdk.Environment(account=os.getenv('CDK_DEFAULT_ACCOUNT'), region=os.getenv('CDK_DEFAULT_REGION')),

    # Uncomment the next line if you know exactly what Account and Region you
    # want to deploy the stack to. */

    #env=cdk.Environment(account='123456789012', region='us-east-1'),

    # For more information, see https://docs.aws.amazon.com/cdk/latest/guide/environments.html
    )

app.synth()
