"""Display themes for LDA package."""

from typing import Dict, Any


class DisplayTheme:
    """Base class for display themes."""
    
    def __init__(self):
        """Initialize theme."""
        self.colors = self._define_colors()
        self.symbols = self._define_symbols()
        self.styles = self._define_styles()
    
    def _define_colors(self) -> Dict[str, str]:
        """Define color scheme."""
        return {
            "primary": "blue",
            "success": "green",
            "error": "red",
            "warning": "yellow",
            "info": "cyan",
            "muted": "white"
        }
    
    def _define_symbols(self) -> Dict[str, str]:
        """Define symbols."""
        return {
            "success": "✓",
            "error": "✗",
            "warning": "!",
            "info": "i",
            "bullet": "•",
            "arrow": "→",
            "box_horizontal": "─",
            "box_vertical": "│",
            "box_top_left": "┌",
            "box_top_right": "┐",
            "box_bottom_left": "└",
            "box_bottom_right": "┘"
        }
    
    def _define_styles(self) -> Dict[str, Any]:
        """Define style settings."""
        return {
            "header_width": 60,
            "box_padding": 2,
            "table_separator": " | ",
            "tree_connector": "├── ",
            "tree_last_connector": "└── ",
            "tree_extension": "│   ",
            "tree_last_extension": "    "
        }


class ConservativeTheme(DisplayTheme):
    """Conservative theme for maximum compatibility."""
    
    def _define_symbols(self) -> Dict[str, str]:
        """Define ASCII-only symbols."""
        return {
            "success": "[OK]",
            "error": "[ERROR]",
            "warning": "[WARN]",
            "info": "[INFO]",
            "bullet": "*",
            "arrow": "->",
            "box_horizontal": "-",
            "box_vertical": "|",
            "box_top_left": "+",
            "box_top_right": "+",
            "box_bottom_left": "+",
            "box_bottom_right": "+"
        }


class RichTheme(DisplayTheme):
    """Rich theme with unicode symbols and colors."""
    
    def _define_colors(self) -> Dict[str, str]:
        """Define rich color scheme."""
        return {
            "primary": "bright_blue",
            "success": "bright_green",
            "error": "bright_red",
            "warning": "bright_yellow",
            "info": "bright_cyan",
            "muted": "dim"
        }
    
    def _define_symbols(self) -> Dict[str, str]:
        """Define unicode symbols."""
        return {
            "success": "✨",
            "error": "❌",
            "warning": "⚠️",
            "info": "ℹ️",
            "bullet": "▪",
            "arrow": "➜",
            "box_horizontal": "━",
            "box_vertical": "┃",
            "box_top_left": "┏",
            "box_top_right": "┓",
            "box_bottom_left": "┗",
            "box_bottom_right": "┛"
        }


class MinimalTheme(DisplayTheme):
    """Minimal theme with no decorations."""
    
    def _define_colors(self) -> Dict[str, str]:
        """Define minimal colors."""
        return {
            "primary": "",
            "success": "",
            "error": "",
            "warning": "",
            "info": "",
            "muted": ""
        }
    
    def _define_symbols(self) -> Dict[str, str]:
        """Define minimal symbols."""
        return {
            "success": "",
            "error": "",
            "warning": "",
            "info": "",
            "bullet": "-",
            "arrow": ">",
            "box_horizontal": "",
            "box_vertical": "",
            "box_top_left": "",
            "box_top_right": "",
            "box_bottom_left": "",
            "box_bottom_right": ""
        }


def get_theme(name: str) -> DisplayTheme:
    """Get theme by name."""
    themes = {
        "conservative": ConservativeTheme,
        "rich": RichTheme,
        "minimal": MinimalTheme
    }
    
    theme_class = themes.get(name.lower(), ConservativeTheme)
    return theme_class()