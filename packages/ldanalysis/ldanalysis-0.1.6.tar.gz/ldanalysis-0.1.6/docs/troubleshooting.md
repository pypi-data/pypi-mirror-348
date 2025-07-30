# Troubleshooting

This guide helps you resolve common issues with LDA. If you don't find your issue here, please check our [GitHub Issues](https://github.com/drpedapati/LDA/issues) or ask in [Discussions](https://github.com/drpedapati/LDA/discussions).

## Installation Issues

### Permission Denied

If you encounter permission errors during installation:

**Solution 1**: Install with --user flag
```bash
pip install --user lda-tool
```

**Solution 2**: Use a virtual environment
```bash
python -m venv lda-env
source lda-env/bin/activate  # On Windows: lda-env\Scripts\activate
pip install lda-tool
```

### Python Version Error

LDA requires Python 3.8 or higher.

**Check your Python version**:
```bash
python --version
```

**Solutions**:
1. Upgrade Python to 3.8+
2. Use pyenv to manage multiple Python versions:
   ```bash
   pyenv install 3.10.0
   pyenv local 3.10.0
   ```

### Module Not Found

If LDA module is not found after installation:

**Solution 1**: Update pip and reinstall
```bash
python -m pip install --upgrade pip
pip install --force-reinstall lda-tool
```

**Solution 2**: Check Python path
```bash
which python
which pip
# Ensure they're from the same environment
```

## Configuration Issues

### Invalid Configuration File

**Error**: `ConfigurationError: Invalid configuration file`

**Common causes**:
1. YAML syntax errors
2. Missing required fields
3. Invalid field values

**Debug steps**:
```bash
# Validate YAML syntax
python -c "import yaml; yaml.safe_load(open('lda_config.yaml'))"

# Check configuration
lda validate config
```

### Missing Placeholders

**Error**: `MissingPlaceholderError: Missing placeholder values`

**Solution**: Define all required placeholders
```yaml
placeholders:
  project_code: "PROJ001"
  analyst: "john.doe"
  date: "2024-01-01"
```

## File Tracking Issues

### Hash Mismatch

**Error**: `Hash mismatch for file: data.csv`

**Causes**:
1. File modified outside LDA
2. Different line endings (Windows/Unix)
3. Encoding issues

**Solutions**:
```bash
# Update hash
lda track data.csv --force

# Check file encoding
file -i data.csv

# Fix line endings
dos2unix data.csv  # Unix
unix2dos data.csv  # Windows
```

### Large File Tracking

**Error**: `MemoryError` when tracking large files

**Solution**: Configure chunk processing
```yaml
performance:
  large_file_threshold: "100MB"
  chunk_size: "10MB"
  use_mmap: true
```

### Permission Denied on Manifest

**Error**: `PermissionError: [Errno 13] Permission denied: 'manifest.json'`

**Solutions**:
```bash
# Fix permissions
chmod 644 manifest.json

# Check file ownership
ls -la manifest.json

# If locked by another process
lsof manifest.json
```

## CLI Issues

### Command Not Found

**Error**: `bash: lda: command not found`

**Solutions**:

1. Add to PATH:
   ```bash
   echo $PATH
   # Add Python scripts directory
   export PATH="$HOME/.local/bin:$PATH"
   ```

2. Use full path:
   ```bash
   python -m lda.cli
   ```

3. Reinstall with pipx:
   ```bash
   pipx install lda-tool
   ```

### Verbose Output Not Working

**Issue**: `--verbose` flag doesn't show detailed output

**Solution**: Set log level
```bash
export LDA_LOG_LEVEL=DEBUG
lda status --verbose
```

## Performance Issues

### Slow File Tracking

**Symptoms**: Tracking takes too long for many files

**Solutions**:

1. Enable parallel processing:
   ```yaml
   performance:
     parallel_tracking: true
     max_workers: 8
   ```

2. Use faster hash algorithm:
   ```yaml
   tracking:
     hash_algorithm: "xxhash"  # Faster than sha256
   ```

3. Exclude unnecessary files:
   ```yaml
   tracking:
     exclude_patterns:
       - "*.tmp"
       - "*.log"
       - "__pycache__/"
   ```

### High Memory Usage

**Solutions**:

1. Limit memory usage:
   ```yaml
   performance:
     limits:
       max_memory: "2GB"
   ```

2. Process files in batches:
   ```yaml
   performance:
     batch_size: 100
   ```

## Integration Issues

### Git Integration

**Issue**: Git commits fail after LDA tracking

**Solution**: Configure git hooks properly
```bash
# Install LDA git hooks
lda git install-hooks

# Or manually create pre-commit hook
cat > .git/hooks/pre-commit << 'EOF'
#!/bin/bash
lda validate --strict
EOF
chmod +x .git/hooks/pre-commit
```

### Database Connection

**Error**: `DatabaseError: could not connect to server`

**Debug steps**:
```bash
# Test connection
psql -h localhost -U lda_user -d lda_db

# Check environment variables
echo $DATABASE_URL

# Verify configuration
lda debug db-test
```

## Platform-Specific Issues

### Windows

#### Path Separators

**Issue**: Incorrect path separators

**Solution**: Use forward slashes or raw strings
```yaml
# Good
root_folder: "C:/Projects/LDA"
# Or
root_folder: "C:\\Projects\\LDA"
```

#### Line Endings

**Issue**: CRLF vs LF issues

**Solution**: Configure Git
```bash
git config core.autocrlf true
```

### macOS

#### SSL Certificate Error

**Error**: `SSL: CERTIFICATE_VERIFY_FAILED`

**Solution**:
```bash
# Install certificates
cd /Applications/Python\ 3.x/
./Install\ Certificates.command
```

### Linux

#### Missing Dependencies

**Error**: `ImportError: libpython3.8.so.1.0`

**Solution**:
```bash
# Ubuntu/Debian
sudo apt-get install python3.8-dev

# Fedora/RHEL
sudo dnf install python38-devel
```

## Debug Mode

Enable debug mode for detailed diagnostics:

```bash
# Set debug environment variable
export LDA_DEBUG=1

# Run with debug output
lda --debug status

# Generate debug report
lda debug report --output debug_report.txt
```

## Common Error Messages

### `FileNotFoundError`

**Possible causes**:
- File doesn't exist
- Wrong working directory
- Incorrect path in config

**Debug**:
```bash
pwd  # Check current directory
ls -la  # List files
lda debug paths  # Show LDA paths
```

### `JSONDecodeError`

**Possible causes**:
- Corrupted manifest.json
- Invalid JSON syntax

**Fix**:
```bash
# Backup and recreate
cp manifest.json manifest.backup
lda repair manifest
```

### `TimeoutError`

**Possible causes**:
- Network issues
- Large file operations
- Slow external services

**Solution**:
```yaml
performance:
  timeouts:
    file_operation: 300  # seconds
    network_request: 60
```

## Getting Help

If you're still experiencing issues:

1. **Search existing issues**:
   ```bash
   # Search GitHub issues
   https://github.com/drpedapati/LDA/issues?q=is:issue+error
   ```

2. **Create detailed bug report**:
   ```bash
   # Generate diagnostic info
   lda debug report --full > debug_info.txt
   ```

3. **Ask for help**:
   - [GitHub Discussions](https://github.com/drpedapati/LDA/discussions)
   - [Stack Overflow](https://stackoverflow.com/questions/tagged/lda-analysis)

4. **Report new issue**:
   - Use issue template
   - Include debug report
   - Provide minimal example

## See Also

- [Installation](getting-started/installation.md) - Installation guide
- [Configuration](user-guide/configuration.md) - Configuration reference
- [Contributing](contributing/index.md) - How to contribute