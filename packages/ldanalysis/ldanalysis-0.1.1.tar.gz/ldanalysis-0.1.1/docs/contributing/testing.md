# Testing Guide

This guide covers testing practices for LDA development, including unit tests, integration tests, and testing guidelines for contributors.

## Test Structure

LDA follows a standard test structure:

```
tests/
├── unit/              # Unit tests
│   ├── test_config.py
│   ├── test_core.py
│   ├── test_tracking.py
│   └── test_utils.py
├── integration/       # Integration tests
│   ├── test_cli.py
│   ├── test_workflows.py
│   └── test_database.py
├── fixtures/         # Test data
│   ├── configs/
│   ├── data/
│   └── projects/
├── conftest.py       # Test configuration
└── utils.py          # Test utilities
```

## Running Tests

### Quick Start

```bash
# Install test dependencies
pip install -e ".[test]"

# Run all tests
pytest

# Run with coverage
pytest --cov=lda --cov-report=html

# Run specific test file
pytest tests/unit/test_config.py

# Run specific test
pytest tests/unit/test_config.py::test_load_config
```

### Test Categories

```bash
# Unit tests only
pytest tests/unit/

# Integration tests only
pytest tests/integration/

# Fast tests (no network/db)
pytest -m "not slow"

# Specific markers
pytest -m "tracking"
pytest -m "cli"
```

## Writing Tests

### Unit Tests

Example unit test:

```python
# tests/unit/test_config.py
import pytest
from lda.config import LDAConfig
from pathlib import Path

class TestLDAConfig:
    """Test configuration functionality."""
    
    def test_load_config(self, tmp_path):
        """Test loading configuration from file."""
        # Create test config
        config_file = tmp_path / "test_config.yaml"
        config_file.write_text("""
        project:
          name: Test Project
          code: TEST001
        """)
        
        # Load config
        config = LDAConfig(str(config_file))
        
        # Assertions
        assert config.get("project.name") == "Test Project"
        assert config.get("project.code") == "TEST001"
    
    def test_missing_config(self):
        """Test handling missing config file."""
        with pytest.raises(FileNotFoundError):
            LDAConfig("nonexistent.yaml")
    
    @pytest.mark.parametrize("path,expected", [
        ("project.name", "Test"),
        ("project.missing", None),
        ("deep.nested.value", None),
    ])
    def test_get_path(self, config, path, expected):
        """Test getting values by path."""
        assert config.get(path) == expected
```

### Integration Tests

```python
# tests/integration/test_cli.py
import pytest
from click.testing import CliRunner
from lda.cli.main import cli

class TestCLIIntegration:
    """Test CLI commands integration."""
    
    @pytest.fixture
    def runner(self):
        """Create CLI test runner."""
        return CliRunner()
    
    def test_init_command(self, runner, tmp_path):
        """Test project initialization."""
        with runner.isolated_filesystem():
            result = runner.invoke(cli, [
                'init',
                '--name', 'Test Project',
                '--analyst', 'test.user'
            ])
            
            assert result.exit_code == 0
            assert Path("lda_config.yaml").exists()
            assert "Project initialized" in result.output
    
    def test_status_command(self, runner, sample_project):
        """Test status command with sample project."""
        result = runner.invoke(cli, ['status'], cwd=sample_project)
        
        assert result.exit_code == 0
        assert "Project Status" in result.output
        assert "Sections: 3" in result.output
```

### Fixtures

Common test fixtures:

```python
# tests/conftest.py
import pytest
from pathlib import Path
import tempfile
import shutil

@pytest.fixture
def tmp_project(tmp_path):
    """Create temporary project structure."""
    project_dir = tmp_path / "test_project"
    project_dir.mkdir()
    
    # Create basic structure
    (project_dir / "lda_config.yaml").write_text("""
    project:
      name: Test Project
      code: TEST001
    sections:
      - id: sec01
        name: Data
    """)
    
    (project_dir / "sec01").mkdir()
    (project_dir / "sec01" / "manifest.json").write_text("{}")
    
    yield project_dir
    
    # Cleanup is automatic with tmp_path

@pytest.fixture
def sample_data():
    """Provide sample data files."""
    data_dir = Path(__file__).parent / "fixtures" / "data"
    return {
        "csv": data_dir / "sample.csv",
        "json": data_dir / "sample.json",
        "large": data_dir / "large_file.dat"
    }

@pytest.fixture
def mock_config():
    """Mock configuration object."""
    from unittest.mock import Mock
    
    config = Mock()
    config.get.side_effect = lambda key, default=None: {
        "project.name": "Mock Project",
        "project.code": "MOCK001",
        "tracking.hash_algorithm": "sha256"
    }.get(key, default)
    
    return config
```

## Testing Best Practices

### 1. Test Isolation

Each test should be independent:

```python
class TestFileTracking:
    def test_track_file(self, tmp_path):
        """Test file tracking in isolation."""
        # Create test file
        test_file = tmp_path / "test.txt"
        test_file.write_text("test content")
        
        # Track file
        tracker = LDATracker()
        result = tracker.track_file(test_file)
        
        # Verify tracking
        assert result["hash"] is not None
        assert result["size"] == 12
        
        # Cleanup happens automatically

    @pytest.fixture(autouse=True)
    def cleanup(self):
        """Ensure clean state between tests."""
        yield
        # Reset any global state
        LDATracker._instances.clear()
```

### 2. Mocking External Dependencies

```python
from unittest.mock import patch, Mock

class TestS3Integration:
    @patch('boto3.client')
    def test_s3_upload(self, mock_boto3):
        """Test S3 upload without real AWS calls."""
        # Mock S3 client
        mock_s3 = Mock()
        mock_boto3.return_value = mock_s3
        
        # Test upload
        s3_integration = S3Integration(config={
            "bucket": "test-bucket",
            "region": "us-east-1"
        })
        
        s3_integration.upload_file("test.txt")
        
        # Verify S3 was called correctly
        mock_s3.upload_file.assert_called_once_with(
            "test.txt",
            "test-bucket",
            "test.txt"
        )
```

### 3. Testing Error Conditions

```python
class TestErrorHandling:
    def test_invalid_config(self):
        """Test handling of invalid configuration."""
        with pytest.raises(ConfigurationError) as exc_info:
            config = LDAConfig()
            config.set("project.name", None)  # Invalid
            config.validate()
        
        assert "Project name is required" in str(exc_info.value)
    
    def test_file_not_found(self):
        """Test handling missing files."""
        tracker = LDATracker()
        
        with pytest.raises(FileNotFoundError):
            tracker.track_file("nonexistent.txt")
    
    @pytest.mark.timeout(5)
    def test_timeout_handling(self):
        """Test operation timeouts."""
        with pytest.raises(TimeoutError):
            slow_operation(timeout=1)
```

### 4. Parametrized Tests

```python
@pytest.mark.parametrize("algorithm,expected_length", [
    ("md5", 32),
    ("sha1", 40),
    ("sha256", 64),
    ("sha512", 128),
])
def test_hash_algorithms(tmp_path, algorithm, expected_length):
    """Test different hash algorithms."""
    test_file = tmp_path / "test.txt"
    test_file.write_text("test content")
    
    hasher = FileHasher(algorithm=algorithm)
    hash_value = hasher.calculate(test_file)
    
    assert len(hash_value) == expected_length
    assert all(c in "0123456789abcdef" for c in hash_value)
```

### 5. Performance Tests

```python
import time
import pytest

class TestPerformance:
    @pytest.mark.performance
    def test_large_file_tracking(self, large_file):
        """Test tracking performance with large files."""
        tracker = LDATracker()
        
        start_time = time.time()
        tracker.track_file(large_file)
        duration = time.time() - start_time
        
        # Should complete within reasonable time
        assert duration < 5.0  # seconds
    
    @pytest.mark.benchmark
    def test_manifest_load_performance(self, benchmark):
        """Benchmark manifest loading."""
        manifest = LDAManifest("large_manifest.json")
        
        # Run benchmark
        result = benchmark(manifest.load)
        
        # Check performance metrics
        assert result.stats.median < 0.1  # seconds
```

## Test Coverage

### Coverage Requirements

- Minimum coverage: 80%
- Core modules: 90%+
- New features: 100%

### Running Coverage

```bash
# Generate coverage report
pytest --cov=lda --cov-report=html --cov-report=term

# Coverage for specific module
pytest --cov=lda.core tests/unit/test_core.py

# Exclude files from coverage
# .coveragerc
[run]
omit = 
    */tests/*
    */migrations/*
    */__init__.py
```

### Coverage Reports

```bash
# View HTML report
open htmlcov/index.html

# Terminal report
pytest --cov=lda --cov-report=term-missing

# XML for CI
pytest --cov=lda --cov-report=xml
```

## Continuous Integration

### GitHub Actions

```yaml
# .github/workflows/tests.yml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.8, 3.9, 3.10, 3.11]
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: ${{ matrix.python-version }}
      
      - name: Install dependencies
        run: |
          pip install -e ".[test]"
      
      - name: Run tests
        run: |
          pytest --cov=lda --cov-report=xml
      
      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          file: ./coverage.xml
```

## Test Utilities

### Helper Functions

```python
# tests/utils.py
import json
from pathlib import Path

def create_test_config(config_dict, path):
    """Create test configuration file."""
    import yaml
    
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(path, 'w') as f:
        yaml.dump(config_dict, f)
    
    return path

def create_test_manifest(files, manifest_path):
    """Create test manifest."""
    manifest = {
        "version": "1.0",
        "files": files,
        "created": "2024-01-01T00:00:00Z"
    }
    
    with open(manifest_path, 'w') as f:
        json.dump(manifest, f, indent=2)
    
    return manifest_path

def assert_file_tracked(manifest, file_path):
    """Assert file is properly tracked."""
    assert file_path in manifest.files
    file_info = manifest.files[file_path]
    assert "hash" in file_info
    assert "size" in file_info
    assert "modified" in file_info
```

## Testing Checklist

Before submitting a PR:

- [ ] All tests pass (`pytest`)
- [ ] Coverage meets requirements (`pytest --cov`)
- [ ] New features have tests
- [ ] Edge cases are tested
- [ ] Error conditions are handled
- [ ] Performance tests for critical paths
- [ ] Documentation for complex tests
- [ ] CI passes on all platforms
- [ ] No hardcoded paths or values
- [ ] Proper cleanup in all tests

## Debugging Tests

### PyTest Options

```bash
# Verbose output
pytest -vv

# Show print statements
pytest -s

# Drop to debugger on failure
pytest --pdb

# Run specific test
pytest -k test_specific_function

# Show local variables
pytest -l

# Rerun failed tests
pytest --lf
```

### Debug Fixtures

```python
@pytest.fixture
def debug_tracker():
    """Tracker with debug logging enabled."""
    import logging
    
    logging.basicConfig(level=logging.DEBUG)
    tracker = LDATracker(debug=True)
    yield tracker
    logging.basicConfig(level=logging.WARNING)
```

## See Also

- [Development](development.md) - Development setup
- [Contributing](index.md) - Contribution guidelines
- [CI/CD](../advanced/ci.md) - Continuous integration