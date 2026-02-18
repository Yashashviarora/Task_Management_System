# 🎯 START HERE - Task Management API

## Welcome! 👋

This is a **production-ready Task Management REST API** built for your assessment. Everything is set up and ready to run!

---

## ⚡ Quick Start (5 Minutes)

### Step 1: Install Poetry
```bash
pip install poetry
```

### Step 2: Install Dependencies
```bash
cd c:\Task_Management_System
poetry install
```

### Step 3: Start Everything
```bash
docker-compose up --build
```

### Step 4: Open Your Browser
Visit: **http://localhost:8000/docs**

### Step 5: Test It!
```bash
# In a new terminal
poetry run pytest
```

**That's it! You're running! 🎉**

---

## 📖 What to Read Next

### For Quick Setup:
1. **CHECKLIST.md** - Step-by-step guide with checkboxes
2. **QUICK_REFERENCE.md** - Command cheat sheet

### For Understanding:
3. **README.md** - Complete project documentation
4. **ARCHITECTURE.md** - System design and diagrams
5. **PROJECT_SUMMARY.md** - All features and requirements

### For Installation Help:
6. **INSTALLATION.md** - Detailed setup instructions
7. **SETUP.md** - Quick setup reference

---

## 🎯 Assessment Requirements - All Met! ✅

### Functional Requirements
- ✅ Create, Read, Update, Delete tasks
- ✅ Mark task as completed
- ✅ Filter by status and priority
- ✅ Sort by any field (asc/desc)
- ✅ Pagination support

### Technical Requirements
- ✅ FastAPI framework
- ✅ PostgreSQL database (via Docker)
- ✅ SQLAlchemy ORM
- ✅ Alembic migrations
- ✅ Modular project structure

### Business Rules
- ✅ Completed tasks cannot be modified
- ✅ Title must not be empty
- ✅ Priority enum validation
- ✅ Proper HTTP status codes
- ✅ Meaningful error messages

### Exploration Requirement
- ✅ **Soft Delete** - Fully implemented and documented
  - Why: Data preservation, audit trails, recovery
  - How: is_deleted flag + deleted_at timestamp
  - Documented in README.md

### Bonus Features
- ✅ Dockerfile + docker-compose
- ✅ Unit tests with pytest
- ✅ Structured logging
- ✅ Environment configuration
- ✅ API versioning (/api/v1/)
- ✅ Standardized responses
- ✅ Custom exception handling
- ✅ Dependency injection

---

## 📁 Project Structure

```
Task_Management_System/
├── app/                    # Application code
│   ├── core/              # Config, logging, exceptions
│   ├── routers/           # API endpoints
│   ├── main.py            # FastAPI app
│   ├── models.py          # Database models
│   ├── schemas.py         # Validation schemas
│   ├── crud.py            # Business logic
│   └── database.py        # DB connection
├── alembic/               # Database migrations
├── tests/                 # Unit tests
├── docker-compose.yml     # Docker services
├── Dockerfile             # API container
├── pyproject.toml         # Dependencies
└── README.md              # Main documentation
```

---

## 🚀 What You Can Do

### Via Swagger UI (http://localhost:8000/docs):
1. Create a task
2. List all tasks
3. Filter by status/priority
4. Update a task
5. Mark as completed
6. Try to update completed task (will fail - business rule!)
7. Delete a task (soft delete)
8. Verify deleted task doesn't appear

### Via Command Line:
```bash
# Create task
curl -X POST "http://localhost:8000/api/v1/tasks/" \
  -H "Content-Type: application/json" \
  -d '{"title": "Test", "priority": "High"}'

# List tasks
curl "http://localhost:8000/api/v1/tasks/"

# Run tests
poetry run pytest
```

---

## 🎓 Key Features Explained

### 1. Soft Delete (Exploration Requirement)
- **What**: Tasks are marked as deleted, not removed
- **Why**: Preserves data for audit trails and recovery
- **How**: `is_deleted` flag + `deleted_at` timestamp
- **Benefit**: Can restore accidentally deleted tasks

### 2. Business Rules Enforcement
- **Completed tasks can't be updated** - Returns 400 error
- **Title must not be empty** - Validated by Pydantic
- **Priority must be valid** - Enum validation

### 3. Advanced Filtering
```
/api/v1/tasks/?status=Pending&priority=High&page=1&page_size=10
```
- Filter by status (Pending/Completed)
- Filter by priority (Low/Medium/High)
- Sort by any field
- Paginate results

### 4. Production-Ready Features
- Database connection pooling
- Proper indexing for performance
- Structured logging
- Custom exception handling
- Comprehensive tests
- Docker deployment

---

## 🧪 Testing

### Run All Tests:
```bash
poetry run pytest
```

### Expected Output:
```
tests/test_tasks.py::TestTaskCreation::test_create_task_success PASSED
tests/test_tasks.py::TestTaskCreation::test_create_task_empty_title PASSED
tests/test_tasks.py::TestTaskRetrieval::test_get_task_by_id PASSED
...
======================== XX passed in X.XXs ========================
```

### Test Coverage:
```bash
poetry run pytest --cov=app --cov-report=html
# Open htmlcov/index.html
```

---

## 📊 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/tasks/` | Create new task |
| GET | `/api/v1/tasks/{id}` | Get single task |
| GET | `/api/v1/tasks/` | List all tasks |
| PUT | `/api/v1/tasks/{id}` | Update task |
| PATCH | `/api/v1/tasks/{id}/complete` | Mark completed |
| DELETE | `/api/v1/tasks/{id}` | Soft delete task |

---

## 🔧 Common Commands

```bash
# Start services
docker-compose up --build

# Stop services
docker-compose down

# View logs
docker-compose logs -f

# Run tests
poetry run pytest

# Access database
docker-compose exec db psql -U taskuser -d taskdb

# Run migrations
docker-compose exec app alembic upgrade head
```

---

## 🐛 Troubleshooting

### Issue: Port 8000 in use
**Solution**: Stop other services or change port in docker-compose.yml

### Issue: Docker not running
**Solution**: Start Docker Desktop and wait for it to initialize

### Issue: Poetry not found
**Solution**: Restart terminal or use `python -m poetry`

### Issue: Tests failing
**Solution**: Make sure Docker services are running first

---

## 📚 Documentation Guide

| Document | When to Read |
|----------|--------------|
| **START_HERE.md** (this file) | First! Overview and quick start |
| **CHECKLIST.md** | Step-by-step setup with checkboxes |
| **QUICK_REFERENCE.md** | Command cheat sheet |
| **README.md** | Complete documentation |
| **INSTALLATION.md** | Detailed setup help |
| **ARCHITECTURE.md** | System design details |
| **PROJECT_SUMMARY.md** | Feature checklist |

---

## ✨ What Makes This Special

1. **Clean Architecture** - Modular, maintainable code
2. **Type Safety** - Pydantic + SQLAlchemy + type hints
3. **Comprehensive Tests** - Full coverage of all scenarios
4. **Production Ready** - Docker, logging, error handling
5. **Well Documented** - Code comments + multiple docs
6. **Business Rules** - Enforced at multiple layers
7. **Soft Delete** - Data preservation built-in
8. **Performance** - Proper indexing and connection pooling

---

## 🎯 Next Steps

### Immediate (5 minutes):
1. ✅ Run `poetry install`
2. ✅ Run `docker-compose up --build`
3. ✅ Visit http://localhost:8000/docs
4. ✅ Create a task via Swagger UI
5. ✅ Run `poetry run pytest`

### Short Term (30 minutes):
6. ✅ Read README.md
7. ✅ Review app/models.py
8. ✅ Review app/routers/tasks.py
9. ✅ Review tests/test_tasks.py
10. ✅ Test all API endpoints

### Complete Understanding (2 hours):
11. ✅ Read ARCHITECTURE.md
12. ✅ Review all code files
13. ✅ Understand soft delete implementation
14. ✅ Review business rules enforcement
15. ✅ Explore database schema

---

## 💡 Pro Tips

1. **Use Swagger UI** - It's interactive and easy to test
2. **Check logs** - `docker-compose logs -f` shows everything
3. **Run tests often** - Catch issues early
4. **Read comments** - Code is well-documented
5. **Try breaking it** - Test business rules by violating them
6. **Explore database** - See soft delete in action

---

## 🆘 Need Help?

### Quick Help:
- **QUICK_REFERENCE.md** - Command cheat sheet
- **CHECKLIST.md** - Step-by-step guide

### Detailed Help:
- **INSTALLATION.md** - Setup troubleshooting
- **README.md** - Complete documentation

### Understanding:
- **ARCHITECTURE.md** - System design
- **Code comments** - Implementation details

---

## ✅ Success Checklist

You're ready when:
- ✅ `docker-compose up` starts without errors
- ✅ http://localhost:8000/docs loads
- ✅ `poetry run pytest` shows all tests passing
- ✅ You can create/read/update/delete tasks
- ✅ Business rules work (can't update completed tasks)
- ✅ Soft delete works (deleted tasks don't show in list)

---

## 🎉 You're All Set!

**Everything is ready to go. Just follow the Quick Start above!**

**Questions?** Check the documentation files listed above.

**Ready to submit?** Review PROJECT_SUMMARY.md for the complete feature list.

---

**Good luck with your assessment! You've got this! 💪**

---

## 📞 Quick Links

- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health
- **Main README**: README.md
- **Setup Guide**: CHECKLIST.md
- **Command Reference**: QUICK_REFERENCE.md

---

**Made with ❤️ using FastAPI, PostgreSQL, and Python best practices**
