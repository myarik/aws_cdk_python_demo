"""
Simple lambda handler
"""

from typing import Any


def lambda_handler(event: dict[str, Any], context: Any) -> dict:
    """
    Simple lambda handler
    """
    return {"message": "Hello from Lambda!"}
