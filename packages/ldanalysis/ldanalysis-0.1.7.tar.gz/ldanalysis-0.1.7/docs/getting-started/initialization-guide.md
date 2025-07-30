# Project Initialization Guide

LDA provides flexible project initialization that adapts to your workflow. This guide covers all initialization options and best practices.

## Basic Initialization

Create a new project with default settings:

```bash
uvx ldanalysis init --name "My Project"
```

This creates:
- A project folder named `my_project`
- A configuration file `my_project_config.yaml`
- An `lda_playground` directory for experimentation
- A manifest file for tracking

## Initialization Options

### Custom Sections

Create specific sections during initialization:

```bash
uvx ldanalysis init --name "Research Study" --sections "intro,methods,results,discussion"
```

Each section gets:
- Input/output directories
- Logs directory
- Run scripts (Python by default)
- README file

### Language Support

Generate run scripts in different languages:

```bash
# Python only (default)
uvx ldanalysis init --name "Project" --language python

# R only
uvx ldanalysis init --name "Project" --language r

# Both Python and R
uvx ldanalysis init --name "Project" --language both
```

### Without Playground

Skip the playground directory:

```bash
uvx ldanalysis init --name "Focused Project" --no-playground
```

### Empty Project

Initialize with no predefined sections:

```bash
uvx ldanalysis init --name "Blank Slate"
```

## Configuration File

The configuration file is automatically named after your project:
- Project: "Climate Analysis 2024"
- Config: `climate_analysis_2024_config.yaml`

This makes it easy to manage multiple projects.

## Example Workflows

### Data Science Project

```bash
uvx ldanalysis init \
  --name "Sales Analysis 2024" \
  --sections "data_import,cleaning,exploration,modeling,reporting" \
  --language both
```

### Research Paper

```bash
uvx ldanalysis init \
  --name "Drug Study Phase 3" \
  --sections "protocol,data_collection,analysis,figures,manuscript" \
  --language r
```

### Quick Exploration

```bash
uvx ldanalysis init \
  --name "Quick Test" \
  --no-playground
```

## Playground Directory

The `lda_playground` directory includes:
- `experiments/`: For exploratory analyses
- `scratch/`: For temporary work
- `notebooks/`: For Jupyter notebooks
- Example scripts in your chosen language(s)

This provides a structured space for experimentation before formalizing analyses into sections.

## Best Practices

1. **Use descriptive project names**: They become folder names and config files
2. **Plan sections upfront**: Each section maps to a document section
3. **Choose languages wisely**: Both is useful for teams, single language for solo work
4. **Use playground for exploration**: Test ideas before creating formal sections
5. **Keep sections focused**: One analysis goal per section

## Next Steps

After initialization:
1. Review the generated configuration file
2. Add input files to section directories
3. Modify run scripts for your analyses
4. Use `lda status` to track progress
5. Use `lda track` to register files