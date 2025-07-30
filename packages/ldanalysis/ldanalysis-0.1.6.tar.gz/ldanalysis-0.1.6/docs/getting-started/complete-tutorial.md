# Complete LDA Tutorial

This comprehensive tutorial will walk you through every feature of LDA with hands-on examples. By the end, you'll have mastered all aspects of the Linked Document Analysis system.

## Prerequisites

Before starting, ensure you have:
- Python 3.8 or higher installed
- LDA installed (`pip install ldanalysis`)
- A terminal or command prompt
- About 30 minutes to complete the tutorial

## Tutorial Project Overview

We'll create a research project analyzing climate data across multiple cities. This project will demonstrate:
- Project initialization and configuration
- Document section creation
- File tracking and provenance
- Multi-analyst collaboration
- Change management
- Report generation
- Advanced workflows

## Part 1: Project Setup

### Step 1: Create Project Directory

```bash
# Create and enter project directory
mkdir climate_analysis
cd climate_analysis
```

### Step 2: Initialize LDA Project

```bash
# Initialize with project details
lda init --name "Climate Analysis 2024" --analyst "jane.doe"
```

Expected output:
```
✨ Initializing LDA project...
✓ Created lda_config.yaml
✓ Created project structure
✓ Project "Climate Analysis 2024" initialized successfully!
```

### Step 3: Examine Project Structure

```bash
# View the created configuration
cat lda_config.yaml
```

You should see:
```yaml
project:
  name: Climate Analysis 2024
  code: CA2024
  analyst: jane.doe
  created: 2024-05-17

sections: []
```

## Part 2: Creating Document Sections

### Step 4: Define Project Sections

Let's create sections for our analysis workflow:

```bash
# Create data collection section
lda create section --id sec01_data --name "Data Collection"

# Create preprocessing section
lda create section --id sec02_preprocessing --name "Data Preprocessing"

# Create analysis section
lda create section --id sec03_analysis --name "Statistical Analysis"

# Create visualization section
lda create section --id sec04_viz --name "Visualizations"
```

### Step 5: View Project Status

```bash
lda status
```

Expected output:
```
📊 Project Status: Climate Analysis 2024
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Sections: 4
├── sec01_data (Data Collection)
├── sec02_preprocessing (Data Preprocessing)
├── sec03_analysis (Statistical Analysis)
└── sec04_viz (Visualizations)

Files Tracked: 0
Total Size: 0 bytes
Last Modified: Just now
```

## Part 3: Working with Files

### Step 6: Add Data Files

```bash
# Navigate to data section
cd sec01_data

# Create sample data files
echo "city,date,temperature,humidity
NYC,2024-01-01,32,65
NYC,2024-01-02,35,70
LA,2024-01-01,68,45
LA,2024-01-02,72,40" > climate_data.csv

echo "# Data Sources
- NOAA Climate Database
- Local Weather Stations
- Satellite Measurements" > data_sources.md
```

### Step 7: Track Files

```bash
# Track the files
lda track --message "Initial data import"
```

Expected output:
```
🔍 Tracking files in sec01_data...
✓ Added: climate_data.csv (91 bytes)
✓ Added: data_sources.md (78 bytes)
✓ 2 files tracked successfully
```

### Step 8: View File Details

```bash
# Check tracking details
lda changes
```

## Part 4: Data Processing Workflow

### Step 9: Create Processing Script

```bash
# Move to preprocessing section
cd ../sec02_preprocessing

# Create a preprocessing script
cat > preprocess.py << 'EOF'
import pandas as pd
import os

# Read raw data
input_file = "../sec01_data/climate_data.csv"
output_file = "outputs/cleaned_data.csv"

# Create output directory
os.makedirs("outputs", exist_ok=True)

# Process data
df = pd.read_csv(input_file)
df['temperature_c'] = (df['temperature'] - 32) * 5/9
df['date'] = pd.to_datetime(df['date'])

# Save cleaned data
df.to_csv(output_file, index=False)
print(f"Processed {len(df)} records")
EOF
```

### Step 10: Run Processing

```bash
# Execute the preprocessing
python preprocess.py

# Track the results
lda track --message "Preprocessed climate data"
```

## Part 5: Analysis and Visualization

### Step 11: Perform Analysis

```bash
# Move to analysis section
cd ../sec03_analysis

# Create analysis script
cat > analyze.py << 'EOF'
import pandas as pd
import json

# Load preprocessed data
df = pd.read_csv("../sec02_preprocessing/outputs/cleaned_data.csv")

# Calculate statistics
stats = {
    "cities": df['city'].unique().tolist(),
    "date_range": {
        "start": df['date'].min(),
        "end": df['date'].max()
    },
    "temperature_stats": {
        "mean": df['temperature_c'].mean(),
        "std": df['temperature_c'].std(),
        "min": df['temperature_c'].min(),
        "max": df['temperature_c'].max()
    }
}

# Save results
with open("outputs/analysis_results.json", "w") as f:
    json.dump(stats, f, indent=2, default=str)

print("Analysis complete!")
EOF

# Create output directory and run
mkdir -p outputs
python analyze.py

# Track results
lda track --message "Statistical analysis complete"
```

### Step 12: Create Visualizations

```bash
# Move to visualization section
cd ../sec04_viz

# Create a simple visualization script
cat > visualize.py << 'EOF'
import pandas as pd
import matplotlib.pyplot as plt

# Load data
df = pd.read_csv("../sec02_preprocessing/outputs/cleaned_data.csv")

# Create temperature plot
plt.figure(figsize=(10, 6))
for city in df['city'].unique():
    city_data = df[df['city'] == city]
    plt.plot(city_data['date'], city_data['temperature_c'], 
             marker='o', label=city)

plt.xlabel('Date')
plt.ylabel('Temperature (°C)')
plt.title('Temperature Trends by City')
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('outputs/temperature_trends.png')
print("Visualization saved!")
EOF

# Create directory and run
mkdir -p outputs
python visualize.py

# Track the output
lda track --message "Created temperature visualization"
```

## Part 6: Managing Changes

### Step 13: Modify Data and Track Changes

```bash
# Go back to data section
cd ../sec01_data

# Add more data
echo "NYC,2024-01-03,30,68
LA,2024-01-03,70,42" >> climate_data.csv

# Check what changed
lda changes
```

Expected output:
```
📝 File Changes in sec01_data
━━━━━━━━━━━━━━━━━━━━━━━━━━━

Modified Files:
  ~ climate_data.csv
    Size: 91 → 135 bytes
    Modified: 2 minutes ago
```

### Step 14: Track Changes

```bash
# Track the modifications
lda track --message "Added January 3rd data"

# View history
lda history
```

## Part 7: Collaboration Features

### Step 15: Add Another Analyst

```bash
# Return to project root
cd ..

# Modify config to add analyst
lda config set project.analysts "jane.doe,john.smith"

# Assign section to different analyst
lda assign sec03_analysis --analyst john.smith
```

### Step 16: View Analyst Activity

```bash
# See who worked on what
lda history --analyst jane.doe
lda history --analyst john.smith
```

## Part 8: Validation and Quality Control

### Step 17: Validate Project Integrity

```bash
# Run validation
lda validate
```

Expected output:
```
🔍 Validating project integrity...
✓ Configuration valid
✓ All manifests valid
✓ No missing files
✓ No hash mismatches
✓ Project structure intact
```

### Step 18: Fix Any Issues

```bash
# If there were issues, fix them
lda validate --fix
```

## Part 9: Reporting

### Step 19: Generate Project Report

```bash
# Generate comprehensive report
lda export report --format html --output project_report.html

# Export manifest as CSV
lda export manifest --format csv --output file_manifest.csv
```

### Step 20: View Section Summary

```bash
# Get detailed section information
lda status --detailed
```

## Part 10: Advanced Features

### Step 21: Working with Templates

```bash
# Save current project as template
lda template save --name "climate_research"

# List available templates
lda template list
```

### Step 22: Bulk Operations

```bash
# Track all sections at once
lda track --all --message "End of day sync"

# Validate all sections
lda validate --all
```

### Step 23: Search Functionality

```bash
# Search for files containing "temperature"
lda search "temperature"

# Find all CSV files
lda search --pattern "*.csv"
```

## Part 11: Integration Examples

### Step 24: Git Integration

```bash
# Initialize git repository
git init

# Add LDA-specific gitignore
echo "*.pyc
__pycache__/
.DS_Store
*.log
lda_sandbox/
" > .gitignore

# Commit with LDA tracking
lda track --all --message "Final state before commit"
git add .
git commit -m "Complete climate analysis project"
```

### Step 25: Export for Archive

```bash
# Create archive-ready package
lda export archive --output climate_analysis_archive.zip
```

## Part 12: Best Practices Demo

### Step 26: Document Your Work

```bash
# Create project documentation
cat > README.md << 'EOF'
# Climate Analysis Project

This project analyzes temperature and humidity data across multiple cities.

## Sections

- `sec01_data`: Raw climate data
- `sec02_preprocessing`: Data cleaning and transformation
- `sec03_analysis`: Statistical analysis
- `sec04_viz`: Visualizations and charts

## Usage

1. Run preprocessing: `cd sec02_preprocessing && python preprocess.py`
2. Run analysis: `cd sec03_analysis && python analyze.py`
3. Generate visualizations: `cd sec04_viz && python visualize.py`

## LDA Commands

- Track changes: `lda track --message "description"`
- View status: `lda status`
- Export report: `lda export report --format html --output report.html`
EOF

# Track the documentation
lda track README.md --message "Added project documentation"
```

## Part 13: Troubleshooting

### Step 27: Debug Commands

```bash
# Check for issues
lda debug check

# View detailed logs
lda --verbose status

# Get help for any command
lda track --help
```

## Part 14: Cleanup and Maintenance

### Step 28: Clean Temporary Files

```bash
# Clean up temporary files
lda clean --temp

# Remove orphaned entries
lda clean --orphaned
```

### Step 29: Backup Project

```bash
# Create full backup
lda backup create --output backups/

# List backups
lda backup list
```

## Part 15: Final Review

### Step 30: Complete Project Summary

```bash
# Generate final summary
lda summary

# View complete project tree
lda tree
```

Expected final output:
```
🌳 Climate Analysis 2024
├── 📁 sec01_data (2 files, 213 bytes)
│   ├── climate_data.csv
│   └── data_sources.md
├── 📁 sec02_preprocessing (2 files, 478 bytes)
│   ├── preprocess.py
│   └── outputs/
│       └── cleaned_data.csv
├── 📁 sec03_analysis (2 files, 892 bytes)
│   ├── analyze.py
│   └── outputs/
│       └── analysis_results.json
└── 📁 sec04_viz (2 files, 1.2 KB)
    ├── visualize.py
    └── outputs/
        └── temperature_trends.png

Total: 8 files, 2.8 KB
Tracked: All files
Last Update: Just now
```

## Conclusion

Congratulations! You've now used every major feature of LDA:

✅ Project initialization and configuration
✅ Section creation and management
✅ File tracking and provenance
✅ Change detection and history
✅ Multi-analyst collaboration
✅ Validation and quality control
✅ Reporting and export features
✅ Advanced search and bulk operations
✅ Integration with other tools
✅ Backup and maintenance

## Next Steps

1. **Explore Advanced Configuration**: Check the [Configuration Guide](../user-guide/configuration.md)
2. **Learn About Workflows**: Read the [Workflows Documentation](../user-guide/workflows.md)
3. **API Usage**: See the [API Reference](../api-reference/core.md)
4. **Customize for Your Needs**: Review [Templates](../user-guide/templates.md)

## Quick Reference Card

Keep these essential commands handy:

```bash
# Project Management
lda init --name "Project"        # Initialize project
lda status                       # View status
lda tree                         # Show project tree

# Section Management  
lda create section --id sec01    # Create section
lda list sections               # List all sections

# File Tracking
lda track                       # Track current directory
lda track --all                 # Track all sections
lda changes                     # Show changes
lda history                     # Show history

# Validation & Export
lda validate                    # Check integrity
lda export report               # Generate report
lda export manifest             # Export file list

# Search & Info
lda search "pattern"            # Search files
lda info file.txt              # File details
lda help <command>             # Get help
```

Happy tracking! 🚀