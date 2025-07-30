"""Tests for configuration system."""

import tempfile
from pathlib import Path

import pytest
import yaml

from lda.config import LDAConfig


def test_default_config():
    """Test default configuration."""
    # Create a fresh config without loading any file
    config = LDAConfig()

    # If no file was loaded, we should have defaults
    if not config.config_file:
        assert config.get("project.name") == "New LDA Project"
        assert config.get("project.code") == "PROJ"
        assert config.get("logging.level") == "INFO"
    else:
        # Skip test if a config file was loaded
        pytest.skip("Config file was loaded from environment")


def test_config_get_set():
    """Test configuration get/set."""
    config = LDAConfig()

    # Test basic get/set
    config.set("test.value", "hello")
    assert config.get("test.value") == "hello"

    # Test nested get/set
    config.set("test.nested.value", 42)
    assert config.get("test.nested.value") == 42

    # Test default value
    assert config.get("nonexistent", "default") == "default"


def test_config_load_yaml():
    """Test loading configuration from YAML."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
        yaml.dump({
            "project": {
                "name": "Test Project",
                "code": "TEST"
            }
        }, f)
        f.flush()

        config = LDAConfig(f.name)
        assert config.get("project.name") == "Test Project"
        assert config.get("project.code") == "TEST"

        Path(f.name).unlink()


def test_config_validation():
    """Test configuration validation."""
    config = LDAConfig()

    # Valid config should not raise
    config.validate()

    # Missing required fields should raise
    config.set("project.code", None)
    with pytest.raises(ValueError):
        config.validate()


def test_placeholder_expansion():
    """Test placeholder expansion."""
    config = LDAConfig()
    config.set("project.code", "TEST")
    config.set("placeholders.custom", "value")

    # Test simple placeholders
    assert config.expand_placeholders("{proj}") == "TEST"
    assert config.expand_placeholders("{custom}") == "value"

    # Test expression placeholders
    result = config.expand_placeholders("${project.code}")
    assert result == "TEST"

    # Test complex patterns
    pattern = "{proj}_{custom}_file.csv"
    result = config.expand_placeholders(pattern)
    assert result == "TEST_value_file.csv"


def test_config_save_load():
    """Test saving and loading configuration."""
    with tempfile.TemporaryDirectory() as tmpdir:
        config_path = Path(tmpdir) / "test_config.yaml"

        # Create and save config
        config1 = LDAConfig()
        config1.set("project.name", "Save Test")
        config1.set("project.code", "SAVE")
        config1.save(str(config_path))

        # Load config
        config2 = LDAConfig(str(config_path))
        assert config2.get("project.name") == "Save Test"
        assert config2.get("project.code") == "SAVE"


def test_config_merge():
    """Test configuration merging."""
    config = LDAConfig()

    # Test that defaults are preserved
    assert config.get("logging.level") == "INFO"

    # Test merging new data
    config.load_from_dict({
        "project": {
            "name": "Merged Project"
        }
    })

    # Original values should be preserved
    assert config.get("logging.level") == "INFO"
    # New values should be added
    assert config.get("project.name") == "Merged Project"
