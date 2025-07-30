"""Progress indicator utilities for LDA package."""

import sys
import time
from typing import Optional, Generator, Any


class ProgressIndicator:
    """Handles progress indicators for LDA operations."""
    
    def __init__(self, total: Optional[int] = None, description: str = ""):
        """Initialize progress indicator."""
        self.total = total
        self.current = 0
        self.description = description
        self.start_time = time.time()
        self.last_update = 0
    
    def update(self, amount: int = 1, description: Optional[str] = None) -> None:
        """Update progress by amount."""
        self.current += amount
        if description:
            self.description = description
        
        # Update display only if enough time has passed
        current_time = time.time()
        if current_time - self.last_update > 0.1:  # Update every 100ms
            self._display()
            self.last_update = current_time
    
    def _display(self) -> None:
        """Display the progress."""
        if self.total:
            percentage = self.current / self.total
            bar_width = 30
            filled = int(bar_width * percentage)
            bar = "█" * filled + "░" * (bar_width - filled)
            
            elapsed = time.time() - self.start_time
            if percentage > 0:
                eta = elapsed / percentage - elapsed
                eta_str = f"ETA: {eta:.1f}s"
            else:
                eta_str = "ETA: --"
            
            print(f"\r{self.description} [{bar}] {percentage:6.1%} {eta_str}", 
                  end="", flush=True)
        else:
            # Spinner for unknown total
            spinner = "⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏"
            spin_idx = int((time.time() * 10) % len(spinner))
            print(f"\r{spinner[spin_idx]} {self.description} ({self.current})", 
                  end="", flush=True)
    
    def finish(self, message: Optional[str] = None) -> None:
        """Finish the progress indicator."""
        if message:
            print(f"\r{message}" + " " * 50)  # Clear the line
        else:
            print()  # New line
    
    def __enter__(self):
        """Enter context manager."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit context manager."""
        self.finish()


class Spinner:
    """Simple spinner for indeterminate progress."""
    
    def __init__(self, description: str = "Processing..."):
        """Initialize spinner."""
        self.description = description
        self.symbols = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        self.current = 0
        self.running = False
    
    def start(self) -> None:
        """Start the spinner."""
        self.running = True
        self._spin()
    
    def _spin(self) -> None:
        """Animate the spinner."""
        while self.running:
            print(f"\r{self.symbols[self.current]} {self.description}", 
                  end="", flush=True)
            self.current = (self.current + 1) % len(self.symbols)
            time.sleep(0.1)
    
    def stop(self, message: Optional[str] = None) -> None:
        """Stop the spinner."""
        self.running = False
        if message:
            print(f"\r{message}" + " " * 50)  # Clear the line
        else:
            print("\r" + " " * 50, end="\r")  # Clear the line
    
    def __enter__(self):
        """Enter context manager."""
        self.start()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit context manager."""
        self.stop()


def track_progress(items: list, description: str = "Processing") -> Generator[Any, None, None]:
    """Generator that tracks progress through a list of items."""
    total = len(items)
    
    with ProgressIndicator(total=total, description=description) as progress:
        for i, item in enumerate(items):
            yield item
            progress.update(description=f"{description} ({i+1}/{total})")


def timed_operation(description: str = "Operation"):
    """Decorator that times an operation and shows progress."""
    def decorator(func):
        def wrapper(*args, **kwargs):
            start_time = time.time()
            
            with Spinner(description=description):
                result = func(*args, **kwargs)
            
            elapsed = time.time() - start_time
            print(f"{description} completed in {elapsed:.2f}s")
            
            return result
        return wrapper
    return decorator