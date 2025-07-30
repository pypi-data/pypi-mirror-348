"""
Environment management commands for TestZeus CLI.
"""

import asyncio
import click
import json
from rich.console import Console
from testzeus_sdk import TestZeusClient
from testzeus_cli.config import get_client_config
from testzeus_cli.utils.formatters import format_output
from testzeus_cli.utils.auth import initialize_client_with_token
from testzeus_sdk.models import Environment

console = Console()


@click.group()
def environments_group():
    """Manage environments in TestZeus"""
    pass


@environments_group.command()
@click.option("--name", required=True, help="Environment name")
@click.option("--data", help="Environment data (JSON string)")
@click.option("--tags", help="Comma-separated list of tags")
@click.pass_context
def create(ctx, name, data, tags):
    """Create a new environment"""

    async def _run():
        config, token = get_client_config(
            ctx.obj["PROFILE"], api_url=ctx.obj.get("API_URL")
        )
        client = TestZeusClient(**config)
        async with client:
            if token:
                initialize_client_with_token(client, token)
            else:
                await client.ensure_authenticated()
            params = {"name": name}
            if data:
                try:
                    params["data"] = json.loads(data)
                except json.JSONDecodeError:
                    console.print("[red]Error: Invalid JSON data format[/red]")
                    raise click.Abort()
            if tags:
                params["tags"] = tags.split(",")
            env = await client.environments.create(params)
            return env.data

    try:
        result = asyncio.run(_run())
        console.print(
            f"[green]Environment created successfully with ID: {result['id']}[/green]"
        )
        format_output(result, ctx.obj["FORMAT"])
    except Exception as e:
        console.print(f"[red]Error creating environment: {str(e)}[/red]")
        raise click.Abort()


@environments_group.command()
@click.pass_context
def list(ctx):
    """List all environments"""

    async def _run():
        config, token = get_client_config(
            ctx.obj["PROFILE"], api_url=ctx.obj.get("API_URL")
        )
        client = TestZeusClient(**config)
        async with client:
            if token:
                initialize_client_with_token(client, token)
            else:
                await client.ensure_authenticated()
            result = await client.environments.get_list()

            return result

    try:
        result = asyncio.run(_run())
        format_output(result, ctx.obj["FORMAT"])
    except Exception as e:
        console.print(f"[red]Error listing environments: {str(e)}[/red]")
        raise click.Abort()


@environments_group.command()
@click.argument("env_id")
@click.pass_context
def delete(ctx, env_id):
    """Delete an environment"""

    async def _run():
        config, token = get_client_config(
            ctx.obj["PROFILE"], api_url=ctx.obj.get("API_URL")
        )
        client = TestZeusClient(**config)
        async with client:
            if token:
                initialize_client_with_token(client, token)
            else:
                await client.ensure_authenticated()
            await client.environments.delete(env_id)
            return {"id": env_id}

    try:
        result = asyncio.run(_run())
        console.print(f"[green]Environment {result['id']} deleted successfully[/green]")
    except Exception as e:
        console.print(f"[red]Error deleting environment: {str(e)}[/red]")
        raise click.Abort()
