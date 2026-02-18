"""
Pydantic schemas for request validation and response serialization.
Ensures data integrity and automatic API documentation.
"""
from pydantic import BaseModel, Field, field_validator, ConfigDict
from typing import Optional
from datetime import datetime
from uuid import UUID
from enum import Enum


class TaskPriority(str, Enum):
    """Task priority levels - predefined values only."""
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"


class TaskStatus(str, Enum):
    """Task status - Pending or Completed."""
    PENDING = "Pending"
    COMPLETED = "Completed"


class TaskBase(BaseModel):
    """Base schema with common task fields."""
    model_config = ConfigDict(use_enum_values=True)
    
    title: str = Field(..., min_length=1, max_length=255, description="Task title (required, non-empty)")
    description: Optional[str] = Field(None, max_length=1000, description="Task description (optional)")
    priority: TaskPriority = Field(default=TaskPriority.MEDIUM.value, description="Task priority level")
    
    @field_validator('title')
    @classmethod
    def title_must_not_be_empty(cls, v: str) -> str:
        """Business Rule: Title must not be empty."""
        if not v or not v.strip():
            raise ValueError('Title must not be empty')
        return v.strip()


class TaskCreate(TaskBase):
    """Schema for creating a new task."""
    pass


class TaskUpdate(BaseModel):
    """
    Schema for updating an existing task.
    All fields are optional to support partial updates.
    """
    model_config = ConfigDict(use_enum_values=True)
    
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=1000)
    priority: Optional[TaskPriority] = None
    
    @field_validator('title')
    @classmethod
    def title_must_not_be_empty(cls, v: Optional[str]) -> Optional[str]:
        """Business Rule: Title must not be empty if provided."""
        if v is not None and (not v or not v.strip()):
            raise ValueError('Title must not be empty')
        return v.strip() if v else v


class TaskResponse(TaskBase):
    """
    Schema for task responses.
    Includes all fields from database model.
    """
    id: UUID
    status: TaskStatus
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True, use_enum_values=True)


class TaskListResponse(BaseModel):
    """
    Standardized response format for task listing.
    Includes pagination metadata.
    """
    total: int = Field(..., description="Total number of tasks matching filters")
    page: int = Field(..., description="Current page number")
    page_size: int = Field(..., description="Number of items per page")
    tasks: list[TaskResponse] = Field(..., description="List of tasks")


class StandardResponse(BaseModel):
    """
    Standardized API response format.
    Used for success messages and metadata.
    """
    success: bool = Field(default=True, description="Operation success status")
    message: str = Field(..., description="Response message")
    data: Optional[dict] = Field(None, description="Additional response data")
