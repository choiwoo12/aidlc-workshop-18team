"""
Logging Configuration
"""
import logging
import os
from datetime import datetime
from backend.app.config import settings


def setup_logging():
    """
    Setup logging configuration
    """
    # Create logs directory if not exists
    log_dir = os.path.dirname(settings.log_file_path_today)
    if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir, exist_ok=True)
    
    # Configure logging
    logging.basicConfig(
        level=getattr(logging, settings.LOG_LEVEL),
        format="[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s",
        handlers=[
            logging.FileHandler(settings.log_file_path_today),
            logging.StreamHandler()
        ]
    )
    
    logger = logging.getLogger(__name__)
    logger.info(f"Logging initialized. Log file: {settings.log_file_path_today}")


def get_logger(name: str) -> logging.Logger:
    """
    Get logger instance
    
    Args:
        name: Logger name
        
    Returns:
        Logger instance
    """
    return logging.getLogger(name)
