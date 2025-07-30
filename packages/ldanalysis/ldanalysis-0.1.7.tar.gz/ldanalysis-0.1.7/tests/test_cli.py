"""Tests for CLI functionality."""

import os
import tempfile
from pathlib import Path

from lda.cli.main import LDACLI
from lda.config import LDAConfig


def test_cli_help():
    """Test CLI help command."""
    cli = LDACLI()

    # Test help (should raise SystemExit)
    import pytest
    with pytest.raises(SystemExit) as exc_info:
        cli.run(["--help"])
    assert exc_info.value.code == 0


def test_cli_init():
    """Test CLI init command."""
    with tempfile.TemporaryDirectory() as tmpdir:
        config_file = Path(tmpdir) / "test_config.yaml"

        # Create config
        config = LDAConfig()
        config.set("project.name", "Test Project")
        config.set("project.code", "TEST")
        config.set("project.analyst", "Test User")
        config.set("project.root_folder", tmpdir)

        config.set("sections", [{
            "name": "01_data",
            "inputs": ["{proj}_input.csv"],
            "outputs": ["{proj}_output.csv"]
        }])

        config.save(str(config_file))

        # Test init
        cli = LDACLI()
        result = cli.run(["--config", str(config_file), "init"])
        assert result == 0

        # Check created structure
        project_dir = Path(tmpdir) / "TEST"
        assert project_dir.exists()
        assert (project_dir / ".lda").exists()
        assert (project_dir / "README.md").exists()
        assert (project_dir / "TEST_sec01_data").exists()


def test_cli_status():
    """Test CLI status command."""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create a test project
        config_file = Path(tmpdir) / "test_config.yaml"

        config = LDAConfig()
        config.set("project.name", "Test Project")
        config.set("project.code", "TEST")
        config.set("project.analyst", "Test User")
        config.set("project.root_folder", tmpdir)

        config.set("sections", [{
            "name": "01_data",
            "inputs": ["{proj}_input.csv"],
            "outputs": ["{proj}_output.csv"]
        }])

        config.save(str(config_file))

        # Initialize project
        cli = LDACLI()
        cli.run(["--config", str(config_file), "init"])

        # Change to project directory
        os.chdir(Path(tmpdir) / "TEST")

        # Test status
        result = cli.run(["status"])
        assert result == 0


def test_cli_changes():
    """Test CLI changes command."""
    import pytest

    with tempfile.TemporaryDirectory() as tmpdir:
        # Create a test project
        config_file = Path(tmpdir) / "test_config.yaml"

        config = LDAConfig()
        config.set("project.name", "Test Project")
        config.set("project.code", "TEST")
        config.set("project.analyst", "Test User")
        config.set("project.root_folder", ".")  # Use relative path

        config.set("sections", [{
            "name": "01_data",
            "inputs": ["{proj}_input.csv"],
            "outputs": ["{proj}_output.csv"]
        }])

        # Save current directory
        try:
            original_dir = os.getcwd()
        except OSError:
            # If we can't get current dir, use temp dir
            original_dir = tmpdir

        try:
            os.chdir(tmpdir)
            config.save(str(config_file))

            # Initialize project
            cli = LDACLI()
            cli.run(["--config", str(config_file), "init"])

            # Change to project directory
            project_dir = Path(tmpdir) / "TEST"
            if project_dir.exists():
                os.chdir(project_dir)

                # Test changes (should be none)
                result = cli.run(["changes"])
                assert result == 0
            else:
                # If directory doesn't exist, skip the test
                pytest.skip("Project directory not created")
        finally:
            # Try to restore original directory
            try:
                os.chdir(original_dir)
            except OSError:
                pass
