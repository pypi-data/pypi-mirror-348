"""Logging utilities for LangChain StackSpot AI integration."""

import logging
import json
from typing import Dict, Any, Optional

def setup_logger(name: str, level: int = logging.INFO) -> logging.Logger:
    """
    Set up a logger with the specified name and level.
    
    Args:
        name: Logger name
        level: Logging level (default: logging.INFO)
        
    Returns:
        Configured logger
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Check if the logger already has handlers to avoid duplicate handlers
    if not logger.handlers:
        # Create console handler
        handler = logging.StreamHandler()
        handler.setLevel(level)
        
        # Create formatter
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        
        # Add handler to logger
        logger.addHandler(handler)
    
    return logger

def log_with_metadata(logger: logging.Logger, level: int, message: str, metadata: Optional[Dict[str, Any]] = None) -> None:
    """
    Log a message with additional metadata in JSON format.
    
    Args:
        logger: Logger to use
        level: Logging level
        message: Log message
        metadata: Additional metadata to include in the log
    """
    if metadata:
        log_data = {
            "message": message,
            "metadata": metadata
        }
        logger.log(level, json.dumps(log_data))
    else:
        logger.log(level, message)

def log_debug(logger: logging.Logger, message: str, metadata: Optional[Dict[str, Any]] = None) -> None:
    """Log a debug message with metadata."""
    log_with_metadata(logger, logging.DEBUG, message, metadata)

def log_info(logger: logging.Logger, message: str, metadata: Optional[Dict[str, Any]] = None) -> None:
    """Log an info message with metadata."""
    log_with_metadata(logger, logging.INFO, message, metadata)

def log_warning(logger: logging.Logger, message: str, metadata: Optional[Dict[str, Any]] = None) -> None:
    """Log a warning message with metadata."""
    log_with_metadata(logger, logging.WARNING, message, metadata)

def log_error(logger: logging.Logger, message: str, metadata: Optional[Dict[str, Any]] = None) -> None:
    """Log an error message with metadata."""
    log_with_metadata(logger, logging.ERROR, message, metadata)

def log_critical(logger: logging.Logger, message: str, metadata: Optional[Dict[str, Any]] = None) -> None:
    """Log a critical message with metadata."""
    log_with_metadata(logger, logging.CRITICAL, message, metadata)

def log_human_message(logger: logging.Logger, message: str, metadata: Optional[Dict[str, Any]] = None) -> None:
    """Log a human message with metadata."""
    metadata = metadata or {}
    metadata["message_type"] = "human"
    log_info(logger, message, metadata)

def log_ai_message(logger: logging.Logger, message: str, metadata: Optional[Dict[str, Any]] = None) -> None:
    """Log an AI message with metadata."""
    metadata = metadata or {}
    metadata["message_type"] = "ai"
    log_info(logger, message, metadata)

def log_system_message(logger: logging.Logger, message: str, metadata: Optional[Dict[str, Any]] = None) -> None:
    """Log a system message with metadata."""
    metadata = metadata or {}
    metadata["message_type"] = "system"
    log_info(logger, message, metadata)

def log_function_message(logger: logging.Logger, message: str, metadata: Optional[Dict[str, Any]] = None) -> None:
    """Log a function message with metadata."""
    metadata = metadata or {}
    metadata["message_type"] = "function"
    log_info(logger, message, metadata)

def log_tool_message(logger: logging.Logger, message: str, metadata: Optional[Dict[str, Any]] = None) -> None:
    """Log a tool message with metadata."""
    metadata = metadata or {}
    metadata["message_type"] = "tool"
    log_info(logger, message, metadata)
