# Basic MCP Microservice Example

This example demonstrates the basic functionality of MCP Microservice with multiple commands
organized in separate files.

## Structure

```
basic_example/
├── commands/                   # Commands directory
│   ├── __init__.py            # Package initialization
│   ├── echo_command.py        # Echo command
│   ├── math_command.py        # Math command
│   └── time_command.py        # Time command
├── config.json                # JSON configuration file
├── docs/                      # Documentation
│   ├── EN/                    # English documentation
│   │   └── README.md          # This file
│   └── RU/                    # Russian documentation
│       └── README.md          # Russian version of this file
├── logs/                      # Logs directory
├── server.py                  # Server startup and application logic
└── tests/                     # Tests directory
    └── conftest.py            # Test configuration and fixtures
```

## Running the Example

```bash
# Navigate to the project directory
cd examples/basic_example

# Create logs directory if it doesn't exist
mkdir -p logs

# Run the server with default configuration (config.json)
python server.py

# Or run with a specific configuration file
python server.py --config other_config.json
```

After starting, the server will be available at [http://localhost:8000](http://localhost:8000).

## Configuration

The server reads configuration from JSON files. By default, it uses `config.json` in the same directory as `server.py`.

You can specify a different configuration file with the `--config` parameter:

```bash
python server.py --config my_custom_config.json
```

If the specified configuration file doesn't exist, the server will try to fall back to `config.json`.

The main configuration options are:

```json
{
  "server": {
    "host": "0.0.0.0",
    "port": 8000,
    "debug": true,
    "log_level": "info"
  },
  "logging": {
    "level": "INFO",
    "file": "logs/basic_example.log"
  }
}
```

The server can run in two modes:
- Normal mode: Uses a pre-configured application instance
- Debug mode: Uses hot reload (when `"debug": true` in config)

## Available Commands

### 1. `echo` - Echo Command

Returns the provided message.

**Parameters:**
- `message` (string) - Message to echo back

**Example request:**
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

### 2. `math` - Math Command

Performs a math operation on two numbers.

**Parameters:**
- `a` (number) - First number
- `b` (number) - Second number
- `operation` (string) - Operation (add, subtract, multiply, divide)

**Example request:**
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

### 3. `time` - Time Command

Returns the current time and date.

**Parameters:**
- `format` (string, optional) - Time format (default: "%Y-%m-%d %H:%M:%S")
- `timezone` (string, optional) - Timezone (default: "UTC")

**Example request:**
```json
{
  "jsonrpc": "2.0",
  "method": "time",
  "params": {
    "format": "%d.%m.%Y %H:%M:%S",
    "timezone": "Europe/London"
  },
  "id": 1
}
```

## Testing the API

### Via Web Interface

Open [http://localhost:8000/docs](http://localhost:8000/docs) in your browser to access the Swagger UI interactive documentation.

### Via Command Line

```bash
# Call echo command via JSON-RPC
curl -X POST "http://localhost:8000/api/jsonrpc" \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc": "2.0", "method": "echo", "params": {"message": "Hello!"}, "id": 1}'

# Call math command via simplified endpoint
curl -X POST "http://localhost:8000/cmd" \
  -H "Content-Type: application/json" \
  -d '{"command": "math", "params": {"a": 10, "b": 5, "operation": "add"}}'

# Call time command via endpoint /api/command/{command_name}
curl -X POST "http://localhost:8000/api/command/time" \
  -H "Content-Type: application/json" \
  -d '{"format": "%d.%m.%Y %H:%M:%S", "timezone": "UTC"}'
```

## Key Features Demonstrated

1. Command organization in separate files
2. Automatic command discovery and registration
3. Different command types and parameter handling
4. Error handling and automatic command reregistration
5. Different ways to call commands (JSON-RPC, /cmd, /api/command/{command_name})
6. Support for debug mode with hot reload
7. Safe command registration for preventing conflicts
8. JSON configuration files with command-line options 