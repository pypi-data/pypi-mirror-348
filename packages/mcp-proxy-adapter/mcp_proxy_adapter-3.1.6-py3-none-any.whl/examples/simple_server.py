#!/usr/bin/env python3
"""
Простой пример запуска сервера JSON-RPC с использованием MCP Proxy Adapter.

Этот скрипт демонстрирует минимальную конфигурацию для запуска сервера JSON-RPC.
Он создаёт экземпляр приложения FastAPI с MCP Proxy Adapter и регистрирует пользовательские команды.
"""

import os
import argparse
import sys
from pathlib import Path
import uvicorn

# Добавляем родительскую директорию в PYTHONPATH для импорта mcp_proxy_adapter
sys.path.insert(0, str(Path(__file__).parent.parent))

from mcp_proxy_adapter import Command, SuccessResult, create_app
from mcp_proxy_adapter.commands.command_registry import registry
from typing import Dict, Any, Optional


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
    parser = argparse.ArgumentParser(description="JSON-RPC Microservice Server")
    parser.add_argument("--host", default="0.0.0.0", help="Host to bind server")
    parser.add_argument("--port", type=int, default=8000, help="Port to bind server")
    parser.add_argument("--reload", action="store_true", help="Enable auto-reload")
    
    args = parser.parse_args()
    
    # Регистрируем только свою пользовательскую команду
    # встроенные команды и примеры регистрируются автоматически
    registry.register(HelloCommand)
    
    # Создаем приложение FastAPI
    app = create_app()
    
    # Запускаем сервер
    uvicorn.run(
        app,
        host=args.host,
        port=args.port,
        reload=args.reload
    )


if __name__ == "__main__":
    # Run the simple server example
    # To test, open http://localhost:8000/docs in your browser
    # or use curl:
    # curl -X POST http://localhost:8000/api/cmd -H "Content-Type: application/json" -d '{"jsonrpc":"2.0","method":"hello","params":{"name":"PyPI"},"id":1}'
    main() 