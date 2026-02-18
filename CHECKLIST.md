# 🚀 Getting Started Checklist

Follow these steps in order to get your Task Management API up and running!

## Prerequisites Installation

### ☐ Step 1: Verify Python Installation
```bash
python --version
```
- Should show Python 3.10 or higher
- If not installed: Download from https://www.python.org/

### ☐ Step 2: Verify Docker Installation
```bash
docker --version
docker-compose --version
```
- Should show Docker version
- If not installed: Download Docker Desktop from https://www.docker.com/
- **Important:** Make sure Docker Desktop is running!

### ☐ Step 3: Verify Git Installation
```bash
git --version
```
- Should show Git version
- If not installed: Download from https://git-scm.com/

## Project Setup

### ☐ Step 4: Install Poetry
```bash
pip install poetry
```
- Verify installation:
```bash
poetry --version
```
- If command not found, restart your terminal

### ☐ Step 5: Navigate to Project Directory
```bash
cd c:\Task_Management_System
```

### ☐ Step 6: Install Project Dependencies
```bash
poetry install
```
- This will take 2-3 minutes
- Creates virtual environment
- Installs all required packages

## Running the Application

### ☐ Step 7: Start Docker Services
```bash
docker-compose up --build
```
- First time will take 5-10 minutes (downloading images)
- Wait for message: "Application startup complete"
- Keep this terminal window open

### ☐ Step 8: Verify Application is Running
Open your browser and visit:
- ✅ http://localhost:8000/docs (Swagger UI)
- ✅ http://localhost:8000/health (Health check)

If you see the API documentation, you're all set! 🎉

## Testing the API

### ☐ Step 9: Create Your First Task
In the Swagger UI (http://localhost:8000/docs):
1. Click on "POST /api/v1/tasks/"
2. Click "Try it out"
3. Use this example:
```json
{
  "title": "My First Task",
  "description": "Testing the API",
  "priority": "High"
}
```
4. Click "Execute"
5. You should see a 201 response with your task!

### ☐ Step 10: List All Tasks
1. Click on "GET /api/v1/tasks/"
2. Click "Try it out"
3. Click "Execute"
4. You should see your task in the list!

### ☐ Step 11: Run Unit Tests
Open a new terminal and run:
```bash
cd c:\Task_Management_System
poetry run pytest
```
- All tests should pass ✅

## Exploring the Code

### ☐ Step 12: Open Project in VSCode
```bash
code .
```

### ☐ Step 13: Review Key Files
Read these files in order:
1. `README.md` - Project overview
2. `app/models.py` - Database models
3. `app/schemas.py` - Request/response schemas
4. `app/crud.py` - Business logic
5. `app/routers/tasks.py` - API endpoints
6. `tests/test_tasks.py` - Unit tests

### ☐ Step 14: Review Documentation
- `INSTALLATION.md` - Detailed setup guide
- `ARCHITECTURE.md` - System architecture
- `PROJECT_SUMMARY.md` - Complete feature list

## Common Commands Reference

### Docker Commands
```bash
# Start services
docker-compose up

# Start in background
docker-compose up -d

# Stop services
docker-compose down

# View logs
docker-compose logs -f

# Restart services
docker-compose restart
```

### Poetry Commands
```bash
# Install dependencies
poetry install

# Add new package
poetry add package-name

# Run tests
poetry run pytest

# Activate virtual environment
poetry shell
```

### Database Commands
```bash
# Run migrations
docker-compose exec app alembic upgrade head

# Create new migration
docker-compose exec app alembic revision --autogenerate -m "description"

# Access database
docker-compose exec db psql -U taskuser -d taskdb
```

## Troubleshooting

### Problem: Port 8000 already in use
**Solution:**
```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Or change port in docker-compose.yml
```

### Problem: Port 5432 already in use
**Solution:**
```bash
# Stop existing PostgreSQL service
# Or change port in docker-compose.yml
```

### Problem: Docker daemon not running
**Solution:**
- Open Docker Desktop application
- Wait for it to fully start
- Try again

### Problem: Poetry command not found
**Solution:**
- Restart terminal
- Or run: `python -m poetry` instead of `poetry`

### Problem: Tests failing
**Solution:**
```bash
# Make sure services are running
docker-compose up -d

# Run tests again
poetry run pytest -v
```

## Next Steps

### ☐ Step 15: Experiment with the API
Try these operations:
- ✅ Create multiple tasks
- ✅ Filter by status: `?status=Pending`
- ✅ Filter by priority: `?priority=High`
- ✅ Update a task
- ✅ Mark task as completed
- ✅ Try to update completed task (should fail!)
- ✅ Delete a task (soft delete)
- ✅ Verify deleted task doesn't appear in list

### ☐ Step 16: Review Business Rules
Test these scenarios:
1. Try creating task with empty title (should fail)
2. Try invalid priority value (should fail)
3. Update a pending task (should work)
4. Complete a task
5. Try to update completed task (should fail with 400)
6. Delete a task
7. Try to get deleted task (should return 404)

### ☐ Step 17: Explore Database
```bash
# Connect to database
docker-compose exec db psql -U taskuser -d taskdb

# View tasks table
\d tasks

# Query tasks
SELECT * FROM tasks;

# Exit
\q
```

### ☐ Step 18: Review Test Coverage
```bash
# Run tests with coverage
poetry run pytest --cov=app --cov-report=html

# Open coverage report
# File: htmlcov/index.html
```

## Assessment Submission Checklist

### ☐ Before Submitting:
- ✅ All tests pass
- ✅ Application runs without errors
- ✅ README.md is complete
- ✅ Code is well-commented
- ✅ Git repository is clean
- ✅ .env file is not committed (check .gitignore)
- ✅ Docker services start successfully
- ✅ API documentation is accessible

### ☐ Documentation Review:
- ✅ Setup instructions are clear
- ✅ Design decisions are documented
- ✅ Trade-offs are explained
- ✅ Assumptions are stated
- ✅ Future improvements are listed
- ✅ Soft delete implementation is justified

### ☐ Code Quality Check:
- ✅ No hardcoded credentials
- ✅ Proper error handling
- ✅ Type hints used
- ✅ Comments explain "why", not "what"
- ✅ Consistent naming conventions
- ✅ No unused imports or code

## Success Criteria

You're ready to submit when:
- ✅ `docker-compose up` starts everything successfully
- ✅ `poetry run pytest` shows all tests passing
- ✅ API documentation loads at http://localhost:8000/docs
- ✅ You can create, read, update, delete tasks via API
- ✅ Business rules are enforced (completed tasks can't be updated)
- ✅ Soft delete works (deleted tasks don't appear in listings)
- ✅ All documentation files are complete

## Quick Start (TL;DR)

If you just want to get it running quickly:

```bash
# 1. Install Poetry
pip install poetry

# 2. Install dependencies
cd c:\Task_Management_System
poetry install

# 3. Start everything
docker-compose up --build

# 4. Open browser
# Visit: http://localhost:8000/docs

# 5. Run tests (in new terminal)
poetry run pytest
```

---

**Congratulations! You now have a production-ready Task Management API! 🎉**

**Questions? Check:**
- `README.md` for detailed documentation
- `INSTALLATION.md` for setup help
- `ARCHITECTURE.md` for system design
- `PROJECT_SUMMARY.md` for feature list
