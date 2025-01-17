from aws_cdk import (
    aws_lambda as _lambda
)
from os import path

def get_requests_layer(stack):
    return _lambda.LayerVersion(stack, "requests",
                                code=_lambda.Code.from_asset(path.join("parkerhazel_cdk","requests_layer")),
                                compatible_runtimes=[_lambda.Runtime.PYTHON_3_8],
                                layer_version_name="requests",
                                description='A layer for the requests module'
                               )
