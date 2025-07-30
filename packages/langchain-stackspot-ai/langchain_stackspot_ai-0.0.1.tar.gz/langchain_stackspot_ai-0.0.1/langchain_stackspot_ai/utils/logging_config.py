"""Logging configuration for LangChain StackSpot AI integration."""

import logging
import json
from typing import Optional, Dict, Any, Union, Literal

# Global configuration variables
_DEBUG_ENABLED = False
_JSON_FORMATTED = False
_PRETTY_JSON = False

def configure_logging(
    debug: bool = False,
    json_format: bool = False,
    pretty_json: bool = False
) -> None:
    """
    Configure global logging settings for the LangChain StackSpot AI library.
    
    Args:
        debug: If True, sets logging level to DEBUG, otherwise INFO
        json_format: If True, all logs will be formatted as JSON
        pretty_json: If True and json_format is True, JSON logs will be pretty-printed
    """
    global _DEBUG_ENABLED, _JSON_FORMATTED, _PRETTY_JSON
    
    _DEBUG_ENABLED = debug
    _JSON_FORMATTED = json_format
    _PRETTY_JSON = pretty_json
    
    # Set the log level based on debug flag
    level = logging.DEBUG if debug else logging.INFO
    
    # Create a custom formatter based on json_format flag
    if json_format:
        formatter_class = JsonFormatter
    else:
        formatter_class = logging.Formatter
        formatter_args = {'fmt': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'}
    
    # Configure the root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(level)
    
    # Remove existing handlers to avoid duplicates
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
    
    # Add a new handler with the configured formatter
    handler = logging.StreamHandler()
    handler.setLevel(level)
    
    if json_format:
        formatter = formatter_class(pretty=pretty_json)
    else:
        formatter = formatter_class(**formatter_args)
    
    handler.setFormatter(formatter)
    root_logger.addHandler(handler)
    
    # Configure the library's loggers
    for logger_name in [
        "langchain_stackspot_ai",
        "langchain_stackspot_ai.agent_executor",
        "langchain_stackspot_ai.function_adapter",
        "langchain_stackspot_ai.output_parser"
    ]:
        logger = logging.getLogger(logger_name)
        logger.setLevel(level)
        # Propagate to the root logger which has our configured handler
        logger.propagate = True


class JsonFormatter(logging.Formatter):
    """Custom formatter that outputs log records as JSON."""
    
    def __init__(self, pretty: bool = False):
        """
        Initialize the JSON formatter.
        
        Args:
            pretty: If True, JSON will be pretty-printed with indentation
        """
        super().__init__()
        self.pretty = pretty
    
    def format(self, record: logging.LogRecord) -> str:
        """
        Format the log record as JSON.
        
        Args:
            record: The log record to format
            
        Returns:
            JSON-formatted log string
        """
        log_data = {
            "timestamp": self.formatTime(record),
            "level": record.levelname,
            "name": record.name,
            "message": record.getMessage()
        }
        
        # Add exception info if present
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)
        
        # Add extra attributes
        for key, value in record.__dict__.items():
            if key not in [
                "args", "asctime", "created", "exc_info", "exc_text", "filename",
                "funcName", "id", "levelname", "levelno", "lineno", "module",
                "msecs", "message", "msg", "name", "pathname", "process",
                "processName", "relativeCreated", "stack_info", "thread", "threadName"
            ]:
                log_data[key] = value
        
        # Check if the message is already a JSON string with metadata
        if hasattr(record, "metadata") and record.metadata:
            log_data["metadata"] = record.metadata
        
        # Format as JSON
        if self.pretty:
            return json.dumps(log_data, indent=2)
        else:
            return json.dumps(log_data)


def is_debug_enabled() -> bool:
    """Check if debug logging is enabled."""
    return _DEBUG_ENABLED


def is_json_formatted() -> bool:
    """Check if JSON formatting is enabled."""
    return _JSON_FORMATTED


def is_pretty_json() -> bool:
    """Check if pretty JSON formatting is enabled."""
    return _PRETTY_JSON
