"""
Минимальный пример использования MCP Proxy Adapter.

Этот пример демонстрирует минимальную конфигурацию для запуска микросервиса
с одной простой командой.
"""

import os
import uvicorn
from typing import Dict, Any, List

from mcp_proxy_adapter import Command, SuccessResult, create_app, registry
from mcp_proxy_adapter.core.logging import setup_logging
from mcp_proxy_adapter.config import config


class HelloResult(SuccessResult):
    """
    Результат выполнения команды hello.
    
    Атрибуты:
        message (str): Приветственное сообщение
    """
    
    def __init__(self, message: str):
        """
        Инициализация результата команды.
        
        Args:
            message: Приветственное сообщение
        """
        self.message = message
        
    def to_dict(self) -> Dict[str, Any]:
        """
        Преобразование результата в словарь.
        
        Returns:
            Словарь с результатом выполнения команды
        """
        return {"message": self.message}
    
    @classmethod
    def get_schema(cls) -> Dict[str, Any]:
        """
        Получение JSON-схемы для результата.
        
        Returns:
            JSON-схема результата
        """
        return {
            "type": "object",
            "properties": {
                "message": {"type": "string", "description": "Приветственное сообщение"}
            },
            "required": ["message"]
        }


class HelloCommand(Command):
    """
    Команда, возвращающая приветственное сообщение.
    
    Эта команда принимает имя пользователя и возвращает приветственное сообщение.
    """
    
    # Имя команды для регистрации
    name = "hello"
    # Класс результата команды
    result_class = HelloResult
    
    async def execute(self, name: str = "World") -> HelloResult:
        """
        Выполнение команды.
        
        Args:
            name: Имя для приветствия (по умолчанию "World")
            
        Returns:
            Результат выполнения команды с приветственным сообщением
        """
        return HelloResult(f"Hello, {name}!")
    
    @classmethod
    def get_schema(cls) -> Dict[str, Any]:
        """
        Получение JSON-схемы для параметров команды.
        
        Returns:
            JSON-схема параметров команды
        """
        return {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "Имя для приветствия"
                }
            },
            "additionalProperties": False
        }
    
    @classmethod
    def _generate_examples(cls, params: Dict[str, Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Генерирует примеры использования команды.
        
        Args:
            params: Информация о параметрах команды
            
        Returns:
            Список примеров
        """
        return [
            {
                "command": "hello",
                "description": "Приветствие по умолчанию"
            },
            {
                "command": "hello",
                "params": {"name": "User"},
                "description": "Приветствие с указанным именем"
            }
        ]


def main():
    """Запуск микросервиса."""
    # Определяем путь к конфигурационному файлу
    current_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(current_dir, "config.json")
    
    # Загружаем конфигурацию, если файл существует
    if os.path.exists(config_path):
        config.load_from_file(config_path)
    
    # Настраиваем логирование
    setup_logging("INFO")
    
    # Создаем приложение FastAPI
    app = create_app()
    app.title = "Minimal Example"
    app.description = "Минимальный пример использования MCP Proxy Adapter"
    app.version = "1.0.0"
    
    # Регистрируем команду
    registry.register(HelloCommand)
    
    # Определяем порт из переменной окружения или используем 8000 по умолчанию
    port = int(os.environ.get("TEST_SERVER_PORT", 8000))
    
    # Запускаем сервер
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=port,
        reload=False,  # Отключаем автоперезагрузку для тестов
        log_level="info"
    )


if __name__ == "__main__":
    main() 