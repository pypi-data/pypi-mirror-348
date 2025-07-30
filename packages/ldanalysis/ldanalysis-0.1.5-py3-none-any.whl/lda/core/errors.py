"""Custom error classes for LDA package."""


class LDAError(Exception):
    """Base class for LDA-specific errors."""
    pass


class MissingPlaceholderError(LDAError):
    """Raised when a placeholder is missing from the configuration."""
    
    def __init__(self, missing: list, pattern: str, section: str = None):
        self.missing = missing
        self.pattern = pattern
        self.section = section
        msg = f"Missing placeholder values: {', '.join(missing)} in pattern: {pattern}"
        if section:
            msg += f" (section: {section})"
        super().__init__(msg)


class ConfigurationError(LDAError):
    """Raised when there's an error in the configuration."""
    pass


class ManifestError(LDAError):
    """Raised when there's an error with the manifest."""
    pass


class ScaffoldError(LDAError):
    """Raised when there's an error during scaffold generation."""
    pass


class FileTrackingError(LDAError):
    """Raised when there's an error with file tracking."""
    pass