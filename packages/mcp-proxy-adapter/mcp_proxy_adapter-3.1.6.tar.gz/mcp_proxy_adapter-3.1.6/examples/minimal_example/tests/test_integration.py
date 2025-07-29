"""
Integration tests for the minimal example of MCP Proxy Adapter.

These tests start a real server instance and test the API endpoints.
"""

import os
import time
import pytest
import requests
from typing import Dict, Any, Callable

from conftest import ServerProcess


class TestHelloCommandIntegration:
    """Integration tests for the HelloCommand API."""

    def test_jsonrpc_hello_default(self, server: ServerProcess, jsonrpc_client: Callable):
        """Test the hello command via JSON-RPC with default parameters."""
        # Make JSON-RPC request
        response = jsonrpc_client("hello", {})
        
        # Check response
        assert "jsonrpc" in response
        assert response["jsonrpc"] == "2.0"
        assert "id" in response
        assert "result" in response
        assert "message" in response["result"]
        assert response["result"]["message"] == "Hello, World!"
    
    def test_jsonrpc_hello_custom_name(self, server: ServerProcess, jsonrpc_client: Callable):
        """Test the hello command via JSON-RPC with custom name parameter."""
        # Make JSON-RPC request
        response = jsonrpc_client("hello", {"name": "Integration Test"})
        
        # Check response
        assert "result" in response
        assert "message" in response["result"]
        assert response["result"]["message"] == "Hello, Integration Test!"
    
    def test_cmd_endpoint_hello(self, server: ServerProcess, api_url: str):
        """Test the hello command via the /cmd endpoint."""
        # Prepare request
        payload = {
            "command": "hello",
            "params": {"name": "CMD Endpoint"}
        }
        
        # Make request
        response = requests.post(
            f"{api_url}/cmd",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        
        # Check response
        assert response.status_code == 200
        data = response.json()
        assert "result" in data
        assert "message" in data["result"]
        assert data["result"]["message"] == "Hello, CMD Endpoint!"
    
    def test_api_command_endpoint_hello(self, server: ServerProcess, api_url: str):
        """Test the hello command via the /api/command/{command_name} endpoint."""
        # Prepare params
        params = {"name": "API Command Endpoint"}
        
        # Make request
        response = requests.post(
            f"{api_url}/api/command/hello",
            json=params,
            headers={"Content-Type": "application/json"}
        )
        
        # Check response
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert data["message"] == "Hello, API Command Endpoint!"
    
    def test_jsonrpc_batch_request(self, server: ServerProcess, api_url: str):
        """Test batch JSON-RPC requests with hello command."""
        # Prepare batch request
        batch = [
            {
                "jsonrpc": "2.0",
                "method": "hello",
                "params": {"name": "Batch 1"},
                "id": 1
            },
            {
                "jsonrpc": "2.0",
                "method": "hello",
                "params": {"name": "Batch 2"},
                "id": 2
            }
        ]
        
        # Make request
        response = requests.post(
            f"{api_url}/api/jsonrpc",
            json=batch,
            headers={"Content-Type": "application/json"}
        )
        
        # Check response
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 2
        
        # Check first result
        assert data[0]["id"] == 1
        assert data[0]["result"]["message"] == "Hello, Batch 1!"
        
        # Check second result
        assert data[1]["id"] == 2
        assert data[1]["result"]["message"] == "Hello, Batch 2!"


class TestServerIntegration:
    """Integration tests for the server itself."""
    
    def test_health_endpoint(self, server: ServerProcess, api_url: str):
        """Test the /health endpoint."""
        response = requests.get(f"{api_url}/health")
        
        # Check response
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert data["status"] == "ok"
    
    def test_openapi_schema(self, server: ServerProcess, api_url: str):
        """Test the OpenAPI schema endpoint."""
        response = requests.get(f"{api_url}/openapi.json")
        
        # Check response
        assert response.status_code == 200
        schema = response.json()
        
        # Check schema structure
        assert "openapi" in schema
        assert "info" in schema
        assert "paths" in schema
        
        # Проверяем наличие основных эндпоинтов
        assert "/api/jsonrpc" in schema["paths"] or "/cmd" in schema["paths"]
        assert "/api/commands" in schema["paths"]
        
    def test_docs_endpoint(self, server: ServerProcess, api_url: str):
        """Test the Swagger UI endpoint."""
        response = requests.get(f"{api_url}/docs")
        
        # Check response
        assert response.status_code == 200
        assert "text/html" in response.headers["Content-Type"]
        
        # Check if swagger UI is in the response
        assert "swagger-ui" in response.text.lower()
    
    def test_commands_list_endpoint(self, server: ServerProcess, api_url: str):
        """Test the commands list endpoint."""
        response = requests.get(f"{api_url}/api/commands")
        
        # Check response
        assert response.status_code == 200
        data = response.json()
        
        # Check data structure
        assert "commands" in data
        assert isinstance(data["commands"], dict)  # Теперь commands это словарь, а не список
        
        # Check if hello command is in the list
        assert "hello" in data["commands"]
        
        # Check hello command details
        hello_cmd = data["commands"]["hello"]
        assert "name" in hello_cmd
        assert hello_cmd["name"] == "hello" 