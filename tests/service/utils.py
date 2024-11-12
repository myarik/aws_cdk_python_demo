import json
from typing import Optional, Any

from aws_lambda_powertools.utilities.typing import LambdaContext


def generate_context() -> LambdaContext:
    context = LambdaContext()
    context._aws_request_id = "888888"
    context._function_name = "test"
    context._memory_limit_in_mb = 128
    context._invoked_function_arn = (
        "arn:aws:lambda:eu-west-1:123456789012:function:test"
    )
    return context


def generate_api_lambda_event(
    path: str,
    body: Optional[dict[str, Any]],
    query_parameters: Optional[dict[str, str]] = None,
    method: str = "GET",
) -> dict[str, Any]:
    return {
        "version": "2.0",
        "routeKey": "$default",
        "rawPath": path,
        "rawQueryString": "",
        "cookies": ["cookie1", "cookie2"],
        "headers": {"header1": "value1", "header2": "value1,value2"},
        "queryStringParameters": query_parameters if query_parameters else {},
        "requestContext": {
            "accountId": "123456789012",
            "apiId": "<urlid>",
            "authentication": None,
            "authorizer": {
                "iam": {
                    "accessKey": "AKIA...",
                    "accountId": "111122223333",
                    "callerId": "AIDA...",
                    "cognitoIdentity": None,
                    "principalOrgId": None,
                    "userArn": "arn:aws:iam::111122223333:user/example-user",
                    "userId": "AIDA...",
                }
            },
            "domainName": "<url-id>.lambda-url.us-west-2.on.aws",
            "domainPrefix": "<url-id>",
            "http": {
                "method": method,
                "path": path,
                "protocol": "HTTP/1.1",
                "sourceIp": "123.123.123.123",
                "userAgent": "agent",
            },
            "requestId": "id",
            "routeKey": "$default",
            "stage": "$default",
            "time": "12/Mar/2020:19:03:58 +0000",
            "timeEpoch": 1583348638390,
        },
        "body": "" if body is None else json.dumps(body),
        "pathParameters": None,
        "isBase64Encoded": False,
        "stageVariables": None,
    }
