# CLI API Reference

The `lda.cli` module provides the command-line interface implementation.

## Classes

### `LDACLI`

Main CLI application class.

```python
from lda.cli.main import LDACLI

cli = LDACLI()
exit_code = cli.run()
```

#### Constructor

```python
LDACLI()
```

**Example:**
```python
cli = LDACLI()
```

#### Properties

##### `parser`

Argument parser instance.

```python
cli.parser  # Returns: argparse.ArgumentParser
```

##### `commands`

Command handler instance.

```python
cli.commands  # Returns: Commands instance
```

##### `display`

Console display instance.

```python
cli.display  # Returns: Console instance
```

#### Methods

##### `run()`

Run the CLI with given arguments.

```python
def run(self, args: Optional[List[str]] = None) -> int
```

**Parameters:**
- `args`: Command line arguments (defaults to sys.argv)

**Returns:**
- Exit code (0 for success)

**Example:**
```python
# Run with system arguments
exit_code = cli.run()

# Run with custom arguments
exit_code = cli.run(["init", "--name", "MyProject"])
```

##### `create_parser()`

Create the argument parser.

```python
def create_parser(self) -> argparse.ArgumentParser
```

**Returns:**
- Configured argument parser

**Example:**
```python
parser = cli.create_parser()
parsed_args = parser.parse_args(["status", "--format", "json"])
```

### `Commands`

Command implementation class.

```python
from lda.cli.commands import Commands

commands = Commands()
```

#### Methods

##### `cmd_init()`

Initialize new project.

```python
@staticmethod
def cmd_init(args: argparse.Namespace, config: Optional[LDAConfig], display: Console) -> int
```

**Parameters:**
- `args`: Parsed command arguments
- `config`: Configuration object
- `display`: Console display

**Returns:**
- Exit code

**Example:**
```python
args = argparse.Namespace(name="Project", template="default")
exit_code = Commands.cmd_init(args, config, display)
```

##### `cmd_status()`

Show project status.

```python
@staticmethod  
def cmd_status(args: argparse.Namespace, config: Optional[LDAConfig], display: Console) -> int
```

**Parameters:**
- `args`: Parsed command arguments
- `config`: Configuration object
- `display`: Console display

**Returns:**
- Exit code

##### `cmd_track()`

Track files in manifest.

```python
@staticmethod
def cmd_track(args: argparse.Namespace, config: Optional[LDAConfig], display: Console) -> int
```

**Parameters:**
- `args`: Parsed command arguments
- `config`: Configuration object
- `display`: Console display

**Returns:**
- Exit code

##### `cmd_changes()`

Show file changes.

```python
@staticmethod
def cmd_changes(args: argparse.Namespace, config: Optional[LDAConfig], display: Console) -> int
```

**Parameters:**
- `args`: Parsed command arguments
- `config`: Configuration object
- `display`: Console display

**Returns:**
- Exit code

##### `cmd_history()`

Show project history.

```python
@staticmethod
def cmd_history(args: argparse.Namespace, config: Optional[LDAConfig], display: Console) -> int
```

**Parameters:**
- `args`: Parsed command arguments
- `config`: Configuration object
- `display`: Console display

**Returns:**
- Exit code

##### `cmd_validate()`

Validate project structure.

```python
@staticmethod
def cmd_validate(args: argparse.Namespace, config: Optional[LDAConfig], display: Console) -> int
```

**Parameters:**
- `args`: Parsed command arguments
- `config`: Configuration object
- `display`: Console display

**Returns:**
- Exit code

##### `cmd_export()`

Export project data.

```python
@staticmethod
def cmd_export(args: argparse.Namespace, config: Optional[LDAConfig], display: Console) -> int
```

**Parameters:**
- `args`: Parsed command arguments
- `config`: Configuration object
- `display`: Console display

**Returns:**
- Exit code

### `Console`

Console display and formatting.

```python
from lda.display.console import Console

console = Console()
```

#### Constructor

```python
Console(style: str = "conservative", colors: bool = True)
```

**Parameters:**
- `style`: Display style
- `colors`: Enable color output

**Example:**
```python
console = Console(colors=True)
console.success("Operation completed")
```

#### Methods

##### `error()`

Display error message.

```python
def error(self, message: str) -> None
```

**Parameters:**
- `message`: Error message to display

**Example:**
```python
console.error("File not found")
```

##### `success()`

Display success message.

```python
def success(self, message: str) -> None
```

**Parameters:**
- `message`: Success message to display

**Example:**
```python
console.success("Project initialized")
```

##### `warning()`

Display warning message.

```python
def warning(self, message: str) -> None
```

**Parameters:**
- `message`: Warning message to display

**Example:**
```python
console.warning("Configuration file missing")
```

##### `info()`

Display info message.

```python
def info(self, message: str) -> None
```

**Parameters:**
- `message`: Info message to display

**Example:**
```python
console.info("Processing files...")
```

##### `header()`

Display a header.

```python
def header(self, title: str, width: int = 60) -> None
```

**Parameters:**
- `title`: Header title
- `width`: Header width

**Example:**
```python
console.header("LDA Project Status")
```

##### `table()`

Display a table.

```python
def table(self, headers: List[str], rows: List[List[str]], 
          column_widths: Optional[List[int]] = None) -> None
```

**Parameters:**
- `headers`: Table headers
- `rows`: Table rows
- `column_widths`: Optional column widths

**Example:**
```python
headers = ["File", "Status", "Modified"]
rows = [
    ["data.csv", "tracked", "2024-01-01"],
    ["output.png", "new", "2024-01-02"]
]
console.table(headers, rows)
```

### `CLIUtils`

CLI utility functions.

```python
from lda.cli.utils import find_project_root, setup_logging
```

#### Functions

##### `find_project_root()`

Find project root directory.

```python
def find_project_root(start_path: str = ".") -> Optional[Path]
```

**Parameters:**
- `start_path`: Starting directory

**Returns:**
- Project root path or None

**Example:**
```python
root = find_project_root()
if root:
    print(f"Project root: {root}")
```

##### `setup_logging()`

Configure logging.

```python
def setup_logging(verbose: bool = False, quiet: bool = False) -> None
```

**Parameters:**
- `verbose`: Enable verbose logging
- `quiet`: Suppress non-error output

**Example:**
```python
setup_logging(verbose=True)
```

##### `parse_date()`

Parse date string.

```python
def parse_date(date_str: str) -> datetime
```

**Parameters:**
- `date_str`: Date string to parse

**Returns:**
- Parsed datetime object

**Example:**
```python
date = parse_date("2024-01-01")
date = parse_date("yesterday")
date = parse_date("1 week ago")
```

## Usage Examples

### Creating a Custom CLI Command

```python
from lda.cli.commands import Commands
from lda.display.console import Console
from lda.config import LDAConfig
import argparse

class CustomCommands(Commands):
    @staticmethod
    def cmd_custom(args: argparse.Namespace, config: Optional[LDAConfig], 
                   display: Console) -> int:
        """Custom command implementation."""
        display.header("Custom Command")
        
        # Access configuration
        project_name = config.get("project.name") if config else "Unknown"
        display.info(f"Project: {project_name}")
        
        # Process arguments
        if args.verbose:
            display.info("Verbose mode enabled")
        
        # Perform operations
        try:
            # Custom logic here
            display.success("Custom operation completed")
            return 0
        except Exception as e:
            display.error(f"Operation failed: {e}")
            return 1
```

### Extending the CLI

```python
from lda.cli.main import LDACLI
import argparse

class CustomCLI(LDACLI):
    def create_parser(self) -> argparse.ArgumentParser:
        """Add custom commands to parser."""
        parser = super().create_parser()
        
        # Get subparsers
        subparsers = parser._subparsers._actions[1]
        
        # Add custom command
        custom_parser = subparsers.add_parser(
            "custom",
            help="Custom command"
        )
        custom_parser.add_argument(
            "--option",
            help="Custom option"
        )
        
        return parser

# Use custom CLI
cli = CustomCLI()
exit_code = cli.run()
```

### Programmatic CLI Usage

```python
from lda.cli.main import LDACLI
from lda.cli.commands import Commands
from lda.display.console import Console
from lda.config import LDAConfig

# Create components
config = LDAConfig("lda_config.yaml")
display = Console(colors=False)  # No colors for logging
commands = Commands()

# Execute commands programmatically
import argparse

# Init command
init_args = argparse.Namespace(
    command="init",
    name="TestProject",
    template="default",
    force=False
)
result = commands.cmd_init(init_args, config, display)

# Status command
status_args = argparse.Namespace(
    command="status",
    format="json",
    section=None,
    detailed=False
)
result = commands.cmd_status(status_args, config, display)
```

### Custom Display Formatting

```python
from lda.display.console import Console

class CustomConsole(Console):
    def project_summary(self, project_info: dict):
        """Display custom project summary."""
        self.header("Project Summary")
        
        # Basic info
        self.info(f"Name: {project_info['name']}")
        self.info(f"Code: {project_info['code']}")
        self.info(f"Created: {project_info['created']}")
        
        # Section table
        if project_info['sections']:
            self.section("Sections")
            headers = ["ID", "Name", "Status"]
            rows = []
            for section in project_info['sections']:
                rows.append([
                    section['id'],
                    section['name'],
                    section['status']
                ])
            self.table(headers, rows)
        
        # Statistics
        self.section("Statistics")
        stats = project_info['stats']
        self.info(f"Total files: {stats['total_files']}")
        self.info(f"Total size: {stats['total_size']}")
        self.info(f"Last updated: {stats['last_updated']}")

# Use custom console
console = CustomConsole()
project_info = {
    "name": "My Project",
    "code": "PROJ001",
    "created": "2024-01-01",
    "sections": [
        {"id": "sec01", "name": "Data", "status": "complete"},
        {"id": "sec02", "name": "Analysis", "status": "in_progress"}
    ],
    "stats": {
        "total_files": 42,
        "total_size": "1.2 GB",
        "last_updated": "2024-01-15"
    }
}
console.project_summary(project_info)
```

### Error Handling in CLI

```python
from lda.cli.main import LDACLI
from lda.core.errors import LDAError, ConfigurationError
import sys

class RobustCLI(LDACLI):
    def run(self, args=None):
        """Run with comprehensive error handling."""
        try:
            return super().run(args)
            
        except ConfigurationError as e:
            self.display.error(f"Configuration error: {e}")
            self.display.info("Check your lda_config.yaml file")
            return 1
            
        except LDAError as e:
            self.display.error(f"LDA error: {e}")
            return 1
            
        except KeyboardInterrupt:
            self.display.warning("Operation cancelled by user")
            return 130
            
        except Exception as e:
            self.display.error(f"Unexpected error: {e}")
            self.display.info("Run with --verbose for full traceback")
            if "--verbose" in sys.argv:
                import traceback
                traceback.print_exc()
            return 1

cli = RobustCLI()
sys.exit(cli.run())
```

## See Also

- [Command Reference](../cli-reference/commands.md) - Detailed command documentation
- [Core API](core.md) - Core classes documentation  
- [Configuration API](config.md) - Configuration management