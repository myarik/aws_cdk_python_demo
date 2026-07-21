"""
Shared fixtures for infrastructure tests
"""

import pytest
import aws_cdk as core
import aws_cdk.assertions as assertions

from infrastructure.component import PythonDemoMonitoringStack, PythonDemoStack
from infrastructure.utils import get_monitoring_stack_name, get_stack_name


@pytest.fixture(scope="session")
def _stacks():
    app = core.App()
    lambda_stack = PythonDemoStack(app, get_stack_name())
    monitoring_stack = PythonDemoMonitoringStack(
        app, get_monitoring_stack_name(), lambda_stack=lambda_stack
    )
    return lambda_stack, monitoring_stack


@pytest.fixture(scope="session")
def lambda_template(_stacks):
    return assertions.Template.from_stack(_stacks[0])


@pytest.fixture(scope="session")
def monitoring_template(_stacks):
    return assertions.Template.from_stack(_stacks[1])
