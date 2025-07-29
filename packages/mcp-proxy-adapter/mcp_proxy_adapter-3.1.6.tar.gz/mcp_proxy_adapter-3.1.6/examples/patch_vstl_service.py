#!/usr/bin/env python3
"""
Скрипт для исправления ошибки 'name null is not defined' в сервисе VSTL.

Этот скрипт обходит проблему с обработкой null в сервисе vstl 
при помощи модификации JSON-RPC запросов, чтобы заменять null на None.

Использование:
python patch_vstl_service.py
"""

import sys
import json
import requests
from typing import Dict, Any, Optional

# URL и заголовки для VSTL сервиса
VSTL_URL = "http://localhost:8000/cmd"
HEADERS = {"Content-Type": "application/json"}

def safe_call_vstl(command: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Безопасно вызывает команду в сервисе VSTL, обрабатывая null значения.
    
    Args:
        command: Имя команды
        params: Параметры для команды
        
    Returns:
        Dict[str, Any]: Ответ от сервиса
    """
    # Обработка null значений - заменяем null на None для Python
    safe_params = {}
    if params:
        for key, value in params.items():
            if value == "null" or value == "none":
                safe_params[key] = None
            else:
                safe_params[key] = value
    
    # Безопасно сериализуем параметры, чтобы null значения были корректно обработаны
    payload = {
        "jsonrpc": "2.0",
        "method": command,
        "params": safe_params or {},
        "id": 1
    }
    
    # Отправляем запрос
    response = requests.post(VSTL_URL, json=payload, headers=HEADERS)
    return response.json()

def test_vstl_commands():
    """
    Тестирует различные команды в сервисе VSTL с безопасной обработкой null.
    """
    print("=== Тестирование команд VSTL с патчем для обработки null ===\n")
    
    # Проверяем команду health
    print("1. Команда health:")
    response = safe_call_vstl("health", {})
    print(f"Ответ: {json.dumps(response, indent=2)}\n")
    
    # Проверяем команду help без параметров
    print("2. Команда help без параметров:")
    response = safe_call_vstl("help", {})
    print(f"Ответ: {json.dumps(response, indent=2)}")
    
    # Если команда help сработала, выведем список всех доступных команд
    if response.get("result") and not response.get("error"):
        commands_info = response["result"].get("commands", {})
        print(f"\nДоступные команды ({len(commands_info)}):")
        for cmd_name, cmd_info in commands_info.items():
            print(f"  - {cmd_name}: {cmd_info.get('summary', 'Нет описания')}")
    
    # Проверяем команду help с параметром cmdname
    print("\n3. Команда help с параметром cmdname:")
    response = safe_call_vstl("help", {"cmdname": "health"})
    print(f"Ответ: {json.dumps(response, indent=2)}\n")
    
    # Проверяем команду config
    print("4. Команда config:")
    response = safe_call_vstl("config", {"operation": "get"})
    print(f"Ответ: {json.dumps(response, indent=2)}\n")
    
    # Выводим рекомендации по полному исправлению
    print("\n=== Рекомендации по полному исправлению проблемы с null в VSTL ===")
    print("""
1. Проверьте исходный код сервиса VSTL на наличие использования переменной 'null'
   без её объявления (обратите внимание на файл help_command.py)

2. Замените все использования JavaScript-стиля null на Python None:
   - Поиск: if value == null
   - Замена: if value is None

3. Обновите сервис до последней версии mcp_proxy_adapter 3.1.6 и перезапустите

4. Если это невозможно, используйте этот скрипт как промежуточное решение,
   чтобы безопасно вызывать команды VSTL с корректной обработкой null.
   
5. Внесите исправления в метод validate_params, как показано в fix_vstl_help.py
    """)

if __name__ == "__main__":
    test_vstl_commands() 