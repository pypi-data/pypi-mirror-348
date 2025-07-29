"""
ANTI-PATTERN EXAMPLE: Global State

This module demonstrates an anti-pattern where a command uses global state
to store and share data between executions.

WARNING: This is a BAD EXAMPLE! Do not use this approach in production.
"""

from typing import Dict, Any, Optional

from mcp_proxy_adapter import Command, SuccessResult


# Global state - an anti-pattern that creates hidden dependencies
# and makes the code hard to test and maintain
GLOBAL_STATE: Dict[str, Any] = {}


class StateResult(SuccessResult):
    """Result of state command."""
    
    def __init__(self, key: str, value: Any):
        """
        Initialize result.
        
        Args:
            key: The key accessed
            value: The value retrieved
        """
        self.key = key
        self.value = value
        
    def to_dict(self) -> Dict[str, Any]:
        """Convert result to dictionary."""
        return {
            "key": self.key,
            "value": self.value
        }
    
    @classmethod
    def get_schema(cls) -> Dict[str, Any]:
        """Get JSON schema for result."""
        return {
            "type": "object",
            "properties": {
                "key": {"type": "string"},
                "value": {"type": "string"}
            },
            "required": ["key"]
        }


class GlobalStateCommand(Command):
    """
    ANTI-PATTERN: This command uses global state.
    
    It stores and retrieves values from a global dictionary,
    creating hidden dependencies and making the code:
    - Not thread-safe
    - Hard to test
    - Prone to unexpected behavior
    - Difficult to reason about
    """
    
    name = "global_state"
    result_class = StateResult
    
    async def execute(self, key: str, value: Any = None) -> StateResult:
        """
        Execute global state command.
        
        Args:
            key: Key to get or set
            value: Value to set (if not None)
        
        Returns:
            Result with key and current value
        """
        # Get or set value in global state
        if value is not None:
            # Set the value in the global state
            GLOBAL_STATE[key] = value
            
        # Return the current value (which might be None if the key doesn't exist)
        current_value = GLOBAL_STATE.get(key)
        return StateResult(key, current_value)
    
    @classmethod
    def get_schema(cls) -> Dict[str, Any]:
        """Get JSON schema for command parameters."""
        return {
            "type": "object",
            "properties": {
                "key": {
                    "type": "string",
                    "description": "Key to get or set"
                },
                "value": {
                    "type": ["string", "number", "boolean", "null", "array", "object"],
                    "description": "Value to set (optional)"
                }
            },
            "required": ["key"]
        }


# Even worse: Command with mixed global and instance state
class MixedStateCommand(Command):
    """
    ANTI-PATTERN: This command mixes global and instance state.
    
    It's even worse than just global state because it creates confusion
    about where state is stored and how it's accessed.
    """
    
    name = "mixed_state"
    result_class = StateResult
    
    def __init__(self):
        """Initialize with instance-specific counter."""
        self._counter = 0  # Instance state
    
    async def execute(self, key: str, value: Any = None, increment: bool = False) -> StateResult:
        """
        Execute mixed state command.
        
        Args:
            key: Key to get or set
            value: Value to set (if not None)
            increment: Whether to increment the instance counter
        
        Returns:
            Result with key and current value
        """
        # Instance state modification
        if increment:
            self._counter += 1
        
        # Global state modification - mixing different state types!
        if value is not None:
            # Set in global state
            GLOBAL_STATE[key] = value
            
        # Mix instance state with the value
        if self._counter > 0:
            # Modify value based on instance state
            if isinstance(GLOBAL_STATE.get(key), (int, float)):
                GLOBAL_STATE[key] = GLOBAL_STATE.get(key, 0) + self._counter
        
        # Return the current value (which might be None if the key doesn't exist)
        current_value = GLOBAL_STATE.get(key)
        return StateResult(key, current_value)


# Example of how this causes problems:
# Both commands modify the same global state, which creates hidden dependencies
# and makes behavior unpredictable, especially with concurrent requests.

# Usage example (don't do this!):
#
# # Command 1 sets a value
# await GlobalStateCommand().execute("user_count", 10)
#
# # Command 2 also modifies the same value
# await MixedStateCommand().execute("user_count", 5)
#
# # Command 1 reads the value but gets a result it didn't expect
# result = await GlobalStateCommand().execute("user_count")
# # result.value might be 5 instead of 10! 