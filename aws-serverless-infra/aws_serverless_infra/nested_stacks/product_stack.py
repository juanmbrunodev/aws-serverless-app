# Nested Stack that creates the Product Rest resource in AWS API Gateway
from aws_cdk import NestedStack
from aws_cdk.aws_apigateway import MockIntegration, RestApi, IntegrationResponse, PassthroughBehavior, MethodResponse

class ProductApiStack(NestedStack):

    def __init__(self, scope, *, restApiId, rootResourceId, parameters=None, timeout=None, notificationArns=None, removalPolicy=None): 
        super().__init__(scope, "restapi-products", parameters=parameters, timeout=timeout, notification_arns=notificationArns, removal_policy=removalPolicy)

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