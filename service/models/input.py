"""
Schema for input data
"""
from pydantic import BaseModel, Field


class CreateTemplateRequest(BaseModel):
    """
    Schema for input data
    """
    title: str = Field(..., description="Title of the template", min_length=3)
    content: str = Field(..., description="Content of the template")
