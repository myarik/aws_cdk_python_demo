import json
from http import HTTPStatus

from service.handlers.demo_lambda import lambda_handler
from tests.service.utils import generate_api_lambda_event, generate_context


def test_get_users():
    response = lambda_handler(
        generate_api_lambda_event("/users", None), generate_context()
    )
    assert response["statusCode"] == HTTPStatus.OK
    response_body = json.loads(response["body"])
    assert len(response_body) == 10

    response = lambda_handler(
        generate_api_lambda_event(
            "/users", None, query_parameters={"is_active": "false"}
        ),
        generate_context(),
    )
    assert response["statusCode"] == HTTPStatus.OK
    response_body = json.loads(response["body"])
    assert len(response_body) == 2


def test_get_user():
    response = lambda_handler(
        generate_api_lambda_event(
            "/users/550e8400-e29b-41d4-a716-446655440008",
            None,
        ),
        generate_context(),
    )
    assert response["statusCode"] == HTTPStatus.OK
    response_body = json.loads(response["body"])
    assert response_body["email"] == "manager3@example.com"

    response = lambda_handler(
        generate_api_lambda_event(
            "/users/550e8400-e29b-41d4-a716-446655441118",
            None,
        ),
        generate_context(),
    )
    assert response["statusCode"] == HTTPStatus.NOT_FOUND


def test_create_user():
    response = lambda_handler(
        generate_api_lambda_event("/users", {"name": "test"}, method="POST"),
        generate_context(),
    )
    assert response["statusCode"] == HTTPStatus.UNPROCESSABLE_ENTITY

    response = lambda_handler(
        generate_api_lambda_event(
            "/users", {"email": "test@example.com"}, method="POST"
        ),
        generate_context(),
    )
    assert response["statusCode"] == HTTPStatus.CREATED


def test_update_user():
    response = lambda_handler(
        generate_api_lambda_event(
            "/users/550e8400-e29b-41d4-a716-446655440008",
            {"email": "test"},
            method="PUT",
        ),
        generate_context(),
    )
    assert response["statusCode"] == HTTPStatus.UNPROCESSABLE_ENTITY

    response = lambda_handler(
        generate_api_lambda_event(
            "/users/550e8400-e29b-41d4-a716-446655440008",
            {"email": "test@example.com"},
            method="PUT",
        ),
        generate_context(),
    )
    assert response["statusCode"] == HTTPStatus.OK
    response_body = json.loads(response["body"])
    assert response_body["email"] == "test@example.com"

    response = lambda_handler(
        generate_api_lambda_event(
            "/users/550e8400-e29b-41d4-a716-446655441118",
            {"email": "test@example.com"},
            method="PUT",
        ),
        generate_context(),
    )
    assert response["statusCode"] == HTTPStatus.NOT_FOUND


def test_delete_user():
    response = lambda_handler(
        generate_api_lambda_event(
            "/users/550e8400-e29b-41d4-a716-446655440008",
            None,
            method="DELETE",
        ),
        generate_context(),
    )
    assert response["statusCode"] == HTTPStatus.NO_CONTENT

    response = lambda_handler(
        generate_api_lambda_event(
            "/users/550e8400-e29b-41d4-a716-446655441118",
            None,
        ),
        generate_context(),
    )
    assert response["statusCode"] == HTTPStatus.NOT_FOUND
