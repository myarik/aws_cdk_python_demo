"""
Test Infrastructure
"""

import aws_cdk as core
import aws_cdk.assertions as assertions

from infrastructure.component import PythonDemoStack


def test_lambda_created():
    app = core.App()
    stack = PythonDemoStack(app, "demo-cdk-test")
    template = assertions.Template.from_stack(stack)

    # Extra function for log rotation
    template.resource_count_is("AWS::Lambda::Function", 2)
