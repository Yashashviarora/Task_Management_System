"""
SQLAlchemy database models.
Defines the Task model with soft delete capability.
"""
from sqlalchemy import Column, String, DateTime, Boolean, Enum as SQLEnum, Index
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
import uuid

from app.database import Base
from app.models import TaskPriority, TaskStatus


class Task(Base):
    """
    Task model with soft delete support.
    
    Soft Delete Implementation (Exploration Requirement):
    - Uses 'is_deleted' flag instead of removing records
    - Preserves data for audit trails and recovery
    - Deleted tasks are filtered out in queries
    """
    __tablename__ = "tasks"
    
    # Primary key - UUID for distributed systems
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    
    # Required fields
    title = Column(String(255), nullable=False, index=True)
    
    # Optional fields
    description = Column(String(1000), nullable=True)
    
    # Enum fields with indexes for filtering
    priority = Column(SQLEnum(TaskPriority, values_callable=lambda x: [e.value for e in x]), nullable=False, default=TaskPriority.MEDIUM, index=True)
    status = Column(SQLEnum(TaskStatus, values_callable=lambda x: [e.value for e in x]), nullable=False, default=TaskStatus.PENDING, index=True)
    
    # Timestamps
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Soft delete flag (Exploration Requirement)
    is_deleted = Column(Boolean, nullable=False, default=False, index=True)
    deleted_at = Column(DateTime, nullable=True)
    
    # Composite indexes for common query patterns
    __table_args__ = (
        Index('idx_status_priority', 'status', 'priority'),
        Index('idx_deleted_created', 'is_deleted', 'created_at'),
    )
    
    def __repr__(self):
        return f"<Task(id={self.id}, title='{self.title}', status={self.status})>"
