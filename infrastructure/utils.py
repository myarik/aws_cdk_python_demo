""" """

import os
import infrastructure.constants as constants


def get_stack_name() -> str:
    """
    Returns a stack name
    """
    cicd_environment = os.getenv("ENVIRONMENT", "dev")
    return f"{constants.SERVICE_NAME}{constants.DELIMITER}{cicd_environment}"
