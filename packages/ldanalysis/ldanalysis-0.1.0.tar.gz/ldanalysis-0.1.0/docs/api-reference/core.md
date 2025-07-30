# Core API Reference

The `lda.core` module provides the foundational classes for LDA functionality.

## Classes

### `LDAScaffold`

Manages project structure creation and scaffolding.

```python
from lda.core.scaffold import LDAScaffold
from lda.config import LDAConfig

config = LDAConfig("lda_config.yaml")
scaffold = LDAScaffold(config)
```

#### Constructor

```python
LDAScaffold(config: LDAConfig)
```

**Parameters:**
- `config`: LDA configuration object

**Example:**
```python
config = LDAConfig("lda_config.yaml")
scaffold = LDAScaffold(config)
```

#### Methods

##### `create_project()`

Create the complete project structure.

```python
def create_project(self) -> dict
```

**Returns:**
- Dictionary with creation results:
  - `project_folder`: Path to created project
  - `sections`: List of created sections
  - `files`: List of created files
  - `duration`: Time taken in seconds

**Example:**
```python
result = scaffold.create_project()
print(f"Created project at: {result['project_folder']}")
print(f"Created {len(result['sections'])} sections")
```

##### `create_section()`

Create a single section.

```python
def create_section(self, section_config: dict) -> dict
```

**Parameters:**
- `section_config`: Section configuration dictionary

**Returns:**
- Dictionary with section details

**Example:**
```python
section = {
    "id": "sec01",
    "name": "Preprocessing",
    "inputs": [{"pattern": "raw_*.csv"}]
}
result = scaffold.create_section(section)
```

##### `validate_config()`

Validate configuration before scaffolding.

```python
def validate_config(self) -> List[str]
```

**Returns:**
- List of validation errors

**Example:**
```python
errors = scaffold.validate_config()
if errors:
    for error in errors:
        print(f"Error: {error}")
```

### `LDAManifest`

Manages file manifests and tracking.

```python
from lda.core.manifest import LDAManifest

manifest = LDAManifest("section/manifest.json")
```

#### Constructor

```python
LDAManifest(manifest_file: str)
```

**Parameters:**
- `manifest_file`: Path to manifest file

**Example:**
```python
manifest = LDAManifest("sec01/manifest.json")
```

#### Properties

##### `version`

Manifest format version.

```python
manifest.version  # Returns: "1.0"
```

##### `section`

Section identifier.

```python
manifest.section  # Returns: "sec01_preprocessing"
```

##### `files`

Dictionary of tracked files.

```python
manifest.files  # Returns: dict of file info
```

#### Methods

##### `load()`

Load manifest from file.

```python
def load(self) -> None
```

**Raises:**
- `FileNotFoundError`: If manifest doesn't exist
- `JSONDecodeError`: If manifest is invalid

**Example:**
```python
manifest = LDAManifest("manifest.json")
manifest.load()
```

##### `save()`

Save manifest to file.

```python
def save(self) -> None
```

**Example:**
```python
manifest.save()
```

##### `track_file()`

Add or update file in manifest.

```python
def track_file(self, file_path: str, message: str = None) -> dict
```

**Parameters:**
- `file_path`: Path to file
- `message`: Optional tracking message

**Returns:**
- File tracking information

**Example:**
```python
info = manifest.track_file("outputs/results.csv", "Updated results")
print(f"File hash: {info['hash']}")
```

##### `remove_file()`

Remove file from manifest.

```python
def remove_file(self, file_path: str) -> bool
```

**Parameters:**
- `file_path`: Path to file

**Returns:**
- True if file was removed

**Example:**
```python
if manifest.remove_file("temp/scratch.txt"):
    print("File removed from tracking")
```

##### `get_file_info()`

Get information about tracked file.

```python
def get_file_info(self, file_path: str) -> Optional[dict]
```

**Parameters:**
- `file_path`: Path to file

**Returns:**
- File information or None

**Example:**
```python
info = manifest.get_file_info("data/input.csv")
if info:
    print(f"Last modified: {info['modified']}")
```

##### `get_changes()`

Get files that have changed.

```python
def get_changes(self) -> List[dict]
```

**Returns:**
- List of changed files

**Example:**
```python
changes = manifest.get_changes()
for change in changes:
    print(f"{change['file']}: {change['status']}")
```

##### `validate()`

Validate manifest integrity.

```python
def validate(self) -> List[str]
```

**Returns:**
- List of validation errors

**Example:**
```python
errors = manifest.validate()
if errors:
    print("Manifest issues found:")
    for error in errors:
        print(f"  - {error}")
```

### `LDATracker`

File tracking and hash management.

```python
from lda.core.tracking import LDATracker

tracker = LDATracker()
```

#### Methods

##### `calculate_hash()`

Calculate file hash.

```python
def calculate_hash(self, file_path: str, algorithm: str = "sha256") -> str
```

**Parameters:**
- `file_path`: Path to file
- `algorithm`: Hash algorithm to use

**Returns:**
- Hex digest of file hash

**Example:**
```python
tracker = LDATracker()
hash_value = tracker.calculate_hash("data.csv")
print(f"SHA256: {hash_value}")
```

##### `track_directory()`

Track all files in directory.

```python
def track_directory(self, directory: str, patterns: List[str] = None) -> dict
```

**Parameters:**
- `directory`: Directory to track
- `patterns`: Optional file patterns to include

**Returns:**
- Dictionary of tracked files

**Example:**
```python
files = tracker.track_directory("outputs", patterns=["*.csv", "*.png"])
print(f"Tracked {len(files)} files")
```

##### `compare_files()`

Compare two files.

```python
def compare_files(self, file1: str, file2: str) -> bool
```

**Parameters:**
- `file1`: First file path
- `file2`: Second file path

**Returns:**
- True if files are identical

**Example:**
```python
if tracker.compare_files("old.csv", "new.csv"):
    print("Files are identical")
else:
    print("Files differ")
```

### `LDAError`

Base exception for LDA errors.

```python
from lda.core.errors import LDAError

try:
    # LDA operations
except LDAError as e:
    print(f"LDA error: {e}")
```

#### Subclasses

##### `ConfigurationError`

Configuration-related errors.

```python
from lda.core.errors import ConfigurationError

raise ConfigurationError("Invalid project name")
```

##### `ManifestError`

Manifest-related errors.

```python
from lda.core.errors import ManifestError

raise ManifestError("Corrupt manifest file")
```

##### `ScaffoldError`

Scaffolding errors.

```python
from lda.core.errors import ScaffoldError

raise ScaffoldError("Section already exists")
```

##### `TrackingError`

File tracking errors.

```python
from lda.core.errors import TrackingError

raise TrackingError("Cannot track system file")
```

## Usage Examples

### Creating a New Project

```python
from lda.config import LDAConfig
from lda.core.scaffold import LDAScaffold

# Create configuration
config = LDAConfig()
config.set("project.name", "Clinical Trial 001")
config.set("project.code", "CT001")

# Define sections
sections = [
    {
        "id": "sec01_protocol",
        "name": "Study Protocol",
        "inputs": [{"pattern": "protocol_*.pdf"}]
    },
    {
        "id": "sec02_data", 
        "name": "Clinical Data",
        "inputs": [{"pattern": "clinical_*.csv"}],
        "outputs": [{"pattern": "cleaned_*.csv"}]
    }
]
config.set("sections", sections)

# Create scaffold
scaffold = LDAScaffold(config)
result = scaffold.create_project()

print(f"Project created: {result['project_folder']}")
```

### Managing File Tracking

```python
from lda.core.manifest import LDAManifest
from lda.core.tracking import LDATracker

# Load manifest
manifest = LDAManifest("sec01/manifest.json")

# Track new files
tracker = LDATracker()
new_files = tracker.track_directory("sec01/outputs", ["*.csv"])

for file_path, file_info in new_files.items():
    manifest.track_file(file_path, "Generated output")

# Check for changes
changes = manifest.get_changes()
if changes:
    print(f"Found {len(changes)} changed files")
    manifest.save()
```

### Error Handling

```python
from lda.core.errors import LDAError, ConfigurationError
from lda.core.scaffold import LDAScaffold

try:
    config = LDAConfig("config.yaml")
    scaffold = LDAScaffold(config)
    scaffold.create_project()
    
except ConfigurationError as e:
    print(f"Configuration error: {e}")
    # Handle configuration issues
    
except ScaffoldError as e:
    print(f"Scaffolding error: {e}")
    # Handle scaffold issues
    
except LDAError as e:
    print(f"General LDA error: {e}")
    # Handle other LDA errors
    
except Exception as e:
    print(f"Unexpected error: {e}")
    # Handle non-LDA errors
```

### Custom Validation

```python
from lda.core.manifest import LDAManifest

class CustomManifest(LDAManifest):
    def validate_custom(self):
        """Add custom validation rules."""
        errors = []
        
        # Check file naming convention
        for file_path in self.files:
            if not file_path.startswith(self.section):
                errors.append(f"File {file_path} doesn't follow naming convention")
        
        # Check required files
        required = ["inputs/data.csv", "outputs/results.csv"]
        for req_file in required:
            if req_file not in self.files:
                errors.append(f"Required file {req_file} is missing")
        
        return errors

manifest = CustomManifest("manifest.json")
custom_errors = manifest.validate_custom()
```

### Batch Operations

```python
from lda.core.manifest import LDAManifest
from lda.core.tracking import LDATracker
import glob

# Track multiple sections
tracker = LDATracker()

for section_dir in glob.glob("sec*"):
    manifest_file = f"{section_dir}/manifest.json"
    manifest = LDAManifest(manifest_file)
    
    # Track all CSV files
    csv_files = glob.glob(f"{section_dir}/**/*.csv", recursive=True)
    
    for csv_file in csv_files:
        if csv_file not in manifest.files:
            manifest.track_file(csv_file, "Batch tracking")
    
    manifest.save()
    print(f"Updated {section_dir}: {len(manifest.files)} files tracked")
```

## See Also

- [Configuration API](config.md) - Configuration management
- [CLI API](cli.md) - Command-line interface
- [Error Handling](errors.md) - Complete error reference