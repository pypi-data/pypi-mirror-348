"""Documentation commands for LDA CLI."""

import os
import sys
import subprocess
from pathlib import Path

from ..display.console import Console
from ..core.errors import LDAError


class DocsCommands:
    """Documentation-related commands."""
    
    def __init__(self):
        """Initialize documentation commands."""
        self.console = Console()
    
    def serve(self, port: int = 8000, dev: bool = False) -> int:
        """Serve documentation locally.
        
        Args:
            port: Port to serve on
            dev: Enable development mode
            
        Returns:
            Exit code
        """
        # Check if mkdocs is installed
        try:
            import mkdocs
        except ImportError:
            self.console.error("MkDocs not installed. Install with: pip install lda[docs]")
            return 1
        
        # Find project root
        project_root = Path.cwd()
        mkdocs_yml = project_root / 'mkdocs.yml'
        
        # Look for mkdocs.yml in parent directories
        if not mkdocs_yml.exists():
            for parent in project_root.parents:
                if (parent / 'mkdocs.yml').exists():
                    project_root = parent
                    mkdocs_yml = parent / 'mkdocs.yml'
                    break
        
        if not mkdocs_yml.exists():
            self.console.error("No mkdocs.yml found. Are you in an LDA project?")
            return 1
        
        # Change to project root
        os.chdir(project_root)
        
        # Build command
        cmd = ['mkdocs', 'serve', '--port', str(port)]
        
        if dev:
            cmd.extend(['--dev-addr', f'0.0.0.0:{port}'])
        
        self.console.info(f"Starting documentation server on http://localhost:{port}")
        self.console.info("Press Ctrl+C to stop")
        
        try:
            subprocess.run(cmd)
            return 0
        except KeyboardInterrupt:
            self.console.info("Documentation server stopped")
            return 0
        except Exception as e:
            self.console.error(f"Failed to start documentation server: {e}")
            return 1
    
    def build(self, output: str = 'site', strict: bool = False, clean: bool = False) -> int:
        """Build documentation site.
        
        Args:
            output: Output directory
            strict: Enable strict mode
            clean: Clean build directory first
            
        Returns:
            Exit code
        """
        # Check if mkdocs is installed
        try:
            import mkdocs
        except ImportError:
            self.console.error("MkDocs not installed. Install with: pip install lda[docs]")
            return 1
        
        # Find project root
        project_root = Path.cwd()
        mkdocs_yml = project_root / 'mkdocs.yml'
        
        if not mkdocs_yml.exists():
            for parent in project_root.parents:
                if (parent / 'mkdocs.yml').exists():
                    project_root = parent
                    mkdocs_yml = parent / 'mkdocs.yml'
                    break
        
        if not mkdocs_yml.exists():
            self.console.error("No mkdocs.yml found. Are you in an LDA project?")
            return 1
        
        # Change to project root
        os.chdir(project_root)
        
        # Build command
        cmd = ['mkdocs', 'build', '--site-dir', output]
        
        if strict:
            cmd.append('--strict')
        
        if clean:
            cmd.append('--clean')
        
        self.console.info(f"Building documentation to {output}/")
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode == 0:
                self.console.success(f"Documentation built successfully to {output}/")
                return 0
            else:
                self.console.error("Documentation build failed:")
                self.console.error(result.stderr)
                return 1
        except Exception as e:
            self.console.error(f"Failed to build documentation: {e}")
            return 1