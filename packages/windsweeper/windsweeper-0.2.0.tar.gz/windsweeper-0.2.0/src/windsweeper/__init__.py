"""
Windsweeper Python SDK
This package provides a client for interacting with the Windsweeper MCP server
"""

from ._version import __version__
from .client import WindsweeperClient, ValidationResult, Resource, ValidationIssue, GenerateOptions
from .monitoring import get_telemetry, configure_telemetry, tracked

__all__ = [
    'WindsweeperClient', 
    'ValidationResult', 
    'Resource', 
    'ValidationIssue', 
    'GenerateOptions', 
    'create_client',
    'get_telemetry',
    'configure_telemetry',
    'tracked',
    '__version__'
]

def create_client(server_url, api_key=None, timeout=30, telemetry=None):
    """Create a new Windsweeper client instance.
    
    Args:
        server_url (str): The URL of the Windsweeper MCP server
        api_key (str, optional): API key for authentication
        timeout (int, optional): Request timeout in seconds (default: 30)
        telemetry (dict, optional): Telemetry configuration with keys:
            - enabled (bool): Whether to enable telemetry
            - application_id (str): Identifier for the client application
            - options (dict): Additional telemetry options
        
    Returns:
        WindsweeperClient: A configured client instance
    """
    return WindsweeperClient(server_url=server_url, api_key=api_key, timeout=timeout, telemetry=telemetry)
