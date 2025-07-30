"""
Generate command for the Windsweeper CLI.
"""
import os
import click
import json
from pathlib import Path
from windsweeper import create_client


@click.command()
@click.argument('prompt', required=True)
@click.option('--url', '-u', default='http://localhost:9001', 
              help='URL of the MCP server')
@click.option('--api-key', '-k', envvar='WINDSWEEPER_API_KEY',
              help='API key for the MCP server (can also be set via WINDSWEEPER_API_KEY env var)')
@click.option('--output', '-o', type=click.Path(), 
              help='Output file to write the generated content to')
@click.option('--format', '-f', type=click.Choice(['text', 'json', 'markdown']), default='text',
              help='Output format (default: text)')
def generate(prompt, url, api_key, output, format):
    """Generate content using the MCP server.
    
    PROMPT is the text prompt to generate content from.
    """
    click.echo(f"Generating content based on prompt: {prompt}")
    
    client = create_client(base_url=url, api_key=api_key)
    
    try:
        response = client.generate(prompt)
        
        if format == 'json':
            result = json.dumps(response, indent=2)
        elif format == 'markdown':
            result = f"# Generated Content\n\n{response.get('text', '')}"
        else:  # text
            result = response.get('text', '')
        
        if output:
            # Create directory if it doesn't exist
            output_path = Path(output)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Write to file
            with open(output, 'w') as f:
                f.write(result)
            click.secho(f"✅ Generated content written to {output}", fg='green')
        else:
            # Print to console
            click.echo("\n--- Generated Content ---\n")
            click.echo(result)
            click.echo("\n--- End of Content ---")
            
        return 0
    except Exception as e:
        click.secho(f"❌ Error generating content: {str(e)}", fg='red')
        return 1
