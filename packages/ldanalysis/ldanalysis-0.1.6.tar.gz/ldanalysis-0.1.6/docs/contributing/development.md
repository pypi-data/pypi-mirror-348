# Development Guide

This guide covers setting up your development environment and contributing to LDA.

## Development Setup

### Prerequisites

- Python 3.8 or higher
- Git
- Virtual environment tool (venv, virtualenv, or conda)

### Clone Repository

```bash
git clone https://github.com/drpedapati/LDA.git
cd LDA
```

### Create Virtual Environment

```bash
# Using venv
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Using conda
conda create -n lda python=3.10
conda activate lda
```

### Install Development Dependencies

```bash
# Install package in development mode
pip install -e .

# Install all development dependencies
pip install -e .[dev,docs]
```

## Development Workflow

### 1. Create Feature Branch

```bash
git checkout -b feature/your-feature-name
```

### 2. Make Changes

Follow the code style guidelines:
- Use Black for formatting
- Follow PEP 8
- Add type hints
- Write docstrings
- Keep functions focused

### 3. Run Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=lda

# Run specific test
pytest tests/unit/test_config.py
```

### 4. Check Code Quality

```bash
# Format code
black lda tests

# Lint code
ruff check lda tests

# Type checking
mypy lda
```

### 5. Update Documentation

If your changes affect user-facing features:

1. Update relevant documentation
2. Add examples
3. Update changelog
4. Test docs locally:

```bash
lda docs serve
```

### 6. Commit Changes

```bash
git add .
git commit -m "feat: Add new feature"
```

Follow conventional commit format:
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation only
- `refactor:` Code refactoring
- `test:` Adding tests
- `chore:` Maintenance tasks

### 7. Push and Create PR

```bash
git push origin feature/your-feature-name
```

Create pull request on GitHub with:
- Clear description
- Link to related issues
- Screenshots if applicable
- Test results

## Project Structure

```
LDA/
├── lda/                    # Main package
│   ├── cli/               # CLI interface
│   ├── core/              # Core functionality
│   ├── display/           # Display utilities
│   └── logging/           # Logging utilities
├── tests/                  # Test suite
│   ├── unit/              # Unit tests
│   ├── integration/       # Integration tests
│   └── fixtures/          # Test fixtures
├── docs/                   # Documentation
├── templates/              # Project templates
├── scripts/                # Utility scripts
└── examples/               # Example projects
```

## Coding Standards

### Python Style

```python
"""Module docstring explaining purpose."""

from typing import Optional, List, Dict
import logging

from lda.core.base import BaseClass


class ExampleClass(BaseClass):
    """Class docstring with description.
    
    Attributes:
        name: The name of the object
        active: Whether object is active
    """
    
    def __init__(self, name: str, active: bool = True) -> None:
        """Initialize ExampleClass.
        
        Args:
            name: Object name
            active: Whether to activate object
        """
        self.name = name
        self.active = active
    
    def process(self, data: List[Dict[str, Any]]) -> Optional[str]:
        """Process data and return result.
        
        Args:
            data: List of data items to process
            
        Returns:
            Processed result or None if failed
            
        Raises:
            ValueError: If data is invalid
        """
        if not data:
            raise ValueError("Data cannot be empty")
        
        # Process data
        result = self._internal_process(data)
        
        return result
```

### Testing Standards

```python
"""Test module for example functionality."""

import pytest
from unittest.mock import Mock, patch

from lda.example import ExampleClass


class TestExampleClass:
    """Tests for ExampleClass."""
    
    @pytest.fixture
    def example(self):
        """Create example instance."""
        return ExampleClass("test")
    
    def test_init(self):
        """Test initialization."""
        obj = ExampleClass("test", active=False)
        assert obj.name == "test"
        assert not obj.active
    
    def test_process_valid_data(self, example):
        """Test processing valid data."""
        data = [{"id": 1}, {"id": 2}]
        result = example.process(data)
        assert result is not None
    
    def test_process_empty_data(self, example):
        """Test processing empty data raises error."""
        with pytest.raises(ValueError, match="Data cannot be empty"):
            example.process([])
    
    @patch('lda.example.external_function')
    def test_with_mock(self, mock_func, example):
        """Test with mocked external dependency."""
        mock_func.return_value = "mocked"
        result = example.call_external()
        assert result == "mocked"
        mock_func.assert_called_once()
```

## Adding Features

### 1. Plan Feature

- Discuss in issue first
- Consider backward compatibility
- Think about testing strategy
- Plan documentation updates

### 2. Implement Feature

- Write tests first (TDD)
- Keep changes focused
- Add appropriate logging
- Handle errors gracefully

### 3. Document Feature

- Add docstrings
- Update user guide
- Add to CLI help
- Include examples

### 4. Test Feature

- Unit tests
- Integration tests
- Manual testing
- Performance testing if needed

## Common Tasks

### Adding a New Command

1. Create command function in `lda/cli/commands.py`
2. Add parser in `lda/cli/main.py`
3. Write tests in `tests/unit/test_cli.py`
4. Update documentation

### Adding a Configuration Option

1. Add to `lda/config.py`
2. Update schema validation
3. Add to default config
4. Document in user guide

### Creating a New Module

1. Create module in appropriate package
2. Add comprehensive docstrings
3. Write unit tests
4. Update `__init__.py` imports

## Debugging

### Debug Mode

```bash
# Enable debug logging
export LDA_DEBUG=true
lda --debug status

# Use Python debugger
python -m pdb -m lda status
```

### Common Issues

1. **Import errors**: Check PYTHONPATH and virtual environment
2. **Config errors**: Validate YAML syntax
3. **Permission errors**: Check file/directory permissions
4. **Test failures**: Run tests in isolation

## Performance

### Profiling

```python
import cProfile
import pstats

# Profile function
cProfile.run('function_to_profile()', 'profile_stats')

# Analyze results
stats = pstats.Stats('profile_stats')
stats.sort_stats('cumulative')
stats.print_stats(10)
```

### Optimization Tips

- Use generators for large datasets
- Cache expensive computations
- Minimize file I/O
- Use appropriate data structures

## Release Process

1. Update version in `setup.py`
2. Update CHANGELOG.md
3. Run full test suite
4. Build documentation
5. Create release PR
6. Tag release after merge
7. Deploy to PyPI

## Getting Help

- Check existing issues
- Ask in discussions
- Join community chat
- Email maintainers

## Resources

- [Python Style Guide](https://www.python.org/dev/peps/pep-0008/)
- [Conventional Commits](https://www.conventionalcommits.org/)
- [MkDocs Documentation](https://www.mkdocs.org/)
- [pytest Documentation](https://docs.pytest.org/)