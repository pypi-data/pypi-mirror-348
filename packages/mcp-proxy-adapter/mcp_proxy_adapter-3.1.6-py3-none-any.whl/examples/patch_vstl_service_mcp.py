#!/usr/bin/env python3
"""
Скрипт для исправления ошибки 'name null is not defined' в сервисе VSTL через MCP Proxy API.

Этот скрипт демонстрирует как обойти проблему с null в сервисе vstl,
используя стандартные средства MCP Proxy API.
"""

import os
import sys
import json
import subprocess
from typing import Dict, Any, Optional

def call_vstl_command(command: str, params: Optional[Dict[str, Any]] = None):
    """
    Вызывает команду vstl через MCP Proxy API.
    
    Args:
        command: Название команды
        params: Параметры команды
        
    Returns:
        Результат выполнения команды
    """
    # Формируем параметры для команды mcp_MCP-Proxy_vstl
    if params is None:
        params = {}
    
    # Сериализуем параметры в JSON
    params_json = json.dumps(params)
    
    # Формируем команду для вызова MCP Proxy API
    cmd = [
        "curl", "-s",
        "-X", "POST",
        "-H", "Content-Type: application/json",
        "-d", f'{{"jsonrpc":"2.0","method":"{command}","params":{params_json},"id":1}}',
        "http://localhost:8000/api/vstl"
    ]
    
    # Выполняем команду
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        # Парсим результат как JSON
        return json.loads(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Ошибка выполнения команды: {e}")
        print(f"STDOUT: {e.stdout}")
        print(f"STDERR: {e.stderr}")
        return {"error": str(e)}
    except json.JSONDecodeError as e:
        print(f"Ошибка декодирования JSON: {e}")
        print(f"Ответ: {result.stdout}")
        return {"error": "Неверный формат JSON в ответе"}

def test_vstl_commands():
    """
    Тестирует различные команды vstl с обходом проблемы null.
    """
    print("=== Тестирование команд VSTL через MCP Proxy API ===\n")
    
    # Проверяем команду health
    print("1. Команда health:")
    response = call_vstl_command("health", {})
    print(f"Ответ: {json.dumps(response, indent=2)}\n")
    
    # Проверяем команду help без параметров
    print("2. Команда help без параметров:")
    response = call_vstl_command("help", {})
    print(f"Ответ: {json.dumps(response, indent=2)}")
    
    # Если есть ошибка в команде help без параметров, попробуем еще несколько вариантов
    if "error" in response:
        print("\n2.1. Попытка обойти ошибку - вызов help с корректными параметрами:")
        response = call_vstl_command("help", {"cmdname": None})
        print(f"Ответ: {json.dumps(response, indent=2)}")
    
    # Проверяем команду help с параметром cmdname
    print("\n3. Команда help с параметром cmdname:")
    response = call_vstl_command("help", {"cmdname": "health"})
    print(f"Ответ: {json.dumps(response, indent=2)}\n")
    
    # Проверяем команду config
    print("4. Команда config:")
    response = call_vstl_command("config", {"operation": "get"})
    print(f"Ответ: {json.dumps(response, indent=2)}\n")
    
    # Выводим рекомендации по исправлению
    print("\n=== Рекомендации по исправлению проблемы с null в VSTL ===")
    print("""
1. Проблема с обработкой null в JavaScript-совместимых API - это распространенная ошибка.
   В JavaScript null - это ключевое слово, а в Python - это None.

2. Для полного решения проблемы необходимо исправить реализацию сервиса VSTL:
   - Найти в коде места, где используется 'null' как переменная
   - Заменить на корректное использование None
   - Добавить к аргументам метода execute в help_command.py параметр **kwargs
   - Обновить метод validate_params для обработки строковых представлений null

3. До исправления сервера можно использовать следующие обходные пути:
   - Использовать MCP Proxy API с корректными значениями параметров (None вместо null)
   - Использовать промежуточный слой, который будет преобразовывать запросы
   - Избегать отправки параметров null/None в командах, где это возможно
    """)

if __name__ == "__main__":
    test_vstl_commands() 