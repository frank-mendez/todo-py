import logging
import sys
from typing import Any
from pathlib import Path
from loguru import logger

# Log file configuration
LOG_FILE_PATH = Path("logs/todo-app.log")
LOG_FILE_PATH.parent.mkdir(parents=True, exist_ok=True)

# Logging configuration
class InterceptHandler(logging.Handler):
    def emit(self, record: logging.LogRecord) -> None:
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(
            level, record.getMessage()
        )

def setup_logging(debug: bool = False) -> None:
    """Configure logging for the application."""
    # Remove default logger
    logger.remove()

    # Configure loguru
    logger.add(
        sys.stdout,
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
        level="DEBUG" if debug else "INFO",
        colorize=True,
    )
    
    # Add file logging
    logger.add(
        LOG_FILE_PATH,
        rotation="10 MB",
        retention="1 week",
        compression="zip",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
        level="INFO",
    )

    # Intercept standard library logging
    logging.basicConfig(handlers=[InterceptHandler()], level=0, force=True)

def get_logger(name: str) -> Any:
    """Get a logger instance."""
    return logger.bind(name=name)

# Initialize logging
setup_logging()
