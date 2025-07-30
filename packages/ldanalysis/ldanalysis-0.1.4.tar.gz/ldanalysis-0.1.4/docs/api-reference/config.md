# Configuration API Reference

The `lda.config` module provides classes for managing LDA project configuration.

## Classes

### `LDAConfig`

Main configuration class for LDA projects.

```python
from lda.config import LDAConfig

# Load configuration from file
config = LDAConfig("lda_config.yaml")

# Create new configuration
config = LDAConfig()
```

#### Constructor

```python
LDAConfig(config_file: Optional[str] = None)
```

**Parameters:**
- `config_file`: Path to configuration file (optional)

**Example:**
```python
# Load from default location
config = LDAConfig()

# Load from specific file
config = LDAConfig("/path/to/config.yaml")

# Create empty config
config = LDAConfig(config_file=None)
```

#### Properties

##### `config_file`

Path to the configuration file.

```python
config.config_file  # Returns: Path object
```

##### `is_loaded`

Check if configuration was loaded from file.

```python
if config.is_loaded:
    print(f"Loaded from: {config.config_file}")
```

#### Methods

##### `load()`

Load configuration from file.

```python
def load(self, config_file: Optional[str] = None) -> None
```

**Parameters:**
- `config_file`: Path to configuration file

**Raises:**
- `FileNotFoundError`: If config file doesn't exist
- `YAMLError`: If config file is invalid

**Example:**
```python
config = LDAConfig()
config.load("custom_config.yaml")
```

##### `save()`

Save configuration to file.

```python
def save(self, output_file: Optional[str] = None) -> None
```

**Parameters:**
- `output_file`: Path to save to (defaults to loaded file)

**Example:**
```python
config.save()  # Save to original file
config.save("backup_config.yaml")  # Save to new file
```

##### `get()`

Get configuration value by path.

```python
def get(self, path: str, default: Any = None) -> Any
```

**Parameters:**
- `path`: Dot-notation path to value
- `default`: Default value if path not found

**Example:**
```python
# Get nested value
name = config.get("project.name")

# Get with default
sections = config.get("sections", [])

# Deep nesting
hash_algo = config.get("tracking.hash_algorithm", "sha256")
```

##### `set()`

Set configuration value by path.

```python
def set(self, path: str, value: Any) -> None
```

**Parameters:**
- `path`: Dot-notation path to value
- `value`: Value to set

**Example:**
```python
# Set simple value
config.set("project.name", "My Project")

# Set nested value
config.set("tracking.auto_track", True)

# Create nested structure
config.set("new.nested.value", 42)
```

##### `validate()`

Validate configuration against schema.

```python
def validate(self) -> List[str]
```

**Returns:**
- List of validation errors (empty if valid)

**Example:**
```python
errors = config.validate()
if errors:
    for error in errors:
        print(f"Error: {error}")
```

##### `merge()`

Merge another configuration into this one.

```python
def merge(self, other: Union[dict, 'LDAConfig']) -> None
```

**Parameters:**
- `other`: Configuration to merge in

**Example:**
```python
# Merge from dict
config.merge({"project": {"name": "Updated"}})

# Merge from another config
other_config = LDAConfig("override.yaml")
config.merge(other_config)
```

##### `to_dict()`

Convert configuration to dictionary.

```python
def to_dict(self) -> dict
```

**Returns:**
- Configuration as dictionary

**Example:**
```python
data = config.to_dict()
print(json.dumps(data, indent=2))
```

##### `template_values()`

Get template values for string substitution.

```python
def template_values(self) -> dict
```

**Returns:**
- Dictionary of template values

**Example:**
```python
values = config.template_values()
# {'project_code': 'PROJ001', 'analyst': 'john.doe', ...}
```

### `ConfigSchema`

Schema for validating LDA configuration files.

```python
from lda.config import ConfigSchema

schema = ConfigSchema()
errors = schema.validate(config_dict)
```

#### Methods

##### `validate()`

Validate configuration dictionary against schema.

```python
def validate(self, config: dict) -> List[str]
```

**Parameters:**
- `config`: Configuration dictionary to validate

**Returns:**
- List of validation errors

**Example:**
```python
schema = ConfigSchema()
config_dict = {"project": {"name": "Test"}}
errors = schema.validate(config_dict)
```

##### `get_schema()`

Get the JSON schema definition.

```python
def get_schema(self) -> dict
```

**Returns:**
- JSON schema dictionary

**Example:**
```python
schema_def = schema.get_schema()
print(json.dumps(schema_def, indent=2))
```

## Configuration File Format

### Basic Structure

```yaml
# Project metadata
project:
  name: "My LDA Project"
  code: "PROJ001"
  analyst: "john.doe"
  created: "2024-01-01"

# Root folder for project files
root_folder: "./projects"

# Section definitions
sections:
  - id: "sec01"
    name: "Data Preprocessing"
    description: "Initial data cleaning"
    inputs:
      - pattern: "{project_code}_raw_*.csv"
        required: true
    outputs:
      - pattern: "{project_code}_clean_*.csv"
        required: true

# Tracking configuration
tracking:
  hash_algorithm: "sha256"
  auto_track: true
  ignore_patterns:
    - "*.tmp"
    - ".DS_Store"

# Workflow configuration
workflow:
  type: "standard"
  stages:
    - import
    - preprocess
    - analyze
    - report
```

### Variable Substitution

Use placeholders in configuration:

```yaml
placeholders:
  project_code: "STUDY001"
  year: "2024"
  site: "NYC"

sections:
  - id: "sec01"
    name: "Site {site} Data {year}"
    inputs:
      - pattern: "{project_code}_{site}_{year}_*.csv"
```

### Environment Variables

Reference environment variables:

```yaml
project:
  name: "${PROJECT_NAME}"
  analyst: "${USER}"

database:
  host: "${DB_HOST:localhost}"  # With default
  port: "${DB_PORT:5432}"
```

## Usage Examples

### Loading and Modifying Configuration

```python
from lda.config import LDAConfig

# Load configuration
config = LDAConfig("lda_config.yaml")

# Modify values
config.set("project.name", "Updated Project Name")
config.set("tracking.auto_track", False)

# Add new section
new_section = {
    "id": "sec99",
    "name": "Additional Analysis",
    "inputs": [{"pattern": "extra_*.csv"}]
}
sections = config.get("sections", [])
sections.append(new_section)
config.set("sections", sections)

# Save changes
config.save()
```

### Creating Configuration Programmatically

```python
from lda.config import LDAConfig

# Create new configuration
config = LDAConfig()

# Set basic project info
config.set("project.name", "New Study")
config.set("project.code", "NS001")
config.set("project.analyst", "jane.doe")

# Define sections
sections = [
    {
        "id": "sec01",
        "name": "Data Import",
        "inputs": [{"pattern": "raw_*.csv"}],
        "outputs": [{"pattern": "imported_*.csv"}]
    },
    {
        "id": "sec02", 
        "name": "Analysis",
        "inputs": [{"pattern": "imported_*.csv"}],
        "outputs": [{"pattern": "results_*.csv"}]
    }
]
config.set("sections", sections)

# Configure tracking
config.set("tracking.hash_algorithm", "sha256")
config.set("tracking.auto_track", True)

# Save configuration
config.save("new_project_config.yaml")
```

### Validating Configuration

```python
from lda.config import LDAConfig, ConfigSchema

# Load configuration
config = LDAConfig("lda_config.yaml")

# Validate structure
errors = config.validate()
if errors:
    print("Configuration errors:")
    for error in errors:
        print(f"  - {error}")
else:
    print("Configuration is valid")

# Custom validation
def validate_custom(config):
    errors = []
    
    # Check project code format
    project_code = config.get("project.code")
    if not project_code or not project_code.isupper():
        errors.append("Project code must be uppercase")
    
    # Check section IDs
    sections = config.get("sections", [])
    section_ids = [s["id"] for s in sections]
    if len(section_ids) != len(set(section_ids)):
        errors.append("Duplicate section IDs found")
    
    return errors

custom_errors = validate_custom(config)
```

### Working with Templates

```python
from lda.config import LDAConfig

config = LDAConfig("lda_config.yaml")

# Get template values
values = config.template_values()
print(f"Available placeholders: {values.keys()}")

# Apply templates to patterns
from string import Template

pattern = config.get("sections.0.inputs.0.pattern")
template = Template(pattern)
resolved = template.substitute(values)
print(f"Resolved pattern: {resolved}")

# Add custom placeholder
config.set("placeholders.custom_value", "test")
values = config.template_values()  # Now includes custom_value
```

## See Also

- [Core API](core.md) - Core classes documentation
- [Configuration Guide](../user-guide/configuration.md) - Configuration file format
- [CLI Reference](cli.md) - CLI configuration usage