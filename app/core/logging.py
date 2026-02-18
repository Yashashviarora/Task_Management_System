"""
Logging configuration for the application.
Provides structured logging for debugging and monitoring.
"""
import logging
import sys
from pathlib import Path

# Create logs directory if it doesn't exist
LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

# Configure logging format
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

# Configure root logger
logging.basicConfig(
    level=logging.INFO,
    format=LOG_FORMAT,
    datefmt=DATE_FORMAT,
    handlers=[
        # Console handler
        logging.StreamHandler(sys.stdout),
        # File handler
        logging.FileHandler(LOG_DIR / "app.log")
    ]
)

# Create logger instance
logger = logging.getLogger("task_management")
logger.setLevel(logging.INFO)


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance with the specified name.
    
    Args:
        name: Logger name (usually __name__ of the module)
    
    Returns:
        Configured logger instance
    """
    return logging.getLogger(f"task_management.{name}")
