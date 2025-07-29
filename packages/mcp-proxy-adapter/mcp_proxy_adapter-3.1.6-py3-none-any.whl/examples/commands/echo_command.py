"""
Module with echo command implementation.
"""

from typing import Any, Dict, Optional, ClassVar, Type

from pydantic import BaseModel, Field, ValidationError as PydanticValidationError

from mcp_proxy_adapter.commands.base import Command
from examples.commands.echo_result import EchoResult
from mcp_proxy_adapter.core.errors import ValidationError
from mcp_proxy_adapter.core.logging import logger


class EchoCommand(Command):
    """
    Command that echoes back the parameters it receives.
    
    This command is useful for testing parameter passing and debugging.
    """
    
    name: ClassVar[str] = "echo"
    result_class: ClassVar[Type[EchoResult]] = EchoResult
    
    @classmethod
    def get_schema(cls) -> Dict[str, Any]:
        """
        Returns JSON schema for command parameters validation.
        
        Returns:
            Dictionary with JSON schema.
        """
        return {
            "type": "object",
            "additionalProperties": True,
            "description": "Any parameters will be echoed back in the response"
        }
    
    async def execute(self, **kwargs) -> EchoResult:
        """
        Executes echo command and returns the parameters back.
        
        Args:
            **kwargs: Any parameters to echo back.
            
        Returns:
            EchoResult: Command execution result with the parameters.
        """
        logger.debug(f"Echo command received parameters: {kwargs}")
        
        # Simply return the parameters that were passed
        return EchoResult(params=kwargs) 