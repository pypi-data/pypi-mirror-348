"""
Create command for the Windsweeper CLI.
"""
import os
import click
import json
from pathlib import Path
from windsweeper import create_client


@click.command()
@click.argument('component_type', required=True, 
                type=click.Choice(['rule', 'workflow', 'template']))
@click.argument('name', required=True)
@click.option('--description', '-d', help='Description of the component')
@click.option('--output', '-o', type=click.Path(), 
              help='Output file or directory')
@click.option('--language', '-l', default='python',
              type=click.Choice(['python', 'javascript', 'typescript']),
              help='Programming language for code generation (default: python)')
@click.option('--template', '-t', help='Template to use for generation')
@click.option('--url', '-u', default='http://localhost:9001', 
              help='URL of the MCP server')
@click.option('--api-key', '-k', envvar='WINDSWEEPER_API_KEY',
              help='API key for the MCP server (can also be set via WINDSWEEPER_API_KEY env var)')
@click.option('--from-prompt', '-p', help='Create from a natural language prompt')
def create(component_type, name, description, output, language, template, url, api_key, from_prompt):
    """Create a new component (rule, workflow, or template).
    
    COMPONENT_TYPE is the type of component to create (rule, workflow, or template).
    
    NAME is the name of the component to create.
    """
    client = create_client(base_url=url, api_key=api_key)
    
    # Set default output path if not provided
    if not output:
        if component_type == 'rule':
            output = f"./rules/{name}.{'py' if language == 'python' else 'js'}"
        elif component_type == 'workflow':
            output = f"./workflows/{name}.{'py' if language == 'python' else 'js'}"
        else:  # template
            output = f"./templates/{name}.{'py' if language == 'python' else 'js'}"
    
    output_path = Path(output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    try:
        if from_prompt:
            # Create from natural language prompt
            click.echo(f"Creating {component_type} '{name}' from prompt: {from_prompt}")
            
            response = client.generate(f"Create a {language} {component_type} named {name} that {from_prompt}")
            
            content = response.get('text', '')
            
            # Write to output file
            with open(output_path, 'w') as f:
                f.write(content)
                
            click.secho(f"✅ {component_type.capitalize()} '{name}' created from prompt at {output_path}", fg='green')
            
        elif template:
            # Create from template
            click.echo(f"Creating {component_type} '{name}' from template: {template}")
            
            # Get the package directory where templates are stored
            package_dir = Path(__file__).parent.parent.parent
            template_path = package_dir / 'templates' / language / component_type / f"{template}{'_template' if not template.endswith('_template') else ''}.{'py' if language == 'python' else 'js'}"
            
            if not template_path.exists():
                click.secho(f"❌ Template '{template}' not found for {language} {component_type}", fg='red')
                return 1
                
            # Read template content
            with open(template_path, 'r') as f:
                template_content = f.read()
                
            # Replace placeholders
            content = template_content.replace('{{name}}', name)
            if description:
                content = content.replace('{{description}}', description)
                
            # Write to output file
            with open(output_path, 'w') as f:
                f.write(content)
                
            click.secho(f"✅ {component_type.capitalize()} '{name}' created from template at {output_path}", fg='green')
            
        else:
            # Create a basic skeleton
            click.echo(f"Creating {component_type} '{name}'")
            
            # Create basic content based on component type and language
            if language == 'python':
                if component_type == 'rule':
                    content = f'''"""
{name} - {'A Windsweeper rule' if not description else description}
"""

def apply(content, context=None):
    """
    Apply the rule to the given content.
    
    Args:
        content (str): The content to process
        context (dict, optional): Additional context
        
    Returns:
        str: The processed content
    """
    # TODO: Implement rule logic here
    return content
'''
                elif component_type == 'workflow':
                    content = f'''"""
{name} - {'A Windsweeper workflow' if not description else description}
"""

def execute(input_data, context=None):
    """
    Execute the workflow on the given input data.
    
    Args:
        input_data (dict): Input data for the workflow
        context (dict, optional): Additional context
        
    Returns:
        dict: The workflow result
    """
    # TODO: Implement workflow logic here
    result = {{}}
    return result
'''
                else:  # template
                    content = f'''"""
{name} - {'A Windsweeper template' if not description else description}
"""

def render(variables):
    """
    Render the template with the provided variables.
    
    Args:
        variables (dict): Variables to use in template rendering
        
    Returns:
        str: The rendered template
    """
    # TODO: Implement template logic here
    rendered = ""
    return rendered
'''
            else:  # JavaScript/TypeScript
                if component_type == 'rule':
                    content = f'''/**
 * {name} - {'A Windsweeper rule' if not description else description}
 */

/**
 * Apply the rule to the given content
 * @param {{string}} content - The content to process
 * @param {{object}} [context] - Additional context
 * @returns {{string}} - The processed content
 */
function apply(content, context) {{
    // TODO: Implement rule logic here
    return content;
}}

module.exports = {{ apply }};
'''
                elif component_type == 'workflow':
                    content = f'''/**
 * {name} - {'A Windsweeper workflow' if not description else description}
 */

/**
 * Execute the workflow on the given input data
 * @param {{object}} inputData - Input data for the workflow
 * @param {{object}} [context] - Additional context
 * @returns {{object}} - The workflow result
 */
function execute(inputData, context) {{
    // TODO: Implement workflow logic here
    const result = {{}};
    return result;
}}

module.exports = {{ execute }};
'''
                else:  # template
                    content = f'''/**
 * {name} - {'A Windsweeper template' if not description else description}
 */

/**
 * Render the template with the provided variables
 * @param {{object}} variables - Variables to use in template rendering
 * @returns {{string}} - The rendered template
 */
function render(variables) {{
    // TODO: Implement template logic here
    let rendered = "";
    return rendered;
}}

module.exports = {{ render }};
'''

            # Write to output file
            with open(output_path, 'w') as f:
                f.write(content)
                
            click.secho(f"✅ {component_type.capitalize()} '{name}' created at {output_path}", fg='green')
            
        return 0
        
    except Exception as e:
        click.secho(f"❌ Error creating {component_type}: {str(e)}", fg='red')
        return 1
