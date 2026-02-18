"""
Task API endpoints.
Implements RESTful routes with proper HTTP status codes.
"""
from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session
from typing import Optional
from uuid import UUID

from app.database import get_db
from app.models import (
    TaskCreate, TaskUpdate, TaskResponse, 
    TaskListResponse, StandardResponse, TaskStatus, TaskPriority
)
from app import crud
from app.core.logging import get_logger

logger = get_logger(__name__)

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.post(
    "/",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new task",
    description="Create a new task with title, description, and priority"
)
def create_task(
    task: TaskCreate,
    db: Session = Depends(get_db)
) -> TaskResponse:
    """
    Create a new task.
    
    - **title**: Required, non-empty string
    - **description**: Optional description
    - **priority**: Low, Medium, or High (default: Medium)
    """
    logger.info(f"Creating task: {task.title}")
    created_task = crud.create_task(db, task)
    return created_task


@router.get(
    "/{task_id}",
    response_model=TaskResponse,
    status_code=status.HTTP_200_OK,
    summary="Get a single task",
    description="Retrieve a task by its ID"
)
def get_task(
    task_id: UUID,
    db: Session = Depends(get_db)
) -> TaskResponse:
    """
    Retrieve a single task by ID.
    
    Returns 404 if task not found or deleted.
    """
    logger.info(f"Retrieving task: {task_id}")
    task = crud.get_task_by_id(db, task_id)
    return task


@router.get(
    "/",
    response_model=TaskListResponse,
    status_code=status.HTTP_200_OK,
    summary="List all tasks",
    description="List tasks with filtering, sorting, and pagination"
)
def list_tasks(
    status_filter: Optional[TaskStatus] = Query(None, alias="status", description="Filter by status"),
    priority_filter: Optional[TaskPriority] = Query(None, alias="priority", description="Filter by priority"),
    sort_by: str = Query("created_at", description="Field to sort by"),
    sort_order: str = Query("desc", regex="^(asc|desc)$", description="Sort order: asc or desc"),
    page: int = Query(1, ge=1, description="Page number (starts from 1)"),
    page_size: int = Query(10, ge=1, le=100, description="Items per page (max 100)"),
    db: Session = Depends(get_db)
) -> TaskListResponse:
    """
    List tasks with advanced filtering and pagination.
    
    Features:
    - Filter by status (Pending/Completed)
    - Filter by priority (Low/Medium/High)
    - Sort by any field (default: created_at)
    - Pagination support
    """
    logger.info(f"Listing tasks - page: {page}, size: {page_size}")
    
    # Calculate skip for pagination
    skip = (page - 1) * page_size
    
    tasks, total = crud.get_tasks(
        db=db,
        status=status_filter,
        priority=priority_filter,
        sort_by=sort_by,
        sort_order=sort_order,
        skip=skip,
        limit=page_size
    )
    
    return TaskListResponse(
        total=total,
        page=page,
        page_size=page_size,
        tasks=tasks
    )


@router.put(
    "/{task_id}",
    response_model=TaskResponse,
    status_code=status.HTTP_200_OK,
    summary="Update a task",
    description="Update task details (cannot update completed tasks)"
)
def update_task(
    task_id: UUID,
    task_update: TaskUpdate,
    db: Session = Depends(get_db)
) -> TaskResponse:
    """
    Update an existing task.
    
    Business Rule: Completed tasks cannot be modified.
    Returns 400 if attempting to update a completed task.
    """
    logger.info(f"Updating task: {task_id}")
    updated_task = crud.update_task(db, task_id, task_update)
    return updated_task


@router.patch(
    "/{task_id}/complete",
    response_model=TaskResponse,
    status_code=status.HTTP_200_OK,
    summary="Mark task as completed",
    description="Change task status to Completed"
)
def complete_task(
    task_id: UUID,
    db: Session = Depends(get_db)
) -> TaskResponse:
    """
    Mark a task as completed.
    
    Once completed, the task cannot be modified further.
    """
    logger.info(f"Marking task as completed: {task_id}")
    completed_task = crud.mark_task_completed(db, task_id)
    return completed_task


@router.delete(
    "/{task_id}",
    response_model=StandardResponse,
    status_code=status.HTTP_200_OK,
    summary="Delete a task",
    description="Soft delete a task (preserves data for audit)"
)
def delete_task(
    task_id: UUID,
    db: Session = Depends(get_db)
) -> StandardResponse:
    """
    Soft delete a task.
    
    Exploration Requirement: Soft Delete Implementation
    - Task is marked as deleted but not removed from database
    - Preserves data for audit trails and potential recovery
    - Deleted tasks are excluded from all queries
    """
    logger.info(f"Deleting task: {task_id}")
    crud.delete_task(db, task_id)
    return StandardResponse(
        success=True,
        message=f"Task {task_id} deleted successfully"
    )
