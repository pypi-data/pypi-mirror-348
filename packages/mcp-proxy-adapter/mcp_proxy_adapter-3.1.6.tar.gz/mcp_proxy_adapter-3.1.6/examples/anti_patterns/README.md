# Anti-Patterns for MCP Microservice

This directory contains examples of anti-patterns and bad practices when using MCP Microservice.
These examples demonstrate what **NOT** to do and common mistakes to avoid.

## Categories

1. **Bad Design Patterns** - Examples of poor architectural and design choices
2. **Performance Issues** - Examples that can cause performance problems
3. **Security Problems** - Examples with potential security vulnerabilities

## Purpose

These examples serve as educational resources to help you:

1. Recognize common mistakes
2. Understand why they are problematic
3. Learn better alternatives

**WARNING:** These examples contain intentional errors, bugs, and security vulnerabilities.
Do not use them in production environments or as a basis for your own code.

## Structure

```
anti_patterns/
├── bad_design/              # Poor architectural and design choices
│   ├── monolithic_command.py    # Example of a command that does too much
│   ├── global_state.py          # Example of using global state
│   └── README.md                # Explanation of bad design patterns
├── performance_issues/      # Performance problems
│   ├── blocking_operations.py   # Example of blocking the event loop
│   ├── memory_leaks.py          # Example of potential memory leaks
│   └── README.md                # Explanation of performance issues
├── security_problems/       # Security vulnerabilities
│   ├── no_validation.py         # Example of missing input validation
│   ├── command_injection.py     # Example of command injection vulnerability
│   └── README.md                # Explanation of security problems
└── README.md                # This file
```

## How to Use

Each example directory contains a README.md file explaining:

1. What the anti-pattern is
2. Why it's problematic
3. Better alternatives
4. How to fix the issues

Use these examples as a reference for what to avoid, not as templates for your code. 