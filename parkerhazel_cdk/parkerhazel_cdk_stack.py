from aws_cdk import (
    aws_lambda as lambda_,
    aws_dynamodb as dynamodb
)
import aws_cdk as cdk
from constructs import Construct
from os import path
from layers import get_requests_layer

class ParkerHazelSiteStack(cdk.Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        DEPLOY_TARGET = self.node.try_get_context("deploy_target") or "dev"

        def env_name(name):
            return f"{name}-{DEPLOY_TARGET}"
        
        requests_layer = get_requests_layer(self)

        # Create DynamoDB table for logging user visits
        visits_table = dynamodb.Table(self, "VisitsTable",
            partition_key=dynamodb.Attribute(name="userId", type=dynamodb.AttributeType.STRING),
            sort_key=dynamodb.Attribute(name="visitTimestamp", type=dynamodb.AttributeType.STRING),
            removal_policy=cdk.RemovalPolicy.DESTROY,  # For dev purposes; removes table on stack deletion
        )

        # Create Lambda function to handle logging visits
        logging_lambda = lambda_.Function(self, "LoggingLambda",
            function_name=env_name('LoggingLambda'),
            code=lambda_.Code.from_asset(path.join("parkerhazel_cdk", "LoggingLambda_fn")),
            handler="index.handler",
            runtime=lambda_.Runtime.PYTHON_3_8,
            layers=[ requests_layer ],
            timeout=cdk.Duration.seconds(30),
            environment={
                "DEPLOY_TARGET": DEPLOY_TARGET,
                "VISITS_TABLE": visits_table.table_name
            }
        )

        # Grant Lambda permissions to write to DynamoDB
        visits_table.grant_read_write_data(logging_lambda)
