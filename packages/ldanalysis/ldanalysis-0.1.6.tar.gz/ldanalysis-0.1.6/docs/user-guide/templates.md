# Project Templates

LDA provides pre-configured templates for common project types. Templates help you get started quickly with best practices and standard structures.

## Available Templates

### Research Template

Perfect for academic research projects with literature review, data collection, and analysis phases.

```bash
lda init --template research
```

**Features:**
- Protocol management
- Ethics tracking
- Literature references
- Data collection workflows
- Statistical analysis
- Publication preparation

**Structure:**
```
research-project/
├── docs/
│   ├── protocol/
│   ├── literature/
│   └── reports/
├── data/
│   ├── raw/
│   ├── processed/
│   └── metadata/
├── analysis/
│   ├── scripts/
│   ├── notebooks/
│   └── results/
├── publications/
│   ├── manuscripts/
│   ├── figures/
│   └── supplements/
└── admin/
    ├── ethics/
    ├── grants/
    └── meetings/
```

### Software Template

Ideal for software development projects with source code, tests, and documentation.

```bash
lda init --template software  
```

**Features:**
- Source code organization
- Test suite tracking
- Documentation management
- Build artifacts
- Release management
- Issue tracking

**Structure:**
```
software-project/
├── src/
│   ├── main/
│   └── test/
├── docs/
│   ├── api/
│   ├── guides/
│   └── tutorials/
├── config/
├── scripts/
├── build/
└── releases/
```

### Documentation Template

Designed for technical writing and documentation projects.

```bash
lda init --template documentation
```

**Features:**
- Multi-format output
- Version tracking
- Translation management
- Review workflows
- Publication pipeline

**Structure:**
```
documentation-project/
├── content/
│   ├── guides/
│   ├── tutorials/
│   ├── reference/
│   └── examples/
├── assets/
│   ├── images/
│   ├── diagrams/
│   └── videos/
├── locales/
├── themes/
└── output/
```

### Data Science Template

Optimized for machine learning and data analysis projects.

```bash
lda init --template data-science
```

**Features:**
- Dataset versioning
- Experiment tracking
- Model management
- Pipeline automation
- Results visualization

**Structure:**
```
datascience-project/
├── data/
│   ├── raw/
│   ├── interim/
│   ├── processed/
│   └── external/
├── notebooks/
│   ├── exploratory/
│   ├── analysis/
│   └── reports/
├── src/
│   ├── data/
│   ├── features/
│   ├── models/
│   └── visualization/
├── models/
├── reports/
│   ├── figures/
│   └── papers/
└── references/
```

### Minimal Template

A bare-bones template for simple projects.

```bash
lda init --template minimal
```

**Features:**
- Basic structure
- Simple configuration
- Quick setup
- Minimal overhead

**Structure:**
```
minimal-project/
├── docs/
├── src/
├── data/
└── output/
```

## Using Templates

### Basic Usage

```bash
# Initialize with template
lda init --template research

# Interactive mode
lda init --template research --interactive

# With custom values
lda init --template research \
  --name "Climate Study" \
  --code "CLIMATE-2024" \
  --author "Dr. Smith"
```

### Template Options

```bash
# List available templates
lda templates list

# Show template details
lda templates show research

# Preview template structure
lda templates preview research

# Create from specific version
lda init --template research@v2.0
```

## Customizing Templates

### Template Configuration

Each template includes a configuration file:

```yaml
# template.yaml
name: research
version: 1.0
description: "Academic research project template"

variables:
  project_type:
    description: "Type of research"
    default: "experimental"
    choices: ["experimental", "theoretical", "review"]
  
  discipline:
    description: "Research discipline"
    default: "general"
    
  includes_data:
    description: "Will project include data collection?"
    type: boolean
    default: true

structure:
  - path: "docs/protocol"
    condition: "{{ project_type == 'experimental' }}"
  
  - path: "data/raw"
    condition: "{{ includes_data }}"
  
  - path: "analysis/statistical"
    condition: "{{ discipline in ['psychology', 'medicine'] }}"

files:
  - source: "README.md.j2"
    destination: "README.md"
    
  - source: "protocol.md.j2"
    destination: "docs/protocol/main.md"
    condition: "{{ project_type == 'experimental' }}"

configuration:
  project:
    type: "{{ project_type }}"
    discipline: "{{ discipline }}"
  
  sections:
    literature:
      enabled: true
      citation_style: "apa"
    
    data:
      enabled: "{{ includes_data }}"
      validation_required: true
```

### Creating Custom Templates

1. **Create template directory**
```bash
mkdir ~/.lda/templates/my-template
```

2. **Add template configuration**
```yaml
# ~/.lda/templates/my-template/template.yaml
name: my-template
version: 1.0
description: "My custom template"

variables:
  feature_x:
    description: "Enable feature X"
    type: boolean
    default: false

structure:
  - path: "src"
  - path: "docs"
  - path: "tests"
  - path: "config"
    condition: "{{ feature_x }}"
```

3. **Add template files**
```bash
# ~/.lda/templates/my-template/files/README.md.j2
# {{ project.name }}

{{ project.description }}

## Getting Started

This project was created with the {{ template.name }} template.

{% if feature_x %}
## Feature X

This project includes Feature X configuration.
{% endif %}
```

4. **Use custom template**
```bash
lda init --template my-template
```

## Template Examples

### Research Project Example

```bash
lda init --template research
```

**Configuration prompts:**
```
Project name: Coral Reef Study
Project code: CORAL-2024
Author: Dr. Jane Smith
Email: jane.smith@oceanlab.edu
Organization: Ocean Research Institute
Research type: experimental
Discipline: marine biology
Include data collection? yes
Include statistical analysis? yes
```

**Generated configuration:**
```yaml
project:
  name: "Coral Reef Study"
  code: "CORAL-2024"
  author: "Dr. Jane Smith"
  email: "jane.smith@oceanlab.edu"
  organization: "Ocean Research Institute"
  type: "experimental"
  discipline: "marine biology"

sections:
  protocol:
    name: "Research Protocol"
    type: "documentation"
    files:
      - "docs/protocol/*.md"
      - "docs/ethics/*.pdf"
  
  fieldwork:
    name: "Field Data Collection"
    type: "data"
    files:
      - "data/field/*.csv"
      - "data/field/*.json"
      - "data/photos/*.jpg"
  
  laboratory:
    name: "Lab Analysis"
    type: "data"
    files:
      - "data/lab/*.xlsx"
      - "data/lab/results/*.csv"
  
  analysis:
    name: "Statistical Analysis"
    type: "code"
    files:
      - "analysis/*.R"
      - "analysis/*.py"
      - "analysis/output/*.png"

tracking:
  monitor_changes: true
  backup_on_change: true
  
  validation:
    required_files:
      - "docs/protocol/main.md"
      - "docs/ethics/approval.pdf"
      - "data/metadata.json"
```

### Software Project Example

```bash
lda init --template software
```

**Configuration prompts:**
```
Project name: Task Manager API
Project code: TASKAPI
Author: John Developer
Email: john@company.com
Language: python
Framework: fastapi
Include tests? yes
Include docs? yes
Include CI/CD? yes
```

**Generated structure:**
```
task-manager-api/
├── src/
│   └── taskapi/
│       ├── __init__.py
│       ├── main.py
│       ├── models/
│       ├── routes/
│       ├── services/
│       └── utils/
├── tests/
│   ├── unit/
│   ├── integration/
│   └── fixtures/
├── docs/
│   ├── api/
│   ├── development/
│   └── deployment/
├── config/
│   ├── development.yaml
│   ├── testing.yaml
│   └── production.yaml
├── scripts/
│   ├── setup.sh
│   ├── test.sh
│   └── deploy.sh
├── .github/
│   └── workflows/
│       ├── test.yml
│       └── deploy.yml
└── requirements/
    ├── base.txt
    ├── development.txt
    └── production.txt
```

## Advanced Template Features

### Conditional Sections

```yaml
sections:
  frontend:
    condition: "{{ project.includes_frontend }}"
    files:
      - "src/frontend/**/*"
  
  backend:
    condition: "{{ project.includes_backend }}"
    files:
      - "src/backend/**/*"
  
  mobile:
    condition: "{{ project.platforms contains 'mobile' }}"
    files:
      - "src/mobile/**/*"
```

### Dynamic File Generation

```yaml
files:
  - source: "config.yaml.j2"
    destination: "config/{{ environment }}.yaml"
    foreach: environment
    in: ["development", "staging", "production"]
```

### Post-Init Hooks

```yaml
hooks:
  post_init:
    - command: "git init"
      condition: "{{ use_git }}"
    
    - command: "npm install"
      condition: "{{ language == 'javascript' }}"
    
    - command: "python -m venv venv"
      condition: "{{ language == 'python' }}"
    
    - script: "scripts/setup.sh"
      condition: "{{ run_setup }}"
```

### Template Inheritance

```yaml
# child-template.yaml
extends: research
version: 1.0

# Override parent settings
variables:
  discipline:
    default: "psychology"
    choices: ["clinical", "cognitive", "social"]

# Add new sections
structure:
  - path: "experiments"
  - path: "participants"
  
# Extend configuration
configuration:
  sections:
    experiments:
      name: "Experiments"
      type: "protocol"
    
    participants:
      name: "Participant Data"
      type: "sensitive"
      encryption: required
```

## Template Best Practices

### 1. Keep Templates Focused

Each template should serve a specific use case:
- Research projects
- Software applications
- Documentation sites
- Data pipelines

### 2. Use Meaningful Defaults

```yaml
variables:
  author:
    default: "{{ env.USER }}"
  
  date:
    default: "{{ datetime.now().strftime('%Y-%m-%d') }}"
  
  organization:
    default: "{{ env.LDA_DEFAULT_ORG }}"
```

### 3. Document Variables

```yaml
variables:
  database_type:
    description: "Database system to use"
    type: choice
    choices: ["postgresql", "mysql", "sqlite"]
    default: "postgresql"
    help: |
      PostgreSQL: Best for production
      MySQL: Good compatibility
      SQLite: Simple, file-based
```

### 4. Provide Examples

Include example files in your template:
```
template/
├── examples/
│   ├── sample_analysis.py
│   ├── example_config.yaml
│   └── demo_notebook.ipynb
```

### 5. Version Templates

```yaml
version: 2.0
minimum_lda_version: 1.5.0
breaking_changes:
  - "Renamed 'data' section to 'datasets'"
  - "Removed deprecated 'output' directory"
```

## Creating Template Packages

### Package Structure

```
my-templates/
├── package.yaml
├── research-extended/
│   ├── template.yaml
│   └── files/
├── lab-notebook/
│   ├── template.yaml
│   └── files/
└── README.md
```

### Publishing Templates

```bash
# Package templates
lda templates package my-templates/

# Publish to registry
lda templates publish my-template-pack-1.0.tar.gz

# Install from registry
lda templates install organization/template-pack
```

## Template Development Workflow

1. **Start with existing template**
```bash
lda templates clone research my-research
```

2. **Modify configuration**
```bash
cd ~/.lda/templates/my-research
edit template.yaml
```

3. **Test template**
```bash
lda init --template my-research --dry-run
```

4. **Iterate and refine**
```bash
lda templates validate my-research
```

5. **Share with team**
```bash
lda templates export my-research
```

## Next Steps

<div class="grid cards" markdown>

-   :material-workflow:{ .lg .middle } __Workflows__

    ---

    Common workflow patterns
    
    [:octicons-arrow-right-24: Learn more](workflows.md)

-   :material-cog:{ .lg .middle } __Configuration__

    ---

    Detailed configuration options
    
    [:octicons-arrow-right-24: Configure](configuration.md)

-   :material-api:{ .lg .middle } __API Reference__

    ---

    Template API documentation
    
    [:octicons-arrow-right-24: View API](../api-reference/templates.md)

</div>