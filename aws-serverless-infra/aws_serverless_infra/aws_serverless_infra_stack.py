from aws_cdk import (
    Stack
)
from constructs import Construct
from aws_cdk.aws_apigateway import RestApi, Deployment, Stage
# from product_stack import ProductApiStack
from aws_cdk import NestedStack
from aws_cdk.aws_apigateway import MockIntegration, RestApi, IntegrationResponse, PassthroughBehavior, MethodResponse

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

class ProductApiStack(NestedStack):

    def __init__(self, scope, *, restApiId, rootResourceId, parameters=None, timeout=None, notificationArns=None, removalPolicy=None): 
        super().__init__(scope, "integ-restapi-import-PetsStack", parameters=parameters, timeout=timeout, notification_arns=notificationArns, removal_policy=removalPolicy)

        api = RestApi.from_rest_api_attributes(self, "RestApi", rest_api_id=restApiId, root_resource_id=rootResourceId)

        # Add Product resource and a method for it, mock the integration response for the moment
        method = api.root.add_resource("product").add_method("GET", MockIntegration(
            integration_responses=[IntegrationResponse(status_code="200")],
            passthrough_behavior=PassthroughBehavior.NEVER,
            request_templates={"application/json": "{ 'statusCode': 200 }"}
        ),
            method_responses=[MethodResponse(status_code="200")]
        )

        self.methods = [method]

class DeployStack(NestedStack):
    def __init__(self, scope, *, restApiId, methods=None, parameters=None, timeout=None, notificationArns=None, removalPolicy=None):
        super().__init__(scope, "integ-restapi-import-DeployStack", parameters=parameters, timeout=timeout, notification_arns=notificationArns, removal_policy=removalPolicy)

        deployment = Deployment(self, "Deployment", api=RestApi.from_rest_api_id(self, "RestApi", restApiId))

        if methods:
            for method in methods:
                deployment.node.add_dependency(method)

        Stage(self, "Stage", deployment=deployment)