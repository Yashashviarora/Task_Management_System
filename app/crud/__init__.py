"""CRUD operations module."""
from app.crud.tasks import (
    create_task,
    get_task_by_id,
    get_tasks,
    update_task,
    mark_task_completed,
    delete_task
)

__all__ = [
    "create_task",
    "get_task_by_id",
    "get_tasks",
    "update_task",
    "mark_task_completed",
    "delete_task"
]
