"""
Example of using dependency injection in a microservice.

This example demonstrates how to:
1. Create service dependencies
2. Configure a dependency container
3. Register commands with dependencies
4. Run a microservice with dependency injection
"""

import asyncio
import logging
import os
from typing import Dict, List, Any

import uvicorn
from fastapi import FastAPI

from mcp_proxy_adapter import create_app
from mcp_proxy_adapter.commands import registry, container
from examples.commands.echo_command_di import EchoCommand, TimeService


class DatabaseService:
    """
    Mock database service as an example dependency.
    """
    
    def __init__(self, connection_string: str):
        """
        Initialize database service.
        
        Args:
            connection_string: Database connection string
        """
        self.connection_string = connection_string
        self.is_connected = False
        self.data = {}
        
    async def connect(self):
        """Connect to the database."""
        # Simulate connection delay
        await asyncio.sleep(0.1)
        self.is_connected = True
        print(f"Connected to database: {self.connection_string}")
        
    async def disconnect(self):
        """Disconnect from the database."""
        if self.is_connected:
            # Simulate disconnection delay
            await asyncio.sleep(0.1)
            self.is_connected = False
            print("Disconnected from database")
    
    def get_item(self, key: str) -> Any:
        """Get item from the database."""
        if not self.is_connected:
            raise RuntimeError("Not connected to database")
        return self.data.get(key)
    
    def set_item(self, key: str, value: Any):
        """Set item in the database."""
        if not self.is_connected:
            raise RuntimeError("Not connected to database")
        self.data[key] = value


class ConfigService:
    """
    Configuration service as an example dependency.
    """
    
    def __init__(self, config_path: str = None):
        """
        Initialize configuration service.
        
        Args:
            config_path: Path to config file (optional)
        """
        self.config_path = config_path
        self.config = {
            "app_name": "DI Example",
            "version": "1.0.0",
            "debug": True
        }
        
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value."""
        return self.config.get(key, default)
        
    def set(self, key: str, value: Any):
        """Set configuration value."""
        self.config[key] = value


class DataCommand(EchoCommand):
    """
    Command that uses multiple dependencies.
    
    This command demonstrates using multiple injected dependencies.
    """
    
    name = "data"
    
    def __init__(self, time_service: TimeService, db_service: DatabaseService, config: ConfigService):
        """
        Initialize command with multiple dependencies.
        
        Args:
            time_service: Service for time operations
            db_service: Service for database operations
            config: Service for configuration
        """
        super().__init__(time_service)
        self.db_service = db_service
        self.config = config
        
    async def execute(self, action: str = "get", key: str = "data", value: str = None) -> Any:
        """
        Execute data command.
        
        Args:
            action: Operation to perform (get or set)
            key: Data key
            value: Data value (for set operation)
            
        Returns:
            Command result
        """
        timestamp = self.time_service.get_current_time()
        
        if action == "get":
            result = self.db_service.get_item(key)
            return EchoCommand.result_class(
                message=f"Got {key}: {result}",
                timestamp=timestamp,
                data=result
            )
        elif action == "set" and value is not None:
            self.db_service.set_item(key, value)
            return EchoCommand.result_class(
                message=f"Set {key} to {value}",
                timestamp=timestamp,
                data={key: value}
            )
        else:
            return EchoCommand.result_class(
                message=f"Invalid action: {action}",
                timestamp=timestamp,
                error="invalid_action"
            )
    
    @classmethod
    def get_schema(cls) -> Dict[str, Any]:
        """Returns JSON schema for command parameters."""
        return {
            "type": "object",
            "properties": {
                "action": {
                    "type": "string",
                    "enum": ["get", "set"],
                    "description": "Action to perform on data"
                },
                "key": {
                    "type": "string",
                    "description": "Data key"
                },
                "value": {
                    "type": ["string", "null"],
                    "description": "Data value (for set action)"
                }
            },
            "required": ["action", "key"]
        }


async def setup_services():
    """Set up and register all services in the container."""
    # Create services
    time_service = TimeService()
    db_service = DatabaseService("sqlite://:memory:")
    config_service = ConfigService()
    
    # Connect to database
    await db_service.connect()
    
    # Register in container
    container.register("time_service", time_service)
    container.register("db_service", db_service)
    container.register("config", config_service)
    
    return {
        "time_service": time_service,
        "db_service": db_service,
        "config": config_service
    }


def register_commands(services):
    """Register commands with dependencies."""
    # Create command instances with dependencies
    echo_command = EchoCommand(services["time_service"])
    data_command = DataCommand(
        services["time_service"],
        services["db_service"],
        services["config"]
    )
    
    # Register commands
    registry.register(echo_command)
    registry.register(data_command)


async def main():
    """Run the example server with dependency injection."""
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    
    # Setup services
    services = await setup_services()
    
    # Register commands with their dependencies
    register_commands(services)
    
    # Create FastAPI app with MCP adapter
    app = create_app()
    
    # Add startup and shutdown events
    @app.on_event("shutdown")
    async def shutdown_event():
        # Disconnect database on shutdown
        await services["db_service"].disconnect()
    
    # Run the server
    config = uvicorn.Config(
        app=app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )
    server = uvicorn.Server(config)
    await server.serve()


if __name__ == "__main__":
    asyncio.run(main()) 