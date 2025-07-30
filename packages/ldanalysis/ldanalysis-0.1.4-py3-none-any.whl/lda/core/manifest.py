"""Centralized manifest management for LDA projects."""

import json
import csv
import os
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional

from .tracking import FileTracker
from .errors import ManifestError


class LDAManifest:
    """Centralized manifest management system."""
    
    def __init__(self, project_root: str):
        """Initialize manifest system."""
        self.project_root = Path(project_root)
        self.manifest_dir = self.project_root / ".lda"
        self.manifest_file = self.manifest_dir / "manifest.json"
        self.csv_manifest = self.project_root / "lda_manifest.csv"
        
        self.file_tracker = FileTracker()
        self.manifest = self._load_or_create_manifest()
    
    def _load_or_create_manifest(self) -> Dict[str, Any]:
        """Load existing manifest or create new one."""
        if self.manifest_file.exists():
            try:
                with open(self.manifest_file, 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                raise ManifestError(f"Invalid manifest file: {self.manifest_file}")
        
        # Create new manifest structure
        return {
            "project": {
                "root": str(self.project_root),
                "created": datetime.now().isoformat(),
                "last_updated": datetime.now().isoformat()
            },
            "sections": {},
            "files": {},
            "history": []
        }
    
    def _save_manifest(self) -> None:
        """Save manifest to disk."""
        self.manifest_dir.mkdir(exist_ok=True)
        
        self.manifest["project"]["last_updated"] = datetime.now().isoformat()
        
        with open(self.manifest_file, 'w') as f:
            json.dump(self.manifest, f, indent=2)
    
    def init_project(self, config: Dict[str, Any]) -> None:
        """Initialize project manifest."""
        self.manifest["project"].update({
            "name": config.get("name", "Unnamed Project"),
            "code": config.get("code", "PROJ"),
            "analyst": config.get("analyst", "Unknown"),
            "created": datetime.now().isoformat()
        })
        
        self._save_manifest()
        self._update_csv_manifest()
    
    def add_section(self, name: str, config: Dict[str, Any], provenance_id: str) -> None:
        """Add or update section in manifest."""
        section_path = self.project_root / config.get("folder", name)
        
        self.manifest["sections"][name] = {
            "folder": str(section_path.relative_to(self.project_root)),
            "created": datetime.now().isoformat(),
            "provenance_id": provenance_id,
            "config": config
        }
        
        self._save_manifest()
        self._update_csv_manifest()
    
    def track_file(self, section: str, file_type: str, filename: str, 
                  metadata: Optional[Dict[str, Any]] = None) -> None:
        """Track a file in the manifest."""
        file_path = self._resolve_file_path(section, file_type, filename)
        
        # Track with FileTracker
        file_info = self.file_tracker.track_file(
            str(file_path), 
            file_type=file_type, 
            metadata=metadata
        )
        
        # Store in manifest
        file_key = f"{section}.{file_type}.{filename}"
        self.manifest["files"][file_key] = {
            "section": section,
            "type": file_type,
            "filename": filename,
            "path": str(file_path.relative_to(self.project_root)),
            "hash": file_info["hash"],
            "size": file_info["size"],
            "last_updated": file_info["tracked_at"],
            "metadata": metadata or {}
        }
        
        self._save_manifest()
    
    def _resolve_file_path(self, section: str, file_type: str, filename: str) -> Path:
        """Resolve full file path from section and type."""
        section_info = self.manifest["sections"].get(section)
        if not section_info:
            raise ManifestError(f"Unknown section: {section}")
        
        section_folder = self.project_root / section_info["folder"]
        type_folder = "inputs" if file_type == "input" else "outputs"
        
        return section_folder / type_folder / filename
    
    def get_section_files(self, section: str) -> Dict[str, List[Dict[str, Any]]]:
        """Get all files for a section."""
        files = {"inputs": [], "outputs": []}
        
        for file_key, file_info in self.manifest["files"].items():
            if file_info["section"] == section:
                file_type = file_info["type"]
                if file_type == "input":
                    files["inputs"].append(file_info)
                else:
                    files["outputs"].append(file_info)
        
        return files
    
    def detect_changes(self, section: Optional[str] = None) -> Dict[str, List[str]]:
        """Detect file changes in the project."""
        changes = {"new": [], "modified": [], "deleted": []}
        
        files_to_check = self.manifest["files"].items()
        if section:
            files_to_check = [(k, v) for k, v in files_to_check if v["section"] == section]
        
        for file_key, file_info in files_to_check:
            file_path = self.project_root / file_info["path"]
            
            if not file_path.exists():
                changes["deleted"].append(file_key)
                continue
            
            current_hash = self.file_tracker.calculate_file_hash(str(file_path))
            
            if file_info["hash"] is None:
                changes["new"].append(file_key)
            elif current_hash != file_info["hash"]:
                changes["modified"].append(file_key)
        
        return changes
    
    def add_history(self, action: str, details: Dict[str, Any]) -> None:
        """Add entry to history log."""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "action": action,
            "details": details
        }
        
        self.manifest["history"].append(entry)
        
        # Keep only last 1000 entries
        if len(self.manifest["history"]) > 1000:
            self.manifest["history"] = self.manifest["history"][-1000:]
        
        self._save_manifest()
    
    def get_history(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent history entries."""
        return self.manifest["history"][-limit:]
    
    def get_project_status(self) -> Dict[str, Any]:
        """Get overall project status."""
        status = {
            "project": self.manifest["project"],
            "sections": len(self.manifest["sections"]),
            "files": {
                "total": len(self.manifest["files"]),
                "inputs": 0,
                "outputs": 0
            },
            "last_activity": None
        }
        
        # Count file types
        for file_info in self.manifest["files"].values():
            if file_info["type"] == "input":
                status["files"]["inputs"] += 1
            else:
                status["files"]["outputs"] += 1
        
        # Get last activity
        if self.manifest["history"]:
            status["last_activity"] = self.manifest["history"][-1]["timestamp"]
        
        return status
    
    def _update_csv_manifest(self) -> None:
        """Update CSV manifest for backward compatibility."""
        rows = []
        
        for section_name, section_info in self.manifest["sections"].items():
            rows.append({
                "section": section_name,
                "folder": section_info["folder"],
                "analyst": self.manifest["project"].get("analyst", "Unknown"),
                "timestamp": section_info["created"],
                "provenance_id": section_info["provenance_id"]
            })
        
        if rows:
            with open(self.csv_manifest, 'w', newline='') as f:
                fieldnames = ["section", "folder", "analyst", "timestamp", "provenance_id"]
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(rows)
    
    def export_to_csv(self, output_path: str) -> None:
        """Export manifest to CSV format."""
        rows = []
        
        for file_key, file_info in self.manifest["files"].items():
            rows.append({
                "section": file_info["section"],
                "type": file_info["type"],
                "filename": file_info["filename"],
                "path": file_info["path"],
                "hash": file_info["hash"],
                "size": file_info["size"],
                "last_updated": file_info["last_updated"]
            })
        
        with open(output_path, 'w', newline='') as f:
            if rows:
                fieldnames = rows[0].keys()
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(rows)