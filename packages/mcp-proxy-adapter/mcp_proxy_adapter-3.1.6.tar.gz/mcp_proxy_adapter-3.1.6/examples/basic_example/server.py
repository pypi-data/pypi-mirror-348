"""
Basic MCP Proxy Adapter example.

This example demonstrates how to use MCP Proxy Adapter to create
a microservice with multiple commands organized in separate files.
"""

import os
import sys
import json
import argparse
import uvicorn
from typing import Dict, Any
from pathlib import Path

from mcp_proxy_adapter import Command, CommandResult, registry
from mcp_proxy_adapter.api.app import create_app
from mcp_proxy_adapter.config import config
from mcp_proxy_adapter.core.logging import logger, setup_logging

# Add commands directory to path for local imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def parse_args():
    """
    Parse command line arguments.
    
    Returns:
        Parsed arguments
    """
    parser = argparse.ArgumentParser(description="Basic MCP Microservice Example")
    parser.add_argument(
        "--config", 
        default="config.json",
        help="Path to configuration file (default: config.json)"
    )
    return parser.parse_args()


def setup_application(config_file=None):
    """
    Настраивает и возвращает FastAPI приложение.
    """
    # Get config file path
    if config_file is None:
        args = parse_args()
        config_file = args.config
    
    # Get absolute paths
    current_dir = Path(__file__).parent.absolute()
    config_path = current_dir / config_file
    
    # Try alternative config file if specified one doesn't exist
    if not config_path.exists() and config_file != "config.json":
        fallback_path = current_dir / "config.json"
        if fallback_path.exists():
            logger.warning(f"Config file {config_path} not found, using {fallback_path} instead")
            config_path = fallback_path
    
    # Create log directory if it doesn't exist
    logs_dir = current_dir / "logs"
    logs_dir.mkdir(exist_ok=True)
    
    # Load configuration if config file exists
    if config_path.exists():
        # Make sure we're only loading JSON files
        if not str(config_path).lower().endswith('.json'):
            logger.warning(f"Config file {config_path} is not a JSON file, only JSON format is supported")
            config_path = current_dir / "config.json"
            if not config_path.exists():
                logger.warning(f"Default config.json not found, using default values")
        
        if config_path.exists():
            config.load_from_file(str(config_path))
            logger.info(f"Loaded configuration from {config_path}")
    else:
        logger.warning(f"Configuration file {config_path} not found, using defaults")
    
    # Create FastAPI app
    app = create_app()
    app.title = "Basic MCP Proxy Adapter Example"
    app.description = "Example microservice with multiple commands using MCP Proxy Adapter"
    app.version = "1.0.0"
    
    # Discover and register commands from the commands directory
    package_path = "commands"
    try:
        # Clear existing commands to prevent conflicts in test environment
        registered_commands = registry.get_all_commands()
        for cmd_name in list(registered_commands.keys()):
            try:
                registry.unregister(cmd_name)
            except Exception as e:
                logger.debug(f"Error unregistering command {cmd_name}: {e}")
        
        # Discover and register commands
        registry.discover_commands(package_path)
        logger.info(f"Discovered commands from package: {package_path}")
    except Exception as e:
        logger.error(f"Error discovering commands: {e}")
    
    return app


def main():
    """Run microservice with command discovery."""
    # Setup logging
    log_level = config.get("logging.level", "INFO")
    setup_logging(log_level)
    
    # Initialize application
    app = setup_application()
    
    # Get server configuration
    host = config.get("server.host", "localhost")
    port = config.get("server.port", 8000)
    
    # Check if port is overridden by environment variable (for testing)
    if "TEST_SERVER_PORT" in os.environ:
        port = int(os.environ["TEST_SERVER_PORT"])
        logger.info(f"Using test port from environment: {port}")
    
    # Run server
    logger.info(f"Starting server on {host}:{port}")
    
    debug = config.get("server.debug", False)
    
    if debug:
        # In debug mode, run with hot reload using import string
        uvicorn.run(
            "server:setup_application",
            host=host,
            port=port,
            reload=True,
            factory=True,
            log_level=config.get("logging.level", "info").lower()
        )
    else:
        # In normal mode, run with app instance
        uvicorn.run(
            app,
            host=host,
            port=port,
            reload=False,
            log_level=config.get("logging.level", "info").lower()
        )


if __name__ == "__main__":
    main() 