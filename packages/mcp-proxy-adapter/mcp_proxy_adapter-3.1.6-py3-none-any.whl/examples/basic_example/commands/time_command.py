"""
Time command module.

This module contains a command for getting current time in different formats and timezones.
"""

import datetime
from typing import Dict, Any, Optional

import pytz

from mcp_proxy_adapter import Command, SuccessResult, InvalidParamsError


class TimeResult(SuccessResult):
    """
    Result of time command.
    
    Attributes:
        time (str): Formatted time string
        timestamp (int): Unix timestamp
        timezone (str): Timezone used
        format (str): Format string used
    """
    
    def __init__(self, time: str, timestamp: int, timezone: str, format: str):
        """
        Initialize result.
        
        Args:
            time: Formatted time string
            timestamp: Unix timestamp
            timezone: Timezone used
            format: Format string used
        """
        self.time = time
        self.timestamp = timestamp
        self.timezone = timezone
        self.format = format
        
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert result to dictionary.
        
        Returns:
            Dictionary representation
        """
        return {
            "time": self.time,
            "timestamp": self.timestamp,
            "timezone": self.timezone,
            "format": self.format
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
                "time": {"type": "string", "description": "Formatted time string"},
                "timestamp": {"type": "integer", "description": "Unix timestamp"},
                "timezone": {"type": "string", "description": "Timezone used"},
                "format": {"type": "string", "description": "Format string used"}
            },
            "required": ["time", "timestamp", "timezone", "format"]
        }


class TimeCommand(Command):
    """
    Command that returns current time.
    
    This command demonstrates optional parameters and timezone handling.
    """
    
    name = "time"
    result_class = TimeResult
    
    async def execute(
        self, 
        format: str = "%Y-%m-%d %H:%M:%S",
        timezone: str = "UTC"
    ) -> TimeResult:
        """
        Execute command.
        
        Args:
            format: Time format string (strftime format)
            timezone: Timezone name (e.g., "UTC", "Europe/London")
            
        Returns:
            Time result with formatted time
            
        Raises:
            InvalidParamsError: If timezone is invalid
        """
        try:
            # Validate timezone
            if timezone not in pytz.all_timezones:
                raise InvalidParamsError(f"Invalid timezone: {timezone}")
            
            # Get current time in the specified timezone
            tz = pytz.timezone(timezone)
            now = datetime.datetime.now(tz)
            
            # Format time according to the format string
            formatted_time = now.strftime(format)
            
            # Get Unix timestamp
            timestamp = int(now.timestamp())
            
            return TimeResult(
                time=formatted_time,
                timestamp=timestamp,
                timezone=timezone,
                format=format
            )
        except Exception as e:
            if not isinstance(e, InvalidParamsError):
                raise InvalidParamsError(f"Error processing time: {str(e)}")
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
                "format": {
                    "type": "string",
                    "description": "Time format string (strftime format)",
                    "default": "%Y-%m-%d %H:%M:%S"
                },
                "timezone": {
                    "type": "string",
                    "description": "Timezone name (e.g., 'UTC', 'Europe/London')",
                    "default": "UTC"
                }
            },
            "additionalProperties": False
        } 