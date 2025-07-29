"""
Main application module.
"""

import os
import sys
import uvicorn
import logging

from mcp_proxy_adapter import create_app

app = create_app()
from mcp_proxy_adapter.config import config
from mcp_proxy_adapter.core.logging import logger, setup_logging


def main():
    """
    Main function to run the application.
    """
    # Убедимся что логирование настроено
    logger.info("Initializing logging configuration")
    
    try:
        # Получаем настройки логирования
        log_level = config.get("logging.level", "INFO")
        log_file = config.get("logging.file")
        rotation_type = config.get("logging.rotation.type", "size")
        
        # Выводим информацию о настройках логирования
        logger.info(f"Log level: {log_level}")
        if log_file:
            logger.info(f"Log file: {log_file}")
            logger.info(f"Log rotation type: {rotation_type}")
            
            if rotation_type.lower() == "time":
                when = config.get("logging.rotation.when", "D")
                interval = config.get("logging.rotation.interval", 1)
                logger.info(f"Log rotation: every {interval} {when}")
            else:
                max_bytes = config.get("logging.rotation.max_bytes", 10 * 1024 * 1024)
                logger.info(f"Log rotation: when size reaches {max_bytes / (1024*1024):.1f} MB")
                
            backup_count = config.get("logging.rotation.backup_count", 5)
            logger.info(f"Log backups: {backup_count}")
        else:
            logger.info("File logging is disabled")
            
        # Get server settings
        host = config.get("server.host", "0.0.0.0")
        port = config.get("server.port", 8000)
        
        logger.info(f"Starting server on {host}:{port}")
        
        # Run server
        uvicorn.run(
            "mcp_proxy_adapter.api.app:app",
            host=host,
            port=port,
            reload=True if os.environ.get("DEBUG") else False,
            log_level=log_level.lower()
        )
    except Exception as e:
        logger.exception(f"Error during application startup: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
