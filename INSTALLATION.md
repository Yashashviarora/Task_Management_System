# Installation Guide - Task Management API

## What You Need to Install

### 1. Install Poetry (Dependency Manager)
Open Command Prompt or PowerShell and run:
```bash
pip install poetry
```

Verify installation:
```bash
poetry --version
```

### 2. Install Project Dependencies
Navigate to the project directory and run:
```bash
cd c:\Task_Management_System
poetry install
```

This will:
- Create a virtual environment
- Install all required packages (FastAPI, SQLAlchemy, PostgreSQL driver, etc.)
- Install development dependencies (pytest, coverage tools)

## Running the Application

### Option 1: Using Docker (Recommended)

**Start everything with one command:**
```bash
docker-compose up --build
```

This will:
- Start PostgreSQL database on port 5432
- Start FastAPI application on port 8000
- Run database migrations automatically
- Enable hot-reload for development

**Access the application:**
- API Documentation: http://localhost:8000/docs
- Alternative Docs: http://localhost:8000/redoc
- Health Check: http://localhost:8000/health

**Stop the services:**
```bash
docker-compose down
```

### Option 2: Running Locally (Without Docker for API)

**Step 1: Start PostgreSQL Database**
```bash
docker-compose up db
```

**Step 2: Activate Poetry Environment**
```bash
poetry shell
```

**Step 3: Run Database Migrations**
```bash
alembic upgrade head
```

**Step 4: Start the API Server**
```bash
uvicorn app.main:app --reload
```

The API will be available at http://localhost:8000

## Running Tests

### Run all tests:
```bash
poetry run pytest
```

### Run tests with coverage report:
```bash
poetry run pytest --cov=app --cov-report=html
```

Then open `htmlcov/index.html` in your browser to see detailed coverage.

### Run specific test file:
```bash
poetry run pytest tests/test_tasks.py -v
```

## Project Structure Overview

```
Task_Management_System/
├── app/                        # Main application code
│   ├── core/                   # Core configurations
│   │   ├── config.py          # Environment settings
│   │   ├── logging.py         # Logging setup
│   │   └── exceptions.py      # Custom exceptions
│   ├── routers/               # API endpoints
│   │   └── tasks.py           # Task routes
│   ├── main.py                # FastAPI app initialization
│   ├── database.py            # Database connection
│   ├── models.py              # SQLAlchemy models
│   ├── schemas.py             # Pydantic schemas
│   └── crud.py                # Database operations
├── alembic/                   # Database migrations
├── tests/                     # Unit tests
├── docker-compose.yml         # Docker services
├── Dockerfile                 # API container
├── pyproject.toml            # Poetry dependencies
└── .env                      # Environment variables
```

## Environment Variables

The `.env` file contains:
```
DATABASE_URL=postgresql://taskuser:taskpass123@localhost:5432/taskdb
APP_NAME=Task Management API
APP_VERSION=1.0.0
DEBUG=True
HOST=0.0.0.0
PORT=8000
```

**Note:** When using Docker, the database host is `db` instead of `localhost`.

## Troubleshooting

### Poetry command not found
- Restart your terminal after installing Poetry
- Or add Poetry to your PATH manually

### Port 5432 already in use
- Stop existing PostgreSQL service
- Or change the port in `docker-compose.yml`

### Port 8000 already in use
- Stop other services using port 8000
- Or change the port in `docker-compose.yml` and `.env`

### Docker daemon not running
- Start Docker Desktop application
- Wait for it to fully start before running docker-compose

### Database connection errors
- Ensure PostgreSQL container is running: `docker-compose ps`
- Check database logs: `docker-compose logs db`
- Verify DATABASE_URL in `.env` file

## Next Steps

1. ✅ Install Poetry
2. ✅ Install dependencies with `poetry install`
3. ✅ Start services with `docker-compose up --build`
4. ✅ Visit http://localhost:8000/docs
5. ✅ Try creating a task via Swagger UI
6. ✅ Run tests with `poetry run pytest`
7. ✅ Explore the code and make modifications

## Quick Reference Commands

```bash
# Install dependencies
poetry install

# Start all services
docker-compose up --build

# Start in background
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Run tests
poetry run pytest

# Run with coverage
poetry run pytest --cov=app

# Access database
docker-compose exec db psql -U taskuser -d taskdb

# Run migrations
docker-compose exec app alembic upgrade head

# Create new migration
docker-compose exec app alembic revision --autogenerate -m "description"
```

## API Usage Examples

### Create a Task
```bash
curl -X POST "http://localhost:8000/api/v1/tasks/" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "My First Task",
    "description": "This is a test task",
    "priority": "High"
  }'
```

### List All Tasks
```bash
curl "http://localhost:8000/api/v1/tasks/"
```

### Filter Tasks
```bash
curl "http://localhost:8000/api/v1/tasks/?status=Pending&priority=High"
```

### Get Single Task
```bash
curl "http://localhost:8000/api/v1/tasks/{task_id}"
```

### Update Task
```bash
curl -X PUT "http://localhost:8000/api/v1/tasks/{task_id}" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Updated Title",
    "priority": "Medium"
  }'
```

### Mark as Completed
```bash
curl -X PATCH "http://localhost:8000/api/v1/tasks/{task_id}/complete"
```

### Delete Task (Soft Delete)
```bash
curl -X DELETE "http://localhost:8000/api/v1/tasks/{task_id}"
```

---

**You're all set! Happy coding! 🚀**
