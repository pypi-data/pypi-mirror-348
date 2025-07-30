"""Console display utilities for LDA package."""

import sys
from typing import List, Dict, Any, Optional


class Console:
    """Handles console output for LDA."""
    
    def __init__(self, style: str = "conservative", colors: bool = True):
        """Initialize console display."""
        self.style = style
        self.colors = colors and sys.stdout.isatty()
        
        # Color codes
        self.colors_map = {
            "reset": "\033[0m",
            "bold": "\033[1m",
            "red": "\033[31m",
            "green": "\033[32m",
            "yellow": "\033[33m",
            "blue": "\033[34m",
            "cyan": "\033[36m",
            "white": "\033[37m"
        } if self.colors else {k: "" for k in ["reset", "bold", "red", "green", "yellow", "blue", "cyan", "white"]}
    
    def color(self, text: str, color: str) -> str:
        """Apply color to text if colors are enabled."""
        return f"{self.colors_map.get(color, '')}{text}{self.colors_map['reset']}"
    
    def bold(self, text: str) -> str:
        """Make text bold."""
        return self.color(text, "bold")
    
    def error(self, message: str) -> None:
        """Display error message."""
        print(f"{self.color('ERROR:', 'red')} {message}", file=sys.stderr)
    
    def success(self, message: str) -> None:
        """Display success message."""
        print(f"{self.color('SUCCESS:', 'green')} {message}")
    
    def warning(self, message: str) -> None:
        """Display warning message."""
        print(f"{self.color('WARNING:', 'yellow')} {message}")
    
    def info(self, message: str) -> None:
        """Display info message."""
        print(f"{self.color('INFO:', 'blue')} {message}")
    
    def header(self, title: str, width: int = 60) -> None:
        """Display a header."""
        print()
        print(self.bold(title.center(width)))
        print("=" * width)
    
    def section(self, title: str) -> None:
        """Display a section title."""
        print()
        print(self.bold(title))
        print("-" * len(title))
    
    def table(self, headers: List[str], rows: List[List[str]], 
              column_widths: Optional[List[int]] = None) -> None:
        """Display a simple table."""
        if not column_widths:
            # Calculate column widths
            column_widths = [len(h) for h in headers]
            for row in rows:
                for i, cell in enumerate(row):
                    column_widths[i] = max(column_widths[i], len(str(cell)))
        
        # Print headers
        header_line = " | ".join(h.ljust(w) for h, w in zip(headers, column_widths))
        print(self.bold(header_line))
        print("-" * len(header_line))
        
        # Print rows
        for row in rows:
            print(" | ".join(str(cell).ljust(w) for cell, w in zip(row, column_widths)))
    
    def list_items(self, items: List[str], bullet: str = "•") -> None:
        """Display a bulleted list."""
        for item in items:
            print(f"{bullet} {item}")
    
    def progress_bar(self, current: int, total: int, width: int = 50, 
                    label: str = "") -> None:
        """Display a simple progress bar."""
        percentage = current / total
        filled = int(width * percentage)
        bar = "█" * filled + "▒" * (width - filled)
        
        print(f"\r{label} [{bar}] {percentage:6.1%}", end="")
        
        if current >= total:
            print()  # New line when complete
    
    def tree(self, data: Dict[str, Any], prefix: str = "", is_last: bool = True) -> None:
        """Display a tree structure."""
        if isinstance(data, dict):
            items = list(data.items())
            for i, (key, value) in enumerate(items):
                is_last_item = i == len(items) - 1
                
                # Print current node
                connector = "└── " if is_last_item else "├── "
                print(f"{prefix}{connector}{key}")
                
                # Print children
                if isinstance(value, (dict, list)):
                    extension = "    " if is_last_item else "│   "
                    self.tree(value, prefix + extension, is_last_item)
                elif value:
                    extension = "    " if is_last_item else "│   "
                    print(f"{prefix}{extension}└── {value}")
        
        elif isinstance(data, list):
            for i, item in enumerate(data):
                is_last_item = i == len(data) - 1
                connector = "└── " if is_last_item else "├── "
                print(f"{prefix}{connector}{item}")
    
    def box(self, content: str, title: Optional[str] = None, width: int = 60) -> None:
        """Display content in a box."""
        lines = content.strip().split('\n')
        max_line_length = max(len(line) for line in lines) if lines else 0
        box_width = max(width, max_line_length + 4)
        
        # Top border
        if title:
            title_line = f"┌─ {title} " + "─" * (box_width - len(title) - 4) + "┐"
            print(self.bold(title_line))
        else:
            print("┌" + "─" * (box_width - 2) + "┐")
        
        # Content
        for line in lines:
            print(f"│ {line.ljust(box_width - 4)} │")
        
        # Bottom border
        print("└" + "─" * (box_width - 2) + "┘")
    
    def status_indicator(self, status: str) -> str:
        """Return colored status indicator."""
        indicators = {
            "success": self.color("✓", "green"),
            "error": self.color("✗", "red"),
            "warning": self.color("!", "yellow"),
            "info": self.color("i", "blue"),
            "pending": self.color("○", "white"),
            "complete": self.color("●", "green")
        }
        return indicators.get(status.lower(), status)