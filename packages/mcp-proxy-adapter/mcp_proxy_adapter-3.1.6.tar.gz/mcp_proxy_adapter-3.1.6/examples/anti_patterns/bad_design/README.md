# Bad Design Patterns

This directory contains examples of poor architectural and design choices when using MCP Microservice.

## Included Examples

1. **[monolithic_command.py](./monolithic_command.py)** - A command that tries to do too much
2. **[global_state.py](./global_state.py)** - Using global state for command data

## Monolithic Command Anti-Pattern

### Problem

The `MonolithicCommand` tries to handle multiple responsibilities:
- Data processing
- Validation
- Database operations
- File operations
- Notification

### Why It's Bad

1. **Violates Single Responsibility Principle**: Each command should do one thing well
2. **Difficult to Test**: Large commands with many responsibilities are hard to test
3. **Hard to Maintain**: Changes to one feature may affect others
4. **Poor Reusability**: Cannot reuse parts of the functionality

### Better Alternative

Split the monolithic command into multiple smaller commands:
- `ProcessDataCommand` - Handles data processing
- `SaveDataCommand` - Handles database operations
- `GenerateReportCommand` - Handles file operations
- `SendNotificationCommand` - Handles notifications

## Global State Anti-Pattern

### Problem

The `GlobalStateCommand` uses global variables to store and share data between command executions.

### Why It's Bad

1. **Thread Safety**: Global state is not thread-safe in asynchronous environments
2. **Testing Difficulty**: Commands with global state are hard to test in isolation
3. **Hidden Dependencies**: Dependencies are not explicit
4. **State Management**: Difficult to track and manage state changes

### Better Alternative

Use proper dependency injection and maintain state within the command instance:

```python
class ProperStateCommand(Command):
    name = "proper_state"
    result_class = StateResult
    
    def __init__(self):
        self._state = {}  # State is maintained per instance
    
    async def execute(self, key: str, value: Any = None) -> StateResult:
        if value is not None:
            self._state[key] = value
        return StateResult(key, self._state.get(key))
```

## How to Fix

1. **Identify Single Responsibilities**: Break down commands by responsibility
2. **Explicit Dependencies**: Use constructor parameters or method arguments
3. **Avoid Global State**: Maintain state within instances or external services
4. **Use Dependency Injection**: Inject dependencies through constructors 