"""Basic tests for LDA package."""

import pytest
from pathlib import Path

def test_imports():
    """Test that all modules can be imported."""
    import lda
    import lda.config
    import lda.core.scaffold
    import lda.core.manifest
    import lda.core.tracking
    import lda.core.errors
    import lda.display.console
    import lda.display.progress
    import lda.display.themes
    import lda.logging.logger
    import lda.logging.formatters
    import lda.cli.main
    import lda.cli.commands
    import lda.cli.utils


def test_package_version():
    """Test that package has version."""
    import lda
    assert hasattr(lda, '__version__')
    assert lda.__version__