"""
Module for testing help command.
"""

import pytest
from mcp_proxy_adapter.commands.help_command import HelpCommand, HelpResult
from mcp_proxy_adapter.commands.command_registry import CommandRegistry
from mcp_proxy_adapter.commands.base import Command
from mcp_proxy_adapter.commands.result import CommandResult


# Test result classes
class MockResult1(CommandResult):
    """Test result 1."""
    
    def to_dict(self) -> dict:
        return {"result": "test1"}
    
    @classmethod
    def get_schema(cls) -> dict:
        return {"type": "object"}


class MockResult2(CommandResult):
    """Test result 2."""
    
    def to_dict(self) -> dict:
        return {"result": "test2"}
    
    @classmethod
    def get_schema(cls) -> dict:
        return {"type": "object"}


# Create test commands
class MockCommand1(Command):
    """Test command 1."""
    
    name = "test1"
    result_class = MockResult1
    
    async def execute(self) -> MockResult1:
        """Execute test command 1."""
        return MockResult1()


class MockCommand2(Command):
    """Test command 2."""
    
    name = "test2"
    result_class = MockResult2
    
    async def execute(self, param: str) -> MockResult2:
        """
        Execute test command 2.
        
        Args:
            param: Test parameter
        """
        return MockResult2()


# Special HelpCommand for testing that uses provided registry
class MockHelpCommand(HelpCommand):
    """Help command for testing that uses provided registry."""
    
    def __init__(self, registry):
        self.registry = registry
        super().__init__()
    
    async def execute(self, cmdname: str = None) -> HelpResult:
        """
        Execute help command with test registry.
        
        Args:
            cmdname: Name of the command to get information about (optional)
            
        Returns:
            HelpResult: Help command result
        """
        # If cmdname is provided, return information about specific command
        if cmdname:
            try:
                # Get command metadata from registry
                command_metadata = self.registry.get_command_metadata(cmdname)
                return HelpResult(command_info=command_metadata)
            except Exception as e:
                # If command not found, raise error
                raise type(e)(f"Command '{cmdname}' not found")
        
        # Otherwise, return information about all available commands
        
        # Get metadata for all commands
        all_metadata = self.registry.get_all_metadata()
        
        # Prepare response format with tool metadata
        result = {
            "tool_info": {
                "name": "MCP-Proxy API Service",
                "description": "JSON-RPC API for microservice command execution",
                "version": "1.0.0"
            },
            "help_usage": {
                "description": "Get information about commands",
                "examples": [
                    {"command": "help", "description": "List of all available commands"},
                    {"command": "help", "params": {"cmdname": "command_name"}, "description": "Get detailed information about a specific command"}
                ]
            },
            "commands": {}
        }
        
        # Add brief information about commands
        for name, metadata in all_metadata.items():
            result["commands"][name] = {
                "summary": metadata["summary"],
                "params_count": len(metadata["params"])
            }
        
        return HelpResult(commands_info=result)


@pytest.fixture
def test_registry():
    """Fixture for creating registry with test commands."""
    registry = CommandRegistry()
    registry.register(MockCommand1)
    registry.register(MockCommand2)
    registry.register(HelpCommand)
    return registry


@pytest.mark.asyncio
async def test_help_command_without_params(test_registry):
    """Test help command without parameters."""
    help_command = MockHelpCommand(test_registry)
    result = await help_command.execute()
    
    # Check response structure
    data = result.to_dict()
    assert "tool_info" in data
    assert "commands" in data
    assert "total" in data
    assert "note" in data
    
    # Check commands information
    assert "test1" in data["commands"]
    assert "test2" in data["commands"]
    assert "help" in data["commands"]
    
    # Check commands count
    assert data["total"] == 3
    
    # Check tool info
    assert "name" in data["tool_info"]
    assert "description" in data["tool_info"]
    assert "version" in data["tool_info"]
    
    # Check help usage
    assert "help_usage" in data
    assert "examples" in data["help_usage"]
    assert len(data["help_usage"]["examples"]) > 0


@pytest.mark.asyncio
async def test_help_command_with_cmdname(test_registry):
    """Test help command with cmdname parameter."""
    help_command = MockHelpCommand(test_registry)
    result = await help_command.execute(cmdname="test2")
    
    # Check response structure
    data = result.to_dict()
    assert "cmdname" in data
    assert "info" in data
    
    # Check command information
    assert data["cmdname"] == "test2"
    assert "description" in data["info"]
    assert "summary" in data["info"]
    assert "params" in data["info"]
    assert "examples" in data["info"]
    
    # Check parameters
    assert "param" in data["info"]["params"]
    assert data["info"]["params"]["param"]["required"] is True
    
    # Check examples
    assert len(data["info"]["examples"]) > 0
    assert any(example.get("command") == "test2" for example in data["info"]["examples"])


@pytest.mark.asyncio
async def test_help_command_with_invalid_cmdname(test_registry):
    """Test help command with invalid cmdname parameter."""
    help_command = MockHelpCommand(test_registry)
    
    # Check that NotFoundError is raised for invalid command name
    with pytest.raises(Exception) as excinfo:
        await help_command.execute(cmdname="invalid_command")
    
    # Error message should contain invalid command name
    assert "invalid_command" in str(excinfo.value) 