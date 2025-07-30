"""Setup configuration for LDA package"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="ldanalysis",
    version="0.1.1",
    author="ErnieP",
    author_email="ernie@cincineuro.com",
    description="Linked Document Analysis - A provenance-driven project management system",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://cincineuro.github.io/ldanalysis/",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[
        "pyyaml>=6.0",
        "rich>=13.0",
        "click>=8.1",
        "jinja2>=3.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0",
            "pytest-cov>=4.0",
            "black>=22.0",
            "flake8>=5.0",
            "mypy>=0.990",
        ],
        "docs": [
            "mkdocs>=1.5.0",
            "mkdocs-material>=9.4.0",
            "mkdocs-material-extensions>=1.3",
            "mkdocs-minify-plugin>=0.7.0",
            "pymdown-extensions>=10.0",
            "mkdocs-git-revision-date-localized-plugin>=1.2.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "lda=lda.cli.main:main",
            "ldanalysis=lda.cli.main:main",
        ],
    },
    include_package_data=True,
    package_data={
        "lda": ["templates/**/*", "examples/**/*"],
    },
)