"""
Example of using MCPHub with Autogen Agents.
1. Initialize MCPHub to manage MCP servers
2. Fetch MCP tools and adapters for Autogen
3. Create and run an agent with MCP tools
"""

import asyncio

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.ui import Console
from autogen_core import CancellationToken
from autogen_ext.models.openai import OpenAIChatCompletionClient
from mcphub import MCPHub


async def main():
    # Initialize MCPHub - automatically loads .mcphub.json and sets up servers
    hub = MCPHub()
    
    # Fetch MCP tools adapted for Autogen
    tool_adapters = await hub.fetch_autogen_mcp_adapters("azure-storage-mcp")
    model_client = OpenAIChatCompletionClient(model="gpt-4")

    # Create and run agent with MCP tools
    complex_task = """Please help me analyze the following complex problem: 
                We need to design a new feature for our product that balances user privacy 
                with data collection for improving the service. Consider the ethical implications, 
                technical feasibility, and business impact. Break down your thinking process 
                step by step, and provide a detailed recommendation with clear justification 
                for each decision point."""
    agent = AssistantAgent(
        name="assistant",
        model_client=model_client,
        tools=tool_adapters,
        system_message="You are a helpful assistant.",
    )
    
    await Console(
        agent.run_stream(task=complex_task, cancellation_token=CancellationToken())
    )

if __name__ == "__main__":
    # Run the async main function
    asyncio.run(main())