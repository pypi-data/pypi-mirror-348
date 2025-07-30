# Linked Document Analysis (LDA)

A project management and provenance system where every analytical process, input, and output is mapped directly to a section of the working document (e.g., manuscript, protocol, regulatory report).

Each analysis folder, manifest, and result is named and organized to mirror the document outline, creating a one-to-one link between text, code, data, and results.

This architecture ensures that every figure, table, or claim in the document is transparently and immutably traceable back to its generating code and data—enabling instant audit, replication, and regulatory review.

## Installation

Requires Python 3.10 or later with the Rich library for enhanced terminal output.

```bash
pip install rich
```

## Usage

Create a new LDA project scaffold:

```bash
python lda_scaffold.py
```

The scaffold will:
1. Create section folders matching your document structure
2. Generate file manifests for inputs and outputs
3. Set up provenance tracking with unique IDs
4. Initialize logging and documentation

## Project Structure

Each LDA project contains:
- **Section folders**: One-to-one mapping with document sections
- **File manifests**: Explicit lists of expected inputs and outputs
- **Provenance tracking**: Hashes, timestamps, and analyst attribution
- **Audit logs**: Complete history of all changes

## Documentation

See [CLAUDE.md](CLAUDE.md) for detailed architecture and usage instructions.

## License

MIT License - see LICENSE file for details.