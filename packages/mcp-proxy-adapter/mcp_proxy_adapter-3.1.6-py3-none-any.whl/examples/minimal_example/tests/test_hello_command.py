"""
Unit tests for the HelloCommand in the minimal example.
"""

import pytest

from simple_server import HelloCommand, HelloResult


class TestHelloCommand:
    """Tests for HelloCommand class."""
    
    @pytest.mark.asyncio
    async def test_execute_with_default_name(self):
        """Test HelloCommand.execute with default name parameter."""
        # Create command instance
        command = HelloCommand()
        
        # Execute command with default parameter
        result = await command.execute()
        
        # Check result type
        assert isinstance(result, HelloResult)
        
        # Check message content
        assert result.message == "Hello, World!"
        
        # Check serialization
        assert result.to_dict() == {"message": "Hello, World!"}
    
    @pytest.mark.asyncio
    async def test_execute_with_custom_name(self):
        """Test HelloCommand.execute with custom name parameter."""
        # Create command instance
        command = HelloCommand()
        
        # Execute command with custom parameter
        result = await command.execute(name="Test")
        
        # Check result
        assert isinstance(result, HelloResult)
        assert result.message == "Hello, Test!"
        
        # Check serialization
        assert result.to_dict() == {"message": "Hello, Test!"}
    
    @pytest.mark.asyncio
    async def test_execute_with_empty_name(self):
        """Test HelloCommand.execute with empty name parameter."""
        # Create command instance
        command = HelloCommand()
        
        # Execute command with empty parameter
        result = await command.execute(name="")
        
        # Check result
        assert isinstance(result, HelloResult)
        assert result.message == "Hello, !"
        
        # Check serialization
        assert result.to_dict() == {"message": "Hello, !"}


class TestHelloResult:
    """Tests for HelloResult class."""
    
    def test_init(self):
        """Test HelloResult initialization."""
        # Create result instance
        result = HelloResult("Hello, Test!")
        
        # Check attributes
        assert result.message == "Hello, Test!"
    
    def test_to_dict(self):
        """Test HelloResult.to_dict method."""
        # Create result instance
        result = HelloResult("Hello, Test!")
        
        # Check serialization
        assert result.to_dict() == {"message": "Hello, Test!"}
    
    def test_get_schema(self):
        """Test HelloResult.get_schema method."""
        # Get schema
        schema = HelloResult.get_schema()
        
        # Check schema structure
        assert schema["type"] == "object"
        assert "properties" in schema
        assert "message" in schema["properties"]
        assert schema["properties"]["message"]["type"] == "string"
        assert "required" in schema
        assert "message" in schema["required"]
        

class TestHelloCommandSchema:
    """Tests for HelloCommand schema."""
    
    def test_get_schema(self):
        """Test HelloCommand.get_schema method."""
        # Get schema
        schema = HelloCommand.get_schema()
        
        # Check schema structure
        assert schema["type"] == "object"
        assert "properties" in schema
        assert "name" in schema["properties"]
        assert schema["properties"]["name"]["type"] == "string"
        assert "additionalProperties" in schema
        assert schema["additionalProperties"] is False 