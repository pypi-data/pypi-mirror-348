"""Main CLI entry point for LDA package."""

import sys
import argparse
from pathlib import Path
from typing import Optional, List

from .commands import Commands
from .utils import find_project_root, setup_logging
from .docs_command import docs_group
from ..config import LDAConfig
from ..display.console import Console


class LDACLI:
    """Main CLI interface for LDA."""
    
    def __init__(self):
        """Initialize CLI."""
        self.commands = Commands()
        self.display = Console()
        self.parser = self._create_parser()
    
    def _create_parser(self) -> argparse.ArgumentParser:
        """Create argument parser."""
        parser = argparse.ArgumentParser(
            prog="lda",
            description="Linked Document Analysis - Project management and provenance tracking",
            formatter_class=argparse.RawDescriptionHelpFormatter
        )
        
        # Global options
        parser.add_argument(
            "--config", "-c",
            help="Path to configuration file",
            type=str
        )
        
        parser.add_argument(
            "--verbose", "-v",
            help="Enable verbose output",
            action="store_true"
        )
        
        parser.add_argument(
            "--quiet", "-q",
            help="Suppress non-error output",
            action="store_true"
        )
        
        # Create subparsers for commands
        subparsers = parser.add_subparsers(
            dest="command",
            help="Available commands"
        )
        
        # Init command
        init_parser = subparsers.add_parser(
            "init",
            help="Initialize new LDA project"
        )
        init_parser.add_argument(
            "--template", "-t",
            help="Project template to use",
            default="default"
        )
        init_parser.add_argument(
            "--name", "-n",
            help="Project name"
        )
        init_parser.add_argument(
            "--analyst", "-a",
            help="Analyst name"
        )
        
        # Status command
        status_parser = subparsers.add_parser(
            "status",
            help="Show project status"
        )
        status_parser.add_argument(
            "--format", "-f",
            help="Output format (text, json)",
            choices=["text", "json"],
            default="text"
        )
        
        # Track command
        track_parser = subparsers.add_parser(
            "track",
            help="Track files in manifest"
        )
        track_parser.add_argument(
            "file",
            help="File to track"
        )
        track_parser.add_argument(
            "--section", "-s",
            help="Section name",
            required=True
        )
        track_parser.add_argument(
            "--type", "-t",
            help="File type (input/output)",
            choices=["input", "output"],
            required=True
        )
        
        # Changes command
        changes_parser = subparsers.add_parser(
            "changes",
            help="Show file changes"
        )
        changes_parser.add_argument(
            "--section", "-s",
            help="Filter by section"
        )
        
        # History command
        history_parser = subparsers.add_parser(
            "history",
            help="Show project history"
        )
        history_parser.add_argument(
            "--limit", "-l",
            help="Number of entries to show",
            type=int,
            default=10
        )
        
        # Validate command
        validate_parser = subparsers.add_parser(
            "validate",
            help="Validate project structure"
        )
        validate_parser.add_argument(
            "--fix",
            help="Attempt to fix issues",
            action="store_true"
        )
        
        # Export command
        export_parser = subparsers.add_parser(
            "export",
            help="Export manifest or reports"
        )
        export_parser.add_argument(
            "type",
            help="Export type",
            choices=["manifest", "report"]
        )
        export_parser.add_argument(
            "--output", "-o",
            help="Output file",
            required=True
        )
        export_parser.add_argument(
            "--format", "-f",
            help="Output format",
            choices=["csv", "json", "html"],
            default="csv"
        )
        
        # Docs command
        docs_parser = subparsers.add_parser(
            "docs",
            help="Documentation commands"
        )
        
        docs_subparsers = docs_parser.add_subparsers(
            dest="docs_command",
            help="Documentation subcommands"
        )
        
        # Docs serve
        serve_parser = docs_subparsers.add_parser(
            "serve",
            help="Serve documentation locally"
        )
        serve_parser.add_argument(
            "--port", "-p",
            help="Port to serve on",
            type=int,
            default=8000
        )
        serve_parser.add_argument(
            "--dev", "-d",
            help="Enable development mode",
            action="store_true"
        )
        
        # Docs build
        build_parser = docs_subparsers.add_parser(
            "build",
            help="Build documentation site"
        )
        build_parser.add_argument(
            "--output", "-o",
            help="Output directory",
            default="site"
        )
        build_parser.add_argument(
            "--strict", "-s",
            help="Enable strict mode",
            action="store_true"
        )
        build_parser.add_argument(
            "--clean", "-c",
            help="Clean build directory first",
            action="store_true"
        )
        
        return parser
    
    def run(self, args: Optional[List[str]] = None) -> int:
        """Run the CLI."""
        try:
            # Parse arguments
            parsed_args = self.parser.parse_args(args)
            
            # Set up logging
            setup_logging(
                verbose=getattr(parsed_args, 'verbose', False),
                quiet=getattr(parsed_args, 'quiet', False)
            )
            
            # Handle no command
            if not getattr(parsed_args, 'command', None):
                self.parser.print_help()
                return 0
            
            # Load configuration if specified
            config = None
            if getattr(parsed_args, 'config', None):
                config = LDAConfig(parsed_args.config)
            
            # Execute command
            command_func = getattr(self.commands, f"cmd_{parsed_args.command}")
            return command_func(parsed_args, config, self.display)
            
        except KeyboardInterrupt:
            self.display.error("Operation cancelled by user")
            return 130
        
        except Exception as e:
            self.display.error(str(e))
            
            if getattr(parsed_args, 'verbose', False):
                import traceback
                traceback.print_exc()
            
            return 1


def main():
    """Main entry point for CLI."""
    cli = LDACLI()
    sys.exit(cli.run())