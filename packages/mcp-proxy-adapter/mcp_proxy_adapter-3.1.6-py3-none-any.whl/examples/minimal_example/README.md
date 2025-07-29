# Минимальный пример MCP Proxy Adapter

Данный пример демонстрирует минимальную конфигурацию для запуска микросервиса с одной простой командой.

## Структура примера

```
minimal_example/
├── config.json            # Файл конфигурации в JSON формате
├── README.md              # Документация
├── simple_server.py       # Пример сервера с одной командой
└── tests/                 # Директория с интеграционными тестами
    ├── conftest.py        # Настройка тестов
    └── test_integration.py # Интеграционные тесты
```

## Запуск примера

```bash
# Перейти в директорию проекта
cd examples/minimal_example

# Запустить сервер
python simple_server.py
```

После запуска сервер будет доступен по адресу [http://localhost:8000](http://localhost:8000).

## Тестирование API

### Через веб-интерфейс

Откройте в браузере [http://localhost:8000/docs](http://localhost:8000/docs) для доступа к интерактивной документации Swagger UI.

### Через командную строку

```bash
# Вызов команды hello через JSON-RPC
curl -X POST "http://localhost:8000/api/jsonrpc" \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc": "2.0", "method": "hello", "params": {"name": "User"}, "id": 1}'

# Вызов команды hello через упрощенный эндпоинт
curl -X POST "http://localhost:8000/cmd" \
  -H "Content-Type: application/json" \
  -d '{"command": "hello", "params": {"name": "User"}}'
```

### Запуск интеграционных тестов

```bash
# Запуск всех тестов
pytest tests/test_integration.py -v

# Запуск конкретного теста
pytest tests/test_integration.py::TestHelloCommandIntegration::test_jsonrpc_hello_default -v
```

## Что демонстрирует этот пример

1. Создание минимального сервиса с MCP Proxy Adapter
2. Определение простой команды с метаданными
3. Основные эндпоинты API
4. Работа с JSON-RPC
5. Тестирование API через интеграционные тесты 