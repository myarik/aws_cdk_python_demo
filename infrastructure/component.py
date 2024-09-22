"""
Service stack
"""

import getpass

from aws_cdk import Stack, Tags
from constructs import Construct

import infrastructure.constants as constants
from infrastructure.basic_lambda.construct import DemoLambdaConstruct


class PythonDemoStack(Stack):
    """
    Python Demo Stack
    """

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        self._add_stack_tags()

        # Create a simple lambda function
        DemoLambdaConstruct(
            self,
            f"{construct_id}{constants.DELIMITER}hello_lambda",
        )

    def _add_stack_tags(self) -> None:
        # best practice to help identify resources in the console
        Tags.of(self).add(constants.SERVICE_NAME_TAG, constants.SERVICE_NAME)
        Tags.of(self).add(constants.OWNER_TAG, getpass.getuser())
