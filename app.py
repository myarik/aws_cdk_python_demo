#!/usr/bin/env python3
import os

import aws_cdk as cdk

from infrastructure.component import PythonDemoStack

from infrastructure.utils import get_stack_name

app = cdk.App()

PythonDemoStack(
    app,
    get_stack_name(),
    env=cdk.Environment(
        account=os.getenv("AWS_DEFAULT_ACCOUNT"), region=os.getenv("AWS_DEFAULT_REGION")
    ),
)

app.synth()
