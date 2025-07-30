"""CLI command implementations for LDA package."""

import os
import json
from pathlib import Path
from typing import Optional

from ..config import LDAConfig
from ..core.scaffold import LDAScaffold
from ..core.manifest import LDAManifest
from ..display.console import Console
from .utils import find_project_root
from .commands_docs import DocsCommands


class Commands:
    """CLI command implementations."""
    
    @staticmethod
    def cmd_init(args, config: Optional[LDAConfig], display: Console) -> int:
        """Initialize new LDA project."""
        display.header("LDA Project Initialization")
        
        # Find or create configuration
        if not config:
            config_file = Path("lda_config.yaml")
            
            if config_file.exists():
                config = LDAConfig(str(config_file))
            else:
                # Create default config
                config = LDAConfig()
            
            # Update with command line arguments (for both new and existing configs)
            if args.name:
                config.set("project.name", args.name)
                # Create project code from name - sanitize for filesystem
                import re
                project_code = re.sub(r'[^\w\s-]', '', args.name.lower())  # Remove special chars
                project_code = re.sub(r'[-\s]+', '_', project_code)  # Replace spaces/dashes with underscore
                project_code = project_code.strip('_')  # Remove leading/trailing underscores
                config.set("project.code", project_code)
            if args.analyst:
                config.set("project.analyst", args.analyst)
            
            # Add default sections if none exist
            if not config.get("sections"):
                default_sections = [
                    {
                        "name": "01",
                        "inputs": [],
                        "outputs": []
                    },
                    {
                        "name": "02",
                        "inputs": [],
                        "outputs": []
                    },
                    {
                        "name": "03",
                        "inputs": [],
                        "outputs": []
                    }
                ]
                config.set("sections", default_sections)
            
            # Save config file
            config.save(str(config_file))
            display.success(f"Updated configuration file: {config_file}")
        
        # Create scaffold
        try:
            scaffold = LDAScaffold(config)
            result = scaffold.create_project()
            
            display.success(f"Project created at: {result['project_folder']}")
            display.info(f"Sections created: {result['sections']}")
            display.info(f"Files created: {len(result['files'])}")
            display.info(f"Time taken: {result['duration']:.2f}s")
            
            return 0
            
        except Exception as e:
            display.error(f"Failed to create project: {e}")
            return 1
    
    @staticmethod
    def cmd_status(args, config: Optional[LDAConfig], display: Console) -> int:
        """Show project status."""
        project_root = find_project_root()
        
        if not project_root:
            display.error("No LDA project found in current directory")
            return 1
        
        try:
            manifest = LDAManifest(project_root)
            status = manifest.get_project_status()
            
            if args.format == "json":
                print(json.dumps(status, indent=2))
            else:
                display.header("Project Status")
                
                # Project info
                display.section("Project Information")
                display.list_items([
                    f"Name: {status['project'].get('name', 'Unknown')}",
                    f"Code: {status['project'].get('code', 'Unknown')}",
                    f"Analyst: {status['project'].get('analyst', 'Unknown')}",
                    f"Created: {status['project'].get('created', 'Unknown')}",
                    f"Root: {status['project'].get('root', 'Unknown')}"
                ])
                
                # Summary
                display.section("Summary")
                display.list_items([
                    f"Sections: {status['sections']}",
                    f"Total files: {status['files']['total']}",
                    f"Input files: {status['files']['inputs']}",
                    f"Output files: {status['files']['outputs']}",
                    f"Last activity: {status.get('last_activity', 'Never')}"
                ])
                
                # Sections detail
                display.section("Sections")
                for section_name, section_info in manifest.manifest["sections"].items():
                    display.list_items([
                        f"{section_name}:",
                        f"  Folder: {section_info['folder']}",
                        f"  Created: {section_info['created']}",
                        f"  Provenance: {section_info['provenance_id']}"
                    ])
            
            return 0
            
        except Exception as e:
            display.error(f"Failed to get status: {e}")
            return 1
    
    @staticmethod
    def cmd_track(args, config: Optional[LDAConfig], display: Console) -> int:
        """Track files in manifest."""
        project_root = find_project_root()
        
        if not project_root:
            display.error("No LDA project found")
            return 1
        
        try:
            manifest = LDAManifest(project_root)
            
            # Track file
            manifest.track_file(
                section=args.section,
                file_type=args.type,
                filename=os.path.basename(args.file)
            )
            
            display.success(f"Tracked {args.type} file: {args.file}")
            return 0
            
        except Exception as e:
            display.error(f"Failed to track file: {e}")
            return 1
    
    @staticmethod
    def cmd_changes(args, config: Optional[LDAConfig], display: Console) -> int:
        """Show file changes."""
        project_root = find_project_root()
        
        if not project_root:
            display.error("No LDA project found")
            return 1
        
        try:
            manifest = LDAManifest(project_root)
            changes = manifest.detect_changes(section=args.section)
            
            display.header("File Changes")
            
            if not any(changes.values()):
                display.info("No changes detected")
            else:
                if changes["new"]:
                    display.section("New Files")
                    display.list_items(changes["new"])
                
                if changes["modified"]:
                    display.section("Modified Files")
                    display.list_items(changes["modified"])
                
                if changes["deleted"]:
                    display.section("Deleted Files")
                    display.list_items(changes["deleted"])
            
            return 0
            
        except Exception as e:
            display.error(f"Failed to check changes: {e}")
            return 1
    
    @staticmethod
    def cmd_history(args, config: Optional[LDAConfig], display: Console) -> int:
        """Show project history."""
        project_root = find_project_root()
        
        if not project_root:
            display.error("No LDA project found")
            return 1
        
        try:
            manifest = LDAManifest(project_root)
            history = manifest.get_history(limit=args.limit)
            
            display.header(f"Project History (last {args.limit} entries)")
            
            for entry in reversed(history):
                display.section(entry["timestamp"])
                display.list_items([
                    f"Action: {entry['action']}",
                    f"Details: {json.dumps(entry['details'], indent=2)}"
                ])
            
            return 0
            
        except Exception as e:
            display.error(f"Failed to get history: {e}")
            return 1
    
    @staticmethod
    def cmd_validate(args, config: Optional[LDAConfig], display: Console) -> int:
        """Validate project structure."""
        project_root = find_project_root()
        
        if not project_root:
            display.error("No LDA project found")
            return 1
        
        display.header("Project Validation")
        
        issues = []
        
        try:
            # Check manifest
            manifest = LDAManifest(project_root)
            
            # Check configuration
            if config:
                config.validate()
            
            # Check sections exist
            for section_name, section_info in manifest.manifest["sections"].items():
                section_path = Path(project_root) / section_info["folder"]
                
                if not section_path.exists():
                    issues.append(f"Section folder missing: {section_path}")
                else:
                    # Check subdirectories
                    if not (section_path / "inputs").exists():
                        issues.append(f"Inputs folder missing: {section_path}/inputs")
                    if not (section_path / "outputs").exists():
                        issues.append(f"Outputs folder missing: {section_path}/outputs")
            
            # Check tracked files
            for file_key, file_info in manifest.manifest["files"].items():
                file_path = Path(project_root) / file_info["path"]
                
                if not file_path.exists():
                    issues.append(f"Tracked file missing: {file_path}")
            
            if issues:
                display.section("Issues Found")
                display.list_items(issues)
                
                if args.fix:
                    display.section("Attempting Fixes")
                    
                    for issue in issues:
                        if "folder missing" in issue:
                            # Create missing folders
                            folder_path = issue.split(": ")[1]
                            Path(folder_path).mkdir(parents=True, exist_ok=True)
                            display.success(f"Created: {folder_path}")
                
                return 1
            else:
                display.success("No issues found")
                return 0
            
        except Exception as e:
            display.error(f"Validation failed: {e}")
            return 1
    
    @staticmethod
    def cmd_export(args, config: Optional[LDAConfig], display: Console) -> int:
        """Export manifest or reports."""
        project_root = find_project_root()
        
        if not project_root:
            display.error("No LDA project found")
            return 1
        
        try:
            manifest = LDAManifest(project_root)
            
            if args.type == "manifest":
                if args.format == "csv":
                    manifest.export_to_csv(args.output)
                elif args.format == "json":
                    with open(args.output, 'w') as f:
                        json.dump(manifest.manifest, f, indent=2)
                else:
                    display.error(f"Unsupported format: {args.format}")
                    return 1
            
            elif args.type == "report":
                # Generate report (to be implemented)
                display.error("Report generation not yet implemented")
                return 1
            
            display.success(f"Exported to: {args.output}")
            return 0
            
        except Exception as e:
            display.error(f"Export failed: {e}")
            return 1
    
    @staticmethod
    def cmd_docs(args, config: Optional[LDAConfig], display: Console) -> int:
        """Documentation commands."""
        docs_commands = DocsCommands()
        
        # Handle subcommands
        if args.docs_command == "serve":
            return docs_commands.serve(
                port=args.port if hasattr(args, 'port') else 8000,
                dev=args.dev if hasattr(args, 'dev') else False
            )
        elif args.docs_command == "build":
            return docs_commands.build(
                output=args.output if hasattr(args, 'output') else 'site',
                strict=args.strict if hasattr(args, 'strict') else False,
                clean=args.clean if hasattr(args, 'clean') else False
            )
        else:
            display.error(f"Unknown docs command: {args.docs_command}")
            return 1