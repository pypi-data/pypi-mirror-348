"""Validation utilities for MCP SDK."""

from typing import Any, Dict, Optional
import json
from pathlib import Path

def validate_schema(schema: Dict[str, Any]) -> bool:
    """Validate a schema against basic requirements.
    
    Args:
        schema: The schema dictionary to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    required_fields = ['name', 'version', 'properties']
    return all(field in schema for field in required_fields)

def load_schema_file(file_path: str) -> Optional[Dict[str, Any]]:
    """Load and validate a schema from a JSON file.
    
    Args:
        file_path: Path to the schema file
        
    Returns:
        Optional[Dict[str, Any]]: The loaded schema if valid, None otherwise
    """
    try:
        with open(file_path, 'r') as f:
            schema = json.load(f)
        if validate_schema(schema):
            return schema
    except (json.JSONDecodeError, FileNotFoundError):
        pass
    return None

def get_schema_path(schema_name: str, version: str = "v1") -> Path:
    """Get the path to a schema file.
    
    Args:
        schema_name: Name of the schema
        version: Schema version
        
    Returns:
        Path: Path to the schema file
    """
    base_path = Path(__file__).parent.parent.parent / "schemas"
    return base_path / f"{schema_name}.{version}.json" 