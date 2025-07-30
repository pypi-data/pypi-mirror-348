# Your First LDA Project

Let's build a complete project from scratch. We'll create a research documentation project that demonstrates all of LDA's key features.

## Project Overview

We'll create a research project about climate data analysis with:
- Research documentation
- Data files
- Analysis scripts
- Visualizations
- Progress tracking

## Step 1: Create Project Directory

```bash
mkdir climate-research
cd climate-research
```

## Step 2: Initialize with Template

Use the research template for a head start:

```bash
lda init --template research
```

When prompted, enter:
```
Project name: Climate Data Analysis
Project code: CLIMATE
Author: Dr. Jane Smith
Email: jane.smith@university.edu
Organization: Research Lab
```

## Step 3: Explore Generated Structure

LDA creates this structure:

```
climate-research/
├── lda_config.yaml      # Project configuration
├── .lda/               # LDA tracking data
├── docs/               # Documentation
├── data/               # Data files
│   ├── raw/           # Original data
│   └── processed/     # Cleaned data
├── scripts/            # Analysis scripts
├── notebooks/          # Jupyter notebooks
├── results/            # Analysis outputs
└── figures/            # Visualizations
```

## Step 4: Add Research Documents

Create your research documentation:

```bash
# Main research document
cat > docs/protocol.md << 'EOF'
# Climate Data Analysis Protocol

## Research Question
How have temperature patterns changed in urban areas over the past decade?

## Methodology
1. Data Collection: NOAA temperature records
2. Analysis: Time series analysis
3. Visualization: Trend charts and heat maps

## Timeline
- Week 1-2: Data collection
- Week 3-4: Analysis
- Week 5: Report writing
EOF

# Literature review
cat > docs/literature_review.md << 'EOF'
# Literature Review

## Key Studies
1. Smith et al. (2023) - Urban heat island effects
2. Johnson (2022) - Climate change in metropolitan areas
3. Davis & Lee (2021) - Temperature trend analysis

## Research Gaps
- Limited long-term studies
- Need for city-specific analysis
EOF
```

## Step 5: Add Data Files

Create sample data files:

```bash
# Sample temperature data
cat > data/raw/temperature_2023.csv << 'EOF'
date,city,temperature_c,humidity
2023-01-01,New York,2.3,65
2023-01-01,Los Angeles,18.5,55
2023-01-01,Chicago,-5.2,70
2023-01-02,New York,3.1,63
2023-01-02,Los Angeles,19.2,52
2023-01-02,Chicago,-4.8,68
EOF

# Metadata file
cat > data/raw/metadata.json << 'EOF'
{
  "source": "NOAA Climate Data",
  "collection_date": "2024-01-15",
  "units": {
    "temperature": "celsius",
    "humidity": "percent"
  },
  "quality_check": "passed"
}
EOF
```

## Step 6: Create Analysis Scripts

Add a data analysis script:

```bash
cat > scripts/analyze_temperature.py << 'EOF'
#!/usr/bin/env python3
"""Temperature data analysis script."""

import pandas as pd
import matplotlib.pyplot as plt

def load_data(filepath):
    """Load temperature data from CSV."""
    return pd.read_csv(filepath, parse_dates=['date'])

def analyze_trends(df):
    """Analyze temperature trends by city."""
    city_avg = df.groupby('city')['temperature_c'].mean()
    return city_avg.sort_values(ascending=False)

def create_visualization(df):
    """Create temperature visualization."""
    fig, ax = plt.subplots(figsize=(10, 6))
    
    for city in df['city'].unique():
        city_data = df[df['city'] == city]
        ax.plot(city_data['date'], city_data['temperature_c'], 
                marker='o', label=city)
    
    ax.set_xlabel('Date')
    ax.set_ylabel('Temperature (°C)')
    ax.set_title('Temperature Trends by City')
    ax.legend()
    
    plt.tight_layout()
    plt.savefig('figures/temperature_trends.png', dpi=300)
    print("Visualization saved to figures/temperature_trends.png")

if __name__ == "__main__":
    # Load and analyze data
    df = load_data('data/raw/temperature_2023.csv')
    city_averages = analyze_trends(df)
    
    print("Average Temperatures by City:")
    print(city_averages)
    
    # Create visualization
    create_visualization(df)
EOF

chmod +x scripts/analyze_temperature.py
```

## Step 7: Track All Files

Now track your project files:

```bash
lda track --all
```

Output:
```
🔍 Scanning project files...
✅ Tracked: docs/protocol.md
✅ Tracked: docs/literature_review.md
✅ Tracked: data/raw/temperature_2023.csv
✅ Tracked: data/raw/metadata.json
✅ Tracked: scripts/analyze_temperature.py
📊 Summary: 5 files tracked across 3 sections
```

## Step 8: Check Project Status

View your project status:

```bash
lda status --verbose
```

Output:
```
🔬 Climate Data Analysis (CLIMATE)
👤 Author: Dr. Jane Smith
🏢 Organization: Research Lab

📁 Sections:
  Documentation (2 files)
    ├── docs/protocol.md (367 bytes)
    └── docs/literature_review.md (284 bytes)
  
  Data Collection (2 files)
    ├── data/raw/temperature_2023.csv (243 bytes)
    └── data/raw/metadata.json (152 bytes)
  
  Analysis (1 file)
    └── scripts/analyze_temperature.py (823 bytes)

⏱️ Last activity: 2 minutes ago
📊 Total files: 5 (1.87 KB)
```

## Step 9: Create Notebook

Add a Jupyter notebook for interactive analysis:

```bash
# Create notebook directory entry
cat > notebooks/exploratory_analysis.ipynb << 'EOF'
{
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# Climate Data Exploratory Analysis\n",
    "Initial exploration of temperature patterns"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 1,
   "metadata": {},
   "outputs": [],
   "source": [
    "import pandas as pd\n",
    "import seaborn as sns\n",
    "import matplotlib.pyplot as plt\n",
    "\n",
    "# Load data\n",
    "df = pd.read_csv('../data/raw/temperature_2023.csv')"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 4
}
EOF

# Track the notebook
lda track notebooks/exploratory_analysis.ipynb
```

## Step 10: Monitor Changes

Make some changes and track them:

```bash
# Modify the protocol
echo -e "\n## Preliminary Results\nInitial analysis shows warming trend." >> docs/protocol.md

# Check changes
lda changes
```

Output:
```
🔄 Changes detected:
  
  📝 Modified: docs/protocol.md
     Size: 367 → 421 bytes (+54)
     Modified: 10 seconds ago
     Hash: abc123... → def456...
```

## Step 11: Generate Report

Create a project report:

```bash
lda export --format html --output project_report.html
```

This generates a comprehensive report with:
- Project overview
- File inventory
- Change history
- Section summaries
- Visualizations

## Step 12: Set Up Automation

Create a watch configuration:

```bash
cat > .ldarc << 'EOF'
# LDA project configuration
watch:
  enabled: true
  interval: 300  # 5 minutes
  
notifications:
  on_change: true
  summary: daily
  
export:
  auto_export: true
  format: markdown
  schedule: "0 17 * * *"  # Daily at 5 PM
EOF
```

## Working with Your Project

### Daily Workflow

```bash
# Start your day
lda status --today

# Work on files...

# Check changes before lunch
lda changes --since 9am

# End of day summary
lda export --format markdown --output daily_summary.md
```

### Collaboration

Share project state with colleagues:

```bash
# Export project snapshot
lda export --format json --output project_snapshot.json

# Create shareable report
lda export --format pdf --output project_report.pdf
```

### Version Control Integration

LDA works great with Git:

```bash
# Initialize git
git init
git add .
git commit -m "Initial project setup with LDA"

# LDA tracks git commits too
lda status --git
```

## Advanced Features

### Custom Sections

Add a new section for presentations:

```yaml
# Edit lda_config.yaml
sections:
  presentations:
    name: "Conference Presentations"
    type: "outputs"
    files:
      - "presentations/*.pptx"
      - "presentations/*.pdf"
```

### Automated Workflows

```bash
# Run analysis when data changes
lda watch --on-change "python scripts/analyze_temperature.py"

# Generate daily reports
lda schedule export --format pdf --at "6:00 PM"
```

### Integration with Tools

```python
# Python integration
from lda import Project

project = Project(".")
status = project.status()
changes = project.get_changes(since="1 hour ago")
```

## What You've Learned

✅ Project initialization with templates  
✅ File organization and tracking  
✅ Change detection and monitoring  
✅ Report generation and export  
✅ Configuration customization  
✅ Workflow automation  

## Next Steps

Now that you have a working project:

<div class="grid cards" markdown>

-   :material-book-open:{ .lg .middle } __Concepts__

    ---

    Deep dive into LDA concepts
    
    [:octicons-arrow-right-24: Learn more](../user-guide/concepts.md)

-   :material-cog:{ .lg .middle } __Configuration__

    ---

    Advanced configuration options
    
    [:octicons-arrow-right-24: Configure](../user-guide/configuration.md)

-   :material-workflow:{ .lg .middle } __Workflows__

    ---

    Common workflow patterns
    
    [:octicons-arrow-right-24: Explore](../user-guide/workflows.md)

</div>

## Tips & Tricks

!!! tip "Best Practices"
    - Commit your `lda_config.yaml` to version control
    - Use meaningful section names
    - Set up `.ldarc` for project-specific settings
    - Regular exports for backups
    - Integrate with your existing tools

!!! example "Real-World Examples"
    - [Research Paper Project](https://github.com/lda-examples/research-paper)
    - [Software Documentation](https://github.com/lda-examples/software-docs)
    - [Data Analysis Pipeline](https://github.com/lda-examples/data-pipeline)