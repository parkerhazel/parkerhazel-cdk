from aws_cdk import (
    core,
    aws_lambda as _lambda,
    aws_dynamodb as dynamodb,
    aws_iam as iam,
)
from os import path

class ParkerHazelSiteStack(core.Stack):
    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        DEPLOY_TARGET = self.node.try_get_context("deploy_target") or "dev"

        def env_name(name):
            return f"{name}-{DEPLOY_TARGET}"

        # Create DynamoDB table for logging user visits
        visits_table = dynamodb.Table(self, "VisitsTable",
            partition_key=dynamodb.Attribute(name="userId", type=dynamodb.AttributeType.STRING),
            sort_key=dynamodb.Attribute(name="visitTimestamp", type=dynamodb.AttributeType.STRING),
            removal_policy=core.RemovalPolicy.DESTROY,  # For dev purposes; removes table on stack deletion
        )

        # Create Lambda function to handle logging visits
        logging_lambda = _lambda.Function(self, "LoggingLambda",
            function_name=env_name('LoggingLambda'),
            code=_lambda.Code.from_asset(path.join("gbc_eventbridge", "LoggingLambda_fn")),
            handler="index.handler",
            runtime=_lambda.Runtime.PYTHON_3_8,
            layers=[],
            timeout=core.Duration.seconds(30),
            environment={
                "DEPLOY_TARGET": DEPLOY_TARGET,
                "VISITS_TABLE": visits_table.table_name
            }
        )

        # Grant Lambda permissions to write to DynamoDB
        visits_table.grant_read_write_data(logging_lambda)
