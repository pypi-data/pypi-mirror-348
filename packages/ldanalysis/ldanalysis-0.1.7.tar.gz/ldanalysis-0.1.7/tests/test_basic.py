"""Basic tests for LDA package."""


def test_imports():
    """Test that all modules can be imported."""


def test_package_version():
    """Test that package has version."""
    import lda
    assert hasattr(lda, '__version__')
    assert lda.__version__
