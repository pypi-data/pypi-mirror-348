# Utilities API Reference

The `lda.utils` module provides utility functions used throughout the LDA package.

## Functions

### File Operations

#### `ensure_directory()`

Ensure directory exists, creating if necessary.

```python
def ensure_directory(path: Union[str, Path]) -> Path
```

**Parameters:**
- `path`: Directory path

**Returns:**
- Path object for the directory

**Example:**
```python
from lda.utils import ensure_directory

output_dir = ensure_directory("outputs/figures")
```

#### `safe_file_write()`

Write file with atomic operation and backup.

```python
def safe_file_write(file_path: str, content: str, backup: bool = True) -> None
```

**Parameters:**
- `file_path`: Path to file
- `content`: Content to write
- `backup`: Create backup of existing file

**Example:**
```python
from lda.utils import safe_file_write

safe_file_write("config.yaml", yaml_content, backup=True)
```

#### `find_files()`

Find files matching patterns.

```python
def find_files(directory: str, patterns: List[str], 
               recursive: bool = True) -> List[Path]
```

**Parameters:**
- `directory`: Directory to search
- `patterns`: Glob patterns to match
- `recursive`: Search subdirectories

**Returns:**
- List of matching file paths

**Example:**
```python
from lda.utils import find_files

csv_files = find_files("data", ["*.csv", "*.tsv"], recursive=True)
```

#### `copy_with_metadata()`

Copy file preserving metadata.

```python
def copy_with_metadata(src: str, dst: str) -> None
```

**Parameters:**
- `src`: Source file path
- `dst`: Destination file path

**Example:**
```python
from lda.utils import copy_with_metadata

copy_with_metadata("original.csv", "backup/original.csv")
```

### String Utilities

#### `slugify()`

Convert string to valid filename/identifier.

```python
def slugify(text: str, separator: str = "_") -> str
```

**Parameters:**
- `text`: Text to slugify
- `separator`: Character to use as separator

**Returns:**
- Slugified string

**Example:**
```python
from lda.utils import slugify

filename = slugify("Project Report v2.1")  # "project_report_v2_1"
section_id = slugify("Data & Analysis", "-")  # "data-analysis"
```

#### `truncate()`

Truncate string to maximum length.

```python
def truncate(text: str, max_length: int, suffix: str = "...") -> str
```

**Parameters:**
- `text`: Text to truncate
- `max_length`: Maximum length
- `suffix`: Suffix to add if truncated

**Returns:**
- Truncated string

**Example:**
```python
from lda.utils import truncate

short = truncate("Long descriptive text", 10)  # "Long de..."
```

#### `format_bytes()`

Format byte size for human reading.

```python
def format_bytes(size: int, precision: int = 2) -> str
```

**Parameters:**
- `size`: Size in bytes
- `precision`: Decimal precision

**Returns:**
- Formatted string

**Example:**
```python
from lda.utils import format_bytes

print(format_bytes(1024))  # "1.00 KB"
print(format_bytes(1234567890))  # "1.15 GB"
```

### Date/Time Utilities

#### `parse_date()`

Parse date string with multiple formats.

```python
def parse_date(date_str: str) -> datetime
```

**Parameters:**
- `date_str`: Date string to parse

**Returns:**
- Parsed datetime object

**Supported formats:**
- ISO format: "2024-01-01"
- Relative: "yesterday", "1 week ago", "2 days ago"
- Natural: "last monday", "next friday"

**Example:**
```python
from lda.utils import parse_date

date1 = parse_date("2024-01-01")
date2 = parse_date("yesterday")
date3 = parse_date("1 week ago")
```

#### `format_timestamp()`

Format timestamp consistently.

```python
def format_timestamp(dt: datetime = None, fmt: str = None) -> str
```

**Parameters:**
- `dt`: Datetime object (defaults to now)
- `fmt`: Format string (defaults to ISO)

**Returns:**
- Formatted timestamp string

**Example:**
```python
from lda.utils import format_timestamp
from datetime import datetime

now_str = format_timestamp()  # Current time in ISO format
custom = format_timestamp(datetime.now(), "%Y-%m-%d")
```

#### `time_ago()`

Convert datetime to human-readable time ago.

```python
def time_ago(dt: datetime) -> str
```

**Parameters:**
- `dt`: Datetime object

**Returns:**
- Human-readable string

**Example:**
```python
from lda.utils import time_ago
from datetime import datetime, timedelta

past = datetime.now() - timedelta(hours=3)
print(time_ago(past))  # "3 hours ago"
```

### Data Processing

#### `flatten_dict()`

Flatten nested dictionary.

```python
def flatten_dict(data: dict, separator: str = ".") -> dict
```

**Parameters:**
- `data`: Dictionary to flatten
- `separator`: Key separator

**Returns:**
- Flattened dictionary

**Example:**
```python
from lda.utils import flatten_dict

nested = {
    "project": {
        "name": "Test",
        "meta": {
            "version": "1.0"
        }
    }
}
flat = flatten_dict(nested)
# {"project.name": "Test", "project.meta.version": "1.0"}
```

#### `merge_dicts()`

Deep merge dictionaries.

```python
def merge_dicts(base: dict, *updates: dict) -> dict
```

**Parameters:**
- `base`: Base dictionary
- `updates`: Dictionaries to merge

**Returns:**
- Merged dictionary

**Example:**
```python
from lda.utils import merge_dicts

base = {"a": 1, "b": {"c": 2}}
update = {"b": {"d": 3}, "e": 4}
result = merge_dicts(base, update)
# {"a": 1, "b": {"c": 2, "d": 3}, "e": 4}
```

#### `chunk_list()`

Split list into chunks.

```python
def chunk_list(items: List[Any], chunk_size: int) -> List[List[Any]]
```

**Parameters:**
- `items`: List to chunk
- `chunk_size`: Size of each chunk

**Returns:**
- List of chunks

**Example:**
```python
from lda.utils import chunk_list

data = list(range(10))
chunks = chunk_list(data, 3)
# [[0, 1, 2], [3, 4, 5], [6, 7, 8], [9]]
```

### Validation

#### `validate_path()`

Validate file/directory path.

```python
def validate_path(path: str, must_exist: bool = False, 
                  path_type: str = "any") -> bool
```

**Parameters:**
- `path`: Path to validate
- `must_exist`: Path must exist
- `path_type`: "file", "dir", or "any"

**Returns:**
- True if valid

**Example:**
```python
from lda.utils import validate_path

if validate_path("data.csv", must_exist=True, path_type="file"):
    print("File exists and is valid")
```

#### `validate_pattern()`

Validate filename pattern.

```python
def validate_pattern(pattern: str) -> bool
```

**Parameters:**
- `pattern`: Pattern to validate

**Returns:**
- True if valid pattern

**Example:**
```python
from lda.utils import validate_pattern

if validate_pattern("{project}_{date}_*.csv"):
    print("Valid pattern")
```

#### `validate_config()`

Validate configuration structure.

```python
def validate_config(config: dict, schema: dict) -> List[str]
```

**Parameters:**
- `config`: Configuration dictionary
- `schema`: Validation schema

**Returns:**
- List of validation errors

**Example:**
```python
from lda.utils import validate_config

schema = {
    "project": {"type": "dict", "required": True},
    "sections": {"type": "list", "required": True}
}
errors = validate_config(config_dict, schema)
```

### System Utilities

#### `get_system_info()`

Get system information.

```python
def get_system_info() -> dict
```

**Returns:**
- Dictionary with system info

**Example:**
```python
from lda.utils import get_system_info

info = get_system_info()
print(f"Python: {info['python_version']}")
print(f"OS: {info['os']} {info['os_version']}")
```

#### `check_dependencies()`

Check if dependencies are available.

```python
def check_dependencies(packages: List[str]) -> dict
```

**Parameters:**
- `packages`: Package names to check

**Returns:**
- Dictionary with availability status

**Example:**
```python
from lda.utils import check_dependencies

deps = check_dependencies(["pandas", "numpy", "missing_pkg"])
for pkg, available in deps.items():
    print(f"{pkg}: {'✓' if available else '✗'}")
```

#### `run_command()`

Run shell command safely.

```python
def run_command(cmd: List[str], cwd: str = None, 
                timeout: int = None) -> dict
```

**Parameters:**
- `cmd`: Command and arguments
- `cwd`: Working directory
- `timeout`: Timeout in seconds

**Returns:**
- Dictionary with output, error, and return code

**Example:**
```python
from lda.utils import run_command

result = run_command(["git", "status"], cwd="/project")
if result["returncode"] == 0:
    print(result["stdout"])
```

### Logging Utilities

#### `setup_logger()`

Setup logger with formatting.

```python
def setup_logger(name: str, level: str = "INFO", 
                 log_file: str = None) -> logging.Logger
```

**Parameters:**
- `name`: Logger name
- `level`: Log level
- `log_file`: Optional log file

**Returns:**
- Configured logger

**Example:**
```python
from lda.utils import setup_logger

logger = setup_logger("lda.analysis", level="DEBUG", 
                     log_file="analysis.log")
logger.info("Starting analysis")
```

#### `log_execution_time()`

Decorator to log function execution time.

```python
def log_execution_time(func: Callable) -> Callable
```

**Example:**
```python
from lda.utils import log_execution_time

@log_execution_time
def process_data(data):
    # Process data
    return results
```

## Usage Examples

### File Processing Pipeline

```python
from lda.utils import (
    find_files, ensure_directory, safe_file_write,
    format_bytes, format_timestamp
)
import json

# Find all CSV files
csv_files = find_files("data", ["*.csv"])
print(f"Found {len(csv_files)} CSV files")

# Create output directory
output_dir = ensure_directory("processed")

# Process files
manifest = []
for csv_file in csv_files:
    # Get file info
    size = csv_file.stat().st_size
    
    # Add to manifest
    manifest.append({
        "file": str(csv_file),
        "size": format_bytes(size),
        "processed": format_timestamp()
    })
    
    # Process file (example)
    # ... processing logic ...

# Save manifest
manifest_json = json.dumps(manifest, indent=2)
safe_file_write(output_dir / "manifest.json", manifest_json)
```

### Data Validation

```python
from lda.utils import validate_config, validate_path, validate_pattern

# Validate configuration
config = {
    "project": {"name": "Test"},
    "sections": [
        {"id": "sec01", "name": "Data"}
    ]
}

schema = {
    "project": {"type": "dict", "required": True},
    "sections": {"type": "list", "required": True, "min_items": 1}
}

errors = validate_config(config, schema)
if errors:
    for error in errors:
        print(f"Config error: {error}")

# Validate file paths
files = ["data.csv", "output/results.xlsx", "/invalid/path"]
for file in files:
    if validate_path(file, must_exist=True, path_type="file"):
        print(f"✓ {file} exists")
    else:
        print(f"✗ {file} not found")

# Validate patterns
patterns = [
    "{project}_{date}_data.csv",
    "**/*.txt",
    "[invalid pattern"
]
for pattern in patterns:
    if validate_pattern(pattern):
        print(f"✓ Valid: {pattern}")
    else:
        print(f"✗ Invalid: {pattern}")
```

### Date/Time Operations

```python
from lda.utils import parse_date, format_timestamp, time_ago
from datetime import datetime, timedelta

# Parse various date formats
dates = [
    "2024-01-01",
    "yesterday",
    "1 week ago",
    "last monday"
]

for date_str in dates:
    try:
        parsed = parse_date(date_str)
        print(f"{date_str} -> {format_timestamp(parsed)}")
    except ValueError as e:
        print(f"Error parsing '{date_str}': {e}")

# Time ago formatting
times = [
    datetime.now() - timedelta(seconds=30),
    datetime.now() - timedelta(hours=2),
    datetime.now() - timedelta(days=5)
]

for time in times:
    print(f"{format_timestamp(time)} was {time_ago(time)}")
```

### System Information

```python
from lda.utils import get_system_info, check_dependencies, run_command

# Get system info
info = get_system_info()
print("System Information:")
for key, value in info.items():
    print(f"  {key}: {value}")

# Check dependencies
required_packages = ["pandas", "numpy", "matplotlib", "seaborn"]
deps = check_dependencies(required_packages)

print("\nDependency Check:")
missing = []
for pkg, available in deps.items():
    status = "✓" if available else "✗"
    print(f"  {status} {pkg}")
    if not available:
        missing.append(pkg)

if missing:
    print(f"\nMissing packages: {', '.join(missing)}")

# Run system command
result = run_command(["python", "--version"])
if result["returncode"] == 0:
    print(f"\nPython version: {result['stdout'].strip()}")
```

### Batch Processing

```python
from lda.utils import chunk_list, log_execution_time, setup_logger
import time

# Setup logging
logger = setup_logger("batch_processor")

# Sample data
data = list(range(100))

@log_execution_time
def process_batch(items):
    """Process a batch of items."""
    logger.info(f"Processing batch of {len(items)} items")
    # Simulate processing
    time.sleep(0.1)
    return [item * 2 for item in items]

# Process in chunks
batch_size = 10
chunks = chunk_list(data, batch_size)
logger.info(f"Processing {len(data)} items in {len(chunks)} batches")

results = []
for i, chunk in enumerate(chunks):
    logger.info(f"Processing batch {i+1}/{len(chunks)}")
    batch_results = process_batch(chunk)
    results.extend(batch_results)

logger.info(f"Completed processing {len(results)} items")
```

## See Also

- [Core API](core.md) - Core functionality
- [Configuration API](config.md) - Configuration utilities
- [CLI API](cli.md) - Command-line utilities