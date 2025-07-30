"""
Serve command for the Windsweeper CLI.
"""
import os
import click
import uvicorn
from pathlib import Path


@click.command()
@click.option('--host', '-h', default='127.0.0.1',
              help='Host to bind the server to (default: 127.0.0.1)')
@click.option('--port', '-p', default=9001,
              help='Port to bind the server to (default: 9001)')
@click.option('--reload', is_flag=True,
              help='Enable auto-reload for development')
@click.option('--log-level', default='info',
              type=click.Choice(['debug', 'info', 'warning', 'error', 'critical']),
              help='Log level (default: info)')
def serve(host, port, reload, log_level):
    """Start the MCP server.
    
    This runs a FastAPI server that provides access to the Windsweeper MCP functionality.
    """
    if not os.environ.get('OPENAI_API_KEY'):
        click.secho('WARNING: OPENAI_API_KEY environment variable is not set. '
                    'Some features may not work correctly.', fg='yellow')
    
    click.echo(f"Starting MCP server on {host}:{port}")
    
    # Import server module at runtime to avoid circular imports
    from windsweeper.server import create_app
    
    try:
        app = create_app()
        uvicorn.run(
            "windsweeper.server:app",
            host=host,
            port=port,
            reload=reload,
            log_level=log_level
        )
        return 0
    except Exception as e:
        click.secho(f"❌ Error starting server: {str(e)}", fg='red')
        return 1
