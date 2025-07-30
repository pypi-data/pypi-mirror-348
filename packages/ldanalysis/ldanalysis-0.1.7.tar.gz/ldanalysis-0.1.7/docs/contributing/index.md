# Contributing to LDA

Thank you for your interest in contributing to Linked Document Analysis (LDA)! This guide will help you get started.

## Ways to Contribute

### 1. Report Issues
- Bug reports
- Feature requests
- Documentation improvements
- Performance issues

### 2. Submit Code
- Bug fixes
- New features
- Performance improvements
- Test coverage

### 3. Improve Documentation
- Fix typos and errors
- Add examples
- Clarify explanations
- Translate documentation

### 4. Help Others
- Answer questions in discussions
- Review pull requests
- Share your use cases
- Write tutorials

## Quick Start

1. **Fork the repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/LDA.git
   cd LDA
   ```

2. **Set up development environment**
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -e .[dev,docs]
   ```

3. **Create a branch**
   ```bash
   git checkout -b feature/your-feature
   ```

4. **Make changes and test**
   ```bash
   pytest
   lda docs serve  # If docs changed
   ```

5. **Submit pull request**
   ```bash
   git push origin feature/your-feature
   ```

## Guidelines

### Code of Conduct
- Be respectful and inclusive
- Welcome newcomers
- Focus on constructive feedback
- Assume good intentions

### Commit Messages
Follow conventional commits:
```
feat: Add new export format
fix: Handle empty file paths
docs: Update installation guide
test: Add config validation tests
```

### Pull Requests
- Keep changes focused
- Include tests
- Update documentation
- Add to changelog
- Reference related issues

### Code Style
- Follow PEP 8
- Use type hints
- Write clear docstrings
- Keep functions small
- Use meaningful names

## Development Guides

<div class="grid cards" markdown>

-   :material-code-braces:{ .lg .middle } __Development Setup__

    ---

    Set up your development environment
    
    [:octicons-arrow-right-24: Get started](development.md)

-   :material-test-tube:{ .lg .middle } __Testing Guide__

    ---

    Write and run tests
    
    [:octicons-arrow-right-24: Learn testing](testing.md)

-   :material-file-document:{ .lg .middle } __Documentation Guide__

    ---

    Update and improve docs
    
    [:octicons-arrow-right-24: Write docs](docs.md)

</div>

## Need Help?

- Read the [development guide](development.md)
- Check [existing issues](https://github.com/drpedapati/LDA/issues)
- Ask in [discussions](https://github.com/drpedapati/LDA/discussions)
- Contact maintainers

## Recognition

Contributors are recognized in:
- CONTRIBUTORS.md file
- Release notes
- Documentation credits
- GitHub contributors page

Thank you for making LDA better! 🎉