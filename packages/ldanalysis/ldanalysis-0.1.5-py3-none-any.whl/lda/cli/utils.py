"""Utility functions for LDA CLI."""

import os
import logging
from pathlib import Path
from typing import Optional

from ..logging.logger import LDALogger


def find_project_root(start_path: str = ".") -> Optional[str]:
    """Find project root by looking for manifest files."""
    current = Path(start_path).resolve()
    
    # Check for .lda directory
    while current != current.parent:
        if (current / ".lda").exists():
            return str(current)
        
        # Also check for old-style manifest
        if (current / "lda_manifest.csv").exists():
            return str(current)
        
        current = current.parent
    
    return None


def setup_logging(verbose: bool = False, quiet: bool = False) -> None:
    """Set up logging based on CLI flags."""
    if quiet:
        log_level = "ERROR"
    elif verbose:
        log_level = "DEBUG"
    else:
        log_level = "INFO"
    
    # Configure root logger
    logging.basicConfig(
        level=getattr(logging, log_level),
        format='%(levelname)s: %(message)s'
    )
    
    # Set up LDA logger
    logger = LDALogger(
        log_level=log_level,
        console_output=not quiet,
        log_format="text"
    )


def expand_path(path: str) -> str:
    """Expand user home directory and make path absolute."""
    expanded = os.path.expanduser(path)
    return str(Path(expanded).resolve())


def ensure_directory(path: str) -> None:
    """Ensure directory exists, creating if necessary."""
    Path(path).mkdir(parents=True, exist_ok=True)


def is_valid_project_name(name: str) -> bool:
    """Check if project name is valid."""
    # Must contain only alphanumeric, underscore, or hyphen
    import re
    return bool(re.match(r'^[a-zA-Z0-9_-]+$', name))


def format_file_size(size: int) -> str:
    """Format file size in human-readable format."""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size < 1024.0:
            return f"{size:.1f} {unit}"
        size /= 1024.0
    return f"{size:.1f} TB"


def format_duration(seconds: float) -> str:
    """Format duration in human-readable format."""
    if seconds < 60:
        return f"{seconds:.1f}s"
    elif seconds < 3600:
        minutes = seconds / 60
        return f"{minutes:.1f}m"
    else:
        hours = seconds / 3600
        return f"{hours:.1f}h"


def confirm_action(prompt: str, default: bool = False) -> bool:
    """Ask user for confirmation."""
    default_answer = "Y/n" if default else "y/N"
    
    response = input(f"{prompt} [{default_answer}]: ").strip().lower()
    
    if not response:
        return default
    
    return response[0] == 'y'


def get_relative_path(path: str, base: Optional[str] = None) -> str:
    """Get relative path from base directory."""
    if base is None:
        base = os.getcwd()
    
    try:
        return str(Path(path).relative_to(base))
    except ValueError:
        # Path is not relative to base
        return path