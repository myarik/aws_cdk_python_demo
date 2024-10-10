"""
Simple lambda handler
"""

from aws_lambda_powertools import Logger
from aws_lambda_powertools.utilities.parser import event_parser
from aws_lambda_powertools.utilities.typing import LambdaContext
from jinja2 import Environment, DictLoader

from service.models.input import CreateTemplateRequest

env = Environment(
    loader=DictLoader(
        {
            "example_template": """
    <html>
        <head><title>{{ title }}</title></head>
        <body>
            <p>{{ content }}</p>
        </body>
    </html>
    """
        }
    ),
    autoescape=True,
)

logger: Logger = Logger()


@event_parser
def lambda_handler(event: CreateTemplateRequest, context: LambdaContext) -> str:
    """
    Simple lambda handler
    """
    logger.debug("Received event", extra={"event": event})
    template = env.get_template("example_template")
    rendered_output = template.render(event)
    return rendered_output
