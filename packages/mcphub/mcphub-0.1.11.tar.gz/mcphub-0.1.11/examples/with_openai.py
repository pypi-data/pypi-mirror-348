"""
Example of using MCPHub with OpenAI Agents.
1. Initialize MCPHub to manage MCP servers
2. Fetch an MCP server with async context manager
3. List available tools from the server
4. Create and run an agent with MCP tools
"""

import asyncio
import json
from agents import Agent, Runner
from mcphub import MCPHub

async def main():
    # Initialize MCPHub - automatically loads .mcphub.json and sets up servers
    hub = MCPHub()
    
    # Fetch MCP server - handles server setup and tool caching
    async with hub.fetch_openai_mcp_server(
        mcp_name="sequential-thinking-mcp",
        cache_tools_list=True
    ) as server:
        # Get available tools from the server
        tools = await server.list_tools()
        tools_dict = [
            dict(tool) if hasattr(tool, "__dict__") else tool for tool in tools
        ]
        print("Available MCP Tools:")
        print(json.dumps(tools_dict, indent=2))

        # Create agent with MCP server integration
        agent = Agent(
            name="Assistant",
            instructions="Use the available tools to accomplish the given task",
            mcp_servers=[server]
        )
        
        # Run agent with a task
        complex_task = """Please help me analyze the following complex problem: 
                      We need to design a new feature for our product that balances user privacy 
                      with data collection for improving the service. Consider the ethical implications, 
                      technical feasibility, and business impact. Break down your thinking process 
                      step by step, and provide a detailed recommendation with clear justification 
                      for each decision point."""
        
        result = await Runner.run(agent, complex_task)
        print("\nAgent Response:")
        print(result)

if __name__ == "__main__":
    asyncio.run(main())