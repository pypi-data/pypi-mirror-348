# Plugin System

LDA supports a plugin architecture that allows extending its functionality without modifying the core codebase. Plugins can add new commands, modify behavior, or integrate with external systems.

## Plugin Architecture

LDA plugins follow a simple architecture:

```
plugins/
├── __init__.py
├── my_plugin/
│   ├── __init__.py
│   ├── plugin.py
│   ├── commands.py
│   └── config.yaml
```

## Creating a Plugin

### Basic Plugin Structure

```python
# my_plugin/plugin.py
from lda.plugins import Plugin

class MyPlugin(Plugin):
    """Custom LDA plugin."""
    
    def __init__(self):
        super().__init__()
        self.name = "my_plugin"
        self.version = "1.0.0"
        self.description = "My custom LDA plugin"
    
    def initialize(self, config):
        """Initialize plugin with configuration."""
        self.config = config
        # Setup plugin resources
    
    def register_commands(self, cli):
        """Register CLI commands."""
        from .commands import MyCommands
        cli.add_command_group("my", MyCommands())
    
    def register_hooks(self, hooks):
        """Register event hooks."""
        hooks.register("pre_track", self.on_pre_track)
        hooks.register("post_scaffold", self.on_post_scaffold)
    
    def on_pre_track(self, event):
        """Handle pre-track event."""
        # Modify tracking behavior
        pass
    
    def on_post_scaffold(self, event):
        """Handle post-scaffold event."""
        # Additional scaffolding steps
        pass
```

### Plugin Configuration

```yaml
# my_plugin/config.yaml
plugin:
  name: my_plugin
  version: "1.0.0"
  author: "Your Name"
  description: "My custom LDA plugin"
  
settings:
  enabled: true
  options:
    custom_setting: "value"
    another_option: 42
```

### Adding Commands

```python
# my_plugin/commands.py
from lda.cli.commands import BaseCommands

class MyCommands(BaseCommands):
    """Custom plugin commands."""
    
    def cmd_custom(self, args, config, display):
        """Custom command implementation."""
        display.header("My Custom Command")
        display.info("Executing custom logic...")
        
        # Access plugin configuration
        plugin_config = config.get("plugins.my_plugin")
        
        # Perform custom operations
        result = self.custom_operation(args)
        
        display.success(f"Operation completed: {result}")
        return 0
    
    def custom_operation(self, args):
        """Plugin-specific logic."""
        # Implementation
        return "success"
```

## Installing Plugins

### From Package

```bash
# Install from PyPI
pip install lda-plugin-myextension

# Install from GitHub
pip install git+https://github.com/user/lda-plugin-myextension
```

### Manual Installation

```bash
# Copy plugin to LDA plugins directory
cp -r my_plugin ~/.lda/plugins/

# Or specify custom plugin directory
export LDA_PLUGIN_PATH=/path/to/plugins
```

### Configuration

Enable plugins in `lda_config.yaml`:

```yaml
plugins:
  enabled:
    - my_plugin
    - another_plugin
  
  my_plugin:
    custom_setting: "override_value"
    features:
      - feature1
      - feature2
```

## Available Hooks

LDA provides various hooks for plugin integration:

### File Tracking Hooks

- `pre_track`: Before files are tracked
- `post_track`: After files are tracked
- `track_filter`: Filter files during tracking
- `hash_calculation`: Custom hash algorithms

### Scaffolding Hooks

- `pre_scaffold`: Before project creation
- `post_scaffold`: After project creation
- `section_create`: When section is created
- `template_process`: Process templates

### Validation Hooks

- `pre_validate`: Before validation
- `post_validate`: After validation
- `custom_validators`: Add custom validators

### Export Hooks

- `pre_export`: Before export
- `post_export`: After export
- `export_format`: Custom export formats

## Example Plugins

### Git Integration Plugin

```python
# git_plugin/plugin.py
import subprocess
from lda.plugins import Plugin

class GitPlugin(Plugin):
    """Git integration for LDA."""
    
    def __init__(self):
        super().__init__()
        self.name = "git"
        self.version = "1.0.0"
    
    def register_hooks(self, hooks):
        hooks.register("post_track", self.auto_commit)
        hooks.register("post_scaffold", self.init_repo)
    
    def auto_commit(self, event):
        """Auto-commit after tracking."""
        if self.config.get("auto_commit", False):
            message = event.data.get("message", "Update tracking")
            subprocess.run(["git", "add", "."])
            subprocess.run(["git", "commit", "-m", message])
    
    def init_repo(self, event):
        """Initialize git repo for new projects."""
        if self.config.get("auto_init", True):
            project_dir = event.data["project_dir"]
            subprocess.run(["git", "init"], cwd=project_dir)
            
            # Create .gitignore
            gitignore = """
*.tmp
*.log
.DS_Store
__pycache__/
"""
            with open(f"{project_dir}/.gitignore", "w") as f:
                f.write(gitignore)
```

### S3 Backup Plugin

```python
# s3_backup/plugin.py
import boto3
from lda.plugins import Plugin

class S3BackupPlugin(Plugin):
    """S3 backup for LDA projects."""
    
    def __init__(self):
        super().__init__()
        self.name = "s3_backup"
        self.version = "1.0.0"
        self.s3 = None
    
    def initialize(self, config):
        """Initialize S3 client."""
        self.config = config
        self.s3 = boto3.client(
            's3',
            aws_access_key_id=config.get("aws_access_key"),
            aws_secret_access_key=config.get("aws_secret_key")
        )
        self.bucket = config.get("bucket")
    
    def register_commands(self, cli):
        from .commands import S3Commands
        cli.add_command_group("s3", S3Commands(self))
    
    def register_hooks(self, hooks):
        hooks.register("post_track", self.backup_files)
    
    def backup_files(self, event):
        """Backup tracked files to S3."""
        if not self.config.get("auto_backup", False):
            return
        
        for file_path in event.data["files"]:
            key = f"{event.data['project']}/{file_path}"
            self.s3.upload_file(file_path, self.bucket, key)
```

### Custom Validator Plugin

```python
# validator_plugin/plugin.py
from lda.plugins import Plugin

class ValidatorPlugin(Plugin):
    """Custom validation rules."""
    
    def __init__(self):
        super().__init__()
        self.name = "custom_validator"
        self.version = "1.0.0"
    
    def register_hooks(self, hooks):
        hooks.register("custom_validators", self.add_validators)
    
    def add_validators(self, event):
        """Add custom validators."""
        validators = event.data["validators"]
        
        # File size validator
        validators.append(self.validate_file_size)
        
        # Naming convention validator
        validators.append(self.validate_naming)
        
        # Required files validator
        validators.append(self.validate_required_files)
    
    def validate_file_size(self, context):
        """Check file sizes."""
        errors = []
        max_size = self.config.get("max_file_size", 100_000_000)  # 100MB
        
        for file_info in context["files"].values():
            if file_info["size"] > max_size:
                errors.append(
                    f"File {file_info['path']} exceeds size limit"
                )
        
        return errors
    
    def validate_naming(self, context):
        """Check naming conventions."""
        errors = []
        pattern = self.config.get("naming_pattern")
        
        if pattern:
            import re
            regex = re.compile(pattern)
            
            for file_path in context["files"]:
                if not regex.match(file_path):
                    errors.append(
                        f"File {file_path} doesn't match naming pattern"
                    )
        
        return errors
```

## Plugin Development Best Practices

### 1. Configuration Management

```python
class MyPlugin(Plugin):
    def initialize(self, config):
        # Validate configuration
        required = ["api_key", "endpoint"]
        for key in required:
            if key not in config:
                raise ValueError(f"Missing required config: {key}")
        
        # Set defaults
        self.config = {
            "timeout": 30,
            "retry_count": 3,
            **config
        }
```

### 2. Error Handling

```python
class MyPlugin(Plugin):
    def my_operation(self):
        try:
            # Plugin operation
            result = self.external_api_call()
        except ConnectionError as e:
            self.logger.error(f"Connection failed: {e}")
            # Graceful fallback
            return None
        except Exception as e:
            self.logger.error(f"Unexpected error: {e}")
            # Don't break LDA operation
            return None
```

### 3. Logging

```python
import logging

class MyPlugin(Plugin):
    def __init__(self):
        super().__init__()
        self.logger = logging.getLogger(f"lda.plugins.{self.name}")
    
    def operation(self):
        self.logger.info("Starting operation")
        # ... do work ...
        self.logger.debug("Operation details")
        self.logger.info("Operation completed")
```

### 4. Testing

```python
# tests/test_plugin.py
import pytest
from my_plugin import MyPlugin

class TestMyPlugin:
    def test_initialization(self):
        plugin = MyPlugin()
        assert plugin.name == "my_plugin"
    
    def test_command_registration(self):
        plugin = MyPlugin()
        cli = MockCLI()
        plugin.register_commands(cli)
        assert "my" in cli.command_groups
    
    def test_hook_behavior(self):
        plugin = MyPlugin()
        event = MockEvent({"files": ["test.csv"]})
        plugin.on_pre_track(event)
        # Assert expected behavior
```

## Publishing Plugins

### Package Structure

```
lda-plugin-myextension/
├── setup.py
├── README.md
├── LICENSE
├── requirements.txt
├── lda_plugin_myextension/
│   ├── __init__.py
│   ├── plugin.py
│   └── commands.py
└── tests/
    └── test_plugin.py
```

### Setup Configuration

```python
# setup.py
from setuptools import setup, find_packages

setup(
    name="lda-plugin-myextension",
    version="1.0.0",
    description="My LDA extension plugin",
    author="Your Name",
    packages=find_packages(),
    install_requires=[
        "lda-tool>=0.1.0",
        "requests>=2.25.0"
    ],
    entry_points={
        "lda.plugins": [
            "myextension = lda_plugin_myextension.plugin:MyPlugin"
        ]
    }
)
```

### Distribution

```bash
# Build package
python setup.py sdist bdist_wheel

# Upload to PyPI
pip install twine
twine upload dist/*
```

## Plugin Ecosystem

### Official Plugins

- **lda-git**: Git integration
- **lda-s3**: AWS S3 backup
- **lda-slack**: Slack notifications
- **lda-jupyter**: Jupyter notebook integration
- **lda-dvc**: Data Version Control integration

### Community Plugins

Find community plugins:
- [GitHub Topics](https://github.com/topics/lda-plugin)
- [PyPI Search](https://pypi.org/search/?q=lda-plugin)
- [LDA Plugin Registry](https://lda-plugins.github.io)

### Contributing Plugins

1. Follow naming convention: `lda-plugin-{name}`
2. Include comprehensive documentation
3. Add tests with >80% coverage
4. Submit to plugin registry
5. Tag with `lda-plugin` on GitHub

## See Also

- [API Reference](../api-reference/core.md) - Plugin API details
- [Integrations](integrations.md) - Built-in integrations
- [Configuration](../user-guide/configuration.md) - Plugin configuration