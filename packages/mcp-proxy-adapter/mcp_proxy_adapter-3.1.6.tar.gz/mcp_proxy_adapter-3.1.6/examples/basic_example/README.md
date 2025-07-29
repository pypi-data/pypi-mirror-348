# Basic MCP Proxy Adapter Example

This example demonstrates how to use MCP Proxy Adapter to create a microservice with multiple commands organized in separate files.

## English Documentation

### Overview

This example shows:
- Creating a microservice using MCP Proxy Adapter
- Configuring the service using JSON configuration file
- Automatic command discovery from a package
- Implementing various command types with their result classes
- Running the service with auto-reload for development

### Setup

1. Make sure you have installed MCP Proxy Adapter package
2. Install additional dependencies:
   ```
   pip install pytz uvicorn
   ```

### Configuration

The service uses `config.json` for configuration. The key settings are:
- Server host and port
- Logging configuration
- Command discovery settings

### Available Commands

The example includes several commands:
- `echo` - Echo back a message
- `time` - Get current time in different formats and timezones
- `math` - Perform basic math operations

### Running the Example

```bash
cd examples/basic_example
python server.py
```

The service will start on http://localhost:8000 by default, with API documentation available at http://localhost:8000/docs

### Testing Commands

You can test commands using curl:

```bash
# Echo command
curl -X POST http://localhost:8000/cmd -H "Content-Type: application/json" -d '{"command": "echo", "params": {"message": "Hello, world!"}}'

# Time command
curl -X POST http://localhost:8000/cmd -H "Content-Type: application/json" -d '{"command": "time", "params": {"timezone": "Europe/London"}}'

# JSON-RPC style request
curl -X POST http://localhost:8000/api/jsonrpc -H "Content-Type: application/json" -d '{"jsonrpc": "2.0", "method": "echo", "params": {"message": "Hello RPC!"}, "id": 1}'
```

## Русская документация

### Обзор

Этот пример демонстрирует:
- Создание микросервиса с использованием MCP Proxy Adapter
- Настройку сервиса с использованием JSON-файла конфигурации
- Автоматическое обнаружение команд из пакета
- Реализацию различных типов команд с их классами результатов
- Запуск сервиса с автоперезагрузкой для разработки

### Настройка

1. Убедитесь, что у вас установлен пакет MCP Proxy Adapter
2. Установите дополнительные зависимости:
   ```
   pip install pytz uvicorn
   ```

### Конфигурация

Сервис использует `config.json` для конфигурации. Основные настройки:
- Хост и порт сервера
- Настройки логирования
- Настройки обнаружения команд

### Доступные команды

Пример включает несколько команд:
- `echo` - Эхо-ответ сообщения
- `time` - Получение текущего времени в разных форматах и часовых поясах
- `math` - Выполнение базовых математических операций

### Запуск примера

```bash
cd examples/basic_example
python server.py
```

Сервис запустится на http://localhost:8000 по умолчанию, документация API доступна по адресу http://localhost:8000/docs

### Тестирование команд

Вы можете тестировать команды с помощью curl:

```bash
# Команда echo
curl -X POST http://localhost:8000/cmd -H "Content-Type: application/json" -d '{"command": "echo", "params": {"message": "Привет, мир!"}}'

# Команда time
curl -X POST http://localhost:8000/cmd -H "Content-Type: application/json" -d '{"command": "time", "params": {"timezone": "Europe/Moscow"}}'

# Запрос в стиле JSON-RPC
curl -X POST http://localhost:8000/api/jsonrpc -H "Content-Type: application/json" -d '{"jsonrpc": "2.0", "method": "echo", "params": {"message": "Привет RPC!"}, "id": 1}'
```

## Структура примера

```
basic_example/
├── commands/                   # Директория с командами
│   ├── __init__.py            # Инициализация пакета команд
│   ├── echo_command.py        # Команда эхо
│   ├── math_command.py        # Математическая команда
│   └── time_command.py        # Команда времени
├── config.json                # Файл конфигурации JSON
├── README.md                  # Документация
└── server.py                  # Файл запуска сервера
```

## Запуск примера

```bash
# Перейти в директорию проекта
cd examples/basic_example

# Создать директорию для логов, если она не существует
mkdir -p logs

# Запустить сервер
python server.py
```

После запуска сервер будет доступен по адресу [http://localhost:8000](http://localhost:8000).

## Доступные команды

### 1. `echo` - Эхо-команда

Возвращает переданное сообщение.

**Параметры:**
- `message` (string) - Сообщение для эхо

**Пример запроса:**
```json
{
  "jsonrpc": "2.0",
  "method": "echo",
  "params": {
    "message": "Hello, World!"
  },
  "id": 1
}
```

### 2. `math` - Математическая команда

Выполняет математическую операцию над двумя числами.

**Параметры:**
- `a` (number) - Первое число
- `b` (number) - Второе число
- `operation` (string) - Операция (add, subtract, multiply, divide)

**Пример запроса:**
```json
{
  "jsonrpc": "2.0",
  "method": "math",
  "params": {
    "a": 10,
    "b": 5,
    "operation": "add"
  },
  "id": 1
}
```

### 3. `time` - Команда времени

Возвращает текущее время и дату.

**Параметры:**
- `format` (string, optional) - Формат времени (default: "%Y-%m-%d %H:%M:%S")
- `timezone` (string, optional) - Часовой пояс (default: "UTC")

**Пример запроса:**
```json
{
  "jsonrpc": "2.0",
  "method": "time",
  "params": {
    "format": "%d.%m.%Y %H:%M:%S",
    "timezone": "Europe/Moscow"
  },
  "id": 1
}
```

## Тестирование API

### Через веб-интерфейс

Откройте в браузере [http://localhost:8000/docs](http://localhost:8000/docs) для доступа к интерактивной документации Swagger UI.

### Через командную строку

```bash
# Вызов команды echo через JSON-RPC
curl -X POST "http://localhost:8000/api/jsonrpc" \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc": "2.0", "method": "echo", "params": {"message": "Hello!"}, "id": 1}'

# Вызов команды math через упрощенный эндпоинт
curl -X POST "http://localhost:8000/cmd" \
  -H "Content-Type: application/json" \
  -d '{"command": "math", "params": {"a": 10, "b": 5, "operation": "add"}}'

# Вызов команды time через endpoint /api/command/{command_name}
curl -X POST "http://localhost:8000/api/command/time" \
  -H "Content-Type: application/json" \
  -d '{"format": "%d.%m.%Y %H:%M:%S", "timezone": "UTC"}'
```

## Что демонстрирует этот пример

1. Прямое использование FastAPI и uvicorn с MCP Proxy Adapter
2. Организация команд в отдельные файлы
3. Автоматическое обнаружение и регистрация команд
4. Различные типы команд и параметров
5. Обработка ошибок
6. Различные способы вызова команд (JSON-RPC, /cmd, /api/command/{command_name}) 