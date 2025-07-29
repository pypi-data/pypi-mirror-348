from typing import Dict, Any, Optional, List
from datetime import datetime
import platform
import os
from pathlib import Path
import json
from .converter import ContextConverter
from ..schemas.loader import SchemaLoader

class ContextBuilder:
    """Builds valid context objects with sensible defaults."""
    
    def __init__(self, schema_loader: Optional[SchemaLoader] = None):
        """Initialize the context builder with optional schema loader."""
        self.schema_loader = schema_loader or SchemaLoader()
        self.converter = ContextConverter()
    
    def build_coding_context(
        self,
        project_name: str,
        project_type: str,
        language: str,
        file_path: Optional[str] = None,
        file_content: Optional[str] = None,
        cursor_line: Optional[int] = None,
        cursor_column: Optional[int] = None,
        user_role: str = "developer",
        expertise_level: str = "intermediate",
        **kwargs
    ) -> Dict[str, Any]:
        """Build a coding context with defaults."""
        context = {
            "version": "v1.0.0",
            "project": {
                "name": project_name,
                "type": project_type,
                "language": language,
                "framework": kwargs.get("framework"),
                "dependencies": kwargs.get("dependencies", [])
            },
            "user": {
                "role": user_role,
                "expertise_level": expertise_level,
                "preferences": {
                    "coding_style": kwargs.get("coding_style", "standard"),
                    "documentation_level": kwargs.get("documentation_level", "moderate"),
                    "testing_approach": kwargs.get("testing_approach", "balanced")
                }
            },
            "current_state": {
                "file": {
                    "path": file_path or "",
                    "content": file_content or "",
                    "language": language
                },
                "cursor_position": {
                    "line": cursor_line or 1,
                    "column": cursor_column or 1
                }
            },
            "environment": {
                "os": platform.system(),
                "ide": kwargs.get("ide", "unknown"),
                "terminal": kwargs.get("terminal", "unknown"),
                "variables": dict(os.environ)
            }
        }
        
        # Add context history if provided
        if "context_history" in kwargs:
            context["context_history"] = kwargs["context_history"]
        else:
            context["context_history"] = [{
                "timestamp": datetime.utcnow().isoformat(),
                "action": "context_created",
                "details": {"builder": "ContextBuilder"}
            }]
        
        # Validate against schema
        self.schema_loader.validate_context(context, "coding", "v1")
        return context
    
    def build_from_file(self, file_path: str, domain: str, version: Optional[str] = None) -> Dict[str, Any]:
        """Build context from a JSON file."""
        with open(file_path, 'r') as f:
            context = json.load(f)
        
        # Validate and fill defaults
        schema = self.schema_loader.get_schema(domain, version)
        self._fill_defaults(context, schema)
        self.schema_loader.validate_context(context, domain, version)
        return context
    
    def _fill_defaults(self, context: Dict[str, Any], schema: Dict[str, Any]) -> None:
        """Fill missing fields with defaults from schema."""
        properties = schema.get("properties", {})
        required = schema.get("required", [])
        
        for field in required:
            if field not in context:
                if field in properties:
                    context[field] = self._get_default_value(properties[field])
        
        for field, prop in properties.items():
            if field not in context and "default" in prop:
                context[field] = prop["default"]
    
    def _get_default_value(self, property_schema: Dict[str, Any]) -> Any:
        """Get default value based on property type."""
        prop_type = property_schema.get("type")
        
        if prop_type == "string":
            return ""
        elif prop_type == "number":
            return 0
        elif prop_type == "integer":
            return 0
        elif prop_type == "boolean":
            return False
        elif prop_type == "array":
            return []
        elif prop_type == "object":
            return {}
        return None
    
    def update_context(
        self,
        context: Dict[str, Any],
        updates: Dict[str, Any],
        domain: str,
        version: Optional[str] = None
    ) -> Dict[str, Any]:
        """Update an existing context with new values."""
        # Deep merge updates
        merged = self._deep_merge(context, updates)
        
        # Validate updated context
        self.schema_loader.validate_context(merged, domain, version)
        
        # Add update to history
        if "context_history" in merged:
            merged["context_history"].append({
                "timestamp": datetime.utcnow().isoformat(),
                "action": "context_updated",
                "details": {"updates": list(updates.keys())}
            })
        
        return merged
    
    def _deep_merge(self, dict1: Dict[str, Any], dict2: Dict[str, Any]) -> Dict[str, Any]:
        """Deep merge two dictionaries."""
        result = dict1.copy()
        
        for key, value in dict2.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._deep_merge(result[key], value)
            else:
                result[key] = value
        
        return result 