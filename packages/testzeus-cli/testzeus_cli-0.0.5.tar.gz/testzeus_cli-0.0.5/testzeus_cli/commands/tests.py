"""
Commands for managing tests in TestZeus CLI.
"""

import asyncio
import os
import json
import click
import datetime
from typing import Dict, Any, Optional, List
from pathlib import Path
from rich.console import Console

from testzeus_sdk import TestZeusClient
from testzeus_cli.config import get_client_config
from testzeus_cli.utils.formatters import format_output
from testzeus_cli.utils.validators import validate_id, parse_key_value_pairs
from testzeus_cli.utils.client import run_client_operation
from testzeus_cli.utils.auth import initialize_client_with_token

console = Console()


def clean_data_for_api(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Clean the data dictionary for API use by converting non-serializable types.
    Also ensures that required fields like name and tenant are preserved.

    Args:
        data: Dictionary of data to clean

    Returns:
        Cleaned dictionary suitable for API use
    """
    clean_data = {}

    # Critical fields that must be preserved if they exist in the original data
    critical_fields = ["name", "tenant", "id", "status"]

    for key, value in data.items():
        # Skip internal PocketBase fields that aren't needed for updates
        if key in ["collection_id", "collection_name", "expand", "created", "updated"]:
            continue

        # Convert datetime objects to ISO format strings
        if isinstance(value, datetime.datetime):
            clean_data[key] = value.isoformat()
        else:
            clean_data[key] = value

    # Double-check critical fields are preserved
    for field in critical_fields:
        if field in data and (field not in clean_data or not clean_data[field]):
            clean_data[field] = data[field]

    return clean_data


@click.group(name="tests")
def tests_group():
    """Manage TestZeus tests"""
    pass


@tests_group.command(name="list")
@click.option(
    "--filters", "-f", multiple=True, help="Filter results (format: key=value)"
)
@click.option("--sort", help="Sort by field")
@click.option("--expand", help="Expand related entities")
@click.pass_context
def list_tests(ctx, filters, sort, expand):
    """List tests with optional filters and sorting"""

    # Parse filters
    filter_dict = parse_key_value_pairs(filters) if filters else {}

    # Define the operation to run with the authenticated client
    async def _list_tests(client: TestZeusClient):
        return await client.tests.get_list(
            expand=expand, sort=sort, filters=filter_dict
        )

    # Run the operation and format the result
    result = run_client_operation(ctx, _list_tests)
    format_output(result, ctx.obj["FORMAT"])


@tests_group.command(name="get")
@click.argument("test_id")
@click.option("--expand", help="Expand related entities")
@click.pass_context
def get_test(ctx, test_id, expand):
    """Get a single test by ID"""

    async def _run():
        config, token = get_client_config(
            ctx.obj["PROFILE"], api_url=ctx.obj.get("API_URL")
        )
        client = TestZeusClient(**config)

        test_id_validated = validate_id(test_id, "test")

        async with client:
            # Apply token from config if available
            if token:
                initialize_client_with_token(client, token)
            else:
                await client.ensure_authenticated()

            test = await client.tests.get_one(test_id_validated, expand=expand)
            return test.data

    result = asyncio.run(_run())
    format_output(result, ctx.obj["FORMAT"])


def _read_feature_file(file_path: str) -> str:
    """
    Read feature content from a file as plain text

    Args:
        file_path: Path to the feature file

    Returns:
        The raw text content of the file
    """
    feature_path = Path(file_path)
    if not feature_path.exists():
        raise click.BadParameter(f"Feature file not found: {file_path}")

    try:
        with open(feature_path, "r", encoding="utf-8") as f:
            content = f.read().strip()
    except Exception as e:
        raise click.BadParameter(f"Failed to read feature file: {str(e)}")

    # Always return the raw text content, regardless of file extension
    return content


@tests_group.command(name="create")
@click.option("--name", required=True, help="Test name")
@click.option("--feature", help="Test feature content as text")
@click.option("--feature-file", help="Path to file containing feature content (text)")
@click.option("--status", default="draft", help="Test status (draft, ready, deleted)")
@click.option("--data", multiple=True, help="Test data IDs")
@click.option("--tags", multiple=True, help="Tag IDs")
@click.option("--environment", help="Environment ID")
@click.pass_context
def create_test(ctx, name, feature, feature_file, status, data, tags, environment):
    """Create a new test with feature content from text or file"""

    if not feature and not feature_file:
        raise click.UsageError("Either --feature or --feature-file is required")

    if feature and feature_file:
        raise click.UsageError("Cannot use both --feature and --feature-file")

    # Process the feature content (from file or directly)
    feature_content = _read_feature_file(feature_file) if feature_file else feature

    async def _run():
        config, token = get_client_config(
            ctx.obj["PROFILE"], api_url=ctx.obj.get("API_URL")
        )
        client = TestZeusClient(**config)

        # Prepare parameters
        test_data = {"name": name, "status": status}

        # Always set feature content as text
        test_data["test_feature"] = feature_content

        if data:
            test_data["test_data"] = list(data)

        if tags:
            test_data["tags"] = list(tags)

        if environment:
            test_data["environment"] = environment

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
                test_data["tenant"] = tenant_id
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
            if user_id:  # Only include if not empty
                test_data["modified_by"] = user_id

            if ctx.obj.get("VERBOSE"):
                console.print(
                    f"[blue]Creating test with parameters: {test_data}[/blue]"
                )

            new_test = await client.tests.create(test_data)
            return new_test.data

    result = asyncio.run(_run())
    console.print(f"[green]Test created successfully with ID: {result['id']}[/green]")
    format_output(result, ctx.obj["FORMAT"])


@tests_group.command(name="update")
@click.argument("test_id")
@click.option("--name", help="New test name")
@click.option("--feature", help="New test feature content as text")
@click.option(
    "--feature-file", help="Path to file containing new feature content (text)"
)
@click.option("--status", help="New test status (draft, ready, deleted)")
@click.option("--data", multiple=True, help="Test data IDs")
@click.option("--tags", multiple=True, help="Tag IDs")
@click.option("--environment", help="Environment ID")
@click.pass_context
def update_test(
    ctx, test_id, name, feature, feature_file, status, data, tags, environment
):
    """Update an existing test with feature content from text or file"""

    if feature and feature_file:
        raise click.UsageError("Cannot use both --feature and --feature-file")

    # Process the feature content if a file was provided
    feature_content = None
    if feature_file:
        feature_content = _read_feature_file(feature_file)
    elif feature:
        feature_content = feature

    async def _run():
        config, token = get_client_config(
            ctx.obj["PROFILE"], api_url=ctx.obj.get("API_URL")
        )
        client = TestZeusClient(**config)

        test_id_validated = validate_id(test_id, "test")

        async with client:
            # Apply token from config if available
            if token:
                # Use the safe initialization method to ensure tenant data is set
                initialize_client_with_token(client, token)
            else:
                await client.ensure_authenticated()

            # First, fetch the existing test to get ALL fields
            existing_test = await client.tests.get_one(test_id_validated)

            if ctx.obj.get("VERBOSE"):
                console.print(f"[blue]Existing test: {existing_test.data}[/blue]")

            # Start with all existing data to ensure we don't lose anything
            updates = dict(existing_test.data)

            # Check if we have at least one field to update
            has_updates = False

            # Add only the fields the user wants to update
            if name:
                updates["name"] = name
                has_updates = True

            if feature_content is not None:
                # Always set feature content as text
                updates["test_feature"] = feature_content
                has_updates = True

            if status:
                updates["status"] = status
                has_updates = True

            if data:
                updates["test_data"] = list(data)
                has_updates = True

            if tags:
                updates["tags"] = list(tags)
                has_updates = True

            if environment:
                updates["environment"] = environment
                has_updates = True

            # Add user ID as modified_by
            user_id = client.get_user_id()
            if user_id:  # Only include if not empty
                updates["modified_by"] = user_id
                has_updates = has_updates or True

            if not has_updates:
                console.print("[yellow]No updates provided[/yellow]")
                return None

            if ctx.obj.get("VERBOSE"):
                console.print(f"[blue]Updating test with: {updates}[/blue]")

            # Clean the data before sending to the API
            clean_updates = clean_data_for_api(updates)

            if ctx.obj.get("VERBOSE"):
                console.print(f"[blue]Cleaned updates for API: {clean_updates}[/blue]")

            updated_test = await client.tests.update(test_id_validated, clean_updates)
            return updated_test.data

    try:
        result = asyncio.run(_run())
        if result:
            console.print(f"[green]Test updated successfully: {result['name']}[/green]")
            format_output(result, ctx.obj["FORMAT"])
    except Exception as e:
        if ctx.obj.get("VERBOSE"):
            console.print(f"[red]Error updating test:[/red]")
            import traceback

            console.print(traceback.format_exc())
        else:
            console.print(f"[red]Error updating test:[/red] {str(e)}")
        exit(1)


@tests_group.command(name="delete")
@click.argument("test_id")
@click.confirmation_option(prompt="Are you sure you want to delete this test?")
@click.pass_context
def delete_test(ctx, test_id):
    """Delete a test"""

    async def _run():
        config, token = get_client_config(
            ctx.obj["PROFILE"], api_url=ctx.obj.get("API_URL")
        )
        client = TestZeusClient(**config)

        test_id_validated = validate_id(test_id, "test")

        async with client:
            # Apply token from config if available
            if token:
                initialize_client_with_token(client, token)
            else:
                await client.ensure_authenticated()

            success = await client.tests.delete(test_id_validated)
            return {"success": success, "id": test_id_validated}

    try:
        result = asyncio.run(_run())
        console.print(f"[green]Test deleted successfully: {result['id']}[/green]")
    except Exception as e:
        console.print(f"[red]Error deleting test:[/red] {str(e)}")
        exit(1)
