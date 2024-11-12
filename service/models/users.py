"""
User models
"""

from enum import Enum
from typing import Optional
from uuid import uuid4, UUID

from pydantic import BaseModel, Field, EmailStr


class UserRole(str, Enum):
    manager = "manager"
    customer = "customer"
    admin = "admin"


class User(BaseModel):
    """
    User model
    """

    user_id: UUID = Field(default_factory=uuid4, description="User ID", frozen=True)
    email: EmailStr
    role: UserRole = Field(..., description="User role")
    active: bool = Field(True, description="User is active")


class UserUpdate(BaseModel):
    """
    User update model
    """

    email: Optional[EmailStr] = None
    role: Optional[UserRole] = None
    active: Optional[bool] = None


class UserCreate(BaseModel):
    """
    User update model
    """

    email: EmailStr
    role: UserRole = Field(default=UserRole.customer, description="User role")
