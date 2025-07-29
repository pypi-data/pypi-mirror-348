import click
import json
from pathlib import Path
from typing import Optional
from .core.builder import ContextBuilder
from .core.converter import ContextConverter
from .schemas.loader import SchemaLoader

@click.group()
def cli():
    """MCP CLI tool for managing context and schemas."""
    pass

@cli.command()
@click.argument('domain')
@click.option('--version', help='Schema version')
def list_schemas(domain: str, version: Optional[str] = None):
    """List available schemas."""
    loader = SchemaLoader()
    if version:
        schema = loader.get_schema(domain, version)
        click.echo(json.dumps(schema, indent=2))
    else:
        versions = loader.list_versions(domain)
        click.echo(f"Available versions for {domain}:")
        for v in versions:
            click.echo(f"- {v}")

@cli.command()
@click.argument('input_file', type=click.Path(exists=True))
@click.argument('domain')
@click.option('--version', help='Schema version')
@click.option('--output', '-o', help='Output file path')
def convert_context(input_file: str, domain: str, version: Optional[str] = None, output: Optional[str] = None):
    """Convert context to prompt."""
    # Load context
    with open(input_file, 'r') as f:
        context = json.load(f)
    
    # Initialize components
    loader = SchemaLoader()
    builder = ContextBuilder(loader)
    converter = ContextConverter()
    
    # Validate and convert
    try:
        loader.validate_context(context, domain, version)
        prompt = converter.to_prompt(context)
        
        if output:
            with open(output, 'w') as f:
                f.write(prompt)
        else:
            click.echo(prompt)
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)
        raise click.Abort()

@cli.command()
@click.argument('domain')
@click.option('--version', help='Schema version')
@click.option('--output', '-o', help='Output file path')
def create_context(domain: str, version: Optional[str] = None, output: Optional[str] = None):
    """Create a new context with defaults."""
    builder = ContextBuilder()
    
    # Get schema metadata
    loader = SchemaLoader()
    metadata = loader.get_schema_metadata(domain, version)
    
    # Create context with defaults
    context = builder.build_coding_context(
        project_name="new-project",
        project_type="web",
        language="python"
    )
    
    if output:
        with open(output, 'w') as f:
            json.dump(context, f, indent=2)
    else:
        click.echo(json.dumps(context, indent=2))

@cli.command()
@click.argument('input_file', type=click.Path(exists=True))
@click.argument('domain')
@click.option('--version', help='Schema version')
def validate_context(input_file: str, domain: str, version: Optional[str] = None):
    """Validate a context against a schema."""
    # Load context
    with open(input_file, 'r') as f:
        context = json.load(f)
    
    # Validate
    loader = SchemaLoader()
    try:
        loader.validate_context(context, domain, version)
        click.echo("Context is valid!")
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)
        raise click.Abort()

@cli.command()
@click.argument('input_file', type=click.Path(exists=True))
@click.argument('updates_file', type=click.Path(exists=True))
@click.argument('domain')
@click.option('--version', help='Schema version')
@click.option('--output', '-o', help='Output file path')
def update_context(
    input_file: str,
    updates_file: str,
    domain: str,
    version: Optional[str] = None,
    output: Optional[str] = None
):
    """Update a context with new values."""
    # Load files
    with open(input_file, 'r') as f:
        context = json.load(f)
    with open(updates_file, 'r') as f:
        updates = json.load(f)
    
    # Update context
    builder = ContextBuilder()
    try:
        updated = builder.update_context(context, updates, domain, version)
        
        if output:
            with open(output, 'w') as f:
                json.dump(updated, f, indent=2)
        else:
            click.echo(json.dumps(updated, indent=2))
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)
        raise click.Abort()

def main():
    cli() 