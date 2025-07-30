# File Tracking

LDA's file tracking system provides comprehensive provenance tracking for every file in your project. Each modification is recorded with timestamps, hash values, and analyst attribution to ensure complete traceability.

## Overview

The tracking system maintains a complete audit trail of all file operations:

- **File creation** - When files are first added to the project
- **Modifications** - All changes with before/after hashes
- **Deletions** - When files are removed from tracking
- **Analyst attribution** - Who made each change

## Using the Track Command

The `lda track` command manages file tracking in your project:

```bash
# Track all files in current section
lda track

# Track specific files
lda track data/input.csv outputs/results.png

# Track with custom message
lda track --message "Updated preprocessing pipeline"

# Force tracking even if no changes
lda track --force
```

## Manifest Structure

Each section maintains a `manifest.json` file that records:

```json
{
  "version": "1.0",
  "section": "sec01_preprocessing", 
  "created": "2024-01-15T10:30:00Z",
  "analyst": "john.doe",
  "files": {
    "inputs/raw_data.csv": {
      "hash": "sha256:abcd1234...",
      "modified": "2024-01-15T10:30:00Z",
      "size": 12345,
      "analyst": "john.doe"
    }
  },
  "history": [
    {
      "timestamp": "2024-01-15T10:30:00Z",
      "action": "created",
      "files": ["inputs/raw_data.csv"],
      "analyst": "john.doe",
      "message": "Initial data import"
    }
  ]
}
```

## Viewing Changes

Use the `changes` command to see file modifications:

```bash
# Show all changes in current section
lda changes

# Show changes since specific date
lda changes --since "2024-01-01"

# Show changes by specific analyst
lda changes --analyst john.doe

# Show detailed diff
lda changes --diff
```

## History and Provenance

View complete file history with the `history` command:

```bash
# Show full history
lda history

# History for specific file
lda history outputs/figure1.png

# Export history to file
lda history --output history.json --format json
```

## Best Practices

1. **Track Early and Often**
   - Run `lda track` after every significant change
   - Use meaningful messages to describe changes

2. **Review Before Committing**
   - Use `lda changes` to review modifications
   - Ensure all expected files are tracked

3. **Maintain Clean History**
   - Use clear, descriptive messages
   - Track related changes together

4. **Regular Validation**
   - Run `lda validate` to check manifest integrity
   - Fix any issues before they accumulate

## Integration with Git

LDA tracking complements Git version control:

- Git tracks code changes
- LDA tracks data and output provenance
- Together they provide complete project history

```bash
# Typical workflow
lda track --message "Updated analysis parameters"
git add .
git commit -m "Updated analysis parameters"
```

## Troubleshooting

### Missing Files

If files are missing from tracking:

```bash
# Check current status
lda status

# Force re-scan
lda track --scan

# Validate manifest
lda validate --fix
```

### Hash Mismatches

When file contents change without tracking:

```bash
# Show files with hash mismatches
lda validate

# Update hashes
lda track --update-hashes
```

### Permission Issues

Ensure proper file permissions:

```bash
# Check file permissions
ls -la

# Fix permissions if needed
chmod 644 manifest.json
```

## Advanced Features

### Custom Hash Algorithms

Configure hash algorithm in `lda_config.yaml`:

```yaml
tracking:
  hash_algorithm: sha256  # or md5, sha1, sha512
  ignore_patterns:
    - "*.tmp"
    - ".DS_Store"
```

### Automated Tracking

Set up automated tracking with file watchers:

```yaml
tracking:
  auto_track: true
  watch_patterns:
    - "inputs/*.csv"
    - "outputs/*.png"
```

### Remote Synchronization

Sync tracking data with remote servers:

```yaml
tracking:
  remote:
    enabled: true
    endpoint: "https://tracking.example.com"
    api_key: "${TRACKING_API_KEY}"
```

## See Also

- [Configuration](configuration.md) - Tracking configuration options
- [Workflows](workflows.md) - Integrating tracking into workflows
- [CLI Reference](../cli-reference/commands.md#track) - Complete track command reference