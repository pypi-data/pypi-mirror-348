"""Configuration management for LDA projects."""

import os
import yaml
import json
from pathlib import Path
from typing import Dict, Any, Optional, List
from datetime import datetime


class LDAConfig:
    """Configuration management for LDA projects."""
    
    DEFAULT_CONFIG = {
        "project": {
            "name": "New LDA Project",
            "code": "PROJ",
            "analyst": "Unknown",
            "root_folder": "."
        },
        "placeholders": {
            "proj": "${project.code}",
            "date": "${datetime.now().strftime('%Y%m%d')}"
        },
        "sections": [],
        "sandbox": [],
        "logging": {
            "level": "INFO",
            "format": "text"
        },
        "display": {
            "style": "conservative",
            "colors": True
        }
    }
    
    def __init__(self, config_file: Optional[str] = None):
        """Initialize with optional config file path."""
        # Deep copy defaults to avoid mutation
        import copy
        self.config = copy.deepcopy(self.DEFAULT_CONFIG)
        self.config_file = config_file
        
        if config_file:
            self.load_from_file(config_file)
    
    def load_from_file(self, path: str) -> None:
        """Load configuration from YAML/JSON file."""
        file_path = Path(path)
        
        if not file_path.exists():
            raise FileNotFoundError(f"Configuration file not found: {path}")
        
        with open(file_path, 'r') as f:
            if file_path.suffix in ['.yaml', '.yml']:
                data = yaml.safe_load(f)
            elif file_path.suffix == '.json':
                data = json.load(f)
            else:
                raise ValueError(f"Unsupported configuration format: {file_path.suffix}")
        
        self.load_from_dict(data)
    
    def load_from_dict(self, config_dict: Dict[str, Any]) -> None:
        """Load configuration from dictionary."""
        # Deep merge with defaults
        self.config = self._merge_dicts(self.DEFAULT_CONFIG, config_dict)
        self.validate()
    
    def _merge_dicts(self, base: Dict, update: Dict) -> Dict:
        """Deep merge two dictionaries."""
        result = base.copy()
        
        for key, value in update.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._merge_dicts(result[key], value)
            else:
                result[key] = value
        
        return result
    
    def validate(self) -> None:
        """Validate configuration schema."""
        # Required fields
        if not self.config.get("project", {}).get("code"):
            raise ValueError("project.code is required")
        
        if not self.config.get("project", {}).get("analyst"):
            raise ValueError("project.analyst is required")
        
        # Validate sections
        sections = self.config.get("sections", [])
        for i, section in enumerate(sections):
            if not isinstance(section, dict):
                raise ValueError(f"Section {i} must be a dictionary")
            
            if "name" not in section:
                raise ValueError(f"Section {i} missing required field: name")
            
            if "inputs" not in section and "outputs" not in section:
                raise ValueError(f"Section {section['name']} must have inputs or outputs")
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value with dot notation support."""
        keys = key.split('.')
        value = self.config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def set(self, key: str, value: Any) -> None:
        """Set configuration value with dot notation support."""
        keys = key.split('.')
        config = self.config
        
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        config[keys[-1]] = value
    
    def expand_placeholders(self, text: str) -> str:
        """Expand placeholders in text."""
        # Import datetime for placeholder expansion
        import datetime
        
        # Get all placeholders
        placeholders = {}
        
        # Add project placeholders
        project_data = self.get("project", {})
        for key, value in project_data.items():
            placeholders[f"project.{key}"] = value
        
        # Add custom placeholders
        custom_placeholders = self.get("placeholders", {})
        placeholders.update(custom_placeholders)
        
        # Add dynamic placeholders
        placeholders["datetime"] = datetime
        
        # Expand placeholders
        result = text
        
        # Handle ${...} style placeholders
        import re
        pattern = r'\$\{([^}]+)\}'
        
        def replace_func(match):
            expr = match.group(1)
            # First check if it's a simple variable reference
            if expr in placeholders:
                return str(placeholders[expr])
            # Try to evaluate as an expression
            try:
                # Create safe evaluation environment
                safe_dict = {"__builtins__": {}, "datetime": datetime}
                safe_dict.update(placeholders)
                return str(eval(expr, safe_dict))
            except:
                return match.group(0)
        
        result = re.sub(pattern, replace_func, result)
        
        # Handle {...} style placeholders
        for key, value in placeholders.items():
            if isinstance(value, str):
                result = result.replace(f"{{{key}}}", value)
        
        # Handle nested placeholders
        if "${" in result or "{" in result:
            # Recursively expand if there are still placeholders
            if result != text:  # Avoid infinite recursion
                result = self.expand_placeholders(result)
        
        return result
    
    def save(self, path: Optional[str] = None) -> None:
        """Save configuration to file."""
        save_path = path or self.config_file
        
        if not save_path:
            raise ValueError("No path specified for saving configuration")
        
        file_path = Path(save_path)
        
        with open(file_path, 'w') as f:
            if file_path.suffix in ['.yaml', '.yml']:
                yaml.dump(self.config, f, default_flow_style=False)
            else:
                json.dump(self.config, f, indent=2)
    
    def get_default_config(self) -> Dict[str, Any]:
        """Return default configuration template."""
        return self.DEFAULT_CONFIG.copy()
    
    def find_config_file(self, start_path: str = ".") -> Optional[str]:
        """Find configuration file by searching up the directory tree."""
        current = Path(start_path).resolve()
        
        # Config file names to search for
        config_names = ["lda_config.yaml", "lda_config.yml", "lda_config.json", 
                       ".lda/config.yaml", ".lda/config.yml", ".lda/config.json"]
        
        while current != current.parent:
            for name in config_names:
                config_path = current / name
                if config_path.exists():
                    return str(config_path)
            current = current.parent
        
        # Check environment variable
        env_config = os.environ.get("LDA_CONFIG")
        if env_config and Path(env_config).exists():
            return env_config
        
        return None