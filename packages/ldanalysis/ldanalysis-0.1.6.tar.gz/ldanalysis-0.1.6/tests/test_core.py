"""Tests for core functionality."""

import tempfile
from pathlib import Path

from lda.config import LDAConfig
from lda.core.errors import MissingPlaceholderError
from lda.core.manifest import LDAManifest
from lda.core.scaffold import LDAScaffold
from lda.core.tracking import FileTracker


def test_scaffold_creation():
    """Test scaffold creation."""
    with tempfile.TemporaryDirectory() as tmpdir:
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

        scaffold = LDAScaffold(config)
        result = scaffold.create_project()

        assert result["success"]
        assert Path(result["project_folder"]).exists()
        assert len(result["sections"]) == 1
        assert len(result["files"]) == 2


def test_manifest_operations():
    """Test manifest operations."""
    with tempfile.TemporaryDirectory() as tmpdir:
        manifest = LDAManifest(tmpdir)

        # Test project initialization
        manifest.init_project({
            "name": "Test Project",
            "code": "TEST",
            "analyst": "Test User"
        })

        assert manifest.manifest["project"]["code"] == "TEST"

        # Test section addition
        manifest.add_section("01_data", {
            "folder": "01_data",
            "inputs": ["input.csv"],
            "outputs": ["output.csv"]
        }, "test_prov_id")

        assert "01_data" in manifest.manifest["sections"]

        # Test file tracking
        Path(tmpdir, "01_data", "inputs").mkdir(parents=True)
        test_file = Path(tmpdir, "01_data", "inputs", "test.csv")
        test_file.write_text("test data")

        manifest.track_file("01_data", "input", "test.csv")

        files = manifest.get_section_files("01_data")
        assert len(files["inputs"]) == 1


def test_file_tracker():
    """Test file tracking."""
    with tempfile.TemporaryDirectory() as tmpdir:
        tracker = FileTracker()

        # Create test file
        test_file = Path(tmpdir, "test.txt")
        test_file.write_text("test content")

        # Track file
        info = tracker.track_file(str(test_file), "text")

        assert info["exists"]
        assert info["hash"] is not None
        assert info["size"] > 0

        # Test change detection
        original_hash = info["hash"]

        # Modify file
        test_file.write_text("modified content")

        # Detect changes
        changes = tracker.detect_changes(str(test_file))

        assert changes["changed"]
        assert "Content changed" in changes["reasons"]


def test_error_handling():
    """Test error handling."""
    # Test missing placeholder error
    error = MissingPlaceholderError(["missing"], "pattern", "section")

    assert "missing" in str(error)
    assert "pattern" in str(error)
    assert "section" in str(error)
