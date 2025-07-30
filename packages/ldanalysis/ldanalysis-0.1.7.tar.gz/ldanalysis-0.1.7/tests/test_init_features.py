"""Test new initialization features."""
import pytest
from pathlib import Path

from lda.cli.commands import Commands
from lda.config import LDAConfig
from lda.display.console import Console


class MockArgs:
    """Mock args for testing."""
    def __init__(self, **kwargs):
        self.name = kwargs.get('name')
        self.analyst = kwargs.get('analyst')
        self.sections = kwargs.get('sections')
        self.no_playground = kwargs.get('no_playground', False)
        self.language = kwargs.get('language', 'python')
        self.template = kwargs.get('template', 'default')


def test_init_with_sections(tmp_path, monkeypatch):
    """Test initialization with custom sections."""
    monkeypatch.chdir(tmp_path)
    
    args = MockArgs(
        name="Test Project",
        sections="intro,methods,results"
    )
    
    display = Console()
    result = Commands.cmd_init(args, None, display)
    
    assert result == 0
    
    # Check config file is named after project
    config_file = tmp_path / "test_project_config.yaml"
    assert config_file.exists()
    
    # Check config contains sections
    config = LDAConfig(config_file)
    sections = config.get("sections")
    assert len(sections) == 3
    assert sections[0]["name"] == "intro"
    assert sections[1]["name"] == "methods"
    assert sections[2]["name"] == "results"


def test_init_with_language_both(tmp_path, monkeypatch):
    """Test initialization with both Python and R scripts."""
    monkeypatch.chdir(tmp_path)
    
    args = MockArgs(
        name="Multilang Project",
        sections="analysis",
        language="both"
    )
    
    display = Console()
    result = Commands.cmd_init(args, None, display)
    
    assert result == 0
    
    # Check both run scripts exist
    section_dir = tmp_path / "multilang_project" / "multilang_project_secanalysis"
    assert (section_dir / "run.py").exists()
    assert (section_dir / "run.R").exists()


def test_init_no_playground(tmp_path, monkeypatch):
    """Test initialization without playground."""
    monkeypatch.chdir(tmp_path)
    
    args = MockArgs(
        name="No Playground",
        no_playground=True
    )
    
    display = Console()
    result = Commands.cmd_init(args, None, display)
    
    assert result == 0
    
    # Check playground doesn't exist
    playground_dir = tmp_path / "no_playground" / "lda_playground"
    assert not playground_dir.exists()


def test_init_empty_project(tmp_path, monkeypatch):
    """Test initialization with no sections."""
    monkeypatch.chdir(tmp_path)
    
    args = MockArgs(
        name="Empty Project"
    )
    
    display = Console()
    result = Commands.cmd_init(args, None, display)
    
    assert result == 0
    
    # Check no sections were created
    project_dir = tmp_path / "empty_project"
    section_dirs = list(project_dir.glob("*_sec*"))
    assert len(section_dirs) == 0
    
    # Check playground was created by default
    playground_dir = project_dir / "lda_playground"
    assert playground_dir.exists()