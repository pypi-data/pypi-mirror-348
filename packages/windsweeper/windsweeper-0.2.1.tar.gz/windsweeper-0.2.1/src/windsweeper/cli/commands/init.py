"""
Initialize command for the Windsweeper CLI.
"""
import os
import click
import shutil
from pathlib import Path


@click.command()
@click.argument('project_name', required=True)
@click.option('--template', '-t', default='basic',
              type=click.Choice(['basic', 'advanced', 'full']), 
              help='Project template to use (default: basic)')
@click.option('--language', '-l', default='python',
              type=click.Choice(['python', 'javascript', 'typescript']),
              help='Programming language to use (default: python)')
@click.option('--output-dir', '-o', type=click.Path(), default='.',
              help='Directory to create the project in (default: current directory)')
def init(project_name, template, language, output_dir):
    """Initialize a new Windsweeper project.

    PROJECT_NAME is the name of the project to create.
    """
    click.echo(f"Initializing new Windsweeper project: {project_name}")
    click.echo(f"  Template: {template}")
    click.echo(f"  Language: {language}")
    
    # Create the project directory
    project_dir = Path(output_dir) / project_name
    if project_dir.exists():
        if not click.confirm(f"Directory {project_dir} already exists. Overwrite?"):
            click.echo("Initialization cancelled.")
            return 1

    project_dir.mkdir(parents=True, exist_ok=True)
    
    # Get the package directory where templates are stored
    package_dir = Path(__file__).parent.parent.parent
    template_dir = package_dir / 'templates' / language / template
    
    if not template_dir.exists():
        click.secho(f"❌ Template '{template}' for language '{language}' not found.", fg='red')
        return 1
    
    # Copy template files
    try:
        for item in template_dir.glob('**/*'):
            if item.is_file():
                relative_path = item.relative_to(template_dir)
                target = project_dir / relative_path
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(item, target)
                
        # Replace placeholders in files
        for ext in ['.py', '.js', '.ts', '.md', '.json', '.yaml', '.yml']:
            for file in project_dir.glob(f"**/*{ext}"):
                _replace_placeholders(file, {'PROJECT_NAME': project_name})
                
        # Create .env file
        env_file = project_dir / '.env'
        with open(env_file, 'w') as f:
            f.write("# Windsweeper environment variables\n")
            f.write("WINDSWEEPER_API_KEY=\n")
            f.write("OPENAI_API_KEY=\n")
            
        click.secho(f"✅ Project initialized successfully in {project_dir}", fg='green')
        click.echo("\nNext steps:")
        click.echo(f"  cd {project_dir}")
        
        if language == 'python':
            click.echo("  python -m venv venv")
            click.echo("  source venv/bin/activate")
            click.echo("  pip install -r requirements.txt")
        else:
            click.echo("  npm install")
            
        click.echo("\nDon't forget to add your API keys to the .env file!")
        return 0
        
    except Exception as e:
        click.secho(f"❌ Error initializing project: {str(e)}", fg='red')
        return 1


def _replace_placeholders(file_path, replacements):
    """Replace placeholders in a file."""
    with open(file_path, 'r') as f:
        content = f.read()
        
    for key, value in replacements.items():
        content = content.replace(f"{{{{{key}}}}}", value)
        
    with open(file_path, 'w') as f:
        f.write(content)
