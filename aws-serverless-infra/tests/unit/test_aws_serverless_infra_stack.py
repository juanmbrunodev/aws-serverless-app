import aws_cdk as core
import aws_cdk.assertions as assertions

from aws_serverless_infra.aws_serverless_infra_stack import AwsServerlessInfraStack

# example tests. To run these tests, uncomment this file along with the example
# resource in aws_serverless_infra/aws_serverless_infra_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = AwsServerlessInfraStack(app, "aws-serverless-infra")
    template = assertions.Template.from_stack(stack)

    print("Executing Unit Test...")
    template.has_resource_properties("AWS::SQS::Queue", {
        "VisibilityTimeout": 300
    })


test_sqs_queue_created()