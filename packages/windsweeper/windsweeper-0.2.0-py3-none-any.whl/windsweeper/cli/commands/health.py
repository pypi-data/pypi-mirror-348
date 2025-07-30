"""
Health check command for the Windsweeper CLI.
"""
import click
from windsweeper import create_client


@click.command()
@click.option('--url', '-u', default='http://localhost:9001', 
              help='URL of the MCP server')
@click.option('--api-key', '-k', envvar='WINDSWEEPER_API_KEY',
              help='API key for the MCP server (can also be set via WINDSWEEPER_API_KEY env var)')
def health(url, api_key):
    """Check the health of the MCP server."""
    click.echo(f"Checking health of MCP server at {url}...")
    
    client = create_client(base_url=url, api_key=api_key)
    
    try:
        response = client.check_health()
        if response.get('status') == 'ok':
            click.secho("✅ MCP server is healthy", fg='green')
            click.echo(f"Version: {response.get('version', 'unknown')}")
            click.echo(f"Uptime: {response.get('uptime', 'unknown')}")
            return 0
        else:
            click.secho("❌ MCP server is not healthy", fg='red')
            click.echo(f"Status: {response.get('status', 'unknown')}")
            return 1
    except Exception as e:
        click.secho(f"❌ Error connecting to MCP server: {str(e)}", fg='red')
        return 1
