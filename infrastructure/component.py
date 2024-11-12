"""
Service stack
"""

import getpass

from aws_cdk import Stack, Tags, Duration, CfnOutput
from constructs import Construct

import infrastructure.constants as constants
from infrastructure.lambdas import DemoLambdaConstruct
from infrastructure.monitoring import MonitoringDashboard


class PythonDemoStack(Stack):
    """
    Python Demo Stack
    """

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        self._add_stack_tags()

        # Monitoring dashboard
        monitoring_dashboard = MonitoringDashboard(
            self,
            f"{construct_id}{constants.DELIMITER}monitoring",
            "Observation",
        )

        # Create a simple lambda function
        demo_lambda_construct = DemoLambdaConstruct(
            self,
            f"{construct_id}{constants.DELIMITER}hello_lambda",
        )

        # Add lambda function metrics to the dashboard
        monitoring_dashboard.add_lambda_function_metrics(
            demo_lambda_construct.lambda_function
        )
        # Add alarms notifications
        monitoring_dashboard.add_p90_latency_lambda_alarm(
            demo_lambda_construct.construct_id,
            demo_lambda_construct.lambda_function,
            threshold_duration=Duration.seconds(30),
        )
        monitoring_dashboard.add_error_rate_lambda_alarm(
            demo_lambda_construct.construct_id,
            demo_lambda_construct.lambda_function,
            threshold_max_count=2,
        )

        # Return the URL of the lambda function
        CfnOutput(
            self,
            "URLLambdaFunction",
            value=demo_lambda_construct.lambda_function_url.url,
            description="URL Lambda Function",
        )

    def _add_stack_tags(self) -> None:
        # best practice to help identify resources in the console
        Tags.of(self).add(constants.SERVICE_NAME_TAG, constants.SERVICE_NAME)
        Tags.of(self).add(constants.OWNER_TAG, getpass.getuser())
