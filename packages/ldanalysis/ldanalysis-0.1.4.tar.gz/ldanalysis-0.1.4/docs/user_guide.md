# LDA User Guide

## Getting Started

LDA (Linked Document Analysis) is a project management system that creates a one-to-one mapping between document sections and analysis folders.

### Installation

```bash
pip install lda-tool
```

### Quick Start

1. Create a configuration file `lda_config.yaml`:

```yaml
project:
  name: "My Project"
  code: "MP2024"
  analyst: "Your Name"

sections:
  - name: "01_data"
    inputs:
      - "{proj}_input.csv"
    outputs:
      - "{proj}_output.csv"
```

2. Initialize the project:

```bash
lda init
```

3. Check project status:

```bash
lda status
```

## Configuration

### Project Settings

The `project` section defines basic project information:

- `name`: Human-readable project name
- `code`: Short project code (used in file naming)
- `analyst`: Name of the analyst
- `root_folder`: Root directory for the project (default: ".")

### Placeholders

Placeholders allow dynamic values in file patterns:

```yaml
placeholders:
  proj: "${project.code}"
  date: "${datetime.now().strftime('%Y%m%d')}"
  custom: "value"
```

### Sections

Each section represents a step in your analysis:

```yaml
sections:
  - name: "01_preprocessing"
    inputs:
      - "{proj}_raw_data.csv"
    outputs:
      - "{proj}_cleaned_data.csv"
```

## Commands

### init

Initialize a new project:

```bash
lda init
lda init --template research
lda init --name "My Project" --analyst "John Doe"
```

### status

Show project status:

```bash
lda status
lda status --format json
```

### track

Track files in the manifest:

```bash
lda track data.csv --section 01_data --type input
```

### changes

Show file changes:

```bash
lda changes
lda changes --section 01_data
```

### history

View project history:

```bash
lda history
lda history --limit 20
```

### validate

Validate project structure:

```bash
lda validate
lda validate --fix
```

### export

Export manifests or reports:

```bash
lda export manifest --output manifest.csv
lda export manifest --output manifest.json --format json
```

## Best Practices

1. **Consistent Naming**: Use consistent naming patterns for files
2. **Regular Commits**: Track changes regularly
3. **Document Sections**: Add README files to each section
4. **Use Placeholders**: Leverage placeholders for flexible file naming
5. **Version Control**: Use Git alongside LDA for complete tracking

## Troubleshooting

### Common Issues

1. **Missing placeholders**: Ensure all placeholders in patterns are defined
2. **File not found**: Check file paths are relative to project root
3. **Permission errors**: Ensure write permissions in project directory

### Getting Help

- Check the [API Reference](api_reference.md)
- Visit the [GitHub repository](https://github.com/yourusername/lda)
- Open an issue for bugs or feature requests