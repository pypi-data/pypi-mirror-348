# Installation

Getting started with LDA is simple. Choose the installation method that works best for your environment.

## Requirements

- Python 3.8 or higher
- pip (Python package manager)
- Git (optional, for development installation)

## Quick Install

The fastest way to install LDA is using pip:

```bash
pip install lda-analysis
```

That's it! You can now start using LDA. Verify your installation:

```bash
lda --version
```

## Installation Methods

### Using pip (Recommended)

=== "Standard Install"

    ```bash
    pip install lda-analysis
    ```

=== "With Documentation Tools"

    ```bash
    pip install lda-analysis[docs]
    ```

=== "Development Version"

    ```bash
    pip install lda-analysis[dev]
    ```

### Using pipx (Isolated Environment)

If you prefer to install LDA in an isolated environment:

```bash
pipx install lda-analysis
```

### Using conda

For Anaconda users:

```bash
conda install -c conda-forge lda-analysis
```

### From Source

To install the latest development version:

```bash
git clone https://github.com/drpedapati/LDA.git
cd LDA
pip install -e .
```

## Platform-Specific Instructions

### macOS

```bash
# Using Homebrew Python
brew install python@3.10
pip3 install lda-analysis
```

### Windows

```powershell
# Using PowerShell
python -m pip install lda-analysis

# Or using py launcher
py -m pip install lda-analysis
```

### Linux

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install python3-pip
pip3 install lda-analysis

# Fedora/RHEL
sudo dnf install python3-pip
pip3 install lda-analysis
```

## Verify Installation

After installation, verify that LDA is working correctly:

```bash
# Check version
lda --version

# View help
lda --help

# Run basic test
lda init --dry-run
```

## Upgrading

To upgrade to the latest version:

```bash
pip install --upgrade lda-analysis
```

## Troubleshooting

### Common Issues

??? error "Permission Denied"

    If you encounter permission errors:
    
    ```bash
    pip install --user lda-analysis
    ```
    
    Or use a virtual environment:
    
    ```bash
    python -m venv lda-env
    source lda-env/bin/activate  # On Windows: lda-env\Scripts\activate
    pip install lda-analysis
    ```

??? error "Python Version Error"

    LDA requires Python 3.8+. Check your version:
    
    ```bash
    python --version
    ```
    
    If needed, upgrade Python or use pyenv to manage versions.

??? error "Module Not Found"

    Ensure pip is up to date:
    
    ```bash
    python -m pip install --upgrade pip
    pip install lda-analysis
    ```

### Getting Help

If you encounter issues:

1. Check the [troubleshooting guide](../troubleshooting.md)
2. Search [existing issues](https://github.com/drpedapati/LDA/issues)
3. Ask in [discussions](https://github.com/drpedapati/LDA/discussions)
4. Report a [new issue](https://github.com/drpedapati/LDA/issues/new)

## Next Steps

Now that you have LDA installed, proceed to:

<div class="grid cards" markdown>

-   :material-rocket-launch:{ .lg .middle } __Quick Start__

    ---

    Learn the basics in 5 minutes
    
    [:octicons-arrow-right-24: Get started](quickstart.md)

-   :material-file-document:{ .lg .middle } __First Project__

    ---

    Create your first LDA project
    
    [:octicons-arrow-right-24: Build project](first-project.md)

</div>