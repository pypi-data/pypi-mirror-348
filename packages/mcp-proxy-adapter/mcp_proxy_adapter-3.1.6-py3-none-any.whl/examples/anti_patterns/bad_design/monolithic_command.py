"""
ANTI-PATTERN EXAMPLE: Monolithic Command

This module demonstrates an anti-pattern where a command tries to do too much,
violating the Single Responsibility Principle.

WARNING: This is a BAD EXAMPLE! Do not use this approach in production.
"""

import os
import json
import sqlite3
import smtplib
import time
from email.message import EmailMessage
from typing import Dict, Any, List, Optional

from mcp_proxy_adapter import Command, SuccessResult


# Global connection pool - another anti-pattern
DB_CONNECTIONS = {}


class MonolithicResult(SuccessResult):
    """Result of monolithic command."""
    
    def __init__(self, status: str, data: Dict[str, Any]):
        """
        Initialize result.
        
        Args:
            status: Operation status
            data: Result data
        """
        self.status = status
        self.data = data
        
    def to_dict(self) -> Dict[str, Any]:
        """Convert result to dictionary."""
        return {
            "status": self.status,
            "data": self.data
        }
    
    @classmethod
    def get_schema(cls) -> Dict[str, Any]:
        """Get JSON schema for result."""
        return {
            "type": "object",
            "properties": {
                "status": {"type": "string"},
                "data": {"type": "object"}
            },
            "required": ["status", "data"]
        }


class MonolithicCommand(Command):
    """
    ANTI-PATTERN: This command tries to do too much.
    
    It handles:
    1. Data processing
    2. Validation
    3. Database operations
    4. File operations
    5. Notifications
    
    This violates the Single Responsibility Principle and makes the code:
    - Hard to test
    - Hard to maintain
    - Difficult to reuse
    """
    
    name = "do_everything"
    result_class = MonolithicResult
    
    async def execute(
        self,
        action: str,
        data: Dict[str, Any],
        save_to_db: bool = True,
        generate_report: bool = True,
        notify_users: List[str] = None
    ) -> MonolithicResult:
        """
        Execute monolithic command.
        
        Args:
            action: Action to perform (process, update, delete)
            data: Input data to process
            save_to_db: Whether to save data to database
            generate_report: Whether to generate a report
            notify_users: List of users to notify
        
        Returns:
            Result of operations
        """
        result_data = {}
        
        # Step 1: Process data - this should be a separate command
        processed_data = self._process_data(action, data)
        result_data["processed"] = processed_data
        
        # Step 2: Save to database - this should be a separate command
        if save_to_db:
            db_result = self._save_to_database(processed_data)
            result_data["database"] = db_result
        
        # Step 3: Generate report - this should be a separate command
        if generate_report:
            report_path = self._generate_report(processed_data)
            result_data["report"] = report_path
        
        # Step 4: Notify users - this should be a separate command
        if notify_users:
            notification_result = self._send_notifications(
                notify_users, processed_data, report_path if generate_report else None
            )
            result_data["notifications"] = notification_result
        
        return MonolithicResult("success", result_data)
    
    def _process_data(self, action: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Process input data based on action."""
        # Simulate data processing
        processed = dict(data)
        
        if action == "process":
            # Complex data processing logic
            processed["status"] = "processed"
            processed["timestamp"] = time.time()
            
            # Calculate some values
            if "values" in processed and isinstance(processed["values"], list):
                processed["sum"] = sum(processed["values"])
                processed["average"] = sum(processed["values"]) / len(processed["values"])
            
        elif action == "update":
            # Update logic
            processed["status"] = "updated"
            processed["updated_at"] = time.time()
            
        elif action == "delete":
            # Delete logic
            processed["status"] = "deleted"
            processed["deleted_at"] = time.time()
            
        return processed
    
    def _save_to_database(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Save data to database - should be a separate command."""
        # Get or create database connection
        conn = self._get_db_connection()
        cursor = conn.cursor()
        
        # Create table if not exists
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY,
            data TEXT,
            status TEXT,
            timestamp REAL
        )
        """)
        
        # Insert data
        data_json = json.dumps(data)
        cursor.execute(
            "INSERT INTO items (data, status, timestamp) VALUES (?, ?, ?)",
            (data_json, data.get("status", "unknown"), time.time())
        )
        
        # Get ID of inserted row
        row_id = cursor.lastrowid
        conn.commit()
        
        return {"id": row_id, "status": "saved"}
    
    def _generate_report(self, data: Dict[str, Any]) -> str:
        """Generate report file - should be a separate command."""
        # Create reports directory if not exists
        os.makedirs("reports", exist_ok=True)
        
        # Generate report filename
        filename = f"reports/report_{int(time.time())}.json"
        
        # Write report to file
        with open(filename, "w") as f:
            json.dump(data, f, indent=2)
        
        return filename
    
    def _send_notifications(
        self, 
        recipients: List[str], 
        data: Dict[str, Any],
        report_path: Optional[str] = None
    ) -> Dict[str, Any]:
        """Send notifications to users - should be a separate command."""
        # Configure email server (hardcoded values - another anti-pattern)
        smtp_server = "smtp.example.com"
        smtp_port = 587
        smtp_user = "service@example.com"
        smtp_password = "password123"  # Hardcoding passwords is a security issue!
        
        # Create message
        msg = EmailMessage()
        msg["Subject"] = f"Data {data.get('status', 'processed')}"
        msg["From"] = "service@example.com"
        msg["To"] = ", ".join(recipients)
        
        # Set content
        content = f"Data has been {data.get('status', 'processed')}.\n\n"
        if report_path:
            content += f"Report is available at: {report_path}\n"
        msg.set_content(content)
        
        # Send email (commented out to prevent actual sending)
        # with smtplib.SMTP(smtp_server, smtp_port) as server:
        #     server.login(smtp_user, smtp_password)
        #     server.send_message(msg)
        
        # Simulate successful sending
        return {
            "sent_to": recipients,
            "status": "sent"
        }
    
    def _get_db_connection(self) -> sqlite3.Connection:
        """Get database connection from pool."""
        if "default" not in DB_CONNECTIONS:
            # Create new connection
            DB_CONNECTIONS["default"] = sqlite3.connect(":memory:")
        
        return DB_CONNECTIONS["default"]
    
    @classmethod
    def get_schema(cls) -> Dict[str, Any]:
        """Get JSON schema for command parameters."""
        return {
            "type": "object",
            "properties": {
                "action": {
                    "type": "string",
                    "enum": ["process", "update", "delete"],
                    "description": "Action to perform"
                },
                "data": {
                    "type": "object",
                    "description": "Input data to process"
                },
                "save_to_db": {
                    "type": "boolean",
                    "description": "Whether to save data to database",
                    "default": True
                },
                "generate_report": {
                    "type": "boolean",
                    "description": "Whether to generate a report",
                    "default": True
                },
                "notify_users": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "List of users to notify",
                    "default": []
                }
            },
            "required": ["action", "data"]
        } 