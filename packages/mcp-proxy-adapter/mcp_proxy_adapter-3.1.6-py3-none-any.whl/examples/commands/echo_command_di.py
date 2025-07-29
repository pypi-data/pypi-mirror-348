"""
Example command with dependency injection.

This module demonstrates how to use dependency injection in commands.
"""

from typing import Any, Dict, List, Optional

from mcp_proxy_adapter.commands import Command, SuccessResult
from mcp_proxy_adapter.commands.result import CommandResult


class EchoCommandResult(SuccessResult):
    """
    Result of echo command execution.
    """
    
    def __init__(self, message: str, timestamp: str, **kwargs):
        """
        Initializes echo command result.
        
        Args:
            message: Echoed message
            timestamp: Time of execution
            **kwargs: Additional parameters
        """
        data = {"message": message, "timestamp": timestamp}
        data.update(kwargs)
        super().__init__(data=data, message=f"Echo response: {message}")
    
    @classmethod
    def get_schema(cls) -> Dict[str, Any]:
        """
        Returns JSON schema for result validation.
        
        Returns:
            Dictionary with JSON schema
        """
        return {
            "type": "object",
            "properties": {
                "success": {"type": "boolean"},
                "data": {
                    "type": "object",
                    "properties": {
                        "message": {"type": "string"},
                        "timestamp": {"type": "string", "format": "date-time"}
                    },
                    "required": ["message", "timestamp"]
                },
                "message": {"type": "string"}
            },
            "required": ["success", "data"]
        }


class TimeService:
    """
    Service for time-related operations.
    
    This is a dependency that will be injected into the EchoCommand.
    """
    
    def get_current_time(self) -> str:
        """
        Get current time formatted as ISO string.
        
        Returns:
            Current time as ISO formatted string
        """
        from datetime import datetime
        return datetime.now().isoformat()


class EchoCommand(Command):
    """
    Command that echoes back a message with timestamp.
    
    This command demonstrates how to use dependency injection in commands
    by accepting a service dependency in the constructor.
    """
    
    # Command name for JSON-RPC endpoint
    name = "echo_di"
    # Command result class
    result_class = EchoCommandResult
    
    def __init__(self, time_service: TimeService):
        """
        Initialize command with dependencies.
        
        Args:
            time_service: Service for getting the current time
        """
        self.time_service = time_service
    
    async def execute(self, message: str = "Hello, World!") -> CommandResult:
        """
        Executes echo command.
        
        Args:
            message: Message to echo back
            
        Returns:
            Command execution result with message and timestamp
        """
        timestamp = self.time_service.get_current_time()
        return EchoCommandResult(message=message, timestamp=timestamp)
    
    @classmethod
    def get_schema(cls) -> Dict[str, Any]:
        """
        Returns JSON schema for command parameters validation.
        
        Returns:
            Dictionary with JSON schema
        """
        return {
            "type": "object",
            "properties": {
                "message": {
                    "type": "string",
                    "description": "Message to echo back"
                }
            },
            "additionalProperties": False
        }


# Example of registering the command with dependency injection
def register_echo_command():
    """
    Register echo command with dependencies.
    
    This function shows how to:
    1. Create a service dependency
    2. Create a command instance with the dependency
    3. Register the command instance in the registry
    """
    from mcp_proxy_adapter.commands import registry, container
    
    # Create and register service in the container
    time_service = TimeService()
    container.register("time_service", time_service)
    
    # Create command with dependencies
    echo_command = EchoCommand(time_service)
    
    # Register command instance
    registry.register(echo_command)
    
    return echo_command 