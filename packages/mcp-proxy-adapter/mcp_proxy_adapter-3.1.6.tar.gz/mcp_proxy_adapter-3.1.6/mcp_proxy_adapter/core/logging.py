"""
Module for configuring logging in the microservice.
"""

import logging
import os
import sys
import uuid
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler
from typing import Dict, Optional, Any

from mcp_proxy_adapter.config import config


class CustomFormatter(logging.Formatter):
    """
    Custom formatter for logs with colored output in console.
    """
    grey = "\x1b[38;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    format_str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    FORMATS = {
        logging.DEBUG: grey + format_str + reset,
        logging.INFO: grey + format_str + reset,
        logging.WARNING: yellow + format_str + reset,
        logging.ERROR: red + format_str + reset,
        logging.CRITICAL: bold_red + format_str + reset
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


class RequestContextFilter(logging.Filter):
    """
    Filter for adding request context to logs.
    """
    
    def __init__(self, request_id: Optional[str] = None):
        super().__init__()
        self.request_id = request_id
    
    def filter(self, record):
        # Add request_id attribute to the record
        record.request_id = self.request_id or "no-request-id"
        return True


class RequestLogger:
    """
    Logger class for logging requests with context.
    """
    
    def __init__(self, logger_name: str, request_id: Optional[str] = None):
        """
        Initialize request logger.
        
        Args:
            logger_name: Logger name.
            request_id: Request identifier.
        """
        self.logger = logging.getLogger(logger_name)
        self.request_id = request_id or str(uuid.uuid4())
        self.filter = RequestContextFilter(self.request_id)
        self.logger.addFilter(self.filter)
    
    def debug(self, msg: str, *args, **kwargs):
        """Log message with DEBUG level."""
        self.logger.debug(f"[{self.request_id}] {msg}", *args, **kwargs)
    
    def info(self, msg: str, *args, **kwargs):
        """Log message with INFO level."""
        self.logger.info(f"[{self.request_id}] {msg}", *args, **kwargs)
    
    def warning(self, msg: str, *args, **kwargs):
        """Log message with WARNING level."""
        self.logger.warning(f"[{self.request_id}] {msg}", *args, **kwargs)
    
    def error(self, msg: str, *args, **kwargs):
        """Log message with ERROR level."""
        self.logger.error(f"[{self.request_id}] {msg}", *args, **kwargs)
    
    def exception(self, msg: str, *args, **kwargs):
        """Log exception with traceback."""
        self.logger.exception(f"[{self.request_id}] {msg}", *args, **kwargs)
    
    def critical(self, msg: str, *args, **kwargs):
        """Log message with CRITICAL level."""
        self.logger.critical(f"[{self.request_id}] {msg}", *args, **kwargs)


def setup_logging(
    level: Optional[str] = None,
    log_file: Optional[str] = None,
    max_bytes: Optional[int] = None,
    backup_count: Optional[int] = None,
    rotation_type: Optional[str] = None,
    rotation_when: Optional[str] = None,
    rotation_interval: Optional[int] = None
) -> logging.Logger:
    """
    Configure logging for the microservice.

    Args:
        level: Logging level. By default, taken from configuration.
        log_file: Path to log file. By default, taken from configuration.
        max_bytes: Maximum log file size in bytes. By default, taken from configuration.
        backup_count: Number of rotation files. By default, taken from configuration.
        rotation_type: Type of log rotation ('size' or 'time'). By default, taken from configuration.
        rotation_when: Time unit for rotation (D, H, M, S). By default, taken from configuration.
        rotation_interval: Interval for rotation. By default, taken from configuration.

    Returns:
        Configured logger.
    """
    # Get parameters from configuration if not explicitly specified
    level = level or config.get("logging.level", "INFO")
    log_file = log_file or config.get("logging.file")
    rotation_type = rotation_type or config.get("logging.rotation.type", "size")
    
    # Size-based rotation parameters
    max_bytes = max_bytes or config.get("logging.rotation.max_bytes", 10 * 1024 * 1024)  # 10 MB by default
    backup_count = backup_count or config.get("logging.rotation.backup_count", 5)
    
    # Time-based rotation parameters
    rotation_when = rotation_when or config.get("logging.rotation.when", "D")  # Daily by default
    rotation_interval = rotation_interval or config.get("logging.rotation.interval", 1)

    # Convert string logging level to constant
    numeric_level = getattr(logging, level.upper(), None)
    if not isinstance(numeric_level, int):
        numeric_level = logging.INFO

    # Create root logger
    logger = logging.getLogger("mcp_proxy_adapter")
    logger.setLevel(numeric_level)
    logger.handlers = []  # Clear handlers in case of repeated call

    # Create console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(numeric_level)
    console_handler.setFormatter(CustomFormatter())
    logger.addHandler(console_handler)

    # Create file handler if file specified
    if log_file:
        # Create directory for log file if it doesn't exist
        log_dir = os.path.dirname(log_file)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir, exist_ok=True)

        # Choose rotation type
        if rotation_type.lower() == "time":
            file_handler = TimedRotatingFileHandler(
                log_file,
                when=rotation_when,
                interval=rotation_interval,
                backupCount=backup_count,
                encoding="utf-8"
            )
        else:  # Default to size-based rotation
            file_handler = RotatingFileHandler(
                log_file,
                maxBytes=max_bytes,
                backupCount=backup_count,
                encoding="utf-8"
            )
            
        file_handler.setLevel(numeric_level)
        file_formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)

    # Configure loggers for external libraries
    log_levels = config.get("logging.levels", {})
    for logger_name, logger_level in log_levels.items():
        lib_logger = logging.getLogger(logger_name)
        lib_logger.setLevel(getattr(logging, logger_level.upper(), logging.INFO))

    return logger


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger with the specified name.
    
    Args:
        name: Logger name.
        
    Returns:
        Configured logger instance.
    """
    return logging.getLogger(name)


# Global logger for use throughout the application
logger = setup_logging()
