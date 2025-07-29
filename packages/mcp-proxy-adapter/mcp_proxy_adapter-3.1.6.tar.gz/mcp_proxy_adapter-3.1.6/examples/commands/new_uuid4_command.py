"""
Module for the new_uuid4 command implementation.
"""

import uuid
from typing import Any, Dict

from mcp_proxy_adapter.commands.base import Command
from mcp_proxy_adapter.commands.result import CommandResult
from mcp_proxy_adapter.commands.command_registry import registry
from mcp_proxy_adapter.core.logging import logger


class NewUuid4Result(CommandResult):
    """Result of UUID4 generation"""
    
    def __init__(self, uuid_str: str):
        """
        Initialize the NewUuid4Result.
        
        Args:
            uuid_str: UUID in string format
        """
        self.uuid = uuid_str
        
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the result to a dictionary.
        
        Returns:
            Dictionary with the UUID
        """
        return {"uuid": self.uuid}
    
    @classmethod
    def get_schema(cls) -> Dict[str, Any]:
        """
        Get the JSON schema for this result.
        
        Returns:
            JSON schema
        """
        return {
            "type": "object",
            "required": ["uuid"],
            "properties": {
                "uuid": {
                    "type": "string",
                    "description": "Generated UUID4 in string format",
                    "pattern": "^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$"
                }
            }
        }


class NewUuid4Command(Command):
    """
    Command that generates a new UUID version 4 (random).
    """
    
    name = "new_uuid4"
    
    async def execute(self) -> NewUuid4Result:
        """
        Execute the new_uuid4 command.
        
        Returns:
            NewUuid4Result: Result with UUID in string format
        """
        # Generate a UUID4
        uuid_str = str(uuid.uuid4())
        
        logger.debug(f"Generated UUID4: {uuid_str}")
        return NewUuid4Result(uuid_str=uuid_str)
    
    @classmethod
    def get_schema(cls) -> Dict[str, Any]:
        """
        Get the JSON schema for this command.
        
        Returns:
            JSON schema
        """
        return {
            "type": "object",
            "properties": {}
        }


# Register the command
registry.register(NewUuid4Command) 