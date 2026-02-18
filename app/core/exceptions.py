"""
Custom exception classes for the application.
Provides meaningful error messages and proper HTTP status codes.
"""
from fastapi import HTTPException, status


class TaskNotFoundException(HTTPException):
    """Raised when a task is not found in the database."""
    def __init__(self, task_id: str):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id '{task_id}' not found"
        )


class TaskAlreadyCompletedException(HTTPException):
    """Raised when attempting to modify a completed task."""
    def __init__(self, task_id: str):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cannot modify completed task '{task_id}'"
        )


class InvalidTaskDataException(HTTPException):
    """Raised when task data validation fails."""
    def __init__(self, message: str):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=message
        )


class UnauthorizedException(HTTPException):
    """Raised when authentication fails."""
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing authentication token"
        )
