"""
Math command module.

This module contains a command for performing math operations on two numbers.
"""

from typing import Dict, Any, Literal, Union

from mcp_proxy_adapter import Command, SuccessResult, ErrorResult, InvalidParamsError


class MathResult(SuccessResult):
    """
    Result of math command.
    
    Attributes:
        result (float): Result of the math operation
        operation (str): Operation that was performed
        a (float): First operand
        b (float): Second operand
    """
    
    def __init__(self, result: float, operation: str, a: float, b: float):
        """
        Initialize result.
        
        Args:
            result: Result of the operation
            operation: Operation performed
            a: First operand
            b: Second operand
        """
        self.result = result
        self.operation = operation
        self.a = a
        self.b = b
        
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert result to dictionary.
        
        Returns:
            Dictionary representation
        """
        return {
            "result": self.result,
            "operation": self.operation,
            "a": self.a,
            "b": self.b
        }
    
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
                "result": {"type": "number", "description": "Result of the operation"},
                "operation": {"type": "string", "description": "Operation performed"},
                "a": {"type": "number", "description": "First operand"},
                "b": {"type": "number", "description": "Second operand"}
            },
            "required": ["result", "operation", "a", "b"]
        }


class MathCommand(Command):
    """
    Command that performs math operations.
    
    This command demonstrates parameter validation and error handling.
    """
    
    name = "math"
    result_class = MathResult
    
    async def execute(
        self, 
        a: float, 
        b: float, 
        operation: Literal["add", "subtract", "multiply", "divide"]
    ) -> Union[MathResult, ErrorResult]:
        """
        Execute command.
        
        Args:
            a: First number
            b: Second number
            operation: Math operation to perform (add, subtract, multiply, divide)
            
        Returns:
            Math result containing the result of the operation
            
        Raises:
            InvalidParamsError: If operation is invalid or division by zero
        """
        try:
            if operation == "add":
                result = a + b
            elif operation == "subtract":
                result = a - b
            elif operation == "multiply":
                result = a * b
            elif operation == "divide":
                if b == 0:
                    raise InvalidParamsError("Division by zero is not allowed")
                result = a / b
            else:
                raise InvalidParamsError(
                    f"Invalid operation: {operation}. Must be one of: add, subtract, multiply, divide"
                )
                
            return MathResult(result, operation, a, b)
        except Exception as e:
            if not isinstance(e, InvalidParamsError):
                raise InvalidParamsError(f"Error performing math operation: {str(e)}")
            raise
    
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
                "a": {
                    "type": "number",
                    "description": "First number"
                },
                "b": {
                    "type": "number",
                    "description": "Second number"
                },
                "operation": {
                    "type": "string",
                    "enum": ["add", "subtract", "multiply", "divide"],
                    "description": "Math operation to perform"
                }
            },
            "required": ["a", "b", "operation"],
            "additionalProperties": False
        } 