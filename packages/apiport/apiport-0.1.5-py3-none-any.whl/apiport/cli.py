"""
Command-line interface for the apiport CLI tool.
"""
import argparse
import sys
import os

from . import commands

def main():
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(prog="apiport", description="CLI tool for managing API secrets")
    subparsers = parser.add_subparsers(dest="command")

    # List command
    list_cmd = subparsers.add_parser("list", description="List all secrets in the vault")
    list_cmd.add_argument("--debug", "-d", action="store_true", help="Show secret values in addition to names")

    # Add command
    add_cmd = subparsers.add_parser("add", description="Add secrets to the vault")
    add_cmd_group = add_cmd.add_mutually_exclusive_group(required=False)
    add_cmd_group.add_argument("--file", "-f", dest="path_to_file", help="Path to a file containing secrets")
    add_cmd.add_argument("secrets", nargs="*", help="One or more KEY=VALUE pairs")

    # Delete command
    del_cmd = subparsers.add_parser("delete", description="Delete a secret or all secrets from the vault")
    del_cmd.add_argument("name", nargs="?", help="Name of the secret to delete. If not provided, deletes all secrets.")

    # Update command
    upd_cmd = subparsers.add_parser("update", description="Update an existing secret")
    upd_cmd.add_argument("name", help="Name of the secret to update")
    upd_cmd.add_argument("value", help="New value for the secret")

    # Import command
    imp_cmd = subparsers.add_parser("import", description="Import secrets to .env file")
    imp_cmd.add_argument("names", nargs="*", help="Names of secrets to import. If none provided, imports all secrets.")

    args = parser.parse_args()

    if args.command == "add":
        if args.path_to_file:
            commands.add(None, None, args.path_to_file)
        elif args.secrets:
            # Handle one or more KEY=VALUE pairs
            commands.add(args.secrets)
        else:
            add_cmd.print_help()
    elif args.command == "delete":
        commands.delete(args.name)
    elif args.command == "update":
        commands.update(args.name, args.value)
    elif args.command == "import":
        commands.import_to_env(*args.names)
    elif args.command == "list":
        commands.list_secrets(debug=args.debug if hasattr(args, 'debug') else False)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
