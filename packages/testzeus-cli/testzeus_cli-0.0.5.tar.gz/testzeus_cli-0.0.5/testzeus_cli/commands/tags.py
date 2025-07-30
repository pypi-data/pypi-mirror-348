"""
Tag management commands for TestZeus CLI.
"""

import asyncio
import click
import json
from rich.console import Console
from testzeus_sdk import TestZeusClient
from testzeus_cli.config import get_client_config
from testzeus_cli.utils.formatters import format_output
from testzeus_cli.utils.auth import initialize_client_with_token

console = Console()


@click.group()
def tags_group():
    """Manage tags in TestZeus"""
    pass


@tags_group.command()
@click.argument("name")
@click.pass_context
def create(ctx, name):
    """Create a new tag"""

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
            tag = await client.tags.create(params)
            return tag.data

    try:
        result = asyncio.run(_run())
        console.print(f"[green]Tag '{result['name']}' created successfully[/green]")
        format_output(result, ctx.obj["FORMAT"])
    except Exception as e:
        console.print(f"[red]Error creating tag: {str(e)}[/red]")
        raise click.Abort()


@tags_group.command()
@click.pass_context
def list(ctx):
    """List all tags"""

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
            result = await client.tags.get_list()

            return result

    try:
        result = asyncio.run(_run())
        format_output(result, ctx.obj["FORMAT"])
    except Exception as e:
        console.print(f"[red]Error listing tags: {str(e)}[/red]")
        raise click.Abort()


@tags_group.command()
@click.argument("name")
@click.pass_context
def delete(ctx, name):
    """Delete a tag"""

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
            await client.tags.delete(name)
            return {"name": name}

    try:
        result = asyncio.run(_run())
        console.print(f"[green]Tag '{result['name']}' deleted successfully[/green]")
    except Exception as e:
        console.print(f"[red]Error deleting tag: {str(e)}[/red]")
        raise click.Abort()
