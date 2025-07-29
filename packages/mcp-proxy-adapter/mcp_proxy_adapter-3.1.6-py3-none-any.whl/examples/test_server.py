#!/usr/bin/env python3
"""
Тестовый скрипт для запуска сервера JSON-RPC с использованием MCP Proxy Adapter.
Использует только базовую команду для тестирования установки пакета.
"""

import os
import argparse
import sys
import uvicorn
from pathlib import Path
from typing import Dict, Any, Optional

# Добавляем родительскую директорию в PYTHONPATH для импорта mcp_proxy_adapter
sys.path.insert(0, str(Path(__file__).parent.parent))

from mcp_proxy_adapter import Command, SuccessResult, create_app, registry
from mcp_proxy_adapter.core.logging import setup_logging
from mcp_proxy_adapter.config import config


class HelloResult(SuccessResult):
    """Result of hello command."""
    
    def __init__(self, message: str):
        """
        Initialize result.
        
        Args:
            message: Hello message
        """
        self.message = message
        
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert result to dictionary.
        
        Returns:
            Dictionary representation
        """
        return {"message": self.message}
    
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
                "message": {"type": "string"}
            },
            "required": ["message"]
        }


class HelloCommand(Command):
    """Command that returns hello message."""
    
    name = "hello"
    result_class = HelloResult
    
    async def execute(self, name: str = "World") -> HelloResult:
        """
        Execute command.
        
        Args:
            name: Name to greet
            
        Returns:
            Hello result
        """
        return HelloResult(f"Hello, {name}!")
    
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
                "name": {"type": "string"}
            },
            "additionalProperties": False
        }


def main():
    """
    Основная функция для запуска сервера.
    """
    parser = argparse.ArgumentParser(description="Test JSON-RPC Microservice Server")
    parser.add_argument("--host", default="0.0.0.0", help="Host to bind server")
    parser.add_argument("--port", type=int, default=8000, help="Port to bind server")
    parser.add_argument("--reload", action="store_true", help="Enable auto-reload")
    parser.add_argument("--config", help="Path to config file")
    
    args = parser.parse_args()
    
    # Инициализируем конфигурацию
    if args.config and os.path.exists(args.config):
        config.load_from_file(args.config)
    
    # Настраиваем логирование
    setup_logging("INFO")
    
    # Создаем приложение FastAPI
    app = create_app()
    app.title = "Test Microservice"
    app.description = "Test microservice for package installation verification"
    app.version = "1.0.0"
    
    # Регистрируем только одну команду для тестирования
    registry.register(HelloCommand)
    
    # Запускаем сервер
    uvicorn.run(
        app,
        host=args.host,
        port=args.port,
        reload=args.reload,
        log_level="info"
    )


if __name__ == "__main__":
    main() 