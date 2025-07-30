"""
Commands for managing test runs in TestZeus CLI.
"""

import asyncio
import os
import time
from pathlib import Path
import click
from typing import Dict, Any, Optional, List
from rich.console import Console
from rich.progress import Progress

from testzeus_sdk import TestZeusClient
from testzeus_cli.config import get_client_config
from testzeus_cli.utils.formatters import format_output
from testzeus_cli.utils.validators import validate_id, parse_key_value_pairs
from testzeus_cli.utils.auth import initialize_client_with_token

console = Console()


@click.group(name="test-runs")
def test_runs_group():
    """Manage TestZeus test runs"""
    pass


@test_runs_group.command(name="create")
@click.option("--name", required=True, help="Test run name")
@click.option("--test", required=True, help="Test ID or name")
@click.option("--env", help="Environment ID")
@click.option("--tag", help="Tag name")
@click.pass_context
def create_test_run(ctx, name, test, env, tag):
    """Create and start a test run"""

    async def _run():
        config, token = get_client_config(
            ctx.obj["PROFILE"], api_url=ctx.obj.get("API_URL")
        )
        client = TestZeusClient(**config)

        async with client:
            # Apply token from config if available
            if token:
                initialize_client_with_token(client, token)
            else:
                await client.ensure_authenticated()

            # Here's the key fix - we need to generate a more unique name
            # The API may be rejecting duplicate names
            import datetime

            timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
            unique_name = f"{name}-{timestamp}-test-run"

            # Get user ID to include as modified_by
            user_id = client.get_user_id()

            # If user_id is empty, try to get the user information to get a valid ID
            if not user_id:
                if ctx.obj.get("VERBOSE"):
                    console.print(
                        "[yellow]User ID not found in token, attempting to fetch user details[/yellow]"
                    )
                try:
                    # Try to get the authenticated user's information
                    user_info = await client.pb.collection("users").auth_refresh()
                    # Access user record as a dictionary
                    if user_info and hasattr(user_info, "record"):
                        # Try various ways to access the user ID
                        record_dict = (
                            vars(user_info.record)
                            if hasattr(user_info.record, "__dict__")
                            else {}
                        )
                        user_id = record_dict.get("id") or getattr(
                            user_info.record, "id", ""
                        )
                        if ctx.obj.get("VERBOSE"):
                            console.print(f"[blue]Retrieved user ID: {user_id}[/blue]")
                except Exception as e:
                    if ctx.obj.get("VERBOSE"):
                        console.print(
                            f"[yellow]Failed to get user ID: {str(e)}[/yellow]"
                        )

            # Try to get test details to access its tenant ID
            try:
                test_id = validate_id(test, "test")
                test_details = await client.tests.get_one(test_id)
                tenant_id = test_details.data.get("tenant")
                if ctx.obj.get("VERBOSE"):
                    console.print(
                        f"[blue]Using tenant ID from test: {tenant_id}[/blue]"
                    )
            except Exception as e:
                # If we can't get test details, use the tenant ID from the client
                tenant_id = client.get_tenant_id()
                if ctx.obj.get("VERBOSE"):
                    console.print(
                        f"[blue]Using tenant ID from client: {tenant_id}[/blue]"
                    )
                    if "_pb_users_auth_" in str(tenant_id):
                        console.print(
                            "[yellow]Warning: Using default tenant ID, which may not work[/yellow]"
                        )

            # Create base parameters
            params = {"name": unique_name, "test": test}

            # Add environment if provided
            if env:
                params["environment"] = env

            # Add tag if provided
            if tag:
                params["tag"] = tag

            # Only set tenant if it's a valid ID (not the default PocketBase one)
            if tenant_id and tenant_id != "_pb_users_auth_":
                params["tenant"] = tenant_id

            # Only add modified_by if we have a valid user ID
            if user_id:
                params["modified_by"] = user_id
                if ctx.obj.get("VERBOSE"):
                    console.print(f"[blue]Setting modified_by to: {user_id}[/blue]")
            else:
                console.print(
                    "[red]Warning: No valid user ID found. Test run creation may fail.[/red]"
                )

            if ctx.obj.get("VERBOSE"):
                console.print(
                    f"[blue]Creating test run with parameters: {params}[/blue]"
                )

            test_run = await client.test_runs.create_and_start(**params)
            return test_run.data

    result = asyncio.run(_run())
    console.print(
        f"[green]Test run created and started with ID: {result['id']}[/green]"
    )
    format_output(result, ctx.obj["FORMAT"])


@test_runs_group.command(name="list")
@click.option(
    "--filters", "-f", multiple=True, help="Filter results (format: key=value)"
)
@click.option("--sort", help="Sort by field")
@click.option("--expand", help="Expand related entities")
@click.pass_context
def list_test_runs(ctx, filters, sort, expand):
    """List test runs with optional filters and sorting"""

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
            else:
                await client.ensure_authenticated()

            test_runs = await client.test_runs.get_list(
                expand=expand, sort=sort, filters=filter_dict
            )
            return test_runs

    result = asyncio.run(_run())
    format_output(result, ctx.obj["FORMAT"])


@test_runs_group.command(name="get")
@click.argument("test_run_id")
@click.option("--expand", help="Expand related entities")
@click.pass_context
def get_test_run(ctx, test_run_id, expand):
    """Get a single test run by ID"""

    async def _run():
        config, token = get_client_config(
            ctx.obj["PROFILE"], api_url=ctx.obj.get("API_URL")
        )
        client = TestZeusClient(**config)

        test_run_id_validated = validate_id(test_run_id, "test run")

        async with client:
            # Apply token from config if available
            if token:
                initialize_client_with_token(client, token)
            else:
                await client.ensure_authenticated()

            test_run = await client.test_runs.get_one(
                test_run_id_validated, expand=expand
            )
            return test_run.data

    result = asyncio.run(_run())
    format_output(result, ctx.obj["FORMAT"])


@test_runs_group.command(name="get-expanded")
@click.argument("test_run_id")
@click.pass_context
def get_expanded_test_run(ctx, test_run_id):
    """Get expanded details for a test run including all outputs and steps"""

    async def _run():
        config, token = get_client_config(
            ctx.obj["PROFILE"], api_url=ctx.obj.get("API_URL")
        )
        client = TestZeusClient(**config)

        test_run_id_validated = validate_id(test_run_id, "test run")

        async with client:
            # Apply token from config if available
            if token:
                initialize_client_with_token(client, token)
            else:
                await client.ensure_authenticated()

            expanded_test_run = await client.test_runs.get_expanded(
                test_run_id_validated
            )
            return expanded_test_run

    result = asyncio.run(_run())
    format_output(result, ctx.obj["FORMAT"])


@test_runs_group.command(name="cancel")
@click.argument("test_run_id")
@click.pass_context
def cancel_test_run(ctx, test_run_id):
    """Cancel a running test"""

    async def _run():
        config, token = get_client_config(
            ctx.obj["PROFILE"], api_url=ctx.obj.get("API_URL")
        )
        client = TestZeusClient(**config)

        test_run_id_validated = validate_id(test_run_id, "test run")

        async with client:
            # Apply token from config if available
            if token:
                initialize_client_with_token(client, token)
            else:
                await client.ensure_authenticated()

            # Get user ID to include as modified_by
            user_id = client.get_user_id()

            # Only include modified_by if user_id is not empty
            params = {"id": test_run_id_validated}
            if user_id:
                params["modified_by"] = user_id

            if ctx.obj.get("VERBOSE"):
                console.print(
                    f"[blue]Cancelling test run with parameters: {params}[/blue]"
                )

            cancelled_test = await client.test_runs.cancel(**params)
            return cancelled_test.data

    try:
        result = asyncio.run(_run())
        console.print(
            f"[green]Test run cancelled successfully: {result['name']}[/green]"
        )
        format_output(result, ctx.obj["FORMAT"])
    except ValueError as e:
        console.print(f"[red]Failed to cancel test run:[/red] {str(e)}")
        exit(1)


@test_runs_group.command(name="watch")
@click.argument("test_run_id")
@click.option("--interval", default=5, help="Check interval in seconds")
@click.pass_context
def watch_test_run(ctx, test_run_id, interval):
    """Watch a test run until completion"""

    async def _monitor_test_run():
        config, token = get_client_config(
            ctx.obj["PROFILE"], api_url=ctx.obj.get("API_URL")
        )
        client = TestZeusClient(**config)

        test_run_id_validated = validate_id(test_run_id, "test run")

        with Progress() as progress:
            task = progress.add_task("[cyan]Running test...", total=None)

            async with client:
                # Apply token from config if available
                if token:
                    initialize_client_with_token(client, token)
                else:
                    await client.ensure_authenticated()

                # Store user ID for future operations that might need it
                user_id = client.get_user_id()

                while True:
                    # get_one doesn't support modified_by parameter
                    test_run = await client.test_runs.get_one(test_run_id_validated)

                    # Update progress description with status
                    progress.update(
                        task, description=f"[cyan]Test status: {test_run.status}[/cyan]"
                    )

                    if test_run.is_completed():
                        progress.update(task, completed=100, total=100)
                        console.print("[green]Test run completed successfully![/green]")
                        return test_run.data
                    elif test_run.is_failed():
                        progress.update(task, completed=100, total=100)
                        console.print("[red]Test run failed![/red]")
                        return test_run.data
                    elif test_run.is_crashed():
                        progress.update(task, completed=100, total=100)
                        console.print("[red]Test run crashed![/red]")
                        return test_run.data
                    elif test_run.is_cancelled():
                        progress.update(task, completed=100, total=100)
                        console.print("[yellow]Test run was cancelled![/yellow]")
                        return test_run.data

                    # Sleep for the specified interval
                    await asyncio.sleep(interval)

    try:
        result = asyncio.run(_monitor_test_run())
        duration = result.get("duration") or "Unknown"
        console.print(f"Test run duration: {duration} seconds")
        format_output(result, ctx.obj["FORMAT"])
    except Exception as e:
        console.print(f"[red]Error watching test run:[/red] {str(e)}")
        exit(1)


@test_runs_group.command(name="download-attachments")
@click.argument("test_run_id")
@click.option(
    "--output-dir", default="./attachments", help="Directory to save attachments"
)
@click.pass_context
def download_attachments(ctx, test_run_id, output_dir):
    """Download all attachments for a test run"""

    async def _run():
        config, token = get_client_config(
            ctx.obj["PROFILE"], api_url=ctx.obj.get("API_URL")
        )
        client = TestZeusClient(**config)

        test_run_id_validated = validate_id(test_run_id, "test run")

        # Create output directory if it doesn't exist
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        async with client:
            # Apply token from config if available
            if token:
                initialize_client_with_token(client, token)
            else:
                await client.ensure_authenticated()

            # Download all attachments for the test run using positional parameters
            result = await client.test_runs.download_all_attachments(
                test_run_id_validated, str(output_path)
            )
            return result

    try:
        result = asyncio.run(_run())

        if not result:
            console.print(
                "[yellow]No attachments found or downloaded for this test run[/yellow]"
            )
            return

        console.print(
            f"[green]Downloaded {len(result)} attachments to {output_dir}[/green]"
        )
        for attachment in result:
            console.print(f"- {attachment}")
    except Exception as e:
        if ctx.obj.get("VERBOSE"):
            console.print(f"[red]Failed to download attachments:[/red]")
            import traceback

            console.print(traceback.format_exc())
        else:
            console.print(f"[red]Failed to download attachments:[/red] {str(e)}")
        exit(1)


@test_runs_group.command(name="status")
@click.argument("test_run_id")
@click.pass_context
def get_test_run_status(ctx, test_run_id):
    """Get the status of a test run"""

    async def _run():
        config, token = get_client_config(
            ctx.obj["PROFILE"], api_url=ctx.obj.get("API_URL")
        )
        client = TestZeusClient(**config)

        test_run_id_validated = validate_id(test_run_id, "test run")

        async with client:
            # Apply token from config if available
            if token:
                initialize_client_with_token(client, token)
            else:
                await client.ensure_authenticated()

            test_run = await client.test_runs.get_one(test_run_id_validated)
            return {
                "id": test_run.data["id"],
                "status": test_run.data["status"],
                "result": test_run.data.get("result"),
                "created": test_run.data["created"],
                "updated": test_run.data["updated"],
            }

    result = asyncio.run(_run())
    format_output(result, ctx.obj["FORMAT"])
