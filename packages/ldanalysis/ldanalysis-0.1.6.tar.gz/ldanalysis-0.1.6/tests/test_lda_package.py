"""Test the LDA package as a whole."""
import subprocess
import sys
from pathlib import Path

import pytest

from lda import __version__
from lda.config import LDAConfig
from lda.core.manifest import LDAManifest
from lda.core.scaffold import LDAScaffold
from lda.core.tracking import FileTracker


class TestLDAPackage:
    """Test the complete LDA package."""

    def test_package_version(self):
        """Test package version is defined."""
        assert __version__ is not None
        assert isinstance(__version__, str)
        assert len(__version__.split('.')) >= 2

    def test_package_imports(self):
        """Test all main modules can be imported."""
        modules = [
            'lda.config',
            'lda.core.errors',
            'lda.core.scaffold',
            'lda.core.manifest',
            'lda.core.tracking',
            'lda.cli.main',
            'lda.cli.commands',
            'lda.display.console',
            'lda.logging.logger'
        ]

        for module in modules:
            try:
                __import__(module)
            except ImportError as e:
                pytest.fail(f"Failed to import {module}: {e}")

    def test_cli_entry_point(self):
        """Test CLI can be invoked as module."""
        result = subprocess.run(
            [sys.executable, "-m", "lda", "--version"],
            capture_output=True,
            text=True
        )

        assert result.returncode == 0
        assert __version__ in result.stdout

    def test_complete_workflow_integration(self, temp_dir: Path):
        """Test complete end-to-end workflow."""
        # 1. Create configuration
        config_data = {
            "project": {
                "name": "Integration Test",
                "code": "INT",
                "description": "Full integration test"
            },
            "sections": {
                "docs": {
                    "name": "Documentation",
                    "files": ["README.md", "docs/*.md"]
                },
                "src": {
                    "name": "Source Code",
                    "files": ["src/*.py", "tests/*.py"]
                }
            }
        }

        # 2. Initialize configuration
        config_file = temp_dir / "lda_config.yaml"
        config = LDAConfig()
        config.config = config_data
        config.save(str(config_file))

        # 3. Create scaffold
        scaffold = LDAScaffold(config)
        scaffold.generate_structure()

        # 4. Initialize manifest
        manifest = LDAManifest(str(temp_dir))
        manifest.create()

        # 5. Initialize tracking
        tracker = FileTracker(str(temp_dir))

        # 6. Create some files
        (temp_dir / "README.md").write_text("# Integration Test")
        (temp_dir / "docs").mkdir(exist_ok=True)
        (temp_dir / "docs" / "guide.md").write_text("# User Guide")
        (temp_dir / "src").mkdir(exist_ok=True)
        (temp_dir / "src" / "main.py").write_text("def main(): pass")

        # 7. Track files
        for file_path in [
            temp_dir / "README.md",
            temp_dir / "docs" / "guide.md",
            temp_dir / "src" / "main.py"
        ]:
            if file_path.exists():
                tracked = tracker.track_file(str(file_path))

                # Determine section
                if "docs" in str(file_path) or "README" in str(file_path):
                    section = "docs"
                else:
                    section = "src"

                # Add to manifest
                manifest.add_file(section, {
                    "path": str(file_path.relative_to(temp_dir)),
                    "hash": tracked.hash,
                    "size": tracked.size
                })

        # 8. Verify everything is set up correctly
        assert (temp_dir / ".lda").exists()
        assert (temp_dir / ".lda" / "manifest.yaml").exists()
        assert len(tracker.get_tracked_files()) >= 3

        # 9. Test change detection
        (temp_dir / "README.md").write_text("# Modified Integration Test")
        changes = tracker.detect_changes(str(temp_dir / "README.md"))
        assert changes["changed"]

        # 10. Verify manifest integrity
        manifest_data = manifest.load()
        assert manifest_data["project"]["name"] == "Integration Test"
        assert len(manifest_data["tracking"]["files"]["docs"]) > 0

    def test_error_handling_cascade(self, temp_dir: Path):
        """Test error handling across modules."""
        # Test configuration error
        with pytest.raises(Exception):
            config = LDAConfig("/nonexistent/config.yaml")

        # Test scaffold error
        config = LDAConfig()
        scaffold = LDAScaffold(config, str(temp_dir))
        scaffold.generate_structure()

        # Should raise error on second attempt without force
        with pytest.raises(Exception):
            scaffold.generate_structure()

        # Test tracking error
        tracker = FileTracker(str(temp_dir))
        with pytest.raises(Exception):
            tracker.track_file("/nonexistent/file.txt")

    def test_cross_platform_compatibility(self, temp_dir: Path):
        """Test cross-platform path handling."""
        config = LDAConfig()
        config.config = {
            "project": {"name": "Cross Platform", "code": "XP"},
            "sections": {
                "test": {
                    "name": "Test",
                    # Use forward slashes - should work on all platforms
                    "files": ["path/to/file.txt", "another/path/file.md"]
                }
            }
        }

        scaffold = LDAScaffold(config, str(temp_dir))
        scaffold.generate_structure()

        # Verify paths are created correctly regardless of platform
        assert (temp_dir / "path" / "to").exists()
        assert (temp_dir / "another" / "path").exists()

    @pytest.mark.slow
    def test_large_project_handling(self, temp_dir: Path):
        """Test handling of large projects."""
        # Create config with many sections
        sections = {}
        for i in range(50):
            sections[f"section_{i}"] = {
                "name": f"Section {i}",
                "files": [f"section_{i}/*.txt", f"section_{i}/*.md"]
            }

        config = LDAConfig()
        config.config = {
            "project": {"name": "Large Project", "code": "LG"},
            "sections": sections
        }

        # Should handle large configurations efficiently
        scaffold = LDAScaffold(config, str(temp_dir))
        scaffold.generate_structure()

        # Create and track many files
        tracker = FileTracker(str(temp_dir))
        files_created = 0

        for i in range(10):  # Reduced for test performance
            section_dir = temp_dir / f"section_{i}"
            section_dir.mkdir(exist_ok=True)

            for j in range(5):
                file_path = section_dir / f"file_{j}.txt"
                file_path.write_text(f"Content {i}-{j}")
                tracker.track_file(str(file_path))
                files_created += 1

        assert files_created == 50
        assert len(tracker.get_tracked_files()) == 50
