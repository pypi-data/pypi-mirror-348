# CLI Commands Reference

Complete reference for all LDA command-line interface commands.

## Global Options

These options work with all commands:

```bash
lda [GLOBAL_OPTIONS] COMMAND [COMMAND_OPTIONS]
```

| Option | Short | Description |
|--------|-------|-------------|
| `--version` | `-V` | Show version and exit |
| `--help` | `-h` | Show help message |
| `--config FILE` | `-c` | Specify config file |
| `--project-dir DIR` | `-p` | Set project directory |
| `--verbose` | `-v` | Increase verbosity (-vvv for debug) |
| `--quiet` | `-q` | Suppress output |
| `--no-color` | | Disable colored output |
| `--json` | | Output in JSON format |
| `--debug` | | Enable debug mode |

## Commands Overview

| Command | Description |
|---------|-------------|
| `init` | Initialize new project |
| `status` | Show project status |
| `track` | Track project files |
| `changes` | Show file changes |
| `export` | Export project data |
| `config` | Manage configuration |
| `templates` | Manage project templates |
| `clean` | Clean temporary files |
| `validate` | Validate project structure |
| `history` | Show project history |

## init

Initialize a new LDA project.

```bash
lda init [OPTIONS]
```

**Options:**
| Option | Description | Default |
|--------|-------------|---------|
| `--template NAME` | Use project template | - |
| `--name NAME` | Project name | Prompt |
| `--code CODE` | Project code | Prompt |
| `--author NAME` | Project author | Current user |
| `--interactive` | Interactive setup | true |
| `--force` | Overwrite existing | false |
| `--dry-run` | Preview changes | false |

**Examples:**
```bash
# Interactive initialization
lda init

# From template
lda init --template research

# Non-interactive
lda init --name "My Project" --code "PROJ-2024" --no-interactive

# Preview without creating
lda init --dry-run
```

## status

Display project status and information.

```bash
lda status [OPTIONS]
```

**Options:**
| Option | Description | Default |
|--------|-------------|---------|
| `--verbose` | Detailed output | false |
| `--sections` | Show section details | false |
| `--changes` | Include recent changes | false |
| `--metrics` | Show project metrics | false |
| `--json` | JSON output | false |

**Examples:**
```bash
# Basic status
lda status

# Detailed status
lda status --verbose

# Section breakdown
lda status --sections

# With metrics
lda status --metrics
```

**Output Example:**
```
Project: Climate Research (CLIMATE-2024)
Author: Dr. Jane Smith
Created: 2024-01-15
Status: Active

Sections:
  Documentation: 15 files (2.3 MB)
  Data: 42 files (156.7 MB)
  Analysis: 8 files (0.5 MB)

Last modified: 2 hours ago
Total files: 65 (159.5 MB)
```

## track

Track files in your project.

```bash
lda track [OPTIONS] [PATHS...]
```

**Options:**
| Option | Description | Default |
|--------|-------------|---------|
| `--all` | Track all files | false |
| `--section NAME` | Track specific section | - |
| `--watch` | Continuous monitoring | false |
| `--interval SEC` | Watch interval | 300 |
| `--exclude PATTERN` | Exclude patterns | From config |
| `--force` | Force retracking | false |

**Examples:**
```bash
# Track all files
lda track --all

# Track specific section
lda track --section documentation

# Track specific files
lda track data/*.csv scripts/*.py

# Watch mode
lda track --watch --interval 60

# With exclusions
lda track --all --exclude "*.tmp" --exclude "*.log"
```

## changes

Show file changes in the project.

```bash
lda changes [OPTIONS]
```

**Options:**
| Option | Description | Default |
|--------|-------------|---------|
| `--since TIME` | Changes since time | - |
| `--section NAME` | Filter by section | All |
| `--type TYPE` | Change type filter | All |
| `--show-diff` | Show file diffs | false |
| `--summary` | Summary only | false |

**Time Formats:**
- `1h` - 1 hour ago
- `2d` - 2 days ago
- `1w` - 1 week ago
- `2024-01-15` - Specific date
- `yesterday` - Natural language

**Examples:**
```bash
# All recent changes
lda changes

# Changes in last hour
lda changes --since 1h

# Changes in specific section
lda changes --section data --since yesterday

# With diffs
lda changes --show-diff

# Summary only
lda changes --summary --since 1w
```

## export

Export project data in various formats.

```bash
lda export [OPTIONS]
```

**Options:**
| Option | Description | Default |
|--------|-------------|---------|
| `--format FORMAT` | Export format | html |
| `--output FILE` | Output file | auto |
| `--sections LIST` | Include sections | All |
| `--include-metadata` | Include metadata | true |
| `--include-history` | Include history | false |
| `--compress` | Compress output | false |

**Formats:**
- `html` - Web page
- `pdf` - PDF document
- `json` - JSON data
- `csv` - CSV tables
- `markdown` - Markdown document
- `excel` - Excel workbook

**Examples:**
```bash
# Export as HTML
lda export --format html

# Export as PDF with history
lda export --format pdf --include-history

# Export specific sections
lda export --sections "data,analysis" --format json

# Compressed output
lda export --format json --compress --output report.json.gz
```

## config

Manage LDA configuration.

```bash
lda config [SUBCOMMAND] [OPTIONS]
```

**Subcommands:**
| Command | Description |
|---------|-------------|
| `show` | Display configuration |
| `get KEY` | Get config value |
| `set KEY VALUE` | Set config value |
| `edit` | Edit config file |
| `validate` | Validate configuration |
| `export` | Export configuration |

**Examples:**
```bash
# Show full config
lda config show

# Get specific value
lda config get tracking.interval

# Set value
lda config set tracking.interval 60

# Edit config
lda config edit

# Validate config
lda config validate

# Export config
lda config export --output config_backup.yaml
```

## templates

Manage project templates.

```bash
lda templates [SUBCOMMAND] [OPTIONS]
```

**Subcommands:**
| Command | Description |
|---------|-------------|
| `list` | List available templates |
| `show NAME` | Show template details |
| `create NAME` | Create new template |
| `clone SOURCE DEST` | Clone existing template |
| `validate NAME` | Validate template |
| `install SOURCE` | Install template |
| `remove NAME` | Remove template |

**Examples:**
```bash
# List templates
lda templates list

# Show template details
lda templates show research

# Create new template
lda templates create my-template

# Clone template
lda templates clone research my-research

# Install from package
lda templates install https://github.com/org/templates.git
```

## clean

Clean temporary and cache files.

```bash
lda clean [OPTIONS]
```

**Options:**
| Option | Description | Default |
|--------|-------------|---------|
| `--cache` | Clean cache files | true |
| `--temp` | Clean temp files | true |
| `--backups` | Clean old backups | false |
| `--all` | Clean everything | false |
| `--dry-run` | Preview only | false |
| `--force` | No confirmation | false |

**Examples:**
```bash
# Clean cache and temp
lda clean

# Clean everything
lda clean --all

# Preview what will be cleaned
lda clean --all --dry-run

# Clean without confirmation
lda clean --force
```

## validate

Validate project structure and configuration.

```bash
lda validate [OPTIONS]
```

**Options:**
| Option | Description | Default |
|--------|-------------|---------|
| `--structure` | Check structure | true |
| `--config` | Check config | true |
| `--files` | Check file integrity | true |
| `--strict` | Strict validation | false |
| `--fix` | Auto-fix issues | false |

**Examples:**
```bash
# Basic validation
lda validate

# Strict validation
lda validate --strict

# Fix issues automatically
lda validate --fix

# Check specific aspects
lda validate --files --no-config
```

## history

Show project history and timeline.

```bash
lda history [OPTIONS]
```

**Options:**
| Option | Description | Default |
|--------|-------------|---------|
| `--limit N` | Number of entries | 50 |
| `--since TIME` | History since time | - |
| `--section NAME` | Filter by section | All |
| `--type TYPE` | Event type filter | All |
| `--reverse` | Reverse order | false |

**Examples:**
```bash
# Recent history
lda history

# Limited entries
lda history --limit 10

# Section history
lda history --section documentation

# Since date
lda history --since "2024-01-01"
```

## Advanced Commands

### watch

Monitor project continuously.

```bash
lda watch [OPTIONS]
```

**Options:**
| Option | Description | Default |
|--------|-------------|---------|
| `--interval SEC` | Check interval | 300 |
| `--on-change CMD` | Run on change | - |
| `--sections LIST` | Watch sections | All |
| `--notify` | Enable notifications | false |

**Examples:**
```bash
# Basic watch
lda watch

# With command execution
lda watch --on-change "make test"

# Specific sections
lda watch --sections "code,tests" --interval 60
```

### backup

Create project backups.

```bash
lda backup [OPTIONS]
```

**Options:**
| Option | Description | Default |
|--------|-------------|---------|
| `--output PATH` | Backup location | .lda/backups |
| `--compress` | Compress backup | true |
| `--include-history` | Include history | true |
| `--encrypt` | Encrypt backup | false |

**Examples:**
```bash
# Create backup
lda backup

# Custom location
lda backup --output /backups/project.tar.gz

# Encrypted backup
lda backup --encrypt --password-file secret.key
```

### migrate

Migrate project between versions.

```bash
lda migrate [OPTIONS]
```

**Options:**
| Option | Description | Default |
|--------|-------------|---------|
| `--from VERSION` | Source version | auto |
| `--to VERSION` | Target version | latest |
| `--backup` | Create backup | true |
| `--dry-run` | Preview changes | false |

**Examples:**
```bash
# Migrate to latest
lda migrate

# Specific version
lda migrate --to 2.0

# Preview migration
lda migrate --dry-run
```

## Command Combinations

### Common Workflows

```bash
# Initialize and track
lda init --template research && lda track --all

# Status with changes
lda status --verbose && lda changes --since 1d

# Export after validation
lda validate && lda export --format pdf

# Watch with notifications
lda watch --notify --on-change "lda export"
```

### Scripting Examples

```bash
#!/bin/bash
# Daily project report

# Update tracking
lda track --all

# Check changes
if lda changes --since 1d --json | jq '.count > 0'; then
    # Export report if changes
    lda export --format html --output daily_$(date +%Y%m%d).html
    
    # Send notification
    lda notify "Daily report generated"
fi
```

### Integration Examples

```python
# Python integration
import subprocess
import json

# Get project status
result = subprocess.run(['lda', 'status', '--json'], 
                      capture_output=True, text=True)
status = json.loads(result.stdout)

# Track files programmatically
subprocess.run(['lda', 'track', '--all'])

# Export data
subprocess.run(['lda', 'export', '--format', 'json', 
               '--output', 'data.json'])
```

## Environment Variables

LDA commands respect these environment variables:

```bash
# Configuration
export LDA_CONFIG_HOME="$HOME/.config/lda"
export LDA_PROJECT_DIR="/path/to/project"

# Runtime options
export LDA_VERBOSE=true
export LDA_NO_COLOR=true
export LDA_JSON_OUTPUT=true

# Feature flags
export LDA_EXPERIMENTAL=true
export LDA_DEBUG=true
```

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | General error |
| 2 | Command line error |
| 3 | Configuration error |
| 4 | File not found |
| 5 | Permission denied |
| 6 | Invalid project |
| 7 | Network error |

## Next Steps

<div class="grid cards" markdown>

-   :material-cog:{ .lg .middle } __Configuration__

    ---

    Configure LDA behavior
    
    [:octicons-arrow-right-24: Learn more](../user-guide/configuration.md)

-   :material-api:{ .lg .middle } __API Reference__

    ---

    Python API documentation
    
    [:octicons-arrow-right-24: View API](../api-reference/core.md)

-   :material-help:{ .lg .middle } __Troubleshooting__

    ---

    Common issues and solutions
    
    [:octicons-arrow-right-24: Get help](../troubleshooting.md)

</div>