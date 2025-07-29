from typing import Dict, Any, Optional, List
import json
from pathlib import Path
import jsonschema
from jsonschema import validate
import yaml
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class SchemaLoader:
    """Handles loading and validation of MCP schemas."""
    
    def __init__(self, schema_dir: Optional[str] = None):
        """Initialize the schema loader with optional schema directory."""
        self.schema_dir = Path(schema_dir) if schema_dir else Path(__file__).parent.parent.parent / "schemas"
        self.schemas: Dict[str, Dict[str, Any]] = {}
        self._load_all_schemas()
    
    def _load_all_schemas(self) -> None:
        """Load all available schemas from the schema directory."""
        if not self.schema_dir.exists():
            logger.warning(f"Schema directory not found: {self.schema_dir}")
            return

        for domain_dir in self.schema_dir.iterdir():
            if not domain_dir.is_dir():
                continue
                
            for version_dir in domain_dir.iterdir():
                if not version_dir.is_dir():
                    continue
                    
                schema_file = version_dir / "context.json"
                if schema_file.exists():
                    try:
                        with open(schema_file, 'r') as f:
                            schema = json.load(f)
                            domain = domain_dir.name
                            version = version_dir.name
                            self.schemas[f"{domain}.{version}"] = schema
                    except Exception as e:
                        logger.error(f"Failed to load schema {schema_file}: {e}")
    
    def list_available_schemas(self) -> List[str]:
        """List all available schema keys."""
        return list(self.schemas.keys())
    
    def get_schema(self, domain: str, version: Optional[str] = None) -> Dict[str, Any]:
        """Get a schema by domain and optional version."""
        if version:
            schema_key = f"{domain}.{version}"
            if schema_key not in self.schemas:
                raise ValueError(f"Schema not found: {schema_key}")
            return self.schemas[schema_key]
        
        # Find latest version if not specified
        available_versions = [k.split('.')[-1] for k in self.schemas.keys() if k.startswith(f"{domain}.")]
        if not available_versions:
            raise ValueError(f"No schemas found for domain: {domain}")
        
        latest_version = sorted(available_versions)[-1]
        return self.schemas[f"{domain}.{latest_version}"]
    
    def list_domains(self) -> List[str]:
        """List all available schema domains."""
        return list(set(k.split('.')[0] for k in self.schemas.keys()))
    
    def list_versions(self, domain: str) -> List[str]:
        """List all available versions for a domain."""
        return [k.split('.')[-1] for k in self.schemas.keys() if k.startswith(f"{domain}.")]
    
    def validate_context(self, context: Dict[str, Any], domain: str, version: Optional[str] = None) -> bool:
        """Validate a context object against a schema."""
        schema = self.get_schema(domain, version)
        try:
            validate(instance=context, schema=schema)
            return True
        except jsonschema.exceptions.ValidationError as e:
            logger.error(f"Context validation failed: {e}")
            raise ValueError(f"Context validation failed: {e}")
    
    def get_schema_metadata(self, domain: str, version: Optional[str] = None) -> Dict[str, Any]:
        """Get metadata about a schema."""
        schema = self.get_schema(domain, version)
        return {
            "title": schema.get("title", ""),
            "description": schema.get("description", ""),
            "required_fields": schema.get("required", []),
            "properties": list(schema.get("properties", {}).keys())
        }

class SchemaRegistry:
    """Manages schema registration and discovery."""
    
    def __init__(self):
        self.registry: Dict[str, Dict[str, Any]] = {}
    
    def register_schema(self, domain: str, version: str, schema: Dict[str, Any]) -> None:
        """Register a new schema."""
        if not self._validate_schema_structure(schema):
            raise ValueError("Invalid schema structure")
        
        key = f"{domain}.{version}"
        self.registry[key] = {
            "schema": schema,
            "registered_at": datetime.utcnow().isoformat(),
            "metadata": {
                "domain": domain,
                "version": version,
                "title": schema.get("title", ""),
                "description": schema.get("description", "")
            }
        }
    
    def _validate_schema_structure(self, schema: Dict[str, Any]) -> bool:
        """Validate basic schema structure."""
        required_keys = {"$schema", "type", "properties"}
        return all(key in schema for key in required_keys)
    
    def get_schema(self, domain: str, version: Optional[str] = None) -> Dict[str, Any]:
        """Get a schema from the registry."""
        if version:
            key = f"{domain}.{version}"
            if key not in self.registry:
                raise ValueError(f"Schema not found: {key}")
            return self.registry[key]["schema"]
        
        # Find latest version
        versions = [k.split('.')[-1] for k in self.registry.keys() if k.startswith(f"{domain}.")]
        if not versions:
            raise ValueError(f"No schemas found for domain: {domain}")
        
        latest_version = sorted(versions)[-1]
        return self.registry[f"{domain}.{latest_version}"]["schema"]
    
    def list_registered_schemas(self) -> List[Dict[str, Any]]:
        """List all registered schemas with metadata."""
        return [
            {
                "key": key,
                "metadata": data["metadata"],
                "registered_at": data["registered_at"]
            }
            for key, data in self.registry.items()
        ] 