"""Documentation server command for LDA CLI."""

import os
import sys
import subprocess
from pathlib import Path

import click
from ..display.console import Console
from ..core.errors import LDAError


@click.group(name='docs')
def docs_group():
    """Manage and serve documentation."""
    pass


@docs_group.command(name='serve')
@click.option('--port', '-p', default=8000, help='Port to serve on')
@click.option('--dev', is_flag=True, help='Enable development mode')
@click.option('--open', is_flag=True, help='Open browser automatically')
def serve_docs(port: int, dev: bool, open: bool):
    """Serve documentation locally."""
    console = Console()
    
    # Check if mkdocs is installed
    try:
        import mkdocs
    except ImportError:
        console.error("MkDocs not installed. Install with: pip install lda[docs]")
        sys.exit(1)
    
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
        console.error("No mkdocs.yml found. Are you in an LDA project?")
        sys.exit(1)
    
    # Change to project root
    os.chdir(project_root)
    
    # Build command
    cmd = ['mkdocs', 'serve', '--port', str(port)]
    
    if dev:
        cmd.append('--dev-addr')
        cmd.append(f'0.0.0.0:{port}')
    
    if not open:
        cmd.append('--no-livereload')
    
    console.info(f"Starting documentation server on http://localhost:{port}")
    console.info("Press Ctrl+C to stop")
    
    try:
        subprocess.run(cmd)
    except KeyboardInterrupt:
        console.info("Documentation server stopped")
    except Exception as e:
        raise LDAError(f"Failed to start documentation server: {e}")


@docs_group.command(name='build')
@click.option('--output', '-o', default='site', help='Output directory')
@click.option('--strict', is_flag=True, help='Enable strict mode')
@click.option('--clean', is_flag=True, help='Clean build directory first')
def build_docs(output: str, strict: bool, clean: bool):
    """Build documentation site."""
    console = Console()
    
    # Check if mkdocs is installed
    try:
        import mkdocs
    except ImportError:
        console.error("MkDocs not installed. Install with: pip install lda[docs]")
        sys.exit(1)
    
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
        console.error("No mkdocs.yml found. Are you in an LDA project?")
        sys.exit(1)
    
    # Change to project root
    os.chdir(project_root)
    
    # Build command
    cmd = ['mkdocs', 'build', '--site-dir', output]
    
    if strict:
        cmd.append('--strict')
    
    if clean:
        cmd.append('--clean')
    
    console.info(f"Building documentation to {output}/")
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            console.success(f"Documentation built successfully to {output}/")
        else:
            console.error("Documentation build failed:")
            console.error(result.stderr)
            sys.exit(1)
    except Exception as e:
        raise LDAError(f"Failed to build documentation: {e}")


@docs_group.command(name='deploy')
@click.option('--message', '-m', default='Deploy documentation', help='Commit message')
@click.option('--force', is_flag=True, help='Force deployment')
@click.option('--remote', default='origin', help='Git remote to deploy to')
@click.option('--branch', default='gh-pages', help='Branch to deploy to')
def deploy_docs(message: str, force: bool, remote: str, branch: str):
    """Deploy documentation to GitHub Pages."""
    console = Console()
    
    # Check if mkdocs is installed
    try:
        import mkdocs
    except ImportError:
        console.error("MkDocs not installed. Install with: pip install lda[docs]")
        sys.exit(1)
    
    # Find project root
    project_root = Path.cwd()
    mkdocs_yml = project_root / 'mkdocs.yml'
    
    if not mkdocs_yml.exists():
        console.error("No mkdocs.yml found. Are you in an LDA project?")
        sys.exit(1)
    
    # Change to project root
    os.chdir(project_root)
    
    # Build command
    cmd = ['mkdocs', 'gh-deploy', '--message', message, '--remote-name', remote, '--remote-branch', branch]
    
    if force:
        cmd.append('--force')
    
    console.info(f"Deploying documentation to {remote}/{branch}")
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            console.success("Documentation deployed successfully!")
            console.info(f"View at: https://[your-username].github.io/[repo-name]/")
        else:
            console.error("Documentation deployment failed:")
            console.error(result.stderr)
            sys.exit(1)
    except Exception as e:
        raise LDAError(f"Failed to deploy documentation: {e}")