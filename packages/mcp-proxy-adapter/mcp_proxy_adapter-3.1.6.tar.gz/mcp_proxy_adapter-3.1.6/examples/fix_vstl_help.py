#!/usr/bin/env python3
"""
Скрипт для исправления проблемы с обработкой JavaScript null в сервисе VSTL.

Этот скрипт демонстрирует проблему с обработкой null значений в VSTL 
и способ её решения с помощью обновленной реализации метода validate_params.
"""

import sys
import json
import requests
from typing import Dict, Any, Optional

# URL и заголовки для VSTL сервиса
VSTL_URL = "http://localhost:8000/cmd"
HEADERS = {"Content-Type": "application/json"}

def call_vstl_help(params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Вызывает команду help в сервисе VSTL.
    
    Args:
        params: Параметры для команды help
        
    Returns:
        Dict[str, Any]: Ответ от сервиса
    """
    payload = {
        "jsonrpc": "2.0",
        "method": "help",
        "params": params or {},
        "id": 1
    }
    
    response = requests.post(VSTL_URL, json=payload, headers=HEADERS)
    return response.json()

def test_validate_params_fix():
    """
    Демонстрирует проблему с обработкой null и решение с помощью
    улучшенной реализации метода validate_params.
    """
    # Оригинальная реализация метода validate_params
    def original_validate_params(params: Dict[str, Any]) -> Dict[str, Any]:
        if params is None:
            params = {}
            
        validated_params = params.copy()
        
        for key, value in list(validated_params.items()):
            if value is None or (isinstance(value, str) and value == ""):
                if key in ["cmdname"]:
                    pass
                else:
                    del validated_params[key]
                
        return validated_params

    # Улучшенная реализация метода validate_params
    def improved_validate_params(params: Dict[str, Any]) -> Dict[str, Any]:
        if params is None:
            params = {}
            
        validated_params = params.copy()
        
        for key, value in list(validated_params.items()):
            if value is None or (isinstance(value, str) and value.lower() in ["null", "none", ""]):
                if key in ["cmdname"]:
                    validated_params[key] = None
                else:
                    del validated_params[key]
                
        return validated_params

    # Тестирование оригинальной реализации
    original_params = {"unknown_param": "null"}
    
    print("\n=== Оригинальные параметры ===")
    print(f"Параметры: {original_params}")
    print("Результат validate_params (оригинальный):")
    try:
        print(original_validate_params(original_params))
    except Exception as e:
        print(f"ОШИБКА: {e}")
        
    # Тестирование улучшенной реализации
    print("\n=== Улучшенная обработка 'null' ===")
    print(f"Параметры: {original_params}")
    print("Результат validate_params (улучшенный):")
    try:
        print(improved_validate_params(original_params))
    except Exception as e:
        print(f"ОШИБКА: {e}")
        
    # Проверка запроса к VSTL с null в параметрах
    print("\n=== Тестирование запроса к VSTL ===")
    
    # Тест с null в параметрах
    print("\nТест 1: Запрос с null в параметрах")
    response = call_vstl_help({"unknown_param": None})
    print(f"Ответ: {json.dumps(response, indent=2)}")
    
    # Тест с строковым "null" в параметрах
    print("\nТест 2: Запрос со строковым 'null' в параметрах")
    response = call_vstl_help({"unknown_param": "null"})
    print(f"Ответ: {json.dumps(response, indent=2)}")
    
    # Рекомендации по исправлению
    print("\n=== Рекомендации по исправлению ===")
    print("""
1. Обновите метод validate_params в файле commands/base.py на улучшенную версию:
   - Добавьте проверку на строки "null" и "none" (в любом регистре)
   - Для параметров, которые могут быть None, преобразуйте их в Python None
   
2. Обновите метод execute команды help, чтобы игнорировать неизвестные параметры:
   - Добавьте аргумент **kwargs в сигнатуру метода

Эти изменения улучшат совместимость с клиентами, отправляющими JavaScript null
и сделают API более устойчивым к различным форматам входных данных.
    """)

if __name__ == "__main__":
    test_validate_params_fix() 