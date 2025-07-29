"""
Complete MCP Microservice example.

This example demonstrates a complete microservice application with Docker support,
environment-specific configuration, and multiple commands.
"""

import os
import sys
import argparse
from pathlib import Path
import uvicorn
from mcp_proxy_adapter.api.app import create_app
from mcp_proxy_adapter.commands.command_registry import registry
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
    parser = argparse.ArgumentParser(description="MCP Complete Example")
    parser.add_argument(
        "--config",
        default="configs/config.dev.yaml",
        help="Path to configuration file"
    )
    return parser.parse_args()


def ensure_directories():
    """
    Create necessary directories based on configuration.
    """
    base_dir = os.path.dirname(os.path.abspath(__file__))
    os.makedirs(os.path.join(base_dir, "logs"), exist_ok=True)
    os.makedirs(os.path.join(base_dir, "cache"), exist_ok=True)
    os.makedirs(os.path.join(base_dir, "data"), exist_ok=True)


def setup_application(config_file=None):
    """
    Setup and configure the microservice application.
    
    Args:
        config_file: Path to configuration file (optional)
        
    Returns:
        Configured FastAPI application
    """
    if config_file is None:
        args = parse_args()
        config_file = args.config
    current_dir = Path(__file__).parent.absolute()
    config_path = current_dir / config_file
    if not config_path.exists():
        config_path = current_dir / "config.json"
    ensure_directories()
    if config_path.exists():
        config.load_from_file(str(config_path))
        logger.info(f"Loaded configuration from {config_path}")
    else:
        logger.warning(f"Configuration file {config_path} not found, using defaults")
    app = create_app()
    app.title = "Complete MCP Microservice Example"
    app.description = "Full-featured microservice with Docker support"
    app.version = "1.0.0"
    # Discover and register commands from the commands directory
    package_path = "commands"
    try:
        registered_commands = registry.get_all_commands()
        for cmd_name in list(registered_commands.keys()):
            try:
                registry.unregister(cmd_name)
            except Exception as e:
                logger.debug(f"Error unregistering command {cmd_name}: {e}")
        registry.discover_commands(package_path)
        logger.info(f"Discovered commands from package: {package_path}")
    except Exception as e:
        logger.error(f"Error discovering commands: {e}")
    return app


def main():
    """Run microservice with command discovery."""
    log_level = config.get("logging.level", "INFO")
    setup_logging(log_level)
    app = setup_application()
    host = config.get("server.host", "0.0.0.0")
    port = config.get("server.port", 8000)
    if "TEST_SERVER_PORT" in os.environ:
        port = int(os.environ["TEST_SERVER_PORT"])
        logger.info(f"Using test port from environment: {port}")
    logger.info(f"Starting server on {host}:{port}")
    debug = config.get("server.debug", False)
    uvicorn.run(
        app,
        host=host,
        port=port,
        reload=debug,
        log_level=log_level.lower()
    )


if __name__ == "__main__":
    main() 