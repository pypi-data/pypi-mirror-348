"""
MCP SDK - Model Context Protocol
A modular, production-ready Python SDK for building structured, context-aware AI systems.
"""

__version__ = "1.0.0"

from mcp.core.context import ContextBuilder
from mcp.core.schema import SchemaLoader
from mcp.core.validator import SchemaValidator

__all__ = [
    "ContextBuilder",
    "SchemaLoader",
    "SchemaValidator",
] 