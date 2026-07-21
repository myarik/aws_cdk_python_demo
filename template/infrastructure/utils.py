""" """

import os
import infrastructure.constants as constants


def get_stack_name() -> str:
    """
    Returns a stack name
    """
    cicd_environment = os.getenv("ENVIRONMENT", "dev")
    return f"{cicd_environment}-{constants.PROJECT_NAME}"


def get_monitoring_stack_name() -> str:
    """
    Returns the monitoring stack name
    """
    cicd_environment = os.getenv("ENVIRONMENT", "dev")
    return f"{cicd_environment}-monitoring-{constants.PROJECT_NAME}"
