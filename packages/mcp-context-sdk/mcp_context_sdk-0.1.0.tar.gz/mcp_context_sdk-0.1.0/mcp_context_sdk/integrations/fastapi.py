from typing import Dict, Any, Optional, List
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.base import BaseHTTPMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from ..core.builder import ContextBuilder
from ..core.converter import ContextConverter
from ..schemas.loader import SchemaLoader

class MCPMiddleware(BaseHTTPMiddleware):
    """FastAPI middleware that enriches requests with MCP context."""
    
    def __init__(
        self,
        app: FastAPI,
        context_builder: ContextBuilder,
        domain: str,
        version: Optional[str] = None
    ):
        """Initialize the MCP middleware."""
        super().__init__(app)
        self.context_builder = context_builder
        self.domain = domain
        self.version = version
    
    async def dispatch(self, request: Request, call_next):
        """Process the request and add MCP context."""
        # Get request data
        try:
            body = await request.json()
        except:
            body = {}
        
        # Build context from request
        context = self.context_builder.build_coding_context(
            project_name=body.get("project_name", "unknown"),
            project_type=body.get("project_type", "unknown"),
            language=body.get("language", "python"),
            file_content=body.get("content", "")
        )
        
        # Add context to request state
        request.state.mcp_context = context
        
        # Process request
        response = await call_next(request)
        return response

class MCPRequest(BaseModel):
    """Base model for MCP-enhanced requests."""
    project_name: str
    project_type: str
    language: str
    content: Optional[str] = None
    mcp_context: Optional[Dict[str, Any]] = None

class MCPResponse(BaseModel):
    """Base model for MCP-enhanced responses."""
    result: Any
    mcp_context: Dict[str, Any]

def create_mcp_app(
    context_builder: ContextBuilder,
    domain: str,
    version: Optional[str] = None
) -> FastAPI:
    """Create a FastAPI app with MCP integration."""
    app = FastAPI(title="MCP API")
    
    # Add MCP middleware
    app.add_middleware(
        MCPMiddleware,
        context_builder=context_builder,
        domain=domain,
        version=version
    )
    
    return app

def get_mcp_context(request: Request) -> Dict[str, Any]:
    """Get MCP context from request state."""
    if not hasattr(request.state, "mcp_context"):
        raise HTTPException(status_code=400, detail="MCP context not found")
    return request.state.mcp_context

class MCPEndpoint:
    """Decorator for creating MCP-enhanced endpoints."""
    
    def __init__(
        self,
        context_builder: ContextBuilder,
        domain: str,
        version: Optional[str] = None
    ):
        """Initialize the MCP endpoint decorator."""
        self.context_builder = context_builder
        self.domain = domain
        self.version = version
    
    def __call__(self, func):
        """Decorate the endpoint function."""
        async def wrapper(request: Request, *args, **kwargs):
            # Get MCP context
            context = get_mcp_context(request)
            
            # Call original function with context
            result = await func(request, context, *args, **kwargs)
            
            # Return response with context
            return MCPResponse(
                result=result,
                mcp_context=context
            )
        
        return wrapper

# Example usage:
"""
app = create_mcp_app(context_builder, "coding", "v1")

@mcp_endpoint = MCPEndpoint(context_builder, "coding", "v1")

@app.post("/process")
@mcp_endpoint
async def process_code(request: Request, context: Dict[str, Any]):
    # Process code with MCP context
    return {"status": "success"}
""" 