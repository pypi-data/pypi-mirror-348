#!/usr/bin/env python3
"""
Clarity CLI - Interactive CLI for test management and execution

This CLI tool provides functionality for:
- Login (generates and stores JWT tokens)
- Executing tests (displays and allows selection from available tests)
"""

# import json
# import datetime
# import uuid
import click
# import inquirer
# from inquirer import themes
# from rich.panel import Panel
# from rich.table import Table
# import jwt
from clarity_cli.helpers import ensure_config_dir
from clarity_cli.commands import CliCommands


commands = CliCommands()


@click.group()
@click.option('--verbose', '-v', is_flag=True, help='Verbose mode')
@click.pass_context
def cli(ctx, verbose=False):
    """Clarity CLI - Interactive test management and execution tool"""
    ctx.ensure_object(dict)
    ctx.obj['VERBOSE'] = verbose
    ensure_config_dir()


@cli.command()
@click.option('--test-id', '-t', help='Specify a test ID to execute directly')
@click.option('--profile', '-p', help='Specify a name for the new profile')
@click.option('--override-config-path', '-c', help='Path to config.json, default config stored in ~/.config.json')
@click.option('--project', '-proj', help='Specify the default project id for clarity operations')
@click.option('--workspace', '-w', help='Specify the default workspace id for clarity operations')
@click.option('--agent-id', '-a', help='Specify the default agent id for executions')
@click.option('--parameters-file', help="Path to a json file that includes all the flow variables values for execution, if flow var doesn't exist using the default value")
@click.pass_context
def execute(ctx, test_id=None, profile=None, override_config_path=None, project=None, workspace=None, agent_id=None, parameters_file=None):
    commands.execute(ctx, test_id, profile, override_config_path, project, workspace, agent_id, parameters_file)


@cli.command()
@click.option('--profile', '-p', help='Specify a name for the new profile')
@click.option('--client-id', '-id', help='Specify the client ID you got from cyclarity portal')
@click.option('--client-secret', '-cs', help='Specify the client secret you got from cyclarity portal')
@click.option('--token-endpoint', '-e', help='Specify the token endpoint you got from cyclarity portal')
@click.option('--scope', '-s', help='Specify the scope you got from cyclarity portal')
@click.option('--project', '-proj', help='Specify the default project id for clarity operations')
@click.option('--workspace', '-w', help='Specify the default workspace id for clarity operations')
@click.option('--agent_id', '-a', help='Specify the default agent id for executions')
@click.option('--default', '-d', help='Use this profile as default profile')
@click.pass_context
def profile_setup(ctx, profile=None, client_id=None, client_secret=None, token_endpoint=None, scope=None, project=None, workspace=None, agent_id=None, default=None):
    commands.write_profile_to_config(ctx, profile, client_id, client_secret, token_endpoint, scope, project, workspace, agent_id, default)


@cli.command()
@click.option('--profile', '-p', help='Profile for login, if not provided use default profile')
@click.option('--override-config-path', '-c', help='Path to config.json, default config stored in ~/.config.json')
@click.pass_context
def login(ctx, profile=None, override_config_path=None):
    commands.login_using_config_file(ctx, profile, override_config_path)


if __name__ == '__main__':
    cli()
