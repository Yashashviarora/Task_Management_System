"""Initial migration - create tasks table

Revision ID: 001
Revises: 
Create Date: 2024-01-01 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID

# revision identifiers, used by Alembic.
revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Create tasks table with all required fields and indexes."""
    op.create_table(
        'tasks',
        sa.Column('id', UUID(as_uuid=True), primary_key=True),
        sa.Column('title', sa.String(255), nullable=False),
        sa.Column('description', sa.String(1000), nullable=True),
        sa.Column('priority', sa.Enum('Low', 'Medium', 'High', name='taskpriority'), nullable=False),
        sa.Column('status', sa.Enum('Pending', 'Completed', name='taskstatus'), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('is_deleted', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('deleted_at', sa.DateTime(), nullable=True),
    )
    
    # Create indexes for performance
    op.create_index('ix_tasks_id', 'tasks', ['id'])
    op.create_index('ix_tasks_title', 'tasks', ['title'])
    op.create_index('ix_tasks_priority', 'tasks', ['priority'])
    op.create_index('ix_tasks_status', 'tasks', ['status'])
    op.create_index('ix_tasks_created_at', 'tasks', ['created_at'])
    op.create_index('ix_tasks_is_deleted', 'tasks', ['is_deleted'])
    
    # Composite indexes for common query patterns
    op.create_index('idx_status_priority', 'tasks', ['status', 'priority'])
    op.create_index('idx_deleted_created', 'tasks', ['is_deleted', 'created_at'])


def downgrade() -> None:
    """Drop tasks table and indexes."""
    op.drop_index('idx_deleted_created', 'tasks')
    op.drop_index('idx_status_priority', 'tasks')
    op.drop_index('ix_tasks_is_deleted', 'tasks')
    op.drop_index('ix_tasks_created_at', 'tasks')
    op.drop_index('ix_tasks_status', 'tasks')
    op.drop_index('ix_tasks_priority', 'tasks')
    op.drop_index('ix_tasks_title', 'tasks')
    op.drop_index('ix_tasks_id', 'tasks')
    op.drop_table('tasks')
    
    # Drop enums
    op.execute('DROP TYPE IF EXISTS taskpriority')
    op.execute('DROP TYPE IF EXISTS taskstatus')
