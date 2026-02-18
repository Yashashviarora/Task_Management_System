@echo off
echo ========================================
echo Task Management API - Quick Setup
echo ========================================
echo.

echo Step 1: Checking Python installation...
python --version
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.10+ from https://www.python.org/
    pause
    exit /b 1
)
echo ✓ Python is installed
echo.

echo Step 2: Checking Docker installation...
docker --version
if %errorlevel% neq 0 (
    echo ERROR: Docker is not installed or not running
    echo Please install Docker Desktop from https://www.docker.com/
    pause
    exit /b 1
)
echo ✓ Docker is installed
echo.

echo Step 3: Installing Poetry...
pip install poetry
if %errorlevel% neq 0 (
    echo ERROR: Failed to install Poetry
    pause
    exit /b 1
)
echo ✓ Poetry installed
echo.

echo Step 4: Installing project dependencies...
poetry install
if %errorlevel% neq 0 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)
echo ✓ Dependencies installed
echo.

echo Step 5: Starting Docker services...
echo This may take a few minutes on first run...
docker-compose up --build -d
if %errorlevel% neq 0 (
    echo ERROR: Failed to start Docker services
    pause
    exit /b 1
)
echo ✓ Services started
echo.

echo ========================================
echo Setup Complete! 🎉
echo ========================================
echo.
echo Your API is now running at:
echo   - API Docs: http://localhost:8000/docs
echo   - Health Check: http://localhost:8000/health
echo.
echo Useful commands:
echo   - View logs: docker-compose logs -f
echo   - Stop services: docker-compose down
echo   - Run tests: poetry run pytest
echo.
echo Opening API documentation in browser...
timeout /t 3 /nobreak >nul
start http://localhost:8000/docs
echo.
pause
