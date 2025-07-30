"""File tracking and provenance management for LDA."""

import os
import hashlib
from pathlib import Path
from datetime import datetime
from typing import Dict, Optional, List, Any


class FileTracker:
    """Handles file tracking and provenance for LDA projects."""
    
    def __init__(self):
        """Initialize file tracker."""
        self.tracked_files = {}
    
    @staticmethod
    def calculate_file_hash(filepath: str) -> Optional[str]:
        """Calculate SHA-256 hash of a file."""
        if not os.path.exists(filepath):
            return None
        
        sha256_hash = hashlib.sha256()
        with open(filepath, "rb") as f:
            # Read and update hash in chunks for memory efficiency
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    
    @staticmethod
    def generate_provenance_id(prefix: str = "") -> str:
        """Generate unique provenance ID based on timestamp."""
        timestamp = datetime.now().isoformat()
        hash_obj = hashlib.sha256(f"{prefix}{timestamp}".encode())
        return hash_obj.hexdigest()[:12]
    
    def track_file(self, filepath: str, file_type: str = "unknown", 
                  metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Track a file and return its metadata."""
        file_path = Path(filepath)
        
        file_info = {
            "path": str(file_path),
            "filename": file_path.name,
            "type": file_type,
            "exists": file_path.exists(),
            "hash": None,
            "size": 0,
            "last_modified": None,
            "tracked_at": datetime.now().isoformat(),
            "metadata": metadata or {}
        }
        
        if file_path.exists():
            file_info["hash"] = self.calculate_file_hash(str(file_path))
            file_info["size"] = file_path.stat().st_size
            file_info["last_modified"] = datetime.fromtimestamp(
                file_path.stat().st_mtime
            ).isoformat()
        
        self.tracked_files[str(file_path)] = file_info
        return file_info
    
    def get_file_info(self, filepath: str) -> Optional[Dict[str, Any]]:
        """Get tracking information for a file."""
        return self.tracked_files.get(str(Path(filepath)))
    
    def detect_changes(self, filepath: str) -> Dict[str, Any]:
        """Detect if a tracked file has changed."""
        file_path = Path(filepath)
        
        # Get current file state
        current_hash = self.calculate_file_hash(str(file_path))
        current_exists = file_path.exists()
        current_size = file_path.stat().st_size if current_exists else 0
        
        # Get previous state if tracked
        previous_info = self.tracked_files.get(str(file_path))
        
        if not previous_info:
            return {"changed": True, "reasons": ["Not previously tracked"]}
        
        changes = {
            "changed": False,
            "reasons": []
        }
        
        if previous_info["hash"] != current_hash:
            changes["changed"] = True
            changes["reasons"].append("Content changed")
        
        if previous_info["size"] != current_size:
            changes["changed"] = True
            changes["reasons"].append("Size changed")
        
        if previous_info["exists"] != current_exists:
            changes["changed"] = True
            changes["reasons"].append("Existence changed")
        
        return changes
    
    def get_all_changes(self) -> Dict[str, Dict[str, Any]]:
        """Get all file changes."""
        all_changes = {}
        
        for filepath in self.tracked_files:
            changes = self.detect_changes(filepath)
            if changes["changed"]:
                all_changes[filepath] = changes
        
        return all_changes
    
    def create_provenance_record(self, section: str, files: List[str]) -> Dict[str, Any]:
        """Create a provenance record for a section."""
        provenance_id = self.generate_provenance_id(section)
        
        record = {
            "section": section,
            "provenance_id": provenance_id,
            "timestamp": datetime.now().isoformat(),
            "files": {}
        }
        
        for filepath in files:
            file_info = self.track_file(filepath)
            record["files"][filepath] = {
                "hash": file_info["hash"],
                "size": file_info["size"],
                "type": file_info["type"]
            }
        
        return record
    
    def verify_provenance(self, record: Dict[str, Any]) -> Dict[str, Any]:
        """Verify a provenance record against current files."""
        verification = {
            "valid": True,
            "issues": [],
            "section": record["section"],
            "provenance_id": record["provenance_id"]
        }
        
        for filepath, expected_info in record["files"].items():
            current_info = self.track_file(filepath)
            
            if not current_info["exists"]:
                verification["valid"] = False
                verification["issues"].append(f"File missing: {filepath}")
                continue
            
            if current_info["hash"] != expected_info["hash"]:
                verification["valid"] = False
                verification["issues"].append(f"File modified: {filepath}")
        
        return verification