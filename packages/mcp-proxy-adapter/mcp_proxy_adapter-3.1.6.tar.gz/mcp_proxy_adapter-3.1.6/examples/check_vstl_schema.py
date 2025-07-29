#!/usr/bin/env python3
"""
Скрипт для проверки схемы команды help в сервисе VSTL
"""

import json
import requests
from typing import Dict, Any, Optional

# URL и заголовки для VSTL сервиса
VSTL_URL = "http://localhost:8007/cmd"
HEADERS = {"Content-Type": "application/json"}

def send_json_rpc(method: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Отправляет JSON-RPC запрос и возвращает ответ
    
    Args:
        method: Имя метода
        params: Параметры запроса
        
    Returns:
        Dict[str, Any]: Ответ сервера
    """
    # Формируем JSON-RPC запрос
    payload = {
        "jsonrpc": "2.0",
        "method": method,
        "id": 1
    }
    
    # Добавляем параметры, если они есть
    if params is not None:
        payload["params"] = params
    
    print(f"Отправляем запрос: {json.dumps(payload, indent=2)}")
    
    # Отправляем запрос
    response = requests.post(VSTL_URL, json=payload, headers=HEADERS)
    
    # Возвращаем ответ
    return response.json()

def test_help_command():
    """
    Проверяет команду help в различных вариантах
    """
    print("\n=== Проверка команды help без параметров ===")
    response = send_json_rpc("help")
    print(f"Ответ: {json.dumps(response, indent=2)}")
    
    print("\n=== Проверка команды help с пустыми параметрами ===")
    response = send_json_rpc("help", {})
    print(f"Ответ: {json.dumps(response, indent=2)}")
    
    print("\n=== Проверка команды help с параметром cmdname=null ===")
    response = send_json_rpc("help", {"cmdname": None})
    print(f"Ответ: {json.dumps(response, indent=2)}")
    
    print("\n=== Проверка команды help с параметром cmdname=\"config\" ===")
    response = send_json_rpc("help", {"cmdname": "config"})
    print(f"Ответ: {json.dumps(response, indent=2)}")
    
    # Проверяем workaround с передачей строки "null"
    print("\n=== Проверка команды help с параметром cmdname=\"null\" ===")
    response = send_json_rpc("help", {"cmdname": "null"})
    print(f"Ответ: {json.dumps(response, indent=2)}")

def check_schema():
    """
    Проверяет схему команд и ищет обязательные параметры
    """
    print("\n=== Проверка схемы команд ===")
    
    # Запрашиваем список всех доступных команд
    health_response = send_json_rpc("health")
    print(f"Здоровье сервиса: {json.dumps(health_response, indent=2)}")
    
    # Проверяем команду config для получения схемы
    config_response = send_json_rpc("config", {"operation": "get"})
    print(f"Конфигурация: {json.dumps(config_response, indent=2)}")
    
    # Пробуем с явным указанием строки вместо null
    print("\n=== Проверка команды help с cmdname=\"\" (пустая строка) ===")
    response = send_json_rpc("help", {"cmdname": ""})
    print(f"Ответ: {json.dumps(response, indent=2)}")
    
    # Создаем свой вариант с переопределением параметров
    print("\n=== Проверка специального запроса с kwargs=null ===")
    # Прямая отправка JSON с null значением для kwargs
    special_payload = {
        "jsonrpc": "2.0",
        "method": "help",
        "params": {"kwargs": None},
        "id": 1
    }
    response = requests.post(VSTL_URL, json=special_payload, headers=HEADERS)
    print(f"Ответ: {json.dumps(response.json(), indent=2)}")

if __name__ == "__main__":
    print("=== Диагностика проблемы с командой help в сервисе VSTL ===")
    try:
        test_help_command()
        check_schema()
    except Exception as e:
        print(f"Ошибка при выполнении: {e}") 