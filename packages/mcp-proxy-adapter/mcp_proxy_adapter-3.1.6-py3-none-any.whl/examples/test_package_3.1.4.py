#!/usr/bin/env python3
"""
Скрипт для проверки работы улучшенной обработки null в версии 3.1.6.

Этот скрипт:
1. Проверяет, что версия пакета 3.1.6
2. Тестирует улучшенный метод validate_params
3. Проверяет, что команда help правильно обрабатывает null значения
"""

import inspect
import sys
from typing import Dict, Any, Optional

try:
    # Импортируем необходимые модули из пакета
    from mcp_proxy_adapter import __version__
    from mcp_proxy_adapter.commands.base import Command
    from mcp_proxy_adapter.commands.help_command import HelpCommand, HelpResult
except ImportError:
    print("ОШИБКА: Не удалось импортировать mcp_proxy_adapter. Убедитесь, что пакет установлен.")
    sys.exit(1)


def check_version():
    """
    Проверяет версию установленного пакета mcp_proxy_adapter.
    """
    expected_version = "3.1.6"
    
    print(f"\n=== Проверка версии ===")
    print(f"Установленная версия: {__version__}")
    print(f"Ожидаемая версия: {expected_version}")
    
    if __version__ != expected_version:
        print(f"ОШИБКА: Версия пакета ({__version__}) не соответствует ожидаемой ({expected_version}).")
        return False
    
    print("OK: Версия соответствует ожидаемой.")
    return True


def test_validate_params():
    """
    Тестирует метод validate_params класса Command для обработки различных вариантов null.
    """
    print(f"\n=== Тестирование validate_params ===")
    
    # Получаем исходный код метода validate_params
    validate_params_source = inspect.getsource(Command.validate_params)
    print(f"Исходный код метода validate_params:")
    print(validate_params_source)
    
    # Проверяем, содержит ли код улучшения для обработки null
    required_improvements = [
        "value.lower() in",
        "null",
        "none",
        "validated_params[key] = None"
    ]
    
    for improvement in required_improvements:
        if improvement not in validate_params_source:
            print(f"ОШИБКА: Не найдено улучшение: {improvement}")
            return False
    
    # Тестируем различные значения null
    test_cases = [
        {"unknown_param": None},
        {"unknown_param": "null"},
        {"unknown_param": "NULL"},
        {"unknown_param": "Null"},
        {"unknown_param": "none"},
        {"unknown_param": "NONE"},
        {"cmdname": None},
        {"cmdname": "null"},
        {"cmdname": "none"},
        {"cmdname": ""}
    ]
    
    print("\nРезультаты тестирования:")
    for case in test_cases:
        result = Command.validate_params(case)
        print(f"Входные данные: {case}")
        print(f"Результат: {result}")
        
        # Проверяем специальный случай с параметром cmdname
        if "cmdname" in case and (case["cmdname"] is None or case["cmdname"].lower() in ["null", "none", ""]):
            if "cmdname" not in result or result["cmdname"] is not None:
                print(f"ОШИБКА: Неверная обработка cmdname. Ожидалось: {{'cmdname': None}}, Получено: {result}")
                return False
        
        # Проверяем, что unknown_param был удален
        if "unknown_param" in case and "unknown_param" in result:
            print(f"ОШИБКА: Параметр unknown_param не был удален: {result}")
            return False
    
    print("OK: Все тесты validate_params пройдены успешно.")
    return True


def test_help_command():
    """
    Тестирует работу команды help с различными вариантами null.
    """
    print(f"\n=== Тестирование команды help ===")
    
    # Получаем исходный код метода execute команды help
    help_execute_source = inspect.getsource(HelpCommand.execute)
    print(f"Исходный код метода execute в HelpCommand:")
    print(help_execute_source)
    
    # Проверяем, содержит ли код поддержку **kwargs
    if "**kwargs" not in help_execute_source:
        print("ОШИБКА: Метод execute в HelpCommand не поддерживает **kwargs.")
        return False
    
    # Создаем экземпляр команды
    help_cmd = HelpCommand()
    
    # Тестируем с разными вариантами null в параметрах
    test_cases = [
        {"cmdname": None, "unknown_param": None},
        {"cmdname": "null", "unknown_param": "null"},
        {"cmdname": "none", "unknown_param": "none"},
        {"cmdname": "", "unknown_param": ""},
        {"unknown_param": "whatever"}
    ]
    
    print("\nРезультаты тестирования:")
    for i, case in enumerate(test_cases):
        print(f"\nТест {i+1}: {case}")
        try:
            # Используем execute напрямую, так как run преобразует параметры
            result = help_cmd.execute(**case)
            print(f"Тест пройден успешно, команда вернула результат типа: {type(result)}")
        except Exception as e:
            print(f"ОШИБКА: Тест не пройден: {e}")
            return False
    
    print("OK: Все тесты команды help пройдены успешно.")
    return True


def main():
    """
    Основная функция для запуска тестов.
    """
    print("=== Проверка MCP Proxy Adapter 3.1.6 ===")
    
    # Проверяем версию пакета
    version_ok = check_version()
    
    # Если версия не соответствует ожидаемой, прекращаем выполнение
    if not version_ok:
        print("ОШИБКА: Версия пакета не соответствует требуемой.")
        return False
    
    # Тестируем validate_params
    validate_params_ok = test_validate_params()
    
    # Тестируем команду help
    help_command_ok = test_help_command()
    
    # Выводим общий результат
    print("\n=== Итоговый результат ===")
    if version_ok and validate_params_ok and help_command_ok:
        print("УСПЕХ: Все тесты пройдены успешно!")
        return True
    else:
        print("ОШИБКА: Не все тесты пройдены.")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 