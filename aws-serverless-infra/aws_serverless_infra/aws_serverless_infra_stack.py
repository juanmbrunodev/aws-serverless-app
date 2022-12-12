from aws_cdk import (
    Stack
)
from constructs import Construct
from aws_cdk.aws_apigateway import RestApi, Deployment, Stage
from aws_cdk import NestedStack
from aws_cdk.aws_apigateway import RestApi
from aws_serverless_infra.nested_stacks.product_stack import ProductApiStack

class AwsServerlessInfraStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Define the root API
        rest_api = RestApi(self, "RestApi", deploy = False)
        rest_api.root.add_method("ANY")

        # Create the nested stack for the Product resource (Rest resource)
        product_api = ProductApiStack(self, restApiId = rest_api.rest_api_id, rootResourceId = rest_api.rest_api_root_resource_id)

        # Deploy the Stack
        DeployStack(self, restApiId=rest_api.rest_api_id, methods=product_api.methods)

class DeployStack(NestedStack):
    def __init__(self, scope, *, restApiId, methods=None, parameters=None, timeout=None, notificationArns=None, removalPolicy=None):
        super().__init__(scope, "integ-restapi-import-DeployStack", parameters=parameters, timeout=timeout, notification_arns=notificationArns, removal_policy=removalPolicy)

        deployment = Deployment(self, "Deployment", api=RestApi.from_rest_api_id(self, "RestApi", restApiId))

        if methods:
            for method in methods:
                deployment.node.add_dependency(method)

        Stage(self, "Staging", deployment=deployment)