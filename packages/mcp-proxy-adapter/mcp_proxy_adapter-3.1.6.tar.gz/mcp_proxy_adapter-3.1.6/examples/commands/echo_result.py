"""
Module with result class for echo command.
"""

from typing import Any, Dict, ClassVar, Type
from pydantic import BaseModel, Field

from mcp_proxy_adapter.commands.result import CommandResult


class EchoResult(CommandResult, BaseModel):
    """
    Result of echo command execution.
    
    Attributes:
        params (Dict[str, Any]): Parameters that were passed to the command.
    """
    
    params: Dict[str, Any] = Field(..., description="Parameters that were passed to the command")
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Converts result to dictionary for serialization.

        Returns:
            Dictionary with result data.
        """
        return {
            "params": self.params
        }
    
    @classmethod
    def get_schema(cls) -> Dict[str, Any]:
        """
        Returns JSON schema for result validation.

        Returns:
            Dictionary with JSON schema.
        """
        return {
            "type": "object",
            "properties": {
                "params": {
                    "type": "object", 
                    "description": "Parameters that were passed to the command",
                    "additionalProperties": True
                }
            },
            "required": ["params"]
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "EchoResult":
        """
        Creates result instance from dictionary.

        Args:
            data: Dictionary with result data.

        Returns:
            EchoResult instance.
        """
        return cls(
            params=data.get("params", {})
        ) 