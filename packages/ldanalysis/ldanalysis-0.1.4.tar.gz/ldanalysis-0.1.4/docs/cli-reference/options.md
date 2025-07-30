# Command Line Options

This page provides a comprehensive reference of all command-line options available in LDA.

## Global Options

These options are available for all LDA commands:

### `--config, -c`

Specify a custom configuration file:

```bash
lda --config custom_config.yaml init
```

**Default**: `lda_config.yaml` in current directory

### `--verbose, -v`

Enable verbose output for debugging:

```bash
lda --verbose status
```

**Effect**: Shows detailed execution information

### `--quiet, -q`

Suppress non-error output:

```bash
lda --quiet track
```

**Effect**: Only shows errors and critical information

### `--help, -h`

Show help for any command:

```bash
lda --help
lda init --help
```

## Command-Specific Options

### `init` Command Options

Initialize a new LDA project:

#### `--template, -t`

Choose a project template:

```bash
lda init --template research
```

**Options**: `default`, `research`, `clinical`, `minimal`

#### `--name, -n`

Set project name:

```bash
lda init --name "COVID-19 Analysis"
```

#### `--analyst, -a`

Set primary analyst:

```bash
lda init --analyst john.doe
```

#### `--force, -f`

Force initialization even if directory is not empty:

```bash
lda init --force
```

### `track` Command Options

Track files in the manifest:

#### `--message, -m`

Add a tracking message:

```bash
lda track --message "Updated preprocessing pipeline"
```

#### `--all, -a`

Track all files in the section:

```bash
lda track --all
```

#### `--force, -f`

Force tracking even without changes:

```bash
lda track --force
```

#### `--exclude`

Exclude files matching pattern:

```bash
lda track --exclude "*.tmp"
```

#### `--dry-run`

Show what would be tracked without making changes:

```bash
lda track --dry-run
```

### `status` Command Options

Show project status:

#### `--format, -f`

Output format:

```bash
lda status --format json
```

**Options**: `table` (default), `json`, `yaml`

#### `--section, -s`

Show status for specific section:

```bash
lda status --section sec01_preprocessing
```

#### `--detailed, -d`

Show detailed file information:

```bash
lda status --detailed
```

### `changes` Command Options

Show file changes:

#### `--since`

Show changes since date:

```bash
lda changes --since "2024-01-01"
lda changes --since "1 week ago"
```

#### `--analyst`

Filter changes by analyst:

```bash
lda changes --analyst jane.doe
```

#### `--section`

Show changes for specific section:

```bash
lda changes --section sec02_analysis
```

#### `--diff`

Show detailed diffs:

```bash
lda changes --diff
```

### `history` Command Options

Show project history:

#### `--limit, -n`

Limit number of entries:

```bash
lda history --limit 10
```

#### `--output, -o`

Export history to file:

```bash
lda history --output history.json
```

#### `--format, -f`

Output format:

```bash
lda history --format csv
```

**Options**: `json`, `csv`, `html`

#### `--file`

Show history for specific file:

```bash
lda history --file outputs/results.csv
```

### `validate` Command Options

Validate project integrity:

#### `--fix`

Attempt to fix issues:

```bash
lda validate --fix
```

#### `--strict`

Use strict validation rules:

```bash
lda validate --strict
```

#### `--report`

Generate validation report:

```bash
lda validate --report validation.html
```

### `export` Command Options

Export project data:

#### `--output, -o`

Output file (required):

```bash
lda export manifest --output manifest.csv
```

#### `--format, -f`

Export format:

```bash
lda export report --format pdf --output report.pdf
```

**Options**: `csv`, `json`, `html`, `pdf`

#### `--sections`

Export specific sections:

```bash
lda export manifest --sections sec01,sec02 --output partial.csv
```

### `docs` Command Options

Documentation management:

#### `serve` Subcommand

Serve documentation locally:

```bash
lda docs serve --port 8080 --dev
```

**Options**:
- `--port, -p`: Port number (default: 8000)
- `--dev`: Enable development mode with auto-reload
- `--host`: Host address (default: 127.0.0.1)

#### `build` Subcommand

Build documentation:

```bash
lda docs build --output site --strict
```

**Options**:
- `--output, -o`: Output directory (default: site)
- `--strict, -s`: Fail on warnings
- `--clean, -c`: Clean build directory first

## Environment Variables

### `LDA_CONFIG`

Default configuration file path:

```bash
export LDA_CONFIG=/path/to/config.yaml
lda status
```

### `LDA_PROJECT_ROOT`

Override project root detection:

```bash
export LDA_PROJECT_ROOT=/path/to/project
lda validate
```

### `LDA_LOG_LEVEL`

Set logging level:

```bash
export LDA_LOG_LEVEL=DEBUG
lda track
```

**Options**: `DEBUG`, `INFO`, `WARNING`, `ERROR`

## Configuration File Options

Many command-line options can be set in the configuration file:

```yaml
# lda_config.yaml
cli:
  default_format: json
  verbose: true
  colors: true
  
track:
  auto_message: true
  exclude_patterns:
    - "*.tmp"
    - ".DS_Store"
    
validate:
  strict: true
  auto_fix: true
```

## Combining Options

Options can be combined for complex operations:

```bash
# Track with multiple options
lda track \
  --all \
  --exclude "*.tmp" \
  --message "Complete analysis run" \
  --verbose

# Export with filters
lda export manifest \
  --sections sec01,sec02 \
  --format json \
  --output filtered_manifest.json \
  --since "2024-01-01"

# Validate with reporting
lda validate \
  --strict \
  --fix \
  --report validation_report.html \
  --verbose
```

## Option Precedence

When the same option is specified multiple times, precedence is:

1. Command-line arguments (highest)
2. Environment variables
3. Configuration file
4. Default values (lowest)

Example:

```bash
# Config file has: verbose: false
# Environment has: LDA_LOG_LEVEL=DEBUG
# Command line has: --quiet

lda status --quiet  # Quiet mode wins
```

## Boolean Options

Boolean options can be negated with `--no-` prefix:

```bash
# Disable colors even if config enables them
lda status --no-colors

# Disable auto-fix even if config enables it
lda validate --no-fix
```

## See Also

- [Commands](commands.md) - Detailed command documentation
- [Configuration](../user-guide/configuration.md) - Configuration file reference
- [Environment Variables](#environment-variables) - Environment variable reference