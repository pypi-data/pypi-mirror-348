"""Main scaffold generator for LDA projects."""

import os
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional

from ..config import LDAConfig
from .manifest import LDAManifest
from .tracking import FileTracker
from .errors import ScaffoldError, MissingPlaceholderError


class LDAScaffold:
    """Main scaffold generator for LDA projects."""
    
    def __init__(self, config: LDAConfig):
        """Initialize with configuration."""
        self.config = config
        self.project_root = Path(config.get("project.root_folder", "."))
        self.project_code = config.get("project.code", "PROJ")
        
        # Create project root if needed
        self.project_folder = self.project_root / self.project_code
        self.project_folder.mkdir(parents=True, exist_ok=True)
        
        # Initialize manifest
        self.manifest = LDAManifest(str(self.project_folder))
        self.file_tracker = FileTracker()
        
        # Track created items
        self.created_sections = []
        self.created_files = []
    
    def create_project(self) -> Dict[str, Any]:
        """Create the complete project structure."""
        start_time = datetime.now()
        
        try:
            # Initialize project in manifest
            self.manifest.init_project({
                "name": self.config.get("project.name"),
                "code": self.config.get("project.code"),
                "analyst": self.config.get("project.analyst")
            })
            
            # Create sections
            sections = self.config.get("sections", [])
            for section_config in sections:
                self.create_section(section_config)
            
            # Create playground if enabled
            if self.config.get("project.create_playground", True):
                self.create_playground()
            
            # Create sandbox sections
            sandbox_items = self.config.get("sandbox", [])
            if sandbox_items:
                self.create_sandbox(sandbox_items)
            
            # Create project-level files
            self.create_project_files()
            
            # Log project creation
            self.manifest.add_history("project_created", {
                "sections": len(self.created_sections),
                "files": len(self.created_files),
                "duration": (datetime.now() - start_time).total_seconds()
            })
            
            return {
                "success": True,
                "project_folder": str(self.project_folder),
                "sections": self.created_sections,
                "files": self.created_files,
                "duration": (datetime.now() - start_time).total_seconds()
            }
            
        except Exception as e:
            raise ScaffoldError(f"Failed to create project: {e}")
    
    def create_section(self, section_config: Dict[str, Any]) -> None:
        """Create a single section."""
        section_name = section_config["name"]
        section_folder = self.project_folder / f"{self.project_code}_sec{section_name}"
        
        # Create section directories
        section_folder.mkdir(exist_ok=True)
        (section_folder / "inputs").mkdir(exist_ok=True)
        (section_folder / "outputs").mkdir(exist_ok=True)
        (section_folder / "logs").mkdir(exist_ok=True)
        
        # Generate provenance ID
        provenance_id = self.file_tracker.generate_provenance_id(section_name)
        
        # Add section to manifest
        self.manifest.add_section(section_name, {
            "folder": str(section_folder.relative_to(self.project_folder)),
            "inputs": section_config.get("inputs", []),
            "outputs": section_config.get("outputs", [])
        }, provenance_id)
        
        # Create placeholder files
        self._create_section_files(section_folder, section_config, section_name)
        
        # Create section README
        self._create_section_readme(section_folder, section_name, provenance_id)
        
        # Create run scripts based on language preference
        language = self.config.get("project.language", "python")
        if language in ["python", "both"]:
            self._create_run_script(section_folder, section_name)
        if language in ["r", "both"]:
            self._create_run_r_script(section_folder, section_name)
        
        self.created_sections.append({
            "name": section_name,
            "folder": str(section_folder),
            "provenance_id": provenance_id,
            "input_count": len(section_config.get("inputs", [])),
            "output_count": len(section_config.get("outputs", []))
        })
    
    def _create_section_files(self, section_folder: Path, section_config: Dict[str, Any], 
                            section_name: str) -> None:
        """Create placeholder files for a section."""
        # Get available placeholders
        placeholders = self.config.get("placeholders", {})
        
        # Add default project placeholder
        if "proj" not in placeholders:
            placeholders["proj"] = self.project_code
        
        # Create input files
        inputs = section_config.get("inputs", [])
        for pattern in inputs:
            self._create_file_from_pattern(
                section_folder / "inputs", 
                pattern, 
                placeholders, 
                section_name, 
                "input"
            )
        
        # Create output files
        outputs = section_config.get("outputs", [])
        for pattern in outputs:
            self._create_file_from_pattern(
                section_folder / "outputs", 
                pattern, 
                placeholders, 
                section_name, 
                "output"
            )
    
    def _create_file_from_pattern(self, directory: Path, pattern: str, 
                                placeholders: Dict[str, str], section_name: str, 
                                file_type: str) -> None:
        """Create a file from a pattern."""
        # Find required placeholders
        required_placeholders = re.findall(r"\{([^}]+)\}", pattern)
        missing = [p for p in required_placeholders if p not in placeholders]
        
        if missing:
            raise MissingPlaceholderError(missing, pattern, section_name)
        
        # Expand pattern using config's placeholder expansion
        try:
            filename = self.config.expand_placeholders(pattern)
        except KeyError as e:
            raise MissingPlaceholderError([str(e).strip("'")], pattern, section_name)
        
        # Create file
        filepath = directory / filename
        filepath.touch()
        
        # Track file in manifest
        self.manifest.track_file(
            section_name, 
            file_type, 
            filename,
            {"pattern": pattern}
        )
        
        self.created_files.append({
            "path": str(filepath),
            "section": section_name,
            "type": file_type,
            "pattern": pattern
        })
    
    def create_sandbox(self, sandbox_items: List[str]) -> None:
        """Create sandbox sections."""
        sandbox_folder = self.project_folder / f"{self.project_code}_sec_sandbox"
        sandbox_folder.mkdir(exist_ok=True)
        
        for item in sandbox_items:
            item_folder = sandbox_folder / item
            item_folder.mkdir(exist_ok=True)
            
            # Create draft file
            draft_file = item_folder / f"{item}_draft.md"
            draft_file.touch()
            
            self.created_files.append({
                "path": str(draft_file),
                "section": "sandbox",
                "type": "sandbox",
                "pattern": None
            })
    
    def _create_section_readme(self, section_folder: Path, section_name: str, 
                             provenance_id: str) -> None:
        """Create README for a section."""
        readme_content = f"""# Section {section_name}

Created: {datetime.now().isoformat()}
Provenance ID: {provenance_id}
Analyst: {self.config.get("project.analyst", "Unknown")}

## Purpose

This folder contains analysis for section {section_name}.

## Files

See .lda/manifest.json for complete file tracking.
"""
        
        readme_path = section_folder / "README.md"
        readme_path.write_text(readme_content)
    
    def _create_run_script(self, section_folder: Path, section_name: str) -> None:
        """Create run.py script for a section."""
        run_content = f'''#!/usr/bin/env python3
"""
Section {section_name} Analysis Script
Project: {self.config.get("project.name", "LDA Project")}
Created: {datetime.now().isoformat()}
"""

import os
import sys
import json
import logging
from datetime import datetime
from pathlib import Path

# Set up logging
log_dir = Path(__file__).parent / "logs"
log_dir.mkdir(exist_ok=True)
log_file = log_dir / f"run_{{datetime.now().strftime('%Y%m%d_%H%M%S')}}.log"

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

def main():
    """Main analysis function for Section {section_name}."""
    logger.info(f"Starting analysis for Section {section_name}")
    
    # Define paths
    inputs_dir = Path(__file__).parent / "inputs"
    outputs_dir = Path(__file__).parent / "outputs"
    outputs_dir.mkdir(exist_ok=True)
    
    # TODO: Add your analysis code here
    logger.info("Analysis placeholder - add your code here")
    
    # Example: List input files
    if inputs_dir.exists():
        input_files = list(inputs_dir.glob("*"))
        logger.info(f"Found {{len(input_files)}} input files")
        for f in input_files:
            logger.info(f"  - {{f.name}}")
    
    logger.info("Analysis complete")

if __name__ == "__main__":
    main()
'''
        
        run_path = section_folder / "run.py"
        run_path.write_text(run_content)
        
        # Make executable on Unix systems
        os.chmod(run_path, 0o755)
        
        self.created_files.append({
            "path": str(run_path),
            "section": section_name,
            "type": "script",
            "pattern": None
        })
    
    def create_project_files(self) -> None:
        """Create project-level files."""
        # Create main README
        readme_content = f"""# {self.config.get("project.name", "LDA Project")}

Project Code: {self.project_code}
Created: {datetime.now().isoformat()}
Analyst: {self.config.get("project.analyst", "Unknown")}

## Overview

This project was created using the Linked Document Analysis (LDA) system.

## Structure

"""
        
        for section in self.created_sections:
            readme_content += f"- `{section['name']}`: {section['folder']}\n"
        
        readme_content += """

## Provenance

All files are tracked in `.lda/manifest.json`. Use `lda status` to check project status.
"""
        
        readme_path = self.project_folder / "README.md"
        readme_path.write_text(readme_content)
    
    def validate_placeholders(self, pattern: str, available_placeholders: Dict[str, str]) -> List[str]:
        """Validate placeholder usage in patterns."""
        required_placeholders = re.findall(r"\{([^}]+)\}", pattern)
        missing = [p for p in required_placeholders if p not in available_placeholders]
        return missing
    
    def expand_pattern(self, pattern: str, placeholders: Dict[str, str]) -> str:
        """Expand pattern with placeholder values."""
        try:
            return pattern.format(**placeholders)
        except KeyError as e:
            raise MissingPlaceholderError([str(e).strip("'")], pattern)
    
    def create_playground(self) -> None:
        """Create the LDA playground directory."""
        playground_folder = self.project_folder / "lda_playground"
        playground_folder.mkdir(exist_ok=True)
        
        # Create subdirectories
        (playground_folder / "experiments").mkdir(exist_ok=True)
        (playground_folder / "scratch").mkdir(exist_ok=True)
        (playground_folder / "notebooks").mkdir(exist_ok=True)
        
        # Create README
        readme_content = f"""# LDA Playground

This directory is for exploratory work, testing ideas, and experiments that aren't yet part of the formal analysis pipeline.

## Directory Structure

- `experiments/`: Exploratory analyses that might become formal sections
- `scratch/`: Temporary work and quick tests
- `notebooks/`: Jupyter notebooks for exploration

## Guidelines

- Work in this directory is not tracked in the main manifest
- Use this space to test approaches before formalizing them in sections
- Consider moving successful experiments to formal sections

Created: {datetime.now().isoformat()}
Project: {self.config.get("project.name", "LDA Project")}
"""
        readme_path = playground_folder / "README.md"
        readme_path.write_text(readme_content)
        
        # Create example scripts
        language = self.config.get("project.language", "python")
        if language in ["python", "both"]:
            self._create_playground_python_example(playground_folder)
        if language in ["r", "both"]:
            self._create_playground_r_example(playground_folder)
    
    def _create_playground_python_example(self, playground_folder: Path) -> None:
        """Create example Python script for playground."""
        example_content = f"""#!/usr/bin/env python3
\"\"\"
Example playground script for exploring data and testing ideas
Project: {self.config.get("project.name", "LDA Project")}
Created: {datetime.now().isoformat()}
\"\"\"

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# Example: Load some data and explore
def explore_data():
    \"\"\"Example function to explore data.\"\"\"
    # Find project root by looking for manifest
    current = Path(__file__).resolve()
    while current.parent != current:
        if (current / '.lda_manifest.csv').exists():
            project_root = current
            break
        current = current.parent
    else:
        print("Could not find project root")
        return
    
    print(f"Project root: {{project_root}}")
    
    # TODO: Add your exploration code here
    print("Add your data exploration code here")

if __name__ == "__main__":
    explore_data()
"""
        example_path = playground_folder / "example_exploration.py"
        example_path.write_text(example_content)
        os.chmod(example_path, 0o755)
    
    def _create_playground_r_example(self, playground_folder: Path) -> None:
        """Create example R script for playground."""
        example_content = f"""#!/usr/bin/env Rscript
# Example playground script for exploring data and testing ideas
# Project: {self.config.get("project.name", "LDA Project")}
# Created: {datetime.now().isoformat()}

library(tidyverse)

# Example: Load some data and explore
explore_data <- function() {{
  # Find project root by looking for manifest
  current_dir <- getwd()
  while (current_dir != dirname(current_dir)) {{
    if (file.exists(file.path(current_dir, ".lda_manifest.csv"))) {{
      project_root <- current_dir
      break
    }}
    current_dir <- dirname(current_dir)
  }}
  
  cat("Project root:", project_root, "\\n")
  
  # TODO: Add your exploration code here
  cat("Add your data exploration code here\\n")
}}

# Run the exploration
explore_data()
"""
        example_path = playground_folder / "example_exploration.R"
        example_path.write_text(example_content)
        os.chmod(example_path, 0o755)
    
    def _create_run_r_script(self, section_folder: Path, section_name: str) -> None:
        """Create run.R script for a section."""
        run_content = f'''#!/usr/bin/env Rscript
# Section {section_name} Analysis Script
# Project: {self.config.get("project.name", "LDA Project")}
# Created: {datetime.now().isoformat()}

library(tidyverse)
library(here)
library(logger)

# Set up logging
log_dir <- file.path(here(), "logs")
dir.create(log_dir, showWarnings = FALSE)
log_file <- file.path(log_dir, paste0("run_", format(Sys.time(), "%Y%m%d_%H%M%S"), ".log"))

log_appender(appender_file(log_file))
log_threshold(INFO)

#' Main analysis function for Section {section_name}
main <- function() {{
  log_info("Starting analysis for Section {section_name}")
  
  # Define paths
  inputs_dir <- file.path(here(), "inputs")
  outputs_dir <- file.path(here(), "outputs")
  dir.create(outputs_dir, showWarnings = FALSE)
  
  # TODO: Add your analysis code here
  log_info("Analysis placeholder - add your code here")
  
  # Example: List input files
  if (dir.exists(inputs_dir)) {{
    input_files <- list.files(inputs_dir, full.names = TRUE)
    log_info(paste("Found", length(input_files), "input files"))
    for (f in input_files) {{
      log_info(paste("  -", basename(f)))
    }}
  }}
  
  log_info("Analysis complete")
}}

# Run if executed as script
if (!interactive()) {{
  main()
}}
'''
        
        run_path = section_folder / "run.R"
        run_path.write_text(run_content)
        
        # Make executable on Unix systems
        os.chmod(run_path, 0o755)
        
        self.created_files.append({
            "path": str(run_path),
            "section": section_name,
            "type": "script",
            "pattern": None
        })