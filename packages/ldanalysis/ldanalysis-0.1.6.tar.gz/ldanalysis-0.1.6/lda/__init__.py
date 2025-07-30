"""
Linked Document Analysis (LDA) - A provenance-driven project management system

LDA provides tools for creating and managing analytical workflows with
one-to-one mapping between document sections and analysis folders.
"""

__version__ = "0.1.5"
__author__ = "ErnieP"
__email__ = "ernie@cincineuro.com"

from .core.scaffold import LDAScaffold
from .core.manifest import LDAManifest
from .config import LDAConfig

__all__ = ["LDAScaffold", "LDAManifest", "LDAConfig"]