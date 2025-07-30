"""
Documentation command for the Windsweeper CLI.
"""
import os
import click
import json
import shutil
from pathlib import Path


@click.command()
@click.option('--output', '-o', type=click.Path(), default='./docs',
              help='Output directory for the generated documentation (default: ./docs)')
@click.option('--format', '-f', default='markdown',
              type=click.Choice(['markdown', 'html']),
              help='Documentation format (default: markdown)')
@click.option('--serve', '-s', is_flag=True,
              help='Serve the documentation after generation')
@click.option('--port', '-p', default=8000,
              help='Port for serving documentation (default: 8000)')
def docs(output, format, serve, port):
    """Generate and serve API documentation for the SDK.
    
    This command generates detailed API documentation for the Windsweeper SDK.
    """
    click.echo(f"Generating {format} documentation in {output}")
    
    # Create output directory
    output_dir = Path(output)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Get the package directory where documentation templates are stored
    package_dir = Path(__file__).parent.parent.parent
    templates_dir = package_dir / 'templates' / 'docs'
    
    try:
        # Generate API reference documentation
        api_dir = output_dir / 'api'
        api_dir.mkdir(parents=True, exist_ok=True)
        
        # Copy API documentation templates
        if (templates_dir / 'api').exists():
            for item in (templates_dir / 'api').glob('**/*'):
                if item.is_file():
                    relative_path = item.relative_to(templates_dir / 'api')
                    target = api_dir / relative_path
                    target.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(item, target)
        
        # Generate API reference from SDK classes and methods
        # This is a simplified version - in a real implementation we would use 
        # introspection or documentation extraction libraries
        from windsweeper import client
        api_reference = {
            'name': 'Windsweeper SDK',
            'version': client.__version__,
            'classes': [
                {
                    'name': 'WindsweeperClient',
                    'description': 'Main client for the Windsweeper API',
                    'methods': [
                        {
                            'name': 'generate',
                            'description': 'Generate content using the Windsweeper API',
                            'parameters': [
                                {'name': 'prompt', 'type': 'str', 'description': 'The prompt to generate from'}
                            ],
                            'returns': {'type': 'dict', 'description': 'Generated response'}
                        },
                        {
                            'name': 'check_health',
                            'description': 'Check the health of the Windsweeper API',
                            'parameters': [],
                            'returns': {'type': 'dict', 'description': 'Health status'}
                        }
                    ]
                }
            ]
        }
        
        # Write API reference
        with open(api_dir / 'reference.json', 'w') as f:
            json.dump(api_reference, f, indent=2)
            
        # Generate guides
        guides_dir = output_dir / 'guides'
        guides_dir.mkdir(parents=True, exist_ok=True)
        
        # Copy guide templates
        if (templates_dir / 'guides').exists():
            for item in (templates_dir / 'guides').glob('**/*'):
                if item.is_file():
                    relative_path = item.relative_to(templates_dir / 'guides')
                    target = guides_dir / relative_path
                    target.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(item, target)
        
        # Generate examples
        examples_dir = output_dir / 'examples'
        examples_dir.mkdir(parents=True, exist_ok=True)
        
        # Copy example templates
        if (templates_dir / 'examples').exists():
            for item in (templates_dir / 'examples').glob('**/*'):
                if item.is_file():
                    relative_path = item.relative_to(templates_dir / 'examples')
                    target = examples_dir / relative_path
                    target.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(item, target)
        
        # Generate index page
        with open(output_dir / 'index.md', 'w') as f:
            f.write(f"""# Windsweeper SDK Documentation

Welcome to the Windsweeper SDK documentation!

## API Reference

- [API Reference](./api/reference.json)

## Guides

- [Getting Started](./guides/getting-started.md)
- [Advanced Usage](./guides/advanced-usage.md)

## Examples

- [Basic Example](./examples/basic.md)
- [Advanced Example](./examples/advanced.md)
""")
            
        click.secho(f"✅ Documentation generated successfully in {output_dir}", fg='green')
        
        # Serve documentation if requested
        if serve:
            click.echo(f"Serving documentation on http://localhost:{port}")
            
            if format == 'html':
                # For HTML serving, we'd use a static file server
                import http.server
                import socketserver
                
                os.chdir(output_dir)
                
                handler = http.server.SimpleHTTPRequestHandler
                httpd = socketserver.TCPServer(("", port), handler)
                
                click.echo("Press Ctrl+C to stop the server")
                httpd.serve_forever()
            else:
                # For markdown, we can use a simple live server like mkdocs
                click.secho("Markdown serving requires mkdocs. Install with: pip install mkdocs", fg='yellow')
                click.echo("Then run: mkdocs serve -f docs/mkdocs.yml")
        
        return 0
        
    except Exception as e:
        click.secho(f"❌ Error generating documentation: {str(e)}", fg='red')
        return 1
