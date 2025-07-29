"""
Минимальный пример приложения MCP Proxy Adapter.
"""

import os
import sys
import uvicorn
import logging
import json
from pathlib import Path

from mcp_proxy_adapter import create_app, Command, SuccessResult
from mcp_proxy_adapter.commands.command_registry import registry
from mcp_proxy_adapter.core.logging import logger
from mcp_proxy_adapter.config import config


class HelloCommand(Command):
    """Простая команда, возвращающая приветствие."""
    
    name = "hello"
    
    async def execute(self, name: str = "World") -> SuccessResult:
        """Выполняет команду с переданным именем."""
        logger.info(f"Executing hello command with name: {name}")
        return SuccessResult({"message": f"Hello, {name}!"})


def ensure_config():
    """Проверяет наличие конфигурационного файла и создает его при необходимости."""
    config_path = Path("config.json")
    
    if not config_path.exists():
        config_data = {
            "server": {
                "host": "0.0.0.0",
                "port": 8000,
                "debug": True,
                "log_level": "INFO"
            },
            "logging": {
                "level": "info",
                "file": "logs/minimal_example.log",
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            },
            "debug": True
        }
        
        # Создаем директорию для логов
        logs_dir = Path("logs")
        logs_dir.mkdir(exist_ok=True)
        
        # Записываем конфигурацию
        with open(config_path, "w") as f:
            json.dump(config_data, f, indent=2)
        
        logger.info(f"Created default configuration at {config_path}")


def setup_application():
    """
    Настраивает и возвращает FastAPI приложение.
    """
    # Проверяем наличие конфигурационного файла
    ensure_config()
    
    # Определяем путь к конфигурационному файлу
    config_path = Path("config.json").absolute()
    
    # Загружаем конфигурацию из файла
    if config_path.exists():
        config.load_from_file(str(config_path))
        logger.info(f"Loaded configuration from {config_path}")
    
    # Создаем приложение
    app = create_app()
    
    # Корректно регистрируем команду
    try:
        # Проверяем, есть ли уже команда в реестре
        if registry.command_exists(HelloCommand.name):
            # Если команда существует, удаляем ее
            logger.info(f"Command '{HelloCommand.name}' already exists, re-registering it")
            registry.unregister(HelloCommand.name)
        
        # Регистрируем команду
        registry.register(HelloCommand)
        logger.info(f"Command '{HelloCommand.name}' successfully registered")
        
        # Выводим список всех зарегистрированных команд
        commands = registry.get_all_commands()
        logger.info(f"Total registered commands: {len(commands)}")
    except Exception as e:
        logger.error(f"Error registering command: {e}")
    
    return app


def main():
    """
    Основная функция для запуска приложения.
    """
    try:
        # Настраиваем приложение
        app = setup_application()
        
        # Получаем настройки сервера из конфигурации
        host = config.get("server.host", "0.0.0.0")
        port = config.get("server.port", 8000)
        debug = config.get("server.debug", False)
        
        logger.info(f"Starting server on {host}:{port} (debug: {debug})")
        
        if debug:
            # В режиме отладки запускаем с перезагрузкой, используя строку импорта
            uvicorn.run(
                "main:setup_application",
                host=host,
                port=port,
                reload=True,
                factory=True
            )
        else:
            # В обычном режиме запускаем экземпляр приложения
            uvicorn.run(
                app,
                host=host,
                port=port
            )
    except Exception as e:
        logger.exception(f"Error during application startup: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
