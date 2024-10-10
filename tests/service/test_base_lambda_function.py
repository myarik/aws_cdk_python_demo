from service.handlers.demo_lambda import lambda_handler


def test_lambda_handler():
    event, context = {}, {}
    assert lambda_handler(event, context) == {"message": "Hello from Lambda!"}
