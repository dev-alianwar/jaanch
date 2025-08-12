"""
Logging configuration
"""
import logging
import sys
from .config import settings


def setup_logging():
    """Setup application logging"""
    
    # Create formatter
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    
    # Create console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    
    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, settings.LOG_LEVEL.upper()))
    root_logger.addHandler(console_handler)
    
    # Configure specific loggers
    loggers = [
        "uvicorn.access",
        "uvicorn.error", 
        "sqlalchemy.engine",
        "app"
    ]
    
    for logger_name in loggers:
        logger = logging.getLogger(logger_name)
        logger.setLevel(getattr(logging, settings.LOG_LEVEL.upper()))


def get_logger(name: str) -> logging.Logger:
    """Get logger instance"""
    return logging.getLogger(f"app.{name}")