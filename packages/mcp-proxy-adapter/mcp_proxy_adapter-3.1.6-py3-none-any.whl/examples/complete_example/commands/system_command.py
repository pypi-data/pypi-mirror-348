"""
System information command module.

This module contains a command that returns detailed information about the system.
"""

import os
import sys
import socket
import platform
import datetime
from typing import Dict, Any, Optional, List

import psutil
import pytz

from mcp_proxy_adapter import Command, SuccessResult


class SystemInfoResult(SuccessResult):
    """
    Result of system_info command.
    
    Attributes:
        system (dict): System information
        cpu (dict): CPU information
        memory (dict): Memory information
        disk (dict): Disk information
        python (dict): Python information
        network (dict): Network information
        time (dict): Time information
    """
    
    def __init__(
        self,
        system: Dict[str, Any],
        cpu: Dict[str, Any],
        memory: Dict[str, Any],
        disk: Dict[str, Any],
        python: Dict[str, Any],
        network: Dict[str, Any],
        time: Dict[str, Any]
    ):
        """
        Initialize result.
        
        Args:
            system: System information
            cpu: CPU information
            memory: Memory information
            disk: Disk information
            python: Python information
            network: Network information
            time: Time information
        """
        self.system = system
        self.cpu = cpu
        self.memory = memory
        self.disk = disk
        self.python = python
        self.network = network
        self.time = time
        
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert result to dictionary.
        
        Returns:
            Dictionary representation
        """
        return {
            "system": self.system,
            "cpu": self.cpu,
            "memory": self.memory,
            "disk": self.disk,
            "python": self.python,
            "network": self.network,
            "time": self.time
        }
    
    @classmethod
    def get_schema(cls) -> Dict[str, Any]:
        """
        Get JSON schema for result.
        
        Returns:
            JSON schema
        """
        return {
            "type": "object",
            "properties": {
                "system": {
                    "type": "object",
                    "description": "System information",
                    "properties": {
                        "platform": {"type": "string"},
                        "system": {"type": "string"},
                        "node": {"type": "string"},
                        "release": {"type": "string"},
                        "version": {"type": "string"},
                        "machine": {"type": "string"},
                        "processor": {"type": "string"},
                        "uptime": {"type": "number"}
                    }
                },
                "cpu": {
                    "type": "object",
                    "description": "CPU information",
                    "properties": {
                        "count_physical": {"type": "integer"},
                        "count_logical": {"type": "integer"},
                        "usage_percent": {"type": "number"},
                        "frequency": {"type": "object"}
                    }
                },
                "memory": {
                    "type": "object",
                    "description": "Memory information",
                    "properties": {
                        "total": {"type": "integer"},
                        "available": {"type": "integer"},
                        "used": {"type": "integer"},
                        "percent": {"type": "number"}
                    }
                },
                "disk": {
                    "type": "object",
                    "description": "Disk information",
                    "properties": {
                        "partitions": {"type": "array"},
                        "usage": {"type": "object"}
                    }
                },
                "python": {
                    "type": "object",
                    "description": "Python information",
                    "properties": {
                        "version": {"type": "string"},
                        "implementation": {"type": "string"},
                        "executable": {"type": "string"},
                        "packages": {"type": "array"}
                    }
                },
                "network": {
                    "type": "object",
                    "description": "Network information",
                    "properties": {
                        "interfaces": {"type": "array"},
                        "connections": {"type": "integer"}
                    }
                },
                "time": {
                    "type": "object",
                    "description": "Time information",
                    "properties": {
                        "current": {"type": "string"},
                        "utc": {"type": "string"},
                        "timezone": {"type": "string"},
                        "timestamp": {"type": "number"}
                    }
                }
            }
        }


class SystemInfoCommand(Command):
    """
    Command that returns detailed system information.
    
    This command demonstrates gathering and formatting complex system data.
    """
    
    name = "system_info"
    result_class = SystemInfoResult
    
    async def execute(
        self,
        include_python_packages: bool = False,
        include_network_interfaces: bool = True
    ) -> SystemInfoResult:
        """
        Execute command.
        
        Args:
            include_python_packages: Whether to include installed Python packages
            include_network_interfaces: Whether to include network interfaces
            
        Returns:
            System information result
        """
        # Gather system information
        system_info = {
            "platform": platform.platform(),
            "system": platform.system(),
            "node": platform.node(),
            "release": platform.release(),
            "version": platform.version(),
            "machine": platform.machine(),
            "processor": platform.processor(),
            "uptime": psutil.boot_time()
        }
        
        # CPU information
        cpu_info = {
            "count_physical": psutil.cpu_count(logical=False),
            "count_logical": psutil.cpu_count(logical=True),
            "usage_percent": psutil.cpu_percent(interval=0.1),
            "frequency": {
                "current": psutil.cpu_freq().current if psutil.cpu_freq() else 0,
                "min": psutil.cpu_freq().min if psutil.cpu_freq() and psutil.cpu_freq().min else 0,
                "max": psutil.cpu_freq().max if psutil.cpu_freq() and psutil.cpu_freq().max else 0
            }
        }
        
        # Memory information
        memory = psutil.virtual_memory()
        memory_info = {
            "total": memory.total,
            "available": memory.available,
            "used": memory.used,
            "percent": memory.percent
        }
        
        # Disk information
        disk_info = {
            "partitions": [],
            "usage": {}
        }
        
        for partition in psutil.disk_partitions():
            try:
                usage = psutil.disk_usage(partition.mountpoint)
                disk_info["partitions"].append({
                    "device": partition.device,
                    "mountpoint": partition.mountpoint,
                    "fstype": partition.fstype,
                    "opts": partition.opts
                })
                disk_info["usage"][partition.mountpoint] = {
                    "total": usage.total,
                    "used": usage.used,
                    "free": usage.free,
                    "percent": usage.percent
                }
            except (PermissionError, FileNotFoundError):
                # Some mountpoints may not be accessible
                pass
        
        # Python information
        python_info = {
            "version": platform.python_version(),
            "implementation": platform.python_implementation(),
            "executable": sys.executable,
            "packages": []
        }
        
        if include_python_packages:
            try:
                import pkg_resources
                python_info["packages"] = [
                    {"name": pkg.key, "version": pkg.version}
                    for pkg in pkg_resources.working_set
                ]
            except ImportError:
                pass
        
        # Network information
        network_info = {
            "interfaces": [],
            "connections": len(psutil.net_connections())
        }
        
        if include_network_interfaces:
            for interface, addresses in psutil.net_if_addrs().items():
                for address in addresses:
                    if address.family == socket.AF_INET:  # IPv4
                        network_info["interfaces"].append({
                            "interface": interface,
                            "address": address.address,
                            "netmask": address.netmask,
                            "broadcast": address.broadcast
                        })
        
        # Time information
        now = datetime.datetime.now()
        utc_now = datetime.datetime.now(pytz.UTC)
        
        time_info = {
            "current": now.isoformat(),
            "utc": utc_now.isoformat(),
            "timezone": str(datetime.datetime.now().astimezone().tzinfo),
            "timestamp": now.timestamp()
        }
        
        return SystemInfoResult(
            system=system_info,
            cpu=cpu_info,
            memory=memory_info,
            disk=disk_info,
            python=python_info,
            network=network_info,
            time=time_info
        )
    
    @classmethod
    def get_schema(cls) -> Dict[str, Any]:
        """
        Get JSON schema for command parameters.
        
        Returns:
            JSON schema
        """
        return {
            "type": "object",
            "properties": {
                "include_python_packages": {
                    "type": "boolean",
                    "description": "Whether to include installed Python packages",
                    "default": False
                },
                "include_network_interfaces": {
                    "type": "boolean",
                    "description": "Whether to include network interfaces",
                    "default": True
                }
            },
            "additionalProperties": False
        } 