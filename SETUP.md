# Task Management API - Quick Setup Guide

## Prerequisites Check
Before starting, ensure you have:
- [ ] Python 3.10 or higher installed
- [ ] Docker Desktop installed and running
- [ ] Git installed
- [ ] VSCode (or your preferred IDE)

## Step-by-Step Setup

### 1. Install Poetry
```bash
pip install poetry
```

### 2. Install Project Dependencies
```bash
poetry install
```

### 3. Start Docker Services
```bash
# Start PostgreSQL and FastAPI containers
docker-compose up --build

# Or run in detached mode
docker-compose up -d --build
```

### 4. Verify Installation
Open your browser and visit:
- API Docs: http://localhost:8000/docs
- Health Check: http://localhost:8000/health

### 5. Run Tests
```bash
poetry run pytest
```

## Common Issues & Solutions

### Issue: Port 5432 already in use
**Solution**: Stop existing PostgreSQL service or change port in docker-compose.yml

### Issue: Port 8000 already in use
**Solution**: Stop other services using port 8000 or change in docker-compose.yml

### Issue: Poetry not found
**Solution**: Restart terminal after installing Poetry or add to PATH

### Issue: Docker daemon not running
**Solution**: Start Docker Desktop application

## Quick Commands

```bash
# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Rebuild containers
docker-compose up --build

# Run migrations manually
docker-compose exec app alembic upgrade head

# Access database
docker-compose exec db psql -U taskuser -d taskdb

# Run tests with coverage
poetry run pytest --cov=app --cov-report=html
```

## Next Steps

1. Explore the API documentation at http://localhost:8000/docs
2. Try creating a task using the Swagger UI
3. Review the code structure in the `app/` directory
4. Run the test suite to understand the test coverage
5. Check the logs in the `logs/` directory

## Need Help?

- Check README.md for detailed documentation
- Review the code comments for implementation details
- Open an issue if you encounter problems
