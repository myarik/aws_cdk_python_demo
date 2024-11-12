"""
Simple lambda handler
"""

from typing import List, Optional, Annotated
from uuid import UUID
from http import HTTPStatus

from aws_lambda_powertools import Logger, Tracer
from aws_lambda_powertools.event_handler import LambdaFunctionUrlResolver, Response
from aws_lambda_powertools.event_handler.exceptions import (
    BadRequestError,
    NotFoundError,
)
from aws_lambda_powertools.event_handler.openapi.params import Query, Path, Body
from aws_lambda_powertools.logging import correlation_paths
from aws_lambda_powertools.utilities.typing import LambdaContext

from service.logic.data import user_records
from service.models.users import User, UserRole, UserUpdate, UserCreate

tracer = Tracer()
logger: Logger = Logger()


app = LambdaFunctionUrlResolver(enable_validation=True)
app.enable_swagger(path="/swagger", title="Demo Lambda", description="Demo Lambda API")


@app.get(
    "/users",
    summary="Get all users",
    description="API returns all users",
    response_description="All users",
    responses={
        HTTPStatus.OK: {
            "description": "All users",
            "content": {"application/json": {"model": List[User]}},
        }
    },
    tags=["users"],
)
def get_users(
    is_active: Optional[bool] = None,
    role: Annotated[Optional[UserRole], Query()] = None,
) -> List[User]:
    """
    Get all users with optional filtering by active status and role.

    Args:
        is_active (Optional[bool]): Filter by user active status
        role (Optional[UserRole]): Filter by user role

    Returns:
        List[User]: List of filtered users
    """
    filtered_users = [User(**user_data) for user_data in user_records]

    if is_active is not None:
        filtered_users = [user for user in filtered_users if user.active == is_active]

    if role is not None:
        filtered_users = [user for user in filtered_users if user.role == role]

    return filtered_users


@app.get(
    "/users/<user_id>",
    summary="Get a user by ID",
    description="API to get a user by ID",
    response_description="User",
    responses={
        HTTPStatus.OK: {
            "description": "User",
            "content": {"application/json": {"model": User}},
        },
        HTTPStatus.NOT_FOUND: {
            "description": "User not found",
            "content": {},
        },
    },
    tags=["users"],
)
def get_user(user_id: Annotated[UUID, Path()]) -> User:
    """
    Get a user by their ID.

    Args:
        user_id: UUID of the user to be retrieved

    Raises:
        NotFoundError: If the user with the given UUID is not found

    Returns:
        User: User object
    """
    existing_users = [User(**user_data) for user_data in user_records]
    user = next((user for user in existing_users if user.user_id == user_id), None)

    if user is None:
        raise NotFoundError(f"User with ID {user_id} not found")

    return user


@app.post(
    "/users",
    summary="Create a new user",
    description="API to create a new user",
    response_description="The created user",
    responses={
        HTTPStatus.CREATED: {
            "description": "User created successfully",
            "content": {"application/json": {"model": User}},
        },
        HTTPStatus.BAD_REQUEST: {
            "description": "Invalid input data",
            "content": {},
        },
    },
    tags=["users"],
)
def create_user(new_user: Annotated[UserCreate, Body()]) -> Response[User]:
    """
    Create a new user if the email doesn't already exist.

    Args:
        new_user (UserCreate): User object to be created

    Returns:
         User: Created user object

    Raises:
        BadRequestError: If a user with the same email already exists
    """

    existing_users = [User(**user_data) for user_data in user_records]
    if any(user.email == new_user.email for user in existing_users):
        raise BadRequestError("User with this email already exists")
    user = User(**new_user.model_dump())
    logger.info("User created", extra={"user_id": user.user_id})
    return Response(
        status_code=HTTPStatus.CREATED,  # 200
        body=user.model_dump_json(),
    )


@app.put(
    "/users/<user_id>",
    summary="Update a user",
    description="API to update a user by ID",
    response_description="The updated user",
    responses={
        HTTPStatus.OK: {
            "description": "User updated successfully",
            "content": {"application/json": {"model": User}},
        },
        HTTPStatus.NOT_FOUND: {
            "description": "User not found",
            "content": {},
        },
    },
    tags=["users"],
)
def update_user(
    user_id: Annotated[UUID, Path()], user_update: Annotated[UserUpdate, Body()]
) -> User:
    """
    Update a user by their ID.

    Args:
        user_id: UUID of the user to be updated
        user_update: UserUpdate object containing the fields to update

    Raises:
        HTTPException: If the user with the given UUID is not found

    Returns:
        User: Updated user object
    """
    existing_users = [User.model_validate(user_data) for user_data in user_records]
    user_to_update = next(
        (user for user in existing_users if user.user_id == user_id), None
    )

    if user_to_update is None:
        raise NotFoundError(f"User with ID {user_id} not found")

    # Update user fields
    update_data = user_update.model_dump(exclude_unset=True)
    updated_user = user_to_update.model_copy(update=update_data)

    # In a real-world scenario, you would update the user in the database here
    # For this example, we'll just log the update
    logger.info("User updated", extra={"user_id": user_id})

    return updated_user


@app.delete(
    "/users/<user_id>",
    summary="Delete a user",
    description="API to delete a user by ID",
    response_description="No content",
    responses={
        HTTPStatus.NO_CONTENT: {
            "description": "204 No Content - returned when up to date",
            "content": {},
        },
        HTTPStatus.NOT_FOUND: {
            "description": "User not found",
            "content": {},
        },
    },
    tags=["users"],
)
def delete_user(user_id: Annotated[UUID, Path()]) -> Response[None]:
    """
    Delete a user by their ID.

    Args:
        user_id: UUID of the user to be deleted

    Raises:
        NotFoundError: If the user with the given UUID is not found

    Returns:
        None
    """
    logger.append_keys(user_id=user_id)
    existing_users = [User(**user_data) for user_data in user_records]
    user_to_delete = next(
        (user for user in existing_users if user.user_id == user_id), None
    )

    if user_to_delete is None:
        raise NotFoundError(f"User with ID {user_id} not found")

    # In a real-world scenario, you would delete the user from the database here
    # For this example, we'll just log the deletion
    logger.info("User deleted", extra={"user_id": user_id})
    return Response(status_code=HTTPStatus.NO_CONTENT)


@logger.inject_lambda_context(correlation_id_path=correlation_paths.LAMBDA_FUNCTION_URL)
@tracer.capture_lambda_handler
def lambda_handler(event: dict, context: LambdaContext) -> dict:
    """
    Simple lambda handler
    """
    return app.resolve(event, context)
