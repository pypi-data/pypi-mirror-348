# Complete MCP Proxy Adapter Example

This example demonstrates a complete MCP Proxy Adapter application with Docker support,
environment-specific configuration, and multiple commands.

## Structure

```
complete_example/
├── cache/                     # Cache directory
├── commands/                  # Commands directory
│   ├── __init__.py           # Package initialization
│   ├── db_command.py         # Database command
│   ├── file_command.py       # File operations command
│   └── system_command.py     # System information command
├── configs/                   # Configuration files
│   ├── config.dev.yaml       # Development config
│   └── config.docker.yaml    # Docker config
├── docker-compose.yml        # Docker Compose file
├── Dockerfile                # Docker image definition
├── logs/                     # Logs directory
├── README.md                 # This documentation file
├── requirements.txt          # Python dependencies
└── server.py                 # Server startup file
```

## Features

- Multiple commands in separate files
- Environment-specific configuration
- Docker support
- Volume mounting for logs, cache, and config
- Network configuration

## Running Locally

```bash
# Navigate to the project directory
cd examples/complete_example

# Create virtual environment (optional)
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
# venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt
pip install -e ../..  # Install mcp_proxy_adapter from parent directory

# Run the server with development config
python server.py --config configs/config.dev.yaml
```

The server will be available at [http://localhost:8000](http://localhost:8000).

## Running with Docker

```bash
# Navigate to the project directory
cd examples/complete_example

# Build the Docker image
docker build -t mcp-proxy-adapter-example .

# Run with Docker Compose
docker-compose up
```

The server will be available at [http://localhost:8000](http://localhost:8000).

## Available Commands

The microservice includes several commands that demonstrate different features:

1. `system_info` - Returns system information
2. `file_operations` - Performs file operations
3. `db_query` - Executes database queries

For details on each command, see the API documentation at [http://localhost:8000/docs](http://localhost:8000/docs)
when the server is running.

## Docker Configuration

The Docker setup includes:

- Volume mounts for logs, cache, and configuration
- Network configuration for integration with other services
- User mapping to avoid permission issues
- Port forwarding

For details, see the `docker-compose.yml` file. 