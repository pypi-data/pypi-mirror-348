"""
Pytest configuration and fixtures for basic example tests.

This module provides fixtures for testing the basic microservice example,
including running an actual server instance for integration tests.
All commands in the microservice are implemented as asynchronous functions.
"""

import os
import sys
import time
import socket
import asyncio
import threading
import multiprocessing
from typing import Callable, Dict, Any, List

import pytest
import requests

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the server module from the parent directory
import server as server_module
from commands.echo_command import EchoCommand
from commands.math_command import MathCommand
from commands.time_command import TimeCommand


def find_free_port() -> int:
    """
    Find a free port on localhost.
    
    Returns:
        Free port number
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(('localhost', 0))
        return sock.getsockname()[1]


class ServerProcess:
    """Helper class to manage server process."""
    
    def __init__(self, port: int):
        """
        Initialize server process with a specified port.
        
        Args:
            port: Port number to use
        """
        self.port = port
        self.process = None
        
    def start(self) -> None:
        """Start the server in a separate process."""
        def run_server():
            # Mock the configuration to use the test port
            os.environ["TEST_SERVER_PORT"] = str(self.port)
            server_module.main()
            
        self.process = multiprocessing.Process(target=run_server)
        self.process.daemon = True
        self.process.start()
        
        # Wait for server to start
        self._wait_for_server()
        
    def stop(self) -> None:
        """Stop the server process."""
        if self.process and self.process.is_alive():
            self.process.terminate()
            self.process.join(timeout=2)
            
    def _wait_for_server(self, max_attempts: int = 10) -> None:
        """
        Wait for the server to become available.
        
        Args:
            max_attempts: Maximum number of connection attempts
        """
        for i in range(max_attempts):
            try:
                response = requests.get(f"http://localhost:{self.port}/health")
                if response.status_code == 200:
                    return
            except requests.ConnectionError:
                pass
            
            time.sleep(0.5)
            
        raise TimeoutError(f"Server did not start within {max_attempts * 0.5} seconds")


@pytest.fixture
def server_port() -> int:
    """
    Fixture that provides a free port for the test server.
    
    Returns:
        Port number
    """
    return find_free_port()


@pytest.fixture
def server(server_port: int) -> ServerProcess:
    """
    Fixture that provides a running server instance.
    
    Args:
        server_port: Port to run the server on
    
    Returns:
        Server process object
    """
    server_process = ServerProcess(server_port)
    server_process.start()
    
    yield server_process
    
    server_process.stop()


@pytest.fixture
def api_url(server_port: int) -> str:
    """
    Fixture that provides the base API URL.
    
    Args:
        server_port: Server port
        
    Returns:
        Base API URL
    """
    return f"http://localhost:{server_port}"


@pytest.fixture
def jsonrpc_client(api_url: str) -> Callable:
    """
    Fixture that provides a JSON-RPC client function.
    
    Args:
        api_url: Base API URL
        
    Returns:
        Function to make JSON-RPC requests
    """
    def make_request(method: str, params: Dict[str, Any], request_id: int = 1) -> Dict[str, Any]:
        """
        Make a JSON-RPC request.
        
        Args:
            method: Method name
            params: Method parameters
            request_id: Request ID
            
        Returns:
            JSON-RPC response
        """
        payload = {
            "jsonrpc": "2.0",
            "method": method,
            "params": params,
            "id": request_id
        }
        
        response = requests.post(
            f"{api_url}/api/jsonrpc",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        
        return response.json()
    
    return make_request


@pytest.fixture
def batch_jsonrpc_client(api_url: str) -> Callable:
    """
    Fixture that provides a batch JSON-RPC client function.
    
    Args:
        api_url: Base API URL
        
    Returns:
        Function to make batch JSON-RPC requests
    """
    def make_batch_request(requests_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Make a batch JSON-RPC request.
        
        Args:
            requests_data: List of request objects
            
        Returns:
            List of JSON-RPC responses
        """
        response = requests.post(
            f"{api_url}/api/jsonrpc",
            json=requests_data,
            headers={"Content-Type": "application/json"}
        )
        
        return response.json()
    
    return make_batch_request


@pytest.fixture
def echo_command() -> EchoCommand:
    """
    Fixture that provides an instance of EchoCommand.
    
    Returns:
        EchoCommand instance
    """
    return EchoCommand()


@pytest.fixture
def math_command() -> MathCommand:
    """
    Fixture that provides an instance of MathCommand.
    
    Returns:
        MathCommand instance
    """
    return MathCommand()


@pytest.fixture
def time_command() -> TimeCommand:
    """
    Fixture that provides an instance of TimeCommand.
    
    Returns:
        TimeCommand instance
    """
    return TimeCommand() 