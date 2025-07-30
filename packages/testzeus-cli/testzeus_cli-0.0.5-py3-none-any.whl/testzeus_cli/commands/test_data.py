"""
Commands for managing test data in TestZeus CLI.
"""

import asyncio
import click
from typing import Dict, Any, Optional, List
from rich.console import Console
from pathlib import Path

from testzeus_sdk import TestZeusClient
from testzeus_cli.config import get_client_config
from testzeus_cli.utils.formatters import format_output
from testzeus_cli.utils.validators import validate_id, parse_key_value_pairs
from testzeus_cli.utils.auth import initialize_client_with_token
from testzeus_cli.commands.tests import clean_data_for_api

console = Console()


def _read_data_file(file_path: str) -> str:
    """
    Read data content from a file as plain text

    Args:
        file_path: Path to the data file

    Returns:
        The raw text content of the file
    """
    data_path = Path(file_path)
    if not data_path.exists():
        raise click.BadParameter(f"Data file not found: {file_path}")

    try:
        with open(data_path, "r", encoding="utf-8") as f:
            content = f.read().strip()
    except Exception as e:
        raise click.BadParameter(f"Failed to read data file: {str(e)}")

    # Always return the raw text content
    return content


@click.group(name="test-data")
def test_data_group():
    """Manage TestZeus test data"""
    pass


@test_data_group.command(name="list")
@click.option(
    "--filters", "-f", multiple=True, help="Filter results (format: key=value)"
)
@click.option("--sort", help="Sort by field")
@click.option("--expand", help="Expand related entities")
@click.pass_context
def list_test_data(ctx, filters, sort, expand):
    """List test data with optional filters and sorting"""

    async def _run():
        config, token = get_client_config(
            ctx.obj["PROFILE"], api_url=ctx.obj.get("API_URL")
        )
        client = TestZeusClient(**config)

        # Parse filters
        filter_dict = parse_key_value_pairs(filters) if filters else {}

        async with client:
            # Apply token from config if available
            if token:
                initialize_client_with_token(client, token)

            test_data = await client.test_data.get_list(
                expand=expand, sort=sort, filters=filter_dict
            )
            return test_data

    result = asyncio.run(_run())
    format_output(result, ctx.obj["FORMAT"])


@test_data_group.command(name="get")
@click.argument("test_data_id")
@click.option("--expand", help="Expand related entities")
@click.pass_context
def get_test_data(ctx, test_data_id, expand):
    """Get a single test data by ID"""

    async def _run():
        config, token = get_client_config(
            ctx.obj["PROFILE"], api_url=ctx.obj.get("API_URL")
        )
        client = TestZeusClient(**config)

        test_data_id_validated = validate_id(test_data_id, "test data")

        async with client:
            # Apply token from config if available
            if token:
                initialize_client_with_token(client, token)

            test_data = await client.test_data.get_one(
                test_data_id_validated, expand=expand
            )
            return test_data.data

    result = asyncio.run(_run())
    format_output(result, ctx.obj["FORMAT"])


@test_data_group.command(name="create")
@click.option("--name", required=True, help="Test data name")
@click.option("--type", default="test", help="Test data type")
@click.option("--status", default="draft", help="Test data status")
@click.option("--input-data", "-d", help="Test data content as text")
@click.option(
    "--file", "-f", type=click.Path(exists=True), help="Text file with test data"
)
@click.pass_context
def create_test_data(ctx, name, type, status, input_data, file):
    """Create new test data"""

    async def _run():
        config, token = get_client_config(
            ctx.obj["PROFILE"], api_url=ctx.obj.get("API_URL")
        )
        client = TestZeusClient(**config)

        # Prepare test data
        data = {"name": name, "type": type, "status": status}

        # Add data content if provided directly
        if input_data:
            data["data_content"] = input_data

        # Read from file if provided
        if file:
            try:
                file_content = _read_data_file(file)
                data["data_content"] = file_content
            except Exception as e:
                console.print(f"[red]Error reading file:[/red] {str(e)}")
                exit(1)

        async with client:
            # Apply token from config if available
            if token:
                initialize_client_with_token(client, token)
            else:
                await client.ensure_authenticated()

            # Add tenant ID only if it's a valid one
            tenant_id = client.get_tenant_id()
            if (
                tenant_id
                and tenant_id != "_pb_users_auth_"
                and tenant_id != "pbc_138639755"
            ):
                data["tenant"] = tenant_id
                if ctx.obj.get("VERBOSE"):
                    console.print(f"[blue]Using tenant ID: {tenant_id}[/blue]")
            else:
                # Let the API determine the appropriate tenant
                if ctx.obj.get("VERBOSE"):
                    console.print(
                        "[yellow]No valid tenant ID found, letting API determine it[/yellow]"
                    )

            # Get user ID to include as modified_by
            user_id = client.get_user_id()
            if user_id:  # Only include if user_id is not empty
                data["modified_by"] = user_id

            if ctx.obj.get("VERBOSE"):
                console.print(
                    f"[blue]Creating test data with parameters: {data}[/blue]"
                )

            new_test_data = await client.test_data.create(data)
            return new_test_data.data

    result = asyncio.run(_run())
    console.print(
        f"[green]Test data created successfully with ID: {result['id']}[/green]"
    )
    format_output(result, ctx.obj["FORMAT"])


@test_data_group.command(name="update")
@click.argument("test_data_id")
@click.option("--name", help="New test data name")
@click.option("--type", help="New test data type")
@click.option("--status", help="New test data status")
@click.option("--input-data", "-d", help="New test data content as text")
@click.option(
    "--file", "-f", type=click.Path(exists=True), help="Text file with new test data"
)
@click.pass_context
def update_test_data(ctx, test_data_id, name, type, status, input_data, file):
    """Update an existing test data"""

    async def _run():
        config, token = get_client_config(
            ctx.obj["PROFILE"], api_url=ctx.obj.get("API_URL")
        )
        client = TestZeusClient(**config)

        test_data_id_validated = validate_id(test_data_id, "test data")

        async with client:
            # Apply token from config if available
            if token:
                initialize_client_with_token(client, token)
            else:
                await client.ensure_authenticated()

            # First get the existing test data
            existing_data = await client.test_data.get_one(test_data_id_validated)

            # Prepare updates starting with all existing data
            updates = dict(existing_data.data)
            has_updates = False

            # Update only the fields that were provided
            if name:
                updates["name"] = name
                has_updates = True

            if type:
                updates["type"] = type
                has_updates = True

            if status:
                updates["status"] = status
                has_updates = True

            # Process input data (either from input or file)
            if input_data:
                updates["data_content"] = input_data
                has_updates = True
            elif file:
                try:
                    file_content = _read_data_file(file)
                    updates["data_content"] = file_content
                    has_updates = True
                except Exception as e:
                    console.print(f"[red]Error reading file:[/red] {str(e)}")
                    exit(1)

            # Add user ID as modified_by
            user_id = client.get_user_id()
            if user_id:  # Only include if user_id is not empty
                updates["modified_by"] = user_id
                has_updates = True

            if ctx.obj.get("VERBOSE"):
                console.print(
                    f"[blue]Updating test data with parameters: {updates}[/blue]"
                )

            if not has_updates:
                console.print("[yellow]No updates provided[/yellow]")
                return None

            updated_data = await client.test_data.update(
                test_data_id_validated, updates
            )
            return updated_data.data

    result = asyncio.run(_run())

    if result:
        console.print(
            f"[green]Test data updated successfully: {result['name']}[/green]"
        )
        format_output(result, ctx.obj["FORMAT"])


@test_data_group.command(name="delete")
@click.argument("test_data_id")
@click.confirmation_option(prompt="Are you sure you want to delete this test data?")
@click.pass_context
def delete_test_data(ctx, test_data_id):
    """Delete test data"""

    async def _run():
        config, token = get_client_config(
            ctx.obj["PROFILE"], api_url=ctx.obj.get("API_URL")
        )
        client = TestZeusClient(**config)

        test_data_id_validated = validate_id(test_data_id, "test data")

        async with client:
            # Apply token from config if available
            if token:
                initialize_client_with_token(client, token)

            # Optionally get the test data before deletion for confirmation
            test_data = await client.test_data.get_one(test_data_id_validated)
            await client.test_data.delete(test_data_id_validated)
            return test_data.data

    try:
        result = asyncio.run(_run())
        console.print(
            f"[green]Test data '{result['name']}' deleted successfully[/green]"
        )
    except Exception as e:
        console.print(f"[red]Failed to delete test data:[/red] {str(e)}")
        exit(1)
