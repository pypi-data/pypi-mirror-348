# LDA Configuration Guide

## Configuration File Format

LDA uses YAML format for configuration files. The default filename is `lda_config.yaml`.

## Configuration Schema

### Root Level

```yaml
project:      # Project metadata
placeholders: # Variable substitutions
sections:     # Analysis sections
sandbox:      # Experimental areas
logging:      # Logging configuration
display:      # Display preferences
```

### Project Configuration

```yaml
project:
  name: "Project Name"          # Human-readable name
  code: "PROJ"                 # Short code for file naming
  analyst: "Analyst Name"      # Primary analyst
  root_folder: "."            # Project root directory
```

### Placeholders

Placeholders allow dynamic values in file patterns:

```yaml
placeholders:
  proj: "${project.code}"                    # From project config
  date: "${datetime.now().strftime('%Y%m%d')}" # Dynamic date
  version: "v1"                             # Static value
  subject: "S{:03d}"                        # Formatted string
```

### Sections

Define analysis workflow sections:

```yaml
sections:
  - name: "01_preprocessing"
    inputs:
      - "{proj}_raw_{date}.csv"
      - "{proj}_metadata.json"
    outputs:
      - "{proj}_cleaned_{date}.csv"
      - "{proj}_qc_report_{date}.pdf"
```

### Sandbox

Define experimental areas:

```yaml
sandbox:
  - "experiments"
  - "prototypes"
  - "scratch"
```

### Logging

Configure logging behavior:

```yaml
logging:
  level: "INFO"           # DEBUG, INFO, WARNING, ERROR
  format: "text"         # text or json
  console_output: true   # Show logs in console
  file_output: true      # Save logs to file
```

### Display

Configure display preferences:

```yaml
display:
  style: "conservative"  # conservative, rich, minimal
  colors: true          # Enable/disable colors
  progress_bars: true   # Show progress indicators
```

## Advanced Configuration

### Multiple Placeholders

```yaml
placeholders:
  proj: "${project.code}"
  site: "SITE{:03d}"
  patient: "P{:04d}"
  visit: "V{:02d}"
  date: "${datetime.now().strftime('%Y%m%d')}"
  time: "${datetime.now().strftime('%H%M%S')}"
```

### Complex Sections

```yaml
sections:
  - name: "01_data_import"
    description: "Import and validate raw data"
    inputs:
      - "{proj}_{site}_{patient}_raw.csv"
      - "{proj}_{site}_metadata.json"
    outputs:
      - "{proj}_{site}_{patient}_validated.csv"
      - "{proj}_{site}_import_report.pdf"
    dependencies: []
    
  - name: "02_preprocessing"
    description: "Clean and preprocess data"
    inputs:
      - "{proj}_{site}_{patient}_validated.csv"
    outputs:
      - "{proj}_{site}_{patient}_cleaned.csv"
      - "{proj}_{site}_preprocessing_log.txt"
    dependencies: ["01_data_import"]
```

## Environment Variables

LDA supports environment variables in configuration:

```yaml
project:
  analyst: "${USER}"
  root_folder: "${PROJECT_ROOT}"
```

## Configuration Inheritance

Create a base configuration:

```yaml
# base_config.yaml
logging:
  level: "INFO"
display:
  style: "conservative"
```

Extend in project configuration:

```yaml
# lda_config.yaml
extends: "base_config.yaml"
project:
  name: "My Project"
  code: "MP2024"
```

## Best Practices

1. **Use meaningful section names**: Number sections for clear workflow
2. **Define all placeholders**: Avoid hardcoding values
3. **Document complex patterns**: Add comments for clarity
4. **Version control config**: Track configuration changes
5. **Use consistent formatting**: Maintain readability

## Examples

### Research Project

```yaml
project:
  name: "Climate Data Analysis"
  code: "CDA2024"
  analyst: "Dr. Jane Smith"

placeholders:
  proj: "${project.code}"
  year: "2024"
  region: "northeast"

sections:
  - name: "01_data_collection"
    inputs:
      - "{proj}_{region}_temperature_{year}.csv"
      - "{proj}_{region}_precipitation_{year}.csv"
    outputs:
      - "{proj}_{region}_combined_{year}.csv"
      
  - name: "02_analysis"
    inputs:
      - "{proj}_{region}_combined_{year}.csv"
    outputs:
      - "{proj}_{region}_trends_{year}.pdf"
      - "{proj}_{region}_statistics_{year}.xlsx"
```

### Clinical Trial

```yaml
project:
  name: "Drug Efficacy Study"
  code: "DES2024"
  analyst: "Clinical Team"

placeholders:
  proj: "${project.code}"
  phase: "phase3"
  site: "SITE{:03d}"

sections:
  - name: "01_enrollment"
    inputs:
      - "{proj}_{phase}_{site}_screening.csv"
    outputs:
      - "{proj}_{phase}_{site}_enrolled.csv"
      
  - name: "02_treatment"
    inputs:
      - "{proj}_{phase}_{site}_enrolled.csv"
      - "{proj}_{phase}_{site}_dosing.csv"
    outputs:
      - "{proj}_{phase}_{site}_outcomes.csv"
      - "{proj}_{phase}_{site}_adverse_events.csv"
```