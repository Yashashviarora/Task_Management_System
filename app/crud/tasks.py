"""
CRUD operations for Task management.
Implements business rules and database queries with soft delete support.
"""
from sqlalchemy.orm import Session
from sqlalchemy import desc, asc
from typing import Optional, List
from uuid import UUID
from datetime import datetime

from app.schemas import Task
from app.models import TaskStatus, TaskPriority, TaskCreate, TaskUpdate
from app.core.exceptions import TaskNotFoundException, TaskAlreadyCompletedException
from app.core.logging import get_logger

logger = get_logger(__name__)


def create_task(db: Session, task_data: TaskCreate) -> Task:
    """
    Create a new task in the database.
    
    Args:
        db: Database session
        task_data: Task creation data
    
    Returns:
        Created task object
    """
    task = Task(
        title=task_data.title,
        description=task_data.description,
        priority=task_data.priority,
        status=TaskStatus.PENDING
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    
    logger.info(f"Task created: {task.id}")
    return task


def get_task_by_id(db: Session, task_id: UUID) -> Task:
    """
    Retrieve a single task by ID.
    Excludes soft-deleted tasks.
    
    Args:
        db: Database session
        task_id: Task UUID
    
    Returns:
        Task object
    
    Raises:
        TaskNotFoundException: If task not found or deleted
    """
    task = db.query(Task).filter(
        Task.id == task_id,
        Task.is_deleted == False  # Soft delete filter
    ).first()
    
    if not task:
        logger.warning(f"Task not found: {task_id}")
        raise TaskNotFoundException(str(task_id))
    
    return task


def get_tasks(
    db: Session,
    status: Optional[TaskStatus] = None,
    priority: Optional[TaskPriority] = None,
    sort_by: str = "created_at",
    sort_order: str = "desc",
    skip: int = 0,
    limit: int = 100
) -> tuple[List[Task], int]:
    """
    List tasks with filtering, sorting, and pagination.
    
    Args:
        db: Database session
        status: Filter by status (optional)
        priority: Filter by priority (optional)
        sort_by: Field to sort by (default: created_at)
        sort_order: Sort order - 'asc' or 'desc' (default: desc)
        skip: Number of records to skip (pagination)
        limit: Maximum number of records to return
    
    Returns:
        Tuple of (tasks list, total count)
    """
    # Base query - exclude soft-deleted tasks
    query = db.query(Task).filter(Task.is_deleted == False)
    
    # Apply filters
    if status:
        query = query.filter(Task.status == status)
        logger.debug(f"Filtering by status: {status}")
    
    if priority:
        query = query.filter(Task.priority == priority)
        logger.debug(f"Filtering by priority: {priority}")
    
    # Get total count before pagination
    total = query.count()
    
    # Apply sorting
    sort_column = getattr(Task, sort_by, Task.created_at)
    if sort_order == "asc":
        query = query.order_by(asc(sort_column))
    else:
        query = query.order_by(desc(sort_column))
    
    # Apply pagination
    tasks = query.offset(skip).limit(limit).all()
    
    logger.info(f"Retrieved {len(tasks)} tasks (total: {total})")
    return tasks, total


def update_task(db: Session, task_id: UUID, task_data: TaskUpdate) -> Task:
    """
    Update an existing task.
    
    Business Rule: Completed tasks cannot be modified.
    
    Args:
        db: Database session
        task_id: Task UUID
        task_data: Updated task data
    
    Returns:
        Updated task object
    
    Raises:
        TaskNotFoundException: If task not found
        TaskAlreadyCompletedException: If task is completed
    """
    task = get_task_by_id(db, task_id)
    
    # Business Rule: Completed tasks cannot be modified
    if task.status == TaskStatus.COMPLETED:
        logger.warning(f"Attempt to modify completed task: {task_id}")
        raise TaskAlreadyCompletedException(str(task_id))
    
    # Update only provided fields
    update_data = task_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(task, field, value)
    
    task.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(task)
    
    logger.info(f"Task updated: {task_id}")
    return task


def mark_task_completed(db: Session, task_id: UUID) -> Task:
    """
    Mark a task as completed.
    
    Args:
        db: Database session
        task_id: Task UUID
    
    Returns:
        Updated task object
    
    Raises:
        TaskNotFoundException: If task not found
    """
    task = get_task_by_id(db, task_id)
    
    task.status = TaskStatus.COMPLETED
    task.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(task)
    
    logger.info(f"Task marked as completed: {task_id}")
    return task


def delete_task(db: Session, task_id: UUID) -> None:
    """
    Soft delete a task.
    
    Exploration Requirement: Soft Delete Implementation
    - Sets is_deleted flag to True instead of removing record
    - Preserves data for audit trails
    - Allows potential recovery
    
    Args:
        db: Database session
        task_id: Task UUID
    
    Raises:
        TaskNotFoundException: If task not found
    """
    task = get_task_by_id(db, task_id)
    
    # Soft delete implementation
    task.is_deleted = True
    task.deleted_at = datetime.utcnow()
    db.commit()
    
    logger.info(f"Task soft deleted: {task_id}")
