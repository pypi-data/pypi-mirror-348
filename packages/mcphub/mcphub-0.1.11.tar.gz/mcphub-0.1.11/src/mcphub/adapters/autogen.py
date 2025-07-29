try:
    from typing import List

    from autogen_ext.tools.mcp import StdioMcpToolAdapter, StdioServerParams

    from .base import MCPBaseAdapter

    class MCPAutogenAdapter(MCPBaseAdapter):
        async def create_adapters(self, mcp_name: str) -> List[StdioMcpToolAdapter]:
            server_params = self.get_server_params(mcp_name)
            
            autogen_mcp_server_params = StdioServerParams(
                command=server_params.command,
                args=server_params.args,
                env=server_params.env,
                cwd=server_params.cwd
            )

            async with self.create_session(mcp_name) as session:
                tools = await session.list_tools()
                return [
                    await StdioMcpToolAdapter.from_server_params(autogen_mcp_server_params, tool.name)
                    for tool in tools.tools
                ]
                
except ImportError:
    class MCPAutogenAdapter:  # type: ignore
        def __init__(self, *args, **kwargs):
            raise ImportError("Autogen dependencies not found. Install with: pip install mcphub[autogen]") 