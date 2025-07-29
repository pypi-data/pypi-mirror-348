from typing import Dict, Any, Optional, List, Callable
import autogen
from ..core.builder import ContextBuilder
from ..core.converter import ContextConverter
from ..schemas.loader import SchemaLoader

class MCPAgent(autogen.AssistantAgent):
    """Enhanced AutoGen agent that uses MCP context."""
    
    def __init__(
        self,
        name: str,
        context_builder: ContextBuilder,
        domain: str,
        version: Optional[str] = None,
        template: Optional[str] = None,
        **kwargs
    ):
        """Initialize the MCP agent."""
        super().__init__(name=name, **kwargs)
        self.context_builder = context_builder
        self.domain = domain
        self.version = version
        self.converter = ContextConverter()
        self.template = template
    
    def generate_reply(
        self,
        messages: Optional[List[Dict[str, Any]]] = None,
        sender: Optional[autogen.Agent] = None,
        config: Optional[Any] = None
    ) -> Optional[str]:
        """Override generate_reply to inject MCP context."""
        if not messages:
            return None
        
        # Get the last message
        last_message = messages[-1]
        
        # Build context from message
        context = self.context_builder.build_coding_context(
            project_name=last_message.get("project_name", "unknown"),
            project_type=last_message.get("project_type", "unknown"),
            language=last_message.get("language", "python"),
            file_content=last_message.get("content", "")
        )
        
        # Convert context to prompt
        context_prompt = self.converter.to_prompt(context, self.template)
        
        # Add context to message
        last_message["mcp_context"] = context_prompt
        
        # Generate reply with enhanced context
        return super().generate_reply(messages, sender, config)

class MCPGroupChat(autogen.GroupChat):
    """Enhanced GroupChat that supports MCP context sharing."""
    
    def __init__(
        self,
        agents: List[autogen.Agent],
        context_builder: ContextBuilder,
        domain: str,
        version: Optional[str] = None,
        **kwargs
    ):
        """Initialize the MCP group chat."""
        super().__init__(agents=agents, **kwargs)
        self.context_builder = context_builder
        self.domain = domain
        self.version = version
    
    def append_message(self, message: Dict[str, Any], sender: autogen.Agent) -> None:
        """Override append_message to add MCP context."""
        # Build context from message
        context = self.context_builder.build_coding_context(
            project_name=message.get("project_name", "unknown"),
            project_type=message.get("project_type", "unknown"),
            language=message.get("language", "python"),
            file_content=message.get("content", "")
        )
        
        # Add context to message
        message["mcp_context"] = context
        
        super().append_message(message, sender)

def create_mcp_agent(
    name: str,
    context_builder: ContextBuilder,
    domain: str,
    version: Optional[str] = None,
    template: Optional[str] = None,
    **kwargs
) -> MCPAgent:
    """Create an MCP-enhanced AutoGen agent."""
    return MCPAgent(
        name=name,
        context_builder=context_builder,
        domain=domain,
        version=version,
        template=template,
        **kwargs
    )

def create_mcp_group_chat(
    agents: List[autogen.Agent],
    context_builder: ContextBuilder,
    domain: str,
    version: Optional[str] = None,
    **kwargs
) -> MCPGroupChat:
    """Create an MCP-enhanced AutoGen group chat."""
    return MCPGroupChat(
        agents=agents,
        context_builder=context_builder,
        domain=domain,
        version=version,
        **kwargs
    )

class MCPConfig:
    """Configuration for MCP-enhanced AutoGen agents."""
    
    def __init__(
        self,
        context_builder: ContextBuilder,
        domain: str,
        version: Optional[str] = None,
        template: Optional[str] = None
    ):
        """Initialize MCP configuration."""
        self.context_builder = context_builder
        self.domain = domain
        self.version = version
        self.template = template
    
    def get_agent_config(self, name: str, **kwargs) -> Dict[str, Any]:
        """Get configuration for an MCP agent."""
        return {
            "name": name,
            "context_builder": self.context_builder,
            "domain": self.domain,
            "version": self.version,
            "template": self.template,
            **kwargs
        }
    
    def get_group_chat_config(self, **kwargs) -> Dict[str, Any]:
        """Get configuration for an MCP group chat."""
        return {
            "context_builder": self.context_builder,
            "domain": self.domain,
            "version": self.version,
            **kwargs
        } 