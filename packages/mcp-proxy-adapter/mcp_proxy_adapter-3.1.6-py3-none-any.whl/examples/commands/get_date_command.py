"""
Module for the get_date command implementation.
"""

from datetime import datetime
from typing import Any, Dict

from mcp_proxy_adapter.commands.base import Command
from mcp_proxy_adapter.commands.result import CommandResult
from mcp_proxy_adapter.commands.command_registry import registry
from mcp_proxy_adapter.core.logging import logger


class GetDateResult(CommandResult):
    """Result of getting current date"""
    
    def __init__(self, date: str):
        """
        Initialize the GetDateResult.
        
        Args:
            date: Date in ISO 8601 format
        """
        self.date = date
        
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the result to a dictionary.
        
        Returns:
            Dictionary with the date
        """
        return {"date": self.date}
    
    @classmethod
    def get_schema(cls) -> Dict[str, Any]:
        """
        Get the JSON schema for this result.
        
        Returns:
            JSON schema
        """
        return {
            "type": "object",
            "required": ["date"],
            "properties": {
                "date": {
                    "type": "string",
                    "description": "Current date and time in ISO 8601 format",
                    "pattern": "^\\d{4}-\\d{2}-\\d{2}T\\d{2}:\\d{2}:\\d{2}[+-]\\d{2}:?\\d{2}$"
                }
            }
        }


class GetDateCommand(Command):
    """
    Command that returns the current date and time in ISO 8601 format.
    """
    
    name = "get_date"
    
    async def execute(self) -> GetDateResult:
        """
        Execute the get_date command.
        
        Returns:
            GetDateResult: Result with date in ISO 8601 format
        """
        # Get current time with timezone info
        now = datetime.now().astimezone()
        
        # Format to ISO 8601
        date_str = now.strftime("%Y-%m-%dT%H:%M:%S%z")
        
        # Insert colon in timezone offset (e.g. +0300 -> +03:00)
        if len(date_str) >= 6:
            date_str = date_str[:-2] + ":" + date_str[-2:]
            
        logger.debug(f"Generated date: {date_str}")
        return GetDateResult(date=date_str)
    
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
registry.register(GetDateCommand) 