"""
Main CLI entry point for Windsweeper.
"""
import os
import sys
import click
from dotenv import load_dotenv

from windsweeper import __version__
from .commands.init import init
from .commands.create import create
from .commands.serve import serve
from .commands.docs import docs
from .commands.rules import rules
from .commands.health import health
from .commands.generate import generate

# Load environment variables from .env file
load_dotenv()

# Check if OPENAI_API_KEY is set
if not os.environ.get('OPENAI_API_KEY'):
    click.secho('WARNING: OPENAI_API_KEY environment variable is not set. '
                'Some commands may not work correctly.', fg='yellow')


@click.group()
@click.version_option(version=__version__, prog_name='windsweeper')
def main():
    """
    Windsweeper SDK/CLI toolset for generating rules, workflows and docs.

    This CLI provides a comprehensive set of tools for working with the Windsweeper platform.
    Use it to initialize projects, create rules, serve documentation, and more.
    """
    pass


# Register commands
main.add_command(init)
main.add_command(create)
main.add_command(serve)
main.add_command(docs)
main.add_command(rules)
main.add_command(health)
main.add_command(generate)

if __name__ == '__main__':
    main()
