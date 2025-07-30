"""Command-line interface for Kwargify workflows."""

import typer
from typing import Optional
from pathlib import Path
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
import pkg_resources

from . import services

# Create console for rich output
console = Console()

# Create the main Typer application
app = typer.Typer(
    name="kwargify",
    help="Kwargify: Define, run, and manage workflows.",
    no_args_is_help=True,
    rich_help_panel="Kwargify CLI"
)

def get_version() -> str:
    """Get the version of kwargify-core package."""
    try:
        return pkg_resources.get_distribution('kwargify-core').version
    except pkg_resources.DistributionNotFound:
        return "unknown"

def version_callback(value: bool):
    """Callback for --version flag."""
    if value:
        typer.echo(f"Kwargify CLI Version: {get_version()}")
        raise typer.Exit()

@app.callback()
def main(
    version: bool = typer.Option(
        None,
        "--version",
        "-v",
        help="Show the application version and exit.",
        callback=version_callback,
        is_eager=True,
    ),
) -> None:
    """
    Kwargify CLI - Define, run, and manage workflows.

    A command-line tool for working with Kwargify workflows. Use this tool to:
    - Run workflows defined in Python files
    - Validate workflow structure
    - Visualize workflow dependencies
    - Register and version workflows
    """
    pass

@app.command("init")
def init_project(
    project_name_opt: Optional[str] = typer.Option(None, "--project-name", help="Your project's name (will prompt if not provided)"),
    db_name_opt: Optional[str] = typer.Option(None, "--db-name", help="Database file name (e.g., my_data.db, will prompt if not provided)")
) -> None:
    """
    Initializes a new Kwargify project.
    """
    project_name = project_name_opt
    if project_name is None:
        project_name = typer.prompt("Project name", default="")

    # Validate project name is not empty
    if not project_name.strip():
        typer.echo("Error: Project name cannot be empty.", err=True)
        raise typer.Exit(code=1)

    db_name = db_name_opt
    if db_name is None:
        db_name = typer.prompt("Database file name (e.g., my_data.db)", default="")

    try:
        result = services.init_project_service(project_name, db_name)
        typer.echo(result["message"])
    except services.ProjectInitError as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(code=1)
    except Exception as e:
        typer.echo(f"Unexpected error: {e}", err=True)
        raise typer.Exit(code=1)

@app.command("run")
def run_workflow(
    workflow_path: Optional[Path] = typer.Argument(
        None,
        exists=True,
        file_okay=True,
        dir_okay=False,
        resolve_path=True,
        help="Path to the workflow Python file (.py)"
    ),
    name: Optional[str] = typer.Option(
        None,
        "--name",
        "-n",
        help="Name of the registered workflow to run"
    ),
    version: Optional[int] = typer.Option(
        None,
        "--version",
        "-v",
        help="Version of the registered workflow to run (default: latest)"
    ),
    resume_id: Optional[str] = typer.Option(
        None,
        "--resume-id",
        help="ID of the previous run to resume from"
    ),
    resume_after: Optional[str] = typer.Option(
        None,
        "--resume-after",
        help="Name of the last completed block after which to resume"
    )
) -> None:
    """
    Run a workflow from a file or from the registry.

    The workflow can be specified either by:
    - A path to a Python file containing the workflow definition
    - A name (and optional version) of a registered workflow
    """
    if not workflow_path and not name:
        typer.echo("Error: Must provide either a workflow path or --name.", err=True)
        raise typer.Exit(code=1)
    if workflow_path and name:
        typer.echo("Error: Cannot provide both workflow path and --name.", err=True)
        raise typer.Exit(code=1)

    try:
        if workflow_path:
            # Path validation is now handled by Typer
            result = services.run_workflow_file_service(
                workflow_path=workflow_path,
                resume_id=resume_id,
                resume_after_block_name=resume_after
            )
        elif name:  # We already checked that either workflow_path or name must be provided
            result = services.run_registered_workflow_service(
                name=name,  # At this point name cannot be None since we checked earlier
                version=version,
                resume_id=resume_id,
                resume_after_block_name=resume_after
            )
        else:
            # This should never happen due to earlier checks
            typer.echo("Error: Must provide either a workflow path or --name.", err=True)
            raise typer.Exit(code=1)

        typer.echo(f"Run ID: {result['run_id']}")
        typer.echo(f"Workflow: {result['workflow_name']}")
        typer.echo(f"Status: {result['status']}")
        typer.echo(result['message'])

    except services.WorkflowLoadErrorService as e:
        typer.echo(f"Error loading workflow: {e}", err=True)
        raise typer.Exit(code=1)
    except (services.WorkflowRunError, services.RegistryServiceError) as e:
        typer.echo(f"Error running workflow: {e}", err=True)
        raise typer.Exit(code=1)
    except services.ServiceError as e:
        typer.echo(f"Service error: {e}", err=True)
        raise typer.Exit(code=1)
    except Exception as e:
        typer.echo(f"Unexpected error: {e}", err=True)
        raise typer.Exit(code=1)

@app.command("validate")
def validate_workflow(
    workflow_path: Path = typer.Argument(
        ...,
        exists=True,
        file_okay=True,
        dir_okay=False,
        resolve_path=True,
        help="Path to the workflow Python file (.py)"
    )
) -> None:
    """
    Validate a workflow defined in a Python file without executing it.

    Checks:
    - File can be loaded successfully
    - get_workflow() function exists and returns a Workflow
    - No circular dependencies in the workflow graph
    - All block dependencies are satisfied
    """
    try:
        result = services.validate_workflow_service(workflow_path)

        if result["is_valid"]:
            typer.echo(typer.style("\n✓ Workflow validation successful!", fg=typer.colors.GREEN, bold=True))
            typer.echo(f"- Name: {result['name']}")
            typer.echo(f"- Blocks: {result['blocks_count']}")
            typer.echo(f"- Dependency Flow: {result['dependency_flow']}")
            typer.echo("\nExecution Order Diagram (Mermaid):")
            typer.echo("```mermaid")
            typer.echo(result['mermaid_diagram'])
            typer.echo("```")
        else:
            typer.echo("Validation failed:", err=True)
            for error in result["errors"]:
                typer.echo(f"- {error}", err=True)
            raise typer.Exit(code=1)

    except services.WorkflowLoadErrorService as e:
        typer.echo(f"Error loading workflow: {e}", err=True)
        raise typer.Exit(code=1)
    except services.WorkflowValidationError as e:
        typer.echo(f"Validation error: {e}", err=True)
        raise typer.Exit(code=1)
    except services.ServiceError as e:
        typer.echo(f"Service error: {e}", err=True)
        raise typer.Exit(code=1)
    except Exception as e:
        typer.echo(f"Unexpected error: {e}", err=True)
        raise typer.Exit(code=1)

@app.command("show")
def show_workflow(
    workflow_path: Path = typer.Argument(
        ...,
        exists=True,
        file_okay=True,
        dir_okay=False,
        resolve_path=True,
        help="Path to the workflow Python file (.py)"
    ),
    diagram: bool = typer.Option(
        False,
        "--diagram",
        "-d",
        help="Show the Mermaid diagram definition instead of summary"
    )
) -> None:
    """
    Display a summary or the Mermaid diagram of a workflow.
    
    Shows a human-readable summary by default, including blocks and their dependencies.
    Use --diagram to get the Mermaid diagram definition instead.
    """
    try:
        result = services.show_workflow_service(workflow_path, diagram)

        if diagram:
            typer.echo("```mermaid")
            typer.echo(result["mermaid_diagram"])
            typer.echo("```")
        else:
            typer.echo(f"\nWorkflow Summary: {result['name']}")
            typer.echo("=" * (len(result['name']) + 16))
            typer.echo(f"\nTotal Blocks: {result['total_blocks']}")
            
            typer.echo("\nExecution Order:")
            for block in result['execution_order']:
                deps = block['dependencies']
                deps_str = f" (depends on: {', '.join(deps)})" if deps else ""
                typer.echo(f"{block['order']}. {block['name']}{deps_str}")
            
            typer.echo("\nBlock Details:")
            for block in result['block_details']:
                typer.echo(f"\n{block['name']}:")
                if block['config']:
                    typer.echo("  Config:")
                    for key, value in block['config'].items():
                        typer.echo(f"    {key}: {value}")
                if block['input_map']:
                    typer.echo("  Input Mappings:")
                    for input_key, mapping in block['input_map'].items():
                        typer.echo(f"    {input_key} <- {mapping['source_block']}.{mapping['output_key']}")

            typer.echo("\nMermaid Diagram:")
            typer.echo("```mermaid")
            typer.echo(result['mermaid_diagram'])
            typer.echo("```")

    except services.WorkflowLoadErrorService as e:
        typer.echo(f"Error loading workflow: {e}", err=True)
        raise typer.Exit(code=1)
    except services.WorkflowShowError as e:
        typer.echo(f"Error showing workflow: {e}", err=True)
        raise typer.Exit(code=1)
    except services.ServiceError as e:
        typer.echo(f"Service error: {e}", err=True)
        raise typer.Exit(code=1)
    except Exception as e:
        typer.echo(f"Unexpected error: {e}", err=True)
        raise typer.Exit(code=1)

@app.command("register")
def register_workflow(
    workflow_path: Path = typer.Argument(
        ...,
        exists=True,
        file_okay=True,
        dir_okay=False,
        resolve_path=True,
        help="Path to the workflow Python file (.py)"
    ),
    description: Optional[str] = typer.Option(
        None,
        "--description",
        "-d",
        help="Optional description of the workflow"
    )
) -> None:
    """
    Register a workflow in the registry or create a new version if it exists.
    """
    try:
        result = services.register_workflow_service(workflow_path, description)
        
        typer.echo(typer.style("\n✓ Workflow registered successfully!", fg=typer.colors.GREEN))
        typer.echo(f"Name: {result['workflow_name']}")
        typer.echo(f"Version: {result['version']}")
        typer.echo(f"Source Hash: {result['source_hash']}")

    except services.WorkflowLoadErrorService as e:
        typer.echo(f"Error loading workflow: {e}", err=True)
        raise typer.Exit(code=1)
    except services.RegistryServiceError as e:
        typer.echo(f"Error registering workflow: {e}", err=True)
        raise typer.Exit(code=1)
    except services.ServiceError as e:
        typer.echo(f"Service error: {e}", err=True)
        raise typer.Exit(code=1)
    except Exception as e:
        typer.echo(f"Unexpected error: {e}", err=True)
        raise typer.Exit(code=1)

@app.command("list")
def list_workflows(
    name: Optional[str] = typer.Option(
        None,
        "--name",
        "-n",
        help="Show versions for a specific workflow"
    )
) -> None:
    """
    List registered workflows or versions of a specific workflow.
    """
    try:
        if name:
            versions = services.list_workflow_versions_service(name)
            
            table = Table(title=f"Versions of Workflow: {name}")
            table.add_column("Version", justify="right")
            table.add_column("Created", justify="left")
            table.add_column("Source Path", justify="left")
            table.add_column("Source Hash", justify="left")
            
            for version in versions:
                created = datetime.fromisoformat(version["created_at"]).strftime("%Y-%m-%d %H:%M:%S")
                table.add_row(
                    str(version["version"]),
                    created,
                    str(version["source_path"]),
                    version["source_hash"][:8] + "..."  # Show first 8 chars
                )
            
            console.print(table)
            
        else:
            workflows = services.list_workflows_service()
            
            table = Table(title="Registered Workflows")
            table.add_column("Name", justify="left")
            table.add_column("Latest Version", justify="right")
            table.add_column("Description", justify="left")
            table.add_column("Created", justify="left")
            
            for workflow in workflows:
                created = datetime.fromisoformat(workflow["created_at"]).strftime("%Y-%m-%d %H:%M:%S")
                table.add_row(
                    workflow["name"],
                    str(workflow["latest_version"] or "N/A"),
                    workflow["description"] or "No description",
                    created
                )
            
            console.print(table)

    except services.RegistryServiceError as e:
        typer.echo(f"Error listing workflows: {e}", err=True)
        raise typer.Exit(code=1)
    except services.ServiceError as e:
        typer.echo(f"Service error: {e}", err=True)
        raise typer.Exit(code=1)
    except Exception as e:
        typer.echo(f"Unexpected error: {e}", err=True)
        raise typer.Exit(code=1)

@app.command("history")
def show_history(
    run_id: Optional[str] = typer.Argument(
        None,
        help="Specific run ID to show details for"
    )
) -> None:
    """
    Show workflow run history or details of a specific run.

    If run_id is provided, shows detailed information about that specific run.
    Otherwise, lists recent workflow runs.
    """
    try:
        if run_id:
            run_details = services.get_run_details_service(run_id)

            console.print(Panel.fit(
                f"[bold]Workflow:[/bold] {run_details['workflow_name']}\n"
                f"[bold]Run ID:[/bold] {run_details['run_id']}\n"
                f"[bold]Status:[/bold] {run_details['status']}\n"
                f"[bold]Started:[/bold] {run_details['start_time']}\n"
                f"[bold]Ended:[/bold] {run_details['end_time'] or 'Not completed'}"
            ))

            table = Table(title="Block Executions")
            table.add_column("Block", justify="left")
            table.add_column("Status", justify="center")
            table.add_column("Started", justify="left")
            table.add_column("Duration", justify="right")
            table.add_column("Retries", justify="center")

            for block in run_details['blocks']:
                start_time = datetime.fromisoformat(block['start_time'])
                end_time = datetime.fromisoformat(block['end_time']) if block['end_time'] else None
                duration = str(end_time - start_time) if end_time else "N/A"

                table.add_row(
                    block['block_name'],
                    f"[{'green' if block['status'] == 'COMPLETED' else 'red'}]{block['status']}[/]",
                    start_time.strftime("%H:%M:%S"),
                    duration,
                    str(block['retries_attempted'])
                )

            console.print("\n[bold]Execution Details:[/bold]")
            console.print(table)

            for block in run_details['blocks']:
                console.print(f"\n[bold]{block['block_name']}[/bold]")
                if block['inputs']:
                    console.print("  [cyan]Inputs:[/cyan]")
                    for key, value in block['inputs'].items():
                        console.print(f"    {key}: {value}")
                if block['outputs']:
                    console.print("  [green]Outputs:[/green]")
                    for key, value in block['outputs'].items():
                        console.print(f"    {key}: {value}")
                if block['error_message']:
                    console.print(f"  [red]Error:[/red] {block['error_message']}")

        else:
            runs = services.list_run_history_service()
            
            table = Table(title="Recent Workflow Runs")
            table.add_column("Run ID", justify="left")
            table.add_column("Workflow", justify="left")
            table.add_column("Status", justify="center")
            table.add_column("Started", justify="left")
            table.add_column("Duration", justify="right")

            for run in runs:
                start_time = datetime.fromisoformat(run['start_time'])
                end_time = datetime.fromisoformat(run['end_time']) if run['end_time'] else None
                duration = str(end_time - start_time) if end_time else "Running..."

                table.add_row(
                    run['run_id'],
                    run['workflow_name'],
                    f"[{'green' if run['status'] == 'COMPLETED' else 'red'}]{run['status']}[/]",
                    start_time.strftime("%Y-%m-%d %H:%M:%S"),
                    duration
                )

            console.print(table)

    except services.HistoryError as e:
        typer.echo(f"Error accessing workflow history: {e}", err=True)
        raise typer.Exit(code=1)
    except services.ServiceError as e:
        typer.echo(f"Service error: {e}", err=True)
        raise typer.Exit(code=1)
    except Exception as e:
        typer.echo(f"Unexpected error: {e}", err=True)
        raise typer.Exit(code=1)

if __name__ == "__main__":
    app()