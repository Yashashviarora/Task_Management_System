# Quick Reference Card

## 🚀 Quick Start (3 Commands)
```bash
pip install poetry          # Install Poetry
poetry install             # Install dependencies
docker-compose up --build  # Start everything
```
**Then visit:** http://localhost:8000/docs

---

## 📋 Essential Commands

### Docker Operations
| Command | Description |
|---------|-------------|
| `docker-compose up --build` | Start all services |
| `docker-compose up -d` | Start in background |
| `docker-compose down` | Stop all services |
| `docker-compose logs -f` | View live logs |
| `docker-compose restart` | Restart services |
| `docker-compose ps` | List running containers |

### Poetry Operations
| Command | Description |
|---------|-------------|
| `poetry install` | Install dependencies |
| `poetry shell` | Activate virtual environment |
| `poetry add <package>` | Add new package |
| `poetry run pytest` | Run tests |
| `poetry run pytest --cov=app` | Run with coverage |

### Database Operations
| Command | Description |
|---------|-------------|
| `alembic upgrade head` | Run migrations |
| `alembic revision --autogenerate -m "msg"` | Create migration |
| `docker-compose exec db psql -U taskuser -d taskdb` | Access database |

---

## 🔗 API Endpoints

### Base URL: `http://localhost:8000/api/v1`

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/tasks/` | Create task |
| GET | `/tasks/{id}` | Get single task |
| GET | `/tasks/` | List all tasks |
| PUT | `/tasks/{id}` | Update task |
| PATCH | `/tasks/{id}/complete` | Mark completed |
| DELETE | `/tasks/{id}` | Delete task (soft) |

---

## 📝 API Examples

### Create Task
```bash
curl -X POST "http://localhost:8000/api/v1/tasks/" \
  -H "Content-Type: application/json" \
  -d '{"title": "My Task", "priority": "High"}'
```

### List Tasks
```bash
curl "http://localhost:8000/api/v1/tasks/"
```

### Filter Tasks
```bash
curl "http://localhost:8000/api/v1/tasks/?status=Pending&priority=High"
```

### Pagination
```bash
curl "http://localhost:8000/api/v1/tasks/?page=1&page_size=10"
```

### Update Task
```bash
curl -X PUT "http://localhost:8000/api/v1/tasks/{id}" \
  -H "Content-Type: application/json" \
  -d '{"title": "Updated"}'
```

### Complete Task
```bash
curl -X PATCH "http://localhost:8000/api/v1/tasks/{id}/complete"
```

### Delete Task
```bash
curl -X DELETE "http://localhost:8000/api/v1/tasks/{id}"
```

---

## 🎯 Query Parameters

### Filtering
- `?status=Pending` - Filter by status (Pending/Completed)
- `?priority=High` - Filter by priority (Low/Medium/High)

### Sorting
- `?sort_by=created_at` - Sort field
- `?sort_order=desc` - Sort order (asc/desc)

### Pagination
- `?page=1` - Page number (starts at 1)
- `?page_size=10` - Items per page (max 100)

### Combined Example
```
/api/v1/tasks/?status=Pending&priority=High&sort_by=created_at&sort_order=desc&page=1&page_size=10
```

---

## 📊 Response Formats

### Success Response (Task)
```json
{
  "id": "uuid",
  "title": "Task Title",
  "description": "Description",
  "priority": "High",
  "status": "Pending",
  "created_at": "2024-01-01T00:00:00",
  "updated_at": "2024-01-01T00:00:00"
}
```

### Success Response (List)
```json
{
  "total": 100,
  "page": 1,
  "page_size": 10,
  "tasks": [...]
}
```

### Error Response
```json
{
  "success": false,
  "message": "Error description",
  "error_type": "ErrorType"
}
```

---

## ⚠️ Business Rules

| Rule | HTTP Status | Description |
|------|-------------|-------------|
| Empty title | 422 | Title must not be empty |
| Invalid priority | 422 | Must be Low/Medium/High |
| Update completed task | 400 | Cannot modify completed tasks |
| Task not found | 404 | Task doesn't exist or deleted |

---

## 🧪 Testing

### Run All Tests
```bash
poetry run pytest
```

### Run with Verbose Output
```bash
poetry run pytest -v
```

### Run Specific Test
```bash
poetry run pytest tests/test_tasks.py::TestTaskCreation -v
```

### Run with Coverage
```bash
poetry run pytest --cov=app --cov-report=html
```

---

## 🗂️ Project Structure

```
app/
├── core/           # Configuration, logging, exceptions
├── routers/        # API endpoints
├── main.py         # FastAPI app
├── database.py     # DB connection
├── models.py       # SQLAlchemy models
├── schemas.py      # Pydantic schemas
└── crud.py         # Business logic
```

---

## 🔍 Useful URLs

| URL | Description |
|-----|-------------|
| http://localhost:8000/docs | Swagger UI (Interactive API docs) |
| http://localhost:8000/redoc | ReDoc (Alternative docs) |
| http://localhost:8000/health | Health check endpoint |
| http://localhost:8000/ | API information |

---

## 🐛 Troubleshooting

### Port Already in Use
```bash
# Windows - Find process
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

### Docker Not Running
- Start Docker Desktop
- Wait for it to fully initialize
- Try command again

### Poetry Not Found
- Restart terminal
- Or use: `python -m poetry` instead

### Database Connection Error
```bash
# Check if database is running
docker-compose ps

# View database logs
docker-compose logs db
```

---

## 📚 Documentation Files

| File | Purpose |
|------|---------|
| `README.md` | Complete project documentation |
| `INSTALLATION.md` | Step-by-step setup guide |
| `ARCHITECTURE.md` | System architecture diagrams |
| `PROJECT_SUMMARY.md` | Feature checklist |
| `CHECKLIST.md` | Getting started checklist |
| `SETUP.md` | Quick setup reference |

---

## 🎓 Key Features

✅ Full CRUD operations
✅ Soft delete (exploration requirement)
✅ Filtering & sorting
✅ Pagination
✅ Business rules enforcement
✅ Custom exception handling
✅ Comprehensive logging
✅ Unit tests with pytest
✅ Docker deployment
✅ API documentation
✅ Database migrations
✅ Type safety with Pydantic

---

## 💡 Pro Tips

1. **Use Swagger UI** for testing - it's interactive!
2. **Check logs** when debugging: `docker-compose logs -f`
3. **Run tests often** to catch issues early
4. **Use pagination** for large datasets
5. **Soft delete** preserves data - use wisely
6. **Completed tasks** can't be modified - by design
7. **Indexes** are already optimized for common queries

---

## 🆘 Need Help?

1. Check `README.md` for detailed docs
2. Review `INSTALLATION.md` for setup issues
3. See `ARCHITECTURE.md` for design details
4. Follow `CHECKLIST.md` step-by-step
5. Check code comments for implementation details

---

**Print this card and keep it handy! 📌**
