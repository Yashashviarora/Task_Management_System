# Architecture Documentation

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                         Client                               │
│                    (Browser/Postman/curl)                    │
└────────────────────────┬────────────────────────────────────┘
                         │ HTTP Requests
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                    FastAPI Application                       │
│                     (Port 8000)                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              app/main.py                             │  │
│  │  - Exception Handlers                                │  │
│  │  - Middleware                                        │  │
│  │  - Lifespan Events                                   │  │
│  └────────────────────┬─────────────────────────────────┘  │
│                       │                                      │
│  ┌────────────────────▼─────────────────────────────────┐  │
│  │         app/routers/tasks.py                         │  │
│  │  - POST   /api/v1/tasks/                            │  │
│  │  - GET    /api/v1/tasks/{id}                        │  │
│  │  - GET    /api/v1/tasks/                            │  │
│  │  - PUT    /api/v1/tasks/{id}                        │  │
│  │  - PATCH  /api/v1/tasks/{id}/complete               │  │
│  │  - DELETE /api/v1/tasks/{id}                        │  │
│  └────────────────────┬─────────────────────────────────┘  │
│                       │                                      │
│  ┌────────────────────▼─────────────────────────────────┐  │
│  │              app/schemas.py                          │  │
│  │  - TaskCreate (Pydantic)                            │  │
│  │  - TaskUpdate (Pydantic)                            │  │
│  │  - TaskResponse (Pydantic)                          │  │
│  │  - Input Validation                                  │  │
│  └────────────────────┬─────────────────────────────────┘  │
│                       │                                      │
│  ┌────────────────────▼─────────────────────────────────┐  │
│  │               app/crud.py                            │  │
│  │  - create_task()                                     │  │
│  │  - get_task_by_id()                                 │  │
│  │  - get_tasks() [filter, sort, paginate]            │  │
│  │  - update_task()                                     │  │
│  │  - mark_task_completed()                            │  │
│  │  - delete_task() [soft delete]                      │  │
│  │  - Business Rules Enforcement                        │  │
│  └────────────────────┬─────────────────────────────────┘  │
│                       │                                      │
│  ┌────────────────────▼─────────────────────────────────┐  │
│  │            app/database.py                           │  │
│  │  - SQLAlchemy Engine                                 │  │
│  │  - Session Management                                │  │
│  │  - Connection Pooling                                │  │
│  │  - get_db() Dependency                              │  │
│  └────────────────────┬─────────────────────────────────┘  │
│                       │                                      │
│  ┌────────────────────▼─────────────────────────────────┐  │
│  │              app/models.py                           │  │
│  │  - Task Model (SQLAlchemy)                          │  │
│  │  - TaskPriority Enum                                │  │
│  │  - TaskStatus Enum                                  │  │
│  │  - Indexes & Relationships                          │  │
│  └──────────────────────────────────────────────────────┘  │
└────────────────────────┬────────────────────────────────────┘
                         │ SQL Queries
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                  PostgreSQL Database                         │
│                     (Port 5432)                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │                  tasks table                         │  │
│  │  - id (UUID, PK)                                    │  │
│  │  - title (VARCHAR)                                  │  │
│  │  - description (VARCHAR)                            │  │
│  │  - priority (ENUM)                                  │  │
│  │  - status (ENUM)                                    │  │
│  │  - created_at (TIMESTAMP)                           │  │
│  │  - updated_at (TIMESTAMP)                           │  │
│  │  - is_deleted (BOOLEAN) ← Soft Delete              │  │
│  │  - deleted_at (TIMESTAMP)                           │  │
│  │                                                      │  │
│  │  Indexes:                                           │  │
│  │  - idx_tasks_id                                     │  │
│  │  - idx_tasks_status                                 │  │
│  │  - idx_tasks_priority                               │  │
│  │  - idx_status_priority (composite)                  │  │
│  │  - idx_deleted_created (composite)                  │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

## Request Flow

### Example: Create Task

```
1. Client sends POST request
   ↓
2. FastAPI receives request at /api/v1/tasks/
   ↓
3. Pydantic validates request body (TaskCreate schema)
   - Checks title is not empty
   - Validates priority enum
   ↓
4. Router calls crud.create_task()
   ↓
5. CRUD creates Task model instance
   ↓
6. SQLAlchemy inserts into database
   ↓
7. Database returns created record
   ↓
8. CRUD returns Task object
   ↓
9. Pydantic serializes to TaskResponse
   ↓
10. FastAPI returns JSON with 201 status
```

## Dependency Injection Flow

```
┌─────────────────────────────────────────┐
│         Request Handler                  │
│  def create_task(                       │
│      task: TaskCreate,                  │
│      db: Session = Depends(get_db)     │◄─── Dependency
│  )                                      │
└────────────────┬────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────┐
│         get_db() Generator               │
│  - Creates database session             │
│  - Yields session to handler            │
│  - Closes session after request         │
└─────────────────────────────────────────┘
```

## Soft Delete Implementation

```
Normal Delete (Hard Delete):
┌──────────┐
│  Task    │  DELETE  ┌─────────┐
│  id: 123 │ ───────► │ REMOVED │
└──────────┘          └─────────┘

Soft Delete (Our Implementation):
┌──────────────────────┐
│  Task                │  UPDATE
│  id: 123             │ ───────► ┌──────────────────────┐
│  is_deleted: false   │          │  Task                │
│  deleted_at: null    │          │  id: 123             │
└──────────────────────┘          │  is_deleted: true    │
                                  │  deleted_at: 2024... │
                                  └──────────────────────┘
                                           │
                                           ▼
                                  Still in database,
                                  but filtered from queries
```

## Business Rules Enforcement

```
┌─────────────────────────────────────────────────────────┐
│                  Update Task Request                     │
└────────────────────────┬────────────────────────────────┘
                         │
                         ▼
                  ┌──────────────┐
                  │ Get Task     │
                  └──────┬───────┘
                         │
                         ▼
              ┌──────────────────────┐
              │ Check Status         │
              └──────┬───────────────┘
                     │
        ┌────────────┴────────────┐
        │                         │
        ▼                         ▼
┌───────────────┐         ┌──────────────┐
│ Status =      │         │ Status =     │
│ Completed     │         │ Pending      │
└───────┬───────┘         └──────┬───────┘
        │                        │
        ▼                        ▼
┌───────────────┐         ┌──────────────┐
│ Raise 400     │         │ Allow Update │
│ Error         │         │              │
└───────────────┘         └──────────────┘
```

## Database Indexing Strategy

```
Query: GET /api/v1/tasks/?status=Pending&priority=High

Without Indexes:
┌─────────────────────────────────────┐
│ Full Table Scan                     │
│ Check every row                     │
│ Time: O(n)                          │
└─────────────────────────────────────┘

With Composite Index (status, priority):
┌─────────────────────────────────────┐
│ Index Lookup                        │
│ Direct access to matching rows      │
│ Time: O(log n)                      │
└─────────────────────────────────────┘

Performance Improvement: 10x - 1000x faster
```

## Error Handling Flow

```
┌─────────────────────────────────────┐
│         Request                      │
└────────────┬────────────────────────┘
             │
             ▼
      ┌──────────────┐
      │ Try Execute  │
      └──────┬───────┘
             │
    ┌────────┴────────┐
    │                 │
    ▼                 ▼
┌────────┐      ┌──────────────────┐
│Success │      │ Exception Raised │
└───┬────┘      └────────┬─────────┘
    │                    │
    │           ┌────────┴────────┐
    │           │                 │
    │           ▼                 ▼
    │    ┌─────────────┐   ┌──────────────┐
    │    │TaskNotFound │   │ValidationErr │
    │    └──────┬──────┘   └──────┬───────┘
    │           │                 │
    │           ▼                 ▼
    │    ┌─────────────┐   ┌──────────────┐
    │    │Return 404   │   │Return 422    │
    │    └─────────────┘   └──────────────┘
    │
    ▼
┌────────────┐
│Return 200  │
└────────────┘
```

## Testing Architecture

```
┌─────────────────────────────────────────┐
│         Test Suite (pytest)              │
└────────────────┬────────────────────────┘
                 │
    ┌────────────┼────────────┐
    │            │            │
    ▼            ▼            ▼
┌────────┐  ┌────────┐  ┌────────┐
│Create  │  │Read    │  │Update  │
│Tests   │  │Tests   │  │Tests   │
└───┬────┘  └───┬────┘  └───┬────┘
    │           │           │
    └───────────┼───────────┘
                │
                ▼
    ┌───────────────────────┐
    │  Test Database        │
    │  (SQLite in-memory)   │
    │  - Fresh for each test│
    │  - Isolated           │
    │  - Fast               │
    └───────────────────────┘
```

## Deployment Architecture (Docker)

```
┌─────────────────────────────────────────────────────────┐
│                    Docker Host                           │
│                                                          │
│  ┌────────────────────────────────────────────────┐    │
│  │         Docker Network (bridge)                 │    │
│  │                                                 │    │
│  │  ┌──────────────────┐    ┌──────────────────┐ │    │
│  │  │  Container: app  │    │  Container: db   │ │    │
│  │  │                  │    │                  │ │    │
│  │  │  FastAPI         │───►│  PostgreSQL      │ │    │
│  │  │  Port: 8000      │    │  Port: 5432      │ │    │
│  │  │                  │    │                  │ │    │
│  │  │  Volume: ./app   │    │  Volume: pgdata  │ │    │
│  │  └────────┬─────────┘    └──────────────────┘ │    │
│  │           │                                    │    │
│  └───────────┼────────────────────────────────────┘    │
│              │                                          │
└──────────────┼──────────────────────────────────────────┘
               │
               ▼ Port Mapping
        ┌──────────────┐
        │   localhost  │
        │   :8000      │
        └──────────────┘
```

## Configuration Management

```
┌─────────────────────────────────────────┐
│         .env file                        │
│  DATABASE_URL=postgresql://...          │
│  APP_NAME=Task Management API           │
│  DEBUG=True                             │
└────────────────┬────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────┐
│    app/core/config.py                   │
│    class Settings(BaseSettings)         │
│    - Loads from .env                    │
│    - Type validation                    │
│    - Default values                     │
└────────────────┬────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────┐
│    settings = Settings()                │
│    Global singleton instance            │
└────────────────┬────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────┐
│    Used throughout application          │
│    - Database connection                │
│    - App configuration                  │
│    - Feature flags                      │
└─────────────────────────────────────────┘
```

---

**This architecture ensures:**
- ✅ Separation of concerns
- ✅ Testability
- ✅ Scalability
- ✅ Maintainability
- ✅ Production readiness
