"""
Example of using MCPHub with LangChain Agents.
1. Initialize MCPHub to manage MCP servers
2. Fetch MCP tools for LangChain
3. Create and run an agent with MCP tools
"""

import asyncio
import json

from langchain_mcp_adapters.tools import load_mcp_tools
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from mcphub import MCPHub

model = ChatOpenAI(model="gpt-4o")

async def main():
    # Initialize MCPHub - automatically loads .mcphub.json and sets up servers
    hub = MCPHub()
    
    # Fetch MCP tools for LangChain
    tools = await hub.fetch_langchain_mcp_tools("azure-storage-mcp")
    tools_dict = [
        {"name": tool.name, "description": tool.description, "args_schema": tool.args_schema} for tool in tools
    ]
    print("Available MCP Tools:")
    print(json.dumps(tools_dict, indent=2))

    # Create and run agent with MCP tools
    complex_task = """Please help me analyze the following complex problem: 
                We need to design a new feature for our product that balances user privacy 
                with data collection for improving the service. Consider the ethical implications, 
                technical feasibility, and business impact. Break down your thinking process 
                step by step, and provide a detailed recommendation with clear justification 
                for each decision point."""
    agent = create_react_agent(model, tools)
    agent_response = await agent.ainvoke({"messages": complex_task})
    print("\nAgent Response:")
    print(agent_response.get("messages")[1].content)

if __name__ == "__main__":
    asyncio.run(main())