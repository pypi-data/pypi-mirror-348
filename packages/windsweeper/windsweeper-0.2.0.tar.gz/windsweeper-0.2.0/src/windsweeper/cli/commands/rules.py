"""
Rules command for the Windsweeper CLI.
"""
import click
import json
import yaml
from pathlib import Path
from windsweeper import create_client


@click.group(name="rules")
def rules():
    """Manage Windsweeper rules."""
    pass


@rules.command(name="list")
@click.option('--url', '-u', default='http://localhost:9001', 
              help='URL of the MCP server')
@click.option('--api-key', '-k', envvar='WINDSWEEPER_API_KEY',
              help='API key for the MCP server (can also be set via WINDSWEEPER_API_KEY env var)')
@click.option('--format', '-f', type=click.Choice(['table', 'json']), default='table',
              help='Output format (default: table)')
def list_rules(url, api_key, format):
    """List available rules."""
    client = create_client(base_url=url, api_key=api_key)
    
    try:
        response = client.list_rules()
        
        if format == 'json':
            click.echo(json.dumps(response, indent=2))
        else:  # table format
            if not response:
                click.echo("No rules found.")
                return 0
                
            click.echo("\nAvailable Rules:")
            click.echo("-" * 80)
            click.echo(f"{'ID':<10} {'Name':<20} {'Description':<40}")
            click.echo("-" * 80)
            
            for rule in response:
                click.echo(
                    f"{rule.get('id', 'N/A'):<10} "
                    f"{rule.get('name', 'N/A'):<20} "
                    f"{rule.get('description', 'N/A')[:40]:<40}"
                )
                
            click.echo("-" * 80)
            click.echo(f"Total: {len(response)} rules")
            
        return 0
    except Exception as e:
        click.secho(f"❌ Error listing rules: {str(e)}", fg='red')
        return 1


@rules.command(name="validate")
@click.argument('rule_file', type=click.Path(exists=True))
@click.option('--url', '-u', default='http://localhost:9001', 
              help='URL of the MCP server')
@click.option('--api-key', '-k', envvar='WINDSWEEPER_API_KEY',
              help='API key for the MCP server (can also be set via WINDSWEEPER_API_KEY env var)')
def validate_rule(rule_file, url, api_key):
    """Validate a rule definition.
    
    RULE_FILE is the path to the rule file (YAML or JSON format).
    """
    client = create_client(base_url=url, api_key=api_key)
    
    try:
        # Load the rule file
        rule_path = Path(rule_file)
        if rule_path.suffix.lower() in ['.yaml', '.yml']:
            with open(rule_path, 'r') as f:
                rule_data = yaml.safe_load(f)
        elif rule_path.suffix.lower() == '.json':
            with open(rule_path, 'r') as f:
                rule_data = json.load(f)
        else:
            click.secho(f"❌ Unsupported file format: {rule_path.suffix}", fg='red')
            return 1
            
        # Validate the rule
        response = client.validate_rule(rule_data)
        
        if response.get('valid', False):
            click.secho(f"✅ Rule is valid!", fg='green')
            return 0
        else:
            click.secho(f"❌ Rule validation failed:", fg='red')
            for error in response.get('errors', []):
                click.echo(f"  - {error}")
            return 1
            
    except Exception as e:
        click.secho(f"❌ Error validating rule: {str(e)}", fg='red')
        return 1


@rules.command(name="apply")
@click.argument('rule_file', type=click.Path(exists=True))
@click.argument('target_file', type=click.Path(exists=True))
@click.option('--url', '-u', default='http://localhost:9001', 
              help='URL of the MCP server')
@click.option('--api-key', '-k', envvar='WINDSWEEPER_API_KEY',
              help='API key for the MCP server (can also be set via WINDSWEEPER_API_KEY env var)')
@click.option('--output', '-o', type=click.Path(),
              help='Output file for the transformed content')
def apply_rule(rule_file, target_file, url, api_key, output):
    """Apply a rule to a target file.
    
    RULE_FILE is the path to the rule file (YAML or JSON format).
    TARGET_FILE is the file to apply the rule to.
    """
    client = create_client(base_url=url, api_key=api_key)
    
    try:
        # Load the rule file
        rule_path = Path(rule_file)
        if rule_path.suffix.lower() in ['.yaml', '.yml']:
            with open(rule_path, 'r') as f:
                rule_data = yaml.safe_load(f)
        elif rule_path.suffix.lower() == '.json':
            with open(rule_path, 'r') as f:
                rule_data = json.load(f)
        else:
            click.secho(f"❌ Unsupported file format: {rule_path.suffix}", fg='red')
            return 1
            
        # Load the target file
        with open(target_file, 'r') as f:
            target_content = f.read()
            
        # Apply the rule
        response = client.apply_rule(rule_data, target_content)
        
        result = response.get('result', '')
        
        if output:
            # Write to output file
            with open(output, 'w') as f:
                f.write(result)
            click.secho(f"✅ Transformed content written to {output}", fg='green')
        else:
            # Print to console
            click.echo("\n--- Transformed Content ---\n")
            click.echo(result)
            click.echo("\n--- End of Content ---")
            
        return 0
    except Exception as e:
        click.secho(f"❌ Error applying rule: {str(e)}", fg='red')
        return 1
