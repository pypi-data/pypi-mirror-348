# LDA API Reference

## Core Modules

### lda.config

#### LDAConfig

Configuration management for LDA projects.

```python
from lda.config import LDAConfig

# Load from file
config = LDAConfig("lda_config.yaml")

# Load from dict
config = LDAConfig()
config.load_from_dict(config_dict)

# Access values
project_name = config.get("project.name")

# Set values
config.set("project.analyst", "John Doe")

# Save configuration
config.save("new_config.yaml")
```

**Methods:**
- `load_from_file(path)`: Load configuration from YAML/JSON file
- `load_from_dict(config_dict)`: Load from dictionary
- `validate()`: Validate configuration schema
- `get(key, default=None)`: Get value with dot notation
- `set(key, value)`: Set value with dot notation
- `expand_placeholders(text)`: Expand placeholders in text
- `save(path)`: Save configuration to file

### lda.core.scaffold

#### LDAScaffold

Main scaffold generator for LDA projects.

```python
from lda.core.scaffold import LDAScaffold
from lda.config import LDAConfig

config = LDAConfig("lda_config.yaml")
scaffold = LDAScaffold(config)

# Create project
result = scaffold.create_project()
```

**Methods:**
- `create_project()`: Create complete project structure
- `create_section(section_config)`: Create a single section
- `create_sandbox(sandbox_items)`: Create sandbox sections
- `validate_placeholders(pattern, placeholders)`: Validate placeholders
- `expand_pattern(pattern, placeholders)`: Expand pattern

### lda.core.manifest

#### LDAManifest

Centralized manifest management system.

```python
from lda.core.manifest import LDAManifest

manifest = LDAManifest("/path/to/project")

# Initialize project
manifest.init_project({
    "name": "My Project",
    "code": "MP2024",
    "analyst": "John Doe"
})

# Add section
manifest.add_section("01_data", section_config, provenance_id)

# Track file
manifest.track_file("01_data", "input", "data.csv")

# Detect changes
changes = manifest.detect_changes()

# Get history
history = manifest.get_history(limit=10)
```

**Methods:**
- `init_project(config)`: Initialize project manifest
- `add_section(name, config, provenance_id)`: Add section
- `track_file(section, file_type, filename, metadata)`: Track file
- `get_section_files(section)`: Get files for a section
- `detect_changes(section)`: Detect file changes
- `add_history(action, details)`: Add history entry
- `get_history(limit)`: Get recent history
- `get_project_status()`: Get project status
- `export_to_csv(output_path)`: Export to CSV

### lda.core.tracking

#### FileTracker

File tracking and provenance management.

```python
from lda.core.tracking import FileTracker

tracker = FileTracker()

# Track file
file_info = tracker.track_file("/path/to/file.csv", 
                              file_type="input",
                              metadata={"source": "experiment"})

# Calculate hash
file_hash = tracker.calculate_file_hash("/path/to/file.csv")

# Generate provenance ID
prov_id = tracker.generate_provenance_id("section_01")

# Detect changes
changes = tracker.detect_changes("/path/to/file.csv")
```

**Methods:**
- `calculate_file_hash(filepath)`: Calculate SHA-256 hash
- `generate_provenance_id(prefix)`: Generate unique ID
- `track_file(filepath, file_type, metadata)`: Track file
- `get_file_info(filepath)`: Get tracking info
- `detect_changes(filepath)`: Detect if file changed
- `get_all_changes()`: Get all file changes

### lda.core.errors

Custom error classes for LDA operations.

```python
from lda.core.errors import (
    LDAError,
    MissingPlaceholderError,
    ConfigurationError,
    ManifestError,
    ScaffoldError,
    FileTrackingError
)
```

## Display Modules

### lda.display.console

#### ConsoleDisplay

Console output utilities.

```python
from lda.display.console import ConsoleDisplay

display = ConsoleDisplay(style="conservative", colors=True)

# Display messages
display.info("Processing...")
display.success("Completed!")
display.warning("Check configuration")
display.error("Failed to process")

# Display structures
display.header("Project Status")
display.section("Details")
display.table(["Name", "Status"], [["File1", "OK"], ["File2", "Error"]])
display.list_items(["Item 1", "Item 2"])
display.tree({"root": {"child1": "value1", "child2": "value2"}})
```

**Methods:**
- `color(text, color)`: Apply color to text
- `bold(text)`: Make text bold
- `error(message)`: Display error
- `success(message)`: Display success
- `warning(message)`: Display warning
- `info(message)`: Display info
- `header(title, width)`: Display header
- `section(title)`: Display section
- `table(headers, rows)`: Display table
- `list_items(items, bullet)`: Display list
- `tree(data)`: Display tree structure

### lda.display.progress

#### ProgressIndicator

Progress tracking utilities.

```python
from lda.display.progress import ProgressIndicator

# With known total
with ProgressIndicator(total=100, description="Processing") as progress:
    for i in range(100):
        # Do work
        progress.update()

# Without total (spinner)
with ProgressIndicator(description="Loading") as progress:
    # Do work
    progress.update()
```

**Functions:**
- `track_progress(items, description)`: Generator for tracking progress
- `timed_operation(description)`: Decorator for timing operations

## Logging Modules

### lda.logging.logger

#### LDALogger

Central logging system.

```python
from lda.logging.logger import LDALogger

logger = LDALogger(
    log_dir=".lda/logs",
    log_level="INFO",
    log_format="text",
    console_output=True
)

# Log messages
logger.info("Starting process")
logger.warning("Low memory")
logger.error("Failed to load", exception=e)

# Log operations
logger.log_operation("data_import", "success", duration=1.5)
logger.log_file_operation("create", "/path/to/file", success=True)
logger.log_section_operation("01_data", "completed", success=True)
```

**Methods:**
- `debug(message, **kwargs)`: Log debug message
- `info(message, **kwargs)`: Log info message
- `warning(message, **kwargs)`: Log warning
- `error(message, exception, **kwargs)`: Log error
- `critical(message, **kwargs)`: Log critical
- `log_operation(operation, status, duration)`: Log operation
- `log_file_operation(action, filepath, success)`: Log file operation
- `log_section_operation(section, action, success)`: Log section operation

## CLI Modules

### lda.cli.main

#### LDACLI

Main CLI interface.

```python
from lda.cli.main import LDACLI

cli = LDACLI()
cli.run()
```

### lda.cli.commands

#### Commands

CLI command implementations.

```python
from lda.cli.commands import Commands

commands = Commands()

# Execute commands
commands.cmd_init(args, config, display)
commands.cmd_status(args, config, display)
commands.cmd_track(args, config, display)
```

### lda.cli.utils

Utility functions for CLI operations.

```python
from lda.cli.utils import (
    find_project_root,
    setup_logging,
    expand_path,
    ensure_directory,
    is_valid_project_name,
    format_file_size,
    format_duration,
    confirm_action,
    get_relative_path
)

# Find project root
project_root = find_project_root()

# Setup logging
setup_logging(verbose=True, quiet=False)

# Format values
size_str = format_file_size(1024000)  # "1.0 MB"
duration_str = format_duration(125.5)  # "2.1m"
```

## Usage Examples

### Creating a Project

```python
from lda import LDAConfig, LDAScaffold

# Create configuration
config = LDAConfig()
config.set("project.name", "My Analysis")
config.set("project.code", "MA2024")
config.set("project.analyst", "John Doe")
config.set("sections", [
    {
        "name": "01_data",
        "inputs": ["{proj}_raw.csv"],
        "outputs": ["{proj}_clean.csv"]
    }
])

# Save configuration
config.save("lda_config.yaml")

# Create scaffold
scaffold = LDAScaffold(config)
result = scaffold.create_project()
```

### Tracking Files

```python
from lda.core.manifest import LDAManifest

manifest = LDAManifest("/path/to/project")

# Track input file
manifest.track_file(
    section="01_data",
    file_type="input",
    filename="data.csv",
    metadata={"source": "database"}
)

# Check for changes
changes = manifest.detect_changes("01_data")
if changes["modified"]:
    print(f"Modified files: {changes['modified']}")
```

### Custom Display

```python
from lda.display.console import ConsoleDisplay
from lda.display.themes import get_theme

# Get theme
theme = get_theme("rich")

# Create display with theme
display = ConsoleDisplay(style="rich", colors=True)

# Use themed display
display.header("Analysis Results")
display.table(
    ["Metric", "Value", "Status"],
    [
        ["Accuracy", "95.2%", display.status_indicator("success")],
        ["Precision", "93.1%", display.status_indicator("success")],
        ["Recall", "89.5%", display.status_indicator("warning")]
    ]
)
```