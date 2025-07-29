from typing import Dict, Any, Optional, List, Callable
from langchain.tools import BaseTool
from langchain.agents import AgentExecutor
from langchain.schema import AgentAction, AgentFinish
from langchain.prompts import PromptTemplate
from ..core.builder import ContextBuilder
from ..core.converter import ContextConverter
from ..schemas.loader import SchemaLoader

class MCPTool(BaseTool):
    """LangChain tool that uses MCP context for enhanced prompts."""
    
    name = "mcp_context_tool"
    description = "Tool that provides structured context for AI operations"
    
    def __init__(
        self,
        context_builder: ContextBuilder,
        domain: str,
        version: Optional[str] = None,
        template: Optional[str] = None
    ):
        """Initialize the MCP tool."""
        super().__init__()
        self.context_builder = context_builder
        self.domain = domain
        self.version = version
        self.converter = ContextConverter()
        self.template = template
    
    def _run(self, query: str) -> str:
        """Run the tool with the given query."""
        # Build context from query
        context = self.context_builder.build_coding_context(
            project_name="langchain_project",
            project_type="library",
            language="python",
            file_content=query
        )
        
        # Convert to prompt
        return self.converter.to_prompt(context, self.template)
    
    async def _arun(self, query: str) -> str:
        """Async implementation of _run."""
        return self._run(query)

class MCPAgentExecutor(AgentExecutor):
    """Enhanced AgentExecutor that uses MCP context."""
    
    def __init__(
        self,
        agent: Any,
        tools: List[BaseTool],
        context_builder: ContextBuilder,
        domain: str,
        version: Optional[str] = None,
        **kwargs
    ):
        """Initialize the MCP agent executor."""
        super().__init__(agent=agent, tools=tools, **kwargs)
        self.context_builder = context_builder
        self.domain = domain
        self.version = version
    
    def _call(self, inputs: Dict[str, str]) -> Dict[str, Any]:
        """Override _call to inject MCP context."""
        # Build context from inputs
        context = self.context_builder.build_coding_context(
            project_name=inputs.get("project_name", "unknown"),
            project_type=inputs.get("project_type", "unknown"),
            language=inputs.get("language", "python"),
            file_content=inputs.get("query", "")
        )
        
        # Add context to inputs
        inputs["mcp_context"] = context
        
        # Run agent with enhanced inputs
        return super()._call(inputs)

class MCPPromptTemplate(PromptTemplate):
    """Enhanced prompt template that supports MCP context."""
    
    def __init__(
        self,
        template: str,
        context_builder: ContextBuilder,
        domain: str,
        version: Optional[str] = None,
        **kwargs
    ):
        """Initialize the MCP prompt template."""
        super().__init__(template=template, **kwargs)
        self.context_builder = context_builder
        self.domain = domain
        self.version = version
    
    def format(self, **kwargs) -> str:
        """Format the prompt with MCP context."""
        # Build context from kwargs
        context = self.context_builder.build_coding_context(
            project_name=kwargs.get("project_name", "unknown"),
            project_type=kwargs.get("project_type", "unknown"),
            language=kwargs.get("language", "python"),
            file_content=kwargs.get("query", "")
        )
        
        # Add context to kwargs
        kwargs["mcp_context"] = context
        
        return super().format(**kwargs)

def create_mcp_chain(
    llm: Any,
    context_builder: ContextBuilder,
    domain: str,
    version: Optional[str] = None,
    template: Optional[str] = None
) -> Any:
    """Create a LangChain chain with MCP integration."""
    from langchain.chains import LLMChain
    
    # Create MCP tool
    mcp_tool = MCPTool(
        context_builder=context_builder,
        domain=domain,
        version=version,
        template=template
    )
    
    # Create chain with MCP tool
    return LLMChain(
        llm=llm,
        prompt=PromptTemplate(
            input_variables=["query", "mcp_context"],
            template="{query}\n\nContext:\n{mcp_context}"
        ),
        tools=[mcp_tool]
    ) 