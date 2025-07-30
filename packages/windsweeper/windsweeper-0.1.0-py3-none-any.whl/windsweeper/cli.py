#!/usr/bin/env python3
"""
Command-line interface for the Windsweeper SDK
"""

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Dict, Any, List, Optional

from windsweeper import create_client, WindsweeperClient


def parse_args():
    """Parse command-line arguments"""
    parser = argparse.ArgumentParser(
        description="Windsweeper CLI - Interact with the Windsweeper MCP server",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  windsweeper health
  windsweeper list-resources my-server
  windsweeper validate-rule ./my-rule.yaml
  windsweeper validate-code ./my-code.js rule1,rule2 javascript
  windsweeper apply-template my-template ./variables.json
  windsweeper generate "Write a function to calculate Fibonacci numbers"
        """
    )

    # Global options
    parser.add_argument(
        "--server", "-s",
        default=os.environ.get("WINDSWEEPER_SERVER_URL", "http://localhost:9001"),
        help="URL of the MCP server (default: $WINDSWEEPER_SERVER_URL or http://localhost:9001)"
    )
    parser.add_argument(
        "--api-key", "-k",
        default=os.environ.get("WINDSWEEPER_API_KEY"),
        help="API key for authentication (default: $WINDSWEEPER_API_KEY)"
    )
    parser.add_argument(
        "--timeout", "-t",
        type=int,
        default=int(os.environ.get("WINDSWEEPER_TIMEOUT", 30)),
        help="Request timeout in seconds (default: $WINDSWEEPER_TIMEOUT or 30)"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose output"
    )

    # Subcommands
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")
    
    # Health check command
    subparsers.add_parser(
        "health",
        help="Check if the MCP server is healthy"
    )
    
    # List resources command
    list_resources_parser = subparsers.add_parser(
        "list-resources",
        help="List resources from the specified server"
    )
    list_resources_parser.add_argument(
        "server_name",
        help="Name of the server to list resources from"
    )
    list_resources_parser.add_argument(
        "cursor",
        nargs="?",
        help="Pagination cursor for retrieving the next page of results"
    )
    
    # Get resource command
    get_resource_parser = subparsers.add_parser(
        "get-resource",
        help="Get a specific resource"
    )
    get_resource_parser.add_argument(
        "server_name",
        help="Name of the server to get the resource from"
    )
    get_resource_parser.add_argument(
        "resource_id",
        help="ID of the resource to get"
    )
    
    # Validate rule command
    validate_rule_parser = subparsers.add_parser(
        "validate-rule",
        help="Validate a rule file"
    )
    validate_rule_parser.add_argument(
        "rule_file",
        help="Path to the rule file to validate"
    )
    
    # Validate code command
    validate_code_parser = subparsers.add_parser(
        "validate-code",
        help="Validate code against rules"
    )
    validate_code_parser.add_argument(
        "code_file",
        help="Path to the code file to validate"
    )
    validate_code_parser.add_argument(
        "rule_ids",
        help="Comma-separated list of rule IDs to validate against"
    )
    validate_code_parser.add_argument(
        "language",
        help="Language of the code file"
    )
    
    # Apply template command
    apply_template_parser = subparsers.add_parser(
        "apply-template",
        help="Apply a template with variables"
    )
    apply_template_parser.add_argument(
        "template_id",
        help="ID of the template to apply"
    )
    apply_template_parser.add_argument(
        "variables_file",
        help="Path to the JSON file containing template variables"
    )
    
    # Generate command
    generate_parser = subparsers.add_parser(
        "generate",
        help="Generate content using the specified prompt"
    )
    generate_parser.add_argument(
        "prompt",
        help="Prompt to generate content from"
    )
    generate_parser.add_argument(
        "options_file",
        nargs="?",
        help="Optional path to a JSON file containing generation options"
    )
    
    return parser.parse_args()


def read_file(file_path: str) -> str:
    """Read content from a file"""
    try:
        with open(Path(file_path).resolve(), "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        print(f"Error reading file: {e}", file=sys.stderr)
        sys.exit(1)


def read_json_file(file_path: str) -> Dict[str, Any]:
    """Read and parse a JSON file"""
    try:
        with open(Path(file_path).resolve(), "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON file: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error reading file: {e}", file=sys.stderr)
        sys.exit(1)


def print_verbose(verbose: bool, message: str) -> None:
    """Print a message if verbose mode is enabled"""
    if verbose:
        print(message)


def execute_command(
    command: str,
    client: WindsweeperClient,
    verbose: bool,
    args: argparse.Namespace
) -> None:
    """Execute the specified command with the given client and arguments"""
    
    print_verbose(verbose, f"Executing command: {command}")
    print_verbose(verbose, f"Server URL: {args.server}")
    print_verbose(verbose, f"Using API key: {'Yes' if args.api_key else 'No'}")
    
    try:
        if command == "health":
            is_healthy = client.check_health()
            print(f"Server health: {'Healthy' if is_healthy else 'Unhealthy'}")
            
        elif command == "list-resources":
            server_name = args.server_name
            cursor = args.cursor
            
            print_verbose(verbose, f"Listing resources for server: {server_name}")
            
            resources = client.list_resources(server_name, cursor)
            print(f"Found {len(resources['resources'])} resources:")
            
            for resource in resources["resources"]:
                print(f"- {resource['name']} ({resource['type']}): {resource['id']}")
            
            if "nextCursor" in resources and resources["nextCursor"]:
                print("\nMore resources available. Use this command to view the next page:")
                print(f"windsweeper list-resources {server_name} {resources['nextCursor']}")
                
        elif command == "get-resource":
            server_name = args.server_name
            resource_id = args.resource_id
            
            print_verbose(verbose, f"Getting resource {resource_id} from server: {server_name}")
            
            resource = client.get_resource(server_name, resource_id)
            print(json.dumps(resource, indent=2))
            
        elif command == "validate-rule":
            rule_file_path = args.rule_file
            rule_content = read_file(rule_file_path)
            
            print_verbose(verbose, f"Validating rule from file: {rule_file_path}")
            
            file_ext = Path(rule_file_path).suffix.lstrip(".")
            language_id = file_ext or "yaml"
            
            validation_result = client.validate_rule(
                content=rule_content,
                language_id=language_id,
                uri=rule_file_path
            )
            
            if validation_result["valid"]:
                print("Rule is valid!")
                print(f"Message: {validation_result['message']}")
            else:
                print("Rule validation failed:")
                print(f"Message: {validation_result['message']}")
                
                for issue in validation_result["issues"]:
                    location = f" at line {issue['line']}" if "line" in issue else ""
                    print(f"- [{issue['severity']}] {issue['message']}{location}")
                    
        elif command == "validate-code":
            code_file_path = args.code_file
            rule_ids = args.rule_ids.split(",")
            language = args.language
            
            code_content = read_file(code_file_path)
            
            print_verbose(verbose, f"Validating code from file: {code_file_path}")
            print_verbose(verbose, f"Against rules: {', '.join(rule_ids)}")
            print_verbose(verbose, f"Language: {language}")
            
            validation_results = client.validate_code(code_content, rule_ids, language)
            
            print("Validation results:")
            for rule_id, result in validation_results.items():
                print(f"\nRule: {rule_id}")
                print(f"Valid: {result['valid']}")
                
                if result["issues"]:
                    print("Issues:")
                    for issue in result["issues"]:
                        location = f" at line {issue['line']}" if "line" in issue else ""
                        print(f"- [{issue['severity']}] {issue['message']}{location}")
                        
        elif command == "apply-template":
            template_id = args.template_id
            variables_file_path = args.variables_file
            
            variables = read_json_file(variables_file_path)
            
            print_verbose(verbose, f"Applying template: {template_id}")
            print_verbose(verbose, f"With variables from: {variables_file_path}")
            
            content = client.apply_template(template_id, variables)
            print(content)
            
        elif command == "generate":
            prompt = args.prompt
            
            print_verbose(verbose, f"Generating content with prompt: {prompt}")
            
            # Parse additional generation options if provided as a JSON file
            options = {}
            if args.options_file:
                options = read_json_file(args.options_file)
                print_verbose(verbose, f"Using generation options from: {args.options_file}")
            
            content = client.generate(prompt, options)
            print(content)
            
        else:
            print(f"Error: Unknown command '{command}'", file=sys.stderr)
            sys.exit(1)
            
    except Exception as e:
        print(f"Error executing command: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    """Main entry point for the CLI"""
    args = parse_args()
    
    # If no command is specified, print help
    if not args.command:
        parser = argparse.ArgumentParser()
        parser.print_help()
        sys.exit(0)
    
    # Create client
    client = create_client(
        server_url=args.server,
        api_key=args.api_key,
        timeout=args.timeout
    )
    
    # Execute command
    execute_command(args.command, client, args.verbose, args)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nOperation cancelled.")
        sys.exit(130)
    except Exception as e:
        print(f"Fatal error: {e}", file=sys.stderr)
        sys.exit(1)
