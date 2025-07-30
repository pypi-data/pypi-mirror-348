"""Main logger class for LDA package."""

import os
import logging
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, Any

from .formatters import JSONFormatter, TextFormatter


class LDALogger:
    """Central logging system for LDA operations."""
    
    def __init__(self, 
                 log_dir: Optional[str] = None,
                 log_level: str = "INFO",
                 log_format: str = "text",
                 console_output: bool = True):
        """Initialize logger."""
        self.log_dir = Path(log_dir) if log_dir else Path(".lda/logs")
        self.log_level = getattr(logging, log_level.upper(), logging.INFO)
        self.log_format = log_format
        self.console_output = console_output
        
        # Create log directory
        self.log_dir.mkdir(parents=True, exist_ok=True)
        
        # Set up logger
        self.logger = logging.getLogger("lda")
        self.logger.setLevel(self.log_level)
        
        # Remove existing handlers
        self.logger.handlers.clear()
        
        # Add file handler
        self._add_file_handler()
        
        # Add console handler if requested
        if self.console_output:
            self._add_console_handler()
    
    def _add_file_handler(self) -> None:
        """Add file handler to logger."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = self.log_dir / f"lda_{timestamp}.log"
        
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(self.log_level)
        
        # Set formatter based on format type
        if self.log_format == "json":
            formatter = JSONFormatter()
        else:
            formatter = TextFormatter()
        
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)
    
    def _add_console_handler(self) -> None:
        """Add console handler to logger."""
        console_handler = logging.StreamHandler()
        console_handler.setLevel(self.log_level)
        
        # Use text formatter for console
        formatter = TextFormatter(include_timestamp=False)
        console_handler.setFormatter(formatter)
        
        self.logger.addHandler(console_handler)
    
    def debug(self, message: str, **kwargs) -> None:
        """Log debug message."""
        self.logger.debug(message, extra=kwargs)
    
    def info(self, message: str, **kwargs) -> None:
        """Log info message."""
        self.logger.info(message, extra=kwargs)
    
    def warning(self, message: str, **kwargs) -> None:
        """Log warning message."""
        self.logger.warning(message, extra=kwargs)
    
    def error(self, message: str, exception: Optional[Exception] = None, **kwargs) -> None:
        """Log error message."""
        if exception:
            kwargs["exception_type"] = type(exception).__name__
            kwargs["exception_message"] = str(exception)
        self.logger.error(message, exc_info=exception, extra=kwargs)
    
    def critical(self, message: str, **kwargs) -> None:
        """Log critical message."""
        self.logger.critical(message, extra=kwargs)
    
    def log_operation(self, operation: str, status: str, 
                     duration: Optional[float] = None, **kwargs) -> None:
        """Log an operation with standard fields."""
        log_data = {
            "operation": operation,
            "status": status,
            "timestamp": datetime.now().isoformat()
        }
        
        if duration is not None:
            log_data["duration"] = duration
        
        log_data.update(kwargs)
        
        if status == "error":
            self.error(f"Operation {operation} failed", **log_data)
        else:
            self.info(f"Operation {operation} {status}", **log_data)
    
    def log_file_operation(self, action: str, filepath: str, 
                          success: bool, **kwargs) -> None:
        """Log file operation."""
        log_data = {
            "action": action,
            "filepath": filepath,
            "success": success,
            "timestamp": datetime.now().isoformat()
        }
        
        log_data.update(kwargs)
        
        if success:
            self.info(f"File {action}: {filepath}", **log_data)
        else:
            self.error(f"File {action} failed: {filepath}", **log_data)
    
    def log_section_operation(self, section: str, action: str, 
                            success: bool, **kwargs) -> None:
        """Log section operation."""
        log_data = {
            "section": section,
            "action": action,
            "success": success,
            "timestamp": datetime.now().isoformat()
        }
        
        log_data.update(kwargs)
        
        if success:
            self.info(f"Section {section}: {action}", **log_data)
        else:
            self.error(f"Section {section}: {action} failed", **log_data)
    
    def get_log_file(self) -> Optional[str]:
        """Get current log file path."""
        for handler in self.logger.handlers:
            if isinstance(handler, logging.FileHandler):
                return handler.baseFilename
        return None
    
    def set_level(self, level: str) -> None:
        """Change log level."""
        self.log_level = getattr(logging, level.upper(), logging.INFO)
        self.logger.setLevel(self.log_level)
        
        for handler in self.logger.handlers:
            handler.setLevel(self.log_level)