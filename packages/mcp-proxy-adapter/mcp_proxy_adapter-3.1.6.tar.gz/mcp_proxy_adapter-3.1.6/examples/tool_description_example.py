#!/usr/bin/env python
"""
Example of using the API tool description functionality.

This script demonstrates how to use the API tool description functionality
to generate rich and informative descriptions for API tools.
"""

import json
import asyncio
import sys
from pathlib import Path

# Add the project root to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

from mcp_proxy_adapter.commands.command_registry import registry
from mcp_proxy_adapter.api.schemas import APIToolDescription
from mcp_proxy_adapter.api.tools import get_tool_description, TSTCommandExecutor
from mcp_proxy_adapter.commands.help_command import HelpCommand


async def main():
    """Main function to demonstrate API tool description functionality."""
    
    # Register the help command so we have at least one command registered
    if not registry.command_exists("help"):
        registry.register(HelpCommand)
    
    # Generate description using the APIToolDescription class directly
    print("Generating tool description using APIToolDescription:")
    description = APIToolDescription.generate_tool_description("tst_execute_command", registry)
    print(json.dumps(description, indent=2, ensure_ascii=False))
    print("\n" + "-" * 80 + "\n")
    
    # Generate text description using the APIToolDescription class
    print("Generating tool description text using APIToolDescription:")
    description_text = APIToolDescription.generate_tool_description_text("tst_execute_command", registry)
    print(description_text)
    print("\n" + "-" * 80 + "\n")
    
    # Get tool description using the tools module
    print("Getting tool description using the tools module:")
    tool_description = get_tool_description("tst_execute_command")
    print(json.dumps(tool_description, indent=2, ensure_ascii=False))
    print("\n" + "-" * 80 + "\n")
    
    # Get tool description in markdown format using the tools module
    print("Getting tool description in markdown format using the tools module:")
    tool_description_md = get_tool_description("tst_execute_command", "markdown")
    print(tool_description_md)
    print("\n" + "-" * 80 + "\n")
    
    # Get tool schema directly from the tool class
    print("Getting tool schema directly from the tool class:")
    tool_schema = TSTCommandExecutor.get_schema()
    print(json.dumps(tool_schema, indent=2, ensure_ascii=False))
    print("\n" + "-" * 80 + "\n")
    
    # Get tool description directly from the tool class
    print("Getting tool description directly from the tool class:")
    tool_desc = TSTCommandExecutor.get_description("json")
    print(json.dumps(tool_desc, indent=2, ensure_ascii=False))
    print("\n" + "-" * 80 + "\n")
    
    # Show how this can be used to create informative command-line help
    print("Example command-line help based on tool description:")
    help_text = f"""
    {TSTCommandExecutor.name} - {TSTCommandExecutor.description}
    
    Available commands:
    """
    
    for cmd_name in tool_schema["parameters"]["properties"]["command"]["enum"]:
        cmd_info = description["supported_commands"].get(cmd_name, {})
        help_text += f"  {cmd_name} - {cmd_info.get('summary', '')}\n"
    
    print(help_text)


if __name__ == "__main__":
    asyncio.run(main()) 