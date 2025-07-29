"""
Echo command module.

This module contains a simple echo command that returns the input message.
"""

from typing import Dict, Any

from mcp_proxy_adapter import Command, SuccessResult


class EchoResult(SuccessResult):
    """
    Result of echo command.
    
    Attributes:
        message (str): Echo message
    """
    
    def __init__(self, message: str):
        """
        Initialize result.
        
        Args:
            message: Message to echo back
        """
        self.message = message
        
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert result to dictionary.
        
        Returns:
            Dictionary representation
        """
        return {"message": self.message}
    
    @classmethod
    def get_schema(cls) -> Dict[str, Any]:
        """
        Get JSON schema for result.
        
        Returns:
            JSON schema
        """
        return {
            "type": "object",
            "properties": {
                "message": {"type": "string", "description": "Echo message"}
            },
            "required": ["message"]
        }


class EchoCommand(Command):
    """
    Command that echoes back input message.
    
    This command demonstrates simple parameter handling.
    """
    
    name = "echo"
    result_class = EchoResult
    
    async def execute(self, message: str) -> EchoResult:
        """
        Execute command.
        
        Args:
            message: Message to echo back
            
        Returns:
            Echo result containing the input message
        """
        return EchoResult(message)
    
    @classmethod
    def get_schema(cls) -> Dict[str, Any]:
        """
        Get JSON schema for command parameters.
        
        Returns:
            JSON schema
        """
        return {
            "type": "object",
            "properties": {
                "message": {
                    "type": "string",
                    "description": "Message to echo back"
                }
            },
            "required": ["message"],
            "additionalProperties": False
        } 