# Windsweeper Python SDK & CLI v0.2.1

[![PyPI version](https://badge.fury.io/py/windsweeper.svg)](https://badge.fury.io/py/windsweeper)
[![Python Version](https://img.shields.io/pypi/pyversions/windsweeper.svg)](https://pypi.org/project/windsweeper/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Tests](https://github.com/windsweeper/windsweeper/actions/workflows/ci.yml/badge.svg)](https://github.com/windsweeper/windsweeper/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/windsweeper/windsweeper/branch/main/graph/badge.svg)](https://codecov.io/gh/windsweeper/windsweeper)

The Windsweeper package provides both a Python SDK client and a powerful CLI for interacting with the Windsweeper MCP (Model Control Protocol) server. It enables you to validate rules and code, apply templates, generate content, manage resources, and more through both programmatic and command-line interfaces.

## Features

- **Dual Interfaces**: Use either the Python SDK or CLI based on your needs
- **Type Safety**: Built with Python type hints and Pydantic for robust data validation
- **Async Support**: All SDK API calls support both synchronous and asynchronous operations
- **Command-Line Interface**: Intuitive CLI commands for all MCP operations
- **Modern Python**: Requires Python 3.8+ with support for the latest language features
- **Extensible**: Easy to extend with custom resource types, validators, and CLI commands
- **Comprehensive Documentation**: Detailed guides, examples, and API references

## Installation

### Standard Installation

The Windsweeper package can be installed via pip, which gives you access to both the SDK and CLI:

```bash
pip install windsweeper
```

After installation, the SDK will be available for import in Python, and the `windsweeper` CLI command will be available in your terminal.

### For Development

Clone the repository and install in development mode:

```bash
git clone https://github.com/windsweeper/windsweeper.git
cd windsweeper/packages/sdk-python
pip install -e '.[dev]'  # Install with development dependencies
pre-commit install  # Install pre-commit hooks
```

### Verifying Installation

To verify that the CLI is properly installed:

```bash
windsweeper --version
# Output: Windsweeper CLI v0.2.1
```

## Quick Start

### SDK Usage

#### Basic SDK Example

```python
from windsweeper import create_client

# Create a client
client = create_client(
    server_url='http://localhost:9001',
    api_key='your-api-key'  # Optional, can also be set via WINDSWEEPER_API_KEY env variable
)

# Check server health
is_healthy = client.check_health()
print(f"Server is {'healthy' if is_healthy else 'unhealthy'}")

# List resources
resources = client.list_resources('my-server')
print(f"Found {len(resources.resources)} resources")

# Validate a rule
validation_result = client.validate_rule('your-rule-content')
if validation_result.valid:
    print('Rule is valid!')
else:
    print('Rule validation failed:')
    for issue in validation_result.issues:
        print(f"- {issue.severity}: {issue.message}")
```

#### Async SDK Example

```python
import asyncio
from windsweeper import create_async_client

async def main():
    async with create_async_client('http://localhost:9001') as client:
        # Check server health
        is_healthy = await client.check_health()
        print(f"Server is {'healthy' if is_healthy else 'unhealthy'}")

        # List resources
        resources = await client.list_resources('my-server')
        print(f"Found {len(resources.resources)} resources")

        # Generate content
        generation_result = await client.generate(
            prompt="Create a Python function to calculate Fibonacci numbers",
            options={
                "mode": "structured",
                "format": "python",
                "max_tokens": 500
            }
        )
        print(generation_result.content)

asyncio.run(main())
```

### CLI Usage

The Windsweeper CLI provides an intuitive command-line interface to all SDK functionality.

#### Getting Started with the CLI

```bash
# Check help to see all available commands
windsweeper --help

# Initialize a new Windsweeper project
windsweeper init my-project

# Check server health
windsweeper health --server http://localhost:9001
```

#### Working with Rules Using the CLI

```bash
# Validate a rule file
windsweeper rules validate path/to/rule.yaml

# Create a new rule from template
windsweeper rules create my-new-rule --template basic-rule

# List all rules
windsweeper rules list --server my-server
```

#### Content Generation with the CLI

```bash
# Generate content from a prompt
windsweeper generate "Create a Python function that sorts a list" --format python --output generated_code.py

# Apply a template
windsweeper generate --template api-endpoint --variables '{"endpoint": "/users", "method": "GET"}' --output api_endpoint.py
```

#### Serving a Local Server

```bash
# Start a local MCP server for development and testing
windsweeper serve --port 9001
```

## Documentation

Full documentation, including comprehensive API references, guides, and examples for both the SDK and CLI, is available at [https://docs.windsweeper.io](https://docs.windsweeper.io).

### SDK Components

- **Client**: The main entry point for interacting with the Windsweeper API
- **Models**: Pydantic models for all request/response objects
- **Exceptions**: Custom exceptions for error handling
- **Extensions**: Plug-in architecture for extending functionality
- **Utils**: Helper functions and utilities
- **CLI**: Command-line interface implementation

## SDK API Reference

The Windsweeper SDK provides both synchronous and asynchronous methods for interacting with the MCP server.

### Core Client Methods

#### Health and Status

```python
# Check server health
is_healthy = client.check_health()

# Get server version information
version_info = client.get_version()
```

#### Resource Management

```python
# List all resources from a server
resources = client.list_resources(server_name, cursor=None)

# Get a specific resource
resource = client.get_resource(server_name, resource_id)
```

#### Rule and Code Validation

```python
# Validate a rule definition
validation_result = client.validate_rule(content, language_id='yaml', uri=None)

# Validate code against rules
validation_results = client.validate_code(code, rule_ids, language_id)
```

#### Content Generation and Template Application

```python
# Generate content from a prompt
generation_result = client.generate(prompt, options=None)

# Apply a template
applied_template = client.apply_template(template_id, variables)
```

#### Feedback and Telemetry

```python
# Submit feedback
client.submit_feedback(feedback_data)

# Log telemetry
client.log_telemetry(event_name, event_data)
```

## CLI Commands Reference

The Windsweeper CLI provides a comprehensive set of commands for interacting with the MCP server.

### Global Options

- `--server`: Specify the MCP server URL
- `--api-key`: Provide API key for authentication
- `--verbose`: Enable verbose output
- `--help`: Show help for any command
- `--version`: Show CLI version

### Project Commands

```bash
# Initialize a new project
windsweeper init [project-name] [--template <template>]

# Show project configuration
windsweeper config show

# Set project configuration
windsweeper config set [key] [value]
```

### Server Management

```bash
# Check server health
windsweeper health [--server <url>]

# Start a local MCP server
windsweeper serve [--port <port>] [--host <host>]
```

### Resource Management

```bash
# List resources
windsweeper resources list [server-name] [--filter <filter>] [--limit <limit>]

# Get a specific resource
windsweeper resources get [server-name] [resource-id]
```

### Rule Commands

```bash
# Create a new rule
windsweeper rules create [name] [--template <template>]

# Validate a rule
windsweeper rules validate [file-path]

# List all rules
windsweeper rules list [--server <server>]
```

### Generation Commands

```bash
# Generate content from a prompt
windsweeper generate [prompt] [--format <format>] [--output <file>]

# Apply a template
windsweeper generate --template [template-id] --variables [json-variables] [--output <file>]
```

### Documentation Commands

```bash
# View documentation
windsweeper docs [topic]

# Start documentation server
windsweeper docs serve [--port <port>]
```

## Development

### Setting Up the Development Environment

1. Clone the repository:
   ```bash
   git clone https://github.com/windsweeper/windsweeper.git
   cd windsweeper/packages/sdk-python
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. Install the package in development mode with all dependencies:
   ```bash
   pip install -e '.[dev]'
   ```

4. Install pre-commit hooks:
   ```bash
   pre-commit install
   ```

### Running Tests

Run the test suite with:

```bash
pytest
```

Run tests with coverage report:

```bash
pytest --cov=windsweeper --cov-report=term-missing
```

### Testing the CLI

When installed in development mode, the CLI will reflect your code changes. Test CLI commands with:

```bash
windsweeper --help
```

### Code Style

This project uses:

- **Black** for code formatting
- **isort** for import sorting
- **flake8** for linting
- **mypy** for type checking

Run all code style checks:

```bash
pre-commit run --all-files
```

## Contributing

Contributions are welcome! Please read our [Contributing Guide](CONTRIBUTING.md) for details on how to submit pull requests, report issues, and suggest improvements.

### Contributing to the SDK

When contributing new features, please ensure both the SDK and CLI interfaces are updated as needed. Add appropriate tests and documentation for both interfaces.

### Contributing to the CLI

When adding new CLI commands, follow these guidelines:
- Place new command implementations in `src/windsweeper/cli/commands/`
- Update the CLI entry point in `src/windsweeper/cli/main.py`
- Include detailed help text for all commands and options
- Add tests in `tests/cli/`

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

For support, please open an issue in the [GitHub repository](https://github.com/windsweeper/windsweeper/issues) or contact us at [support@windsweeper.io](mailto:support@windsweeper.io).

## Changelog

### v0.2.1 (2025-05-18)

- Documentation updates for SDK and CLI integration
- Extended CLI command reference
- Improved error handling in CLI commands
- Enhanced code examples for both SDK and CLI

### v0.2.0 (2025-05-16)

- Added comprehensive CLI functionality
- Implemented command structure for all MCP operations
- Added `init`, `serve`, `rules`, `generate`, and `docs` commands
- Improved SDK client with additional helper methods
- Added CLI-specific configuration handling

### v0.1.0 (2025-05-01)

- Initial release of Windsweeper Python SDK
- Basic client implementation for MCP server
- Support for rule validation and resource management
- Async and sync client interfaces

For a complete list of changes in each version, see [CHANGELOG.md](CHANGELOG.md).
