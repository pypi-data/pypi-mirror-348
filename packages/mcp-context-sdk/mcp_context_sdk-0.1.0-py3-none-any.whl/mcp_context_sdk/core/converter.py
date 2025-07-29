from typing import Dict, Any, Optional
import json
from pathlib import Path
import jsonschema
from datetime import datetime

class ContextConverter:
    """Converts structured context into formatted prompts for LLMs."""
    
    def __init__(self, schema_path: Optional[str] = None):
        """Initialize the converter with an optional schema path."""
        self.schema = None
        if schema_path:
            self.load_schema(schema_path)
    
    def load_schema(self, schema_path: str) -> None:
        """Load and validate a JSON schema."""
        with open(schema_path, 'r') as f:
            self.schema = json.load(f)
    
    def validate_context(self, context: Dict[str, Any]) -> bool:
        """Validate context against the loaded schema."""
        if not self.schema:
            raise ValueError("No schema loaded. Call load_schema first.")
        
        try:
            jsonschema.validate(instance=context, schema=self.schema)
            return True
        except jsonschema.exceptions.ValidationError as e:
            raise ValueError(f"Context validation failed: {str(e)}")
    
    def to_prompt(self, context: Dict[str, Any], template: Optional[str] = None) -> str:
        """Convert context to a formatted prompt string."""
        if not self.validate_context(context):
            raise ValueError("Invalid context")
        
        if template:
            return self._apply_template(context, template)
        
        return self._default_format(context)
    
    def _default_format(self, context: Dict[str, Any]) -> str:
        """Default formatting for context to prompt conversion."""
        prompt_parts = []
        
        # Project information
        project = context.get('project', {})
        prompt_parts.append(f"Project: {project.get('name', 'Unknown')}")
        prompt_parts.append(f"Type: {project.get('type', 'Unknown')}")
        prompt_parts.append(f"Language: {project.get('language', 'Unknown')}")
        
        if framework := project.get('framework'):
            prompt_parts.append(f"Framework: {framework}")
        
        # User context
        user = context.get('user', {})
        prompt_parts.append(f"\nUser Role: {user.get('role', 'Unknown')}")
        prompt_parts.append(f"Expertise Level: {user.get('expertise_level', 'Unknown')}")
        
        # Current state
        current_state = context.get('current_state', {})
        if file_info := current_state.get('file'):
            prompt_parts.append(f"\nCurrent File: {file_info.get('path', 'Unknown')}")
            prompt_parts.append(f"Language: {file_info.get('language', 'Unknown')}")
            
            if cursor := current_state.get('cursor_position'):
                prompt_parts.append(f"Cursor Position: Line {cursor.get('line')}, Column {cursor.get('column')}")
        
        # Environment
        if env := context.get('environment'):
            prompt_parts.append(f"\nEnvironment:")
            prompt_parts.append(f"OS: {env.get('os', 'Unknown')}")
            prompt_parts.append(f"IDE: {env.get('ide', 'Unknown')}")
        
        return "\n".join(prompt_parts)
    
    def _apply_template(self, context: Dict[str, Any], template: str) -> str:
        """Apply a custom template to the context."""
        # Simple template replacement for now
        # TODO: Implement more sophisticated templating
        result = template
        for key, value in self._flatten_dict(context):
            placeholder = f"{{{{{key}}}}}"
            if placeholder in result:
                result = result.replace(placeholder, str(value))
        return result
    
    def _flatten_dict(self, d: Dict[str, Any], parent_key: str = '') -> Dict[str, Any]:
        """Flatten a nested dictionary with dot notation."""
        items = []
        for k, v in d.items():
            new_key = f"{parent_key}.{k}" if parent_key else k
            if isinstance(v, dict):
                items.extend(self._flatten_dict(v, new_key).items())
            else:
                items.append((new_key, v))
        return dict(items)

class PromptTemplate:
    """Manages prompt templates for different use cases."""
    
    def __init__(self):
        self.templates = {}
    
    def add_template(self, name: str, template: str) -> None:
        """Add a new template."""
        self.templates[name] = template
    
    def get_template(self, name: str) -> str:
        """Get a template by name."""
        if name not in self.templates:
            raise KeyError(f"Template '{name}' not found")
        return self.templates[name]
    
    def list_templates(self) -> list[str]:
        """List all available template names."""
        return list(self.templates.keys()) 