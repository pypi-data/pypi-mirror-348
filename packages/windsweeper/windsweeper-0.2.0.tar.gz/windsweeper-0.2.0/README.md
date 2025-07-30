# Windsweeper SDK for Python

# Windsweeper Python SDK

[![PyPI version](https://badge.fury.io/py/windsweeper.svg)](https://badge.fury.io/py/windsweeper)
[![Python Version](https://img.shields.io/pypi/pyversions/windsweeper.svg)](https://pypi.org/project/windsweeper/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Tests](https://github.com/windsweeper/windsweeper/actions/workflows/ci.yml/badge.svg)](https://github.com/windsweeper/windsweeper/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/windsweeper/windsweeper/branch/main/graph/badge.svg?token=YOUR-TOKEN)](https://codecov.io/gh/windsweeper/windsweeper)

This package provides a Python client for interacting with the Windsweeper MCP (Model Control Protocol) server. It allows you to validate rules and code, apply templates, generate content, and manage resources in a type-safe and efficient manner.

## Features

- **Type Safety**: Built with Python type hints and Pydantic for robust data validation
- **Async Support**: All API calls support both synchronous and asynchronous operations
- **Comprehensive Testing**: Extensive test suite with high coverage
- **Modern Python**: Requires Python 3.8+ with support for the latest language features
- **Extensible**: Easy to extend with custom resource types and validators

## Installation

### Using pip

```bash
pip install windsweeper
```

### For Development

Clone the repository and install in development mode:

```bash
git clone https://github.com/windsweeper/windsweeper.git
cd windsepper/packages/sdk-python
pip install -e '.[dev]'  # Install with development dependencies
pre-commit install  # Install pre-commit hooks
```

## Quick Start

### Basic Usage

```python
from windsweeper import create_client

# Create a client
client = create_client(
    server_url='http://localhost:9001',
    api_key='your-api-key'  # Optional, can also be set via WINDSWEEPER_API_KEY
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

### Async Usage

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

asyncio.run(main())
```

## Documentation

For full documentation, including API reference and examples, please visit [https://docs.windsweeper.io](https://docs.windsweeper.io).

### Key Components

- **Client**: The main entry point for interacting with the Windsweeper API
- **Models**: Pydantic models for all request/response objects
- **Exceptions**: Custom exceptions for error handling
- **Utils**: Helper functions and utilities

## Development

### Setting Up the Development Environment

1. Clone the repository:
   ```bash
   git clone https://github.com/windsweeper/windsweeper.git
   cd windsepper/packages/sdk-python
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

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

For support, please open an issue in the [GitHub repository](https://github.com/windsweeper/windsweeper/issues) or contact us at [support@windsweeper.io](mailto:support@windsweeper.io).

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for a list of changes in each version.

#### `check_health()`

Checks if the server is healthy.

**Returns:** `bool` - True if the server is healthy

#### `list_resources(server_name, cursor=None)`

Lists resources from the MCP server.

**Parameters:**
- `server_name` - Name of the server to list resources from
- `cursor` - Optional pagination cursor

**Returns:** `dict` - Dictionary containing resources and optional next cursor

#### `get_resource(server_name, resource_id)`

Gets a specific resource from the MCP server.

**Parameters:**
- `server_name` - Name of the server to get the resource from
- `resource_id` - ID of the resource to get

**Returns:** The requested resource

#### `validate_rule(content, language_id='yaml', uri=None)`

Validates a rule definition.

**Parameters:**
- `content` - Rule content to validate
- `language_id` - Language of the rule content (default: 'yaml')
- `uri` - Optional URI of the rule

**Returns:** `dict` - Validation result with 'valid', 'issues', and 'message' keys

#### `validate_code(code, rule_ids, language_id)`

Validates code against multiple rules.

**Parameters:**
- `code` - Code to validate
- `rule_ids` - List of rule IDs to validate against
- `language_id` - Language of the code

**Returns:** `dict` - Dictionary mapping rule IDs to validation results

#### `apply_template(template_id, variables)`

Applies a template.

**Parameters:**
- `template_id` - ID of the template to apply
- `variables` - Dictionary of variables to use in the template

**Returns:** `str` - Generated content

#### `generate(prompt, options=None)`

Generates content.

**Parameters:**
- `prompt` - Prompt to generate from
- `options` - Optional dictionary of generation options
  - `mode` - Generation mode
  - `format` - Output format
  - `temperature` - Temperature for generation
  - `max_tokens` - Maximum tokens to generate
  - `include_sources` - Whether to include sources in the response

**Returns:** `str` - Generated content

## Type Definitions

The SDK includes TypedDict definitions for the following types:

- `ValidationIssue` - Issue found during validation
- `ValidationResult` - Result of a validation operation
- `Resource` - A resource from the MCP server
- `GenerateOptions` - Options for generation requests

## Development

### Installing for Development

```bash
pip install -e ".[dev]"
```

### Testing

```bash
pytest
```

## License

MIT
