"""Log formatters for LDA package."""

import json
import logging
from datetime import datetime
from typing import Dict, Any


class JSONFormatter(logging.Formatter):
    """JSON formatter for structured logging."""
    
    def format(self, record: logging.LogRecord) -> str:
        """Format log record as JSON."""
        log_data = {
            "timestamp": datetime.fromtimestamp(record.created).isoformat(),
            "level": record.levelname,
            "module": record.module,
            "message": record.getMessage()
        }
        
        # Add extra fields
        if hasattr(record, "operation"):
            log_data["operation"] = record.operation
        
        if hasattr(record, "status"):
            log_data["status"] = record.status
        
        if hasattr(record, "duration"):
            log_data["duration"] = record.duration
        
        if hasattr(record, "filepath"):
            log_data["filepath"] = record.filepath
        
        if hasattr(record, "section"):
            log_data["section"] = record.section
        
        # Add any other extra fields
        for key, value in record.__dict__.items():
            if key not in ["name", "msg", "args", "created", "filename", 
                          "funcName", "levelname", "levelno", "lineno", 
                          "module", "msecs", "pathname", "process", 
                          "processName", "relativeCreated", "thread", 
                          "threadName", "exc_info", "exc_text", "stack_info"]:
                log_data[key] = value
        
        # Add exception info if present
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)
        
        return json.dumps(log_data)


class TextFormatter(logging.Formatter):
    """Human-readable text formatter."""
    
    def __init__(self, include_timestamp: bool = True):
        """Initialize formatter."""
        self.include_timestamp = include_timestamp
        
        if include_timestamp:
            format_string = "%(asctime)s - %(levelname)s - %(message)s"
        else:
            format_string = "%(levelname)s - %(message)s"
        
        super().__init__(format_string, datefmt="%Y-%m-%d %H:%M:%S")
    
    def format(self, record: logging.LogRecord) -> str:
        """Format log record as text."""
        # Get base format
        result = super().format(record)
        
        # Add extra fields if present
        extras = []
        
        if hasattr(record, "operation"):
            extras.append(f"operation={record.operation}")
        
        if hasattr(record, "status"):
            extras.append(f"status={record.status}")
        
        if hasattr(record, "duration"):
            extras.append(f"duration={record.duration:.2f}s")
        
        if hasattr(record, "filepath"):
            extras.append(f"file={record.filepath}")
        
        if hasattr(record, "section"):
            extras.append(f"section={record.section}")
        
        if extras:
            result += f" [{', '.join(extras)}]"
        
        return result


class ColoredTextFormatter(TextFormatter):
    """Colored text formatter for console output."""
    
    # Color codes
    COLORS = {
        'DEBUG': '\033[36m',    # Cyan
        'INFO': '\033[32m',     # Green
        'WARNING': '\033[33m',  # Yellow
        'ERROR': '\033[31m',    # Red
        'CRITICAL': '\033[35m', # Magenta
        'RESET': '\033[0m'      # Reset
    }
    
    def format(self, record: logging.LogRecord) -> str:
        """Format log record with colors."""
        # Get base format
        result = super().format(record)
        
        # Add color if terminal supports it
        if hasattr(record, 'levelname') and record.levelname in self.COLORS:
            color = self.COLORS[record.levelname]
            reset = self.COLORS['RESET']
            result = f"{color}{result}{reset}"
        
        return result