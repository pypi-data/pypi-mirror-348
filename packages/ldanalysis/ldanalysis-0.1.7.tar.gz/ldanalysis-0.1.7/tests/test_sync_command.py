"""Test sync command functionality."""
import pytest
from pathlib import Path
import yaml

from lda.cli.commands import Commands
from lda.config import LDAConfig
from lda.display.console import Console


class MockArgs:
    """Mock args for testing."""
    def __init__(self, **kwargs):
        # Init command attributes
        self.name = kwargs.get('name')
        self.analyst = kwargs.get('analyst')
        self.sections = kwargs.get('sections')
        self.no_playground = kwargs.get('no_playground', False)
        self.language = kwargs.get('language', 'python')
        self.template = kwargs.get('template', 'default')
        
        # Sync command attributes
        self.config = kwargs.get('config')
        self.dry_run = kwargs.get('dry_run', False)


def test_sync_create_missing_sections(tmp_path, monkeypatch):
    """Test sync creates missing sections from config."""
    monkeypatch.chdir(tmp_path)
    
    # Create initial project with one section
    init_config = {
        "project": {
            "name": "Test Project",
            "code": "test_project",
            "analyst": "Test User"
        },
        "sections": [
            {"name": "intro", "inputs": [], "outputs": []}
        ]
    }
    
    config_file = tmp_path / "test_project_config.yaml"
    with open(config_file, 'w') as f:
        yaml.dump(init_config, f)
    
    # Initialize project with existing config
    config = LDAConfig(config_file)
    init_args = MockArgs()  # Empty args since we're using existing config
    Commands.cmd_init(init_args, config, Console())
    
    # Update config to add more sections
    init_config["sections"].extend([
        {"name": "methods", "inputs": [], "outputs": []},
        {"name": "results", "inputs": [], "outputs": []}
    ])
    
    with open(config_file, 'w') as f:
        yaml.dump(init_config, f)
    
    # Run sync
    sync_args = MockArgs(config=str(config_file))
    result = Commands.cmd_sync(sync_args, None, Console())
    
    assert result == 0
    
    # Check new sections were created
    project_dir = tmp_path / "test_project"
    assert (project_dir / "test_project_secmethods").exists()
    assert (project_dir / "test_project_secresults").exists()


def test_sync_dry_run(tmp_path, monkeypatch, capsys):
    """Test sync dry run mode."""
    monkeypatch.chdir(tmp_path)
    
    # Create initial project
    init_config = {
        "project": {
            "name": "Dry Run Test",
            "code": "dry_run_test",
            "analyst": "Test User"
        },
        "sections": [
            {"name": "existing", "inputs": [], "outputs": []}
        ]
    }
    
    config_file = tmp_path / "dry_run_test_config.yaml"
    with open(config_file, 'w') as f:
        yaml.dump(init_config, f)
    
    # Initialize project with existing config
    config = LDAConfig(config_file)
    init_args = MockArgs()  # Empty args since we're using existing config
    Commands.cmd_init(init_args, config, Console())
    
    # Update config to add section
    init_config["sections"].append(
        {"name": "new_section", "inputs": [], "outputs": []}
    )
    
    with open(config_file, 'w') as f:
        yaml.dump(init_config, f)
    
    # Clear previous output
    capsys.readouterr()
    
    # Run sync with dry-run
    sync_args = MockArgs(config=str(config_file), dry_run=True)
    result = Commands.cmd_sync(sync_args, None, Console())
    
    assert result == 0
    
    # Check output mentions what would be done
    captured = capsys.readouterr()
    assert "Sections to create: new_section" in captured.out
    
    # Verify section was NOT actually created
    project_dir = tmp_path / "dry_run_test"
    assert not (project_dir / "dry_run_test_secnew_section").exists()


def test_sync_playground_creation(tmp_path, monkeypatch):
    """Test sync creates playground when added to config."""
    monkeypatch.chdir(tmp_path)
    
    # Create project without playground
    init_config = {
        "project": {
            "name": "No Playground",
            "code": "no_playground",
            "analyst": "Test User",
            "create_playground": False
        },
        "sections": []
    }
    
    config_file = tmp_path / "no_playground_config.yaml"
    with open(config_file, 'w') as f:
        yaml.dump(init_config, f)
    
    # Initialize project with existing config
    config = LDAConfig(config_file)
    init_args = MockArgs()  # Empty args since we're using existing config
    Commands.cmd_init(init_args, config, Console())
    
    # Verify no playground
    project_dir = tmp_path / "no_playground"
    assert not (project_dir / "lda_playground").exists()
    
    # Update config to add playground
    init_config["project"]["create_playground"] = True
    
    with open(config_file, 'w') as f:
        yaml.dump(init_config, f)
    
    # Run sync
    sync_args = MockArgs(config=str(config_file))
    result = Commands.cmd_sync(sync_args, None, Console())
    
    assert result == 0
    
    # Check playground was created
    assert (project_dir / "lda_playground").exists()


def test_sync_no_changes_needed(tmp_path, monkeypatch, capsys):
    """Test sync when no changes are needed."""
    monkeypatch.chdir(tmp_path)
    
    # Create project
    init_config = {
        "project": {
            "name": "No Changes",
            "code": "no_changes",
            "analyst": "Test User"
        },
        "sections": [
            {"name": "section1", "inputs": [], "outputs": []}
        ]
    }
    
    config_file = tmp_path / "no_changes_config.yaml"
    with open(config_file, 'w') as f:
        yaml.dump(init_config, f)
    
    # Initialize project with existing config
    config = LDAConfig(config_file)
    init_args = MockArgs()  # Empty args since we're using existing config
    Commands.cmd_init(init_args, config, Console())
    
    # Clear previous output
    capsys.readouterr()
    
    # Run sync without config changes
    sync_args = MockArgs(config=str(config_file))
    result = Commands.cmd_sync(sync_args, None, Console())
    
    assert result == 0
    
    # Check output mentions no changes
    captured = capsys.readouterr()
    assert "No changes needed" in captured.out


def test_sync_warns_about_removed_sections(tmp_path, monkeypatch, capsys):
    """Test sync warns about sections that exist but not in config."""
    monkeypatch.chdir(tmp_path)
    
    # Create project with two sections
    init_config = {
        "project": {
            "name": "Remove Section Test",
            "code": "remove_test",
            "analyst": "Test User"
        },
        "sections": [
            {"name": "keep", "inputs": [], "outputs": []},
            {"name": "remove", "inputs": [], "outputs": []}
        ]
    }
    
    config_file = tmp_path / "remove_test_config.yaml"
    with open(config_file, 'w') as f:
        yaml.dump(init_config, f)
    
    # Initialize project with existing config
    config = LDAConfig(config_file)
    init_args = MockArgs()  # Empty args since we're using existing config
    Commands.cmd_init(init_args, config, Console())
    
    # Remove section from config
    init_config["sections"] = [
        {"name": "keep", "inputs": [], "outputs": []}
    ]
    
    with open(config_file, 'w') as f:
        yaml.dump(init_config, f)
    
    # Clear previous output
    capsys.readouterr()
    
    # Run sync
    sync_args = MockArgs(config=str(config_file))
    result = Commands.cmd_sync(sync_args, None, Console())
    
    assert result == 0
    
    # Check warning was shown
    captured = capsys.readouterr()
    assert "Sections exist but not in config: remove" in captured.out
    assert "These sections were NOT removed" in captured.out
    
    # Verify section still exists
    project_dir = tmp_path / "remove_test"
    assert (project_dir / "remove_test_secremove").exists()