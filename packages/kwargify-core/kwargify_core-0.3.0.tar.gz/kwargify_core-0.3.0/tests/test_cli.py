"""Tests for the command-line interface."""

import os
from pathlib import Path
from typer.testing import CliRunner
import pytest
from unittest.mock import patch, MagicMock
from kwargify_core.cli import app, get_version
from kwargify_core import services
from datetime import datetime
import toml


@pytest.fixture
def runner():
    """Create a CLI runner for testing."""
    return CliRunner()


def test_version_display(runner):
    """Test that --version displays the correct version."""
    result = runner.invoke(app, ["--version"])
    assert result.exit_code == 0
    assert "Kwargify CLI Version:" in result.stdout


def test_help_display(runner):
    """Test that help text is displayed correctly."""
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "kwargify" in result.stdout.lower()
    assert "Define, run, and manage workflows" in result.stdout


def test_no_args_shows_help(runner):
    """Test that running CLI without arguments shows help."""
    result = runner.invoke(app)
    assert result.exit_code == 0
    assert "usage:" in result.stdout.lower()
    assert "--help" in result.stdout


def test_version_function():
    """Test the version retrieval function."""
    version = get_version()
    assert isinstance(version, str)
    assert version != ""  # Should not be empty


@patch("kwargify_core.cli.services.run_workflow_file_service")
def test_run_with_resume_options(mock_service, runner, valid_workflow_file):
    """Test running a workflow with resume options."""
    # Mock the service response
    mock_service.return_value = {
        "run_id": "123",
        "workflow_name": "test_workflow",
        "status": "COMPLETED",
        "message": "Workflow completed successfully"
    }

    result = runner.invoke(app, [
        "run",
        str(valid_workflow_file),
        "--resume-id", "123",
        "--resume-after", "test_block"
    ])

    workflow_path = Path(valid_workflow_file).resolve()
    mock_service.assert_called_once_with(
        workflow_path=workflow_path,
        resume_id="123",
        resume_after_block_name="test_block"
    )

    assert result.exit_code == 0
    assert "Workflow: test_workflow" in result.stdout
    assert "Status: COMPLETED" in result.stdout
    assert "Workflow completed successfully" in result.stdout


@patch("kwargify_core.cli.services.run_workflow_file_service")
def test_run_resume_id_without_after(mock_service, runner, valid_workflow_file):
    """Test that providing resume-id without resume-after automatically determines last successful block."""
    # Mock the service response
    mock_service.return_value = {
        "run_id": "123",
        "workflow_name": "test_workflow",
        "status": "COMPLETED",
        "message": "Workflow completed successfully"
    }

    result = runner.invoke(app, [
        "run",
        str(valid_workflow_file),
        "--resume-id", "123"
    ])

    workflow_path = Path(valid_workflow_file).resolve()
    mock_service.assert_called_once_with(
        workflow_path=workflow_path,
        resume_id="123",
        resume_after_block_name=None  # Service layer handles finding last successful block
    )

    assert result.exit_code == 0
    assert "Workflow: test_workflow" in result.stdout
    assert "Status: COMPLETED" in result.stdout
    assert "Workflow completed successfully" in result.stdout


def test_run_resume_after_without_id(runner, valid_workflow_file):
    """Test that providing resume-after without resume-id fails."""
    result = runner.invoke(app, [
        "run",
        str(valid_workflow_file),
        "--resume-after", "block1"
    ])
    assert result.exit_code == 1
    assert "Cannot specify resume_after_block_name without resume_id" in result.stdout


@patch("kwargify_core.cli.services.validate_workflow_service")
def test_validate_valid_workflow(mock_service, runner, valid_workflow_file):
    """Test validating a valid workflow."""
    mock_service.return_value = {
        "is_valid": True,
        "name": "test_workflow",
        "blocks_count": 2,
        "dependency_flow": "block1 >> block2",
        "mermaid_diagram": "graph TD\nA-->B",
        "errors": None
    }

    result = runner.invoke(app, ["validate", str(valid_workflow_file)])

    workflow_path = Path(valid_workflow_file).resolve()
    mock_service.assert_called_once_with(workflow_path)

    assert result.exit_code == 0
    assert "Workflow validation successful!" in result.stdout
    assert "test_workflow" in result.stdout


@patch("kwargify_core.cli.services.validate_workflow_service")
def test_validate_invalid_workflow(mock_service, runner, valid_workflow_file):
    """Test validating an invalid workflow."""
    mock_service.return_value = {
        "is_valid": False,
        "name": None,
        "blocks_count": None,
        "dependency_flow": None,
        "mermaid_diagram": None,
        "errors": ["Circular dependency detected"]
    }

    result = runner.invoke(app, ["validate", str(valid_workflow_file)])

    assert result.exit_code == 1
    assert "Validation failed:" in result.stdout
    assert "Circular dependency detected" in result.stdout


def test_validate_nonexistent_file(runner):
    """Test validating a non-existent workflow file."""
    result = runner.invoke(app, ["validate", "nonexistent.py"])
    assert result.exit_code == 2  # Typer's error code for invalid arguments
    assert "does not exist" in result.stdout.lower()


@patch("kwargify_core.cli.services.run_workflow_file_service")
def test_run_file_based_workflow(mock_service, runner, valid_workflow_file):
    """Test running a workflow directly from file."""
    mock_service.return_value = {
        "run_id": "123",
        "workflow_name": "test_workflow",
        "status": "COMPLETED",
        "message": "Workflow completed successfully"
    }

    result = runner.invoke(app, ["run", str(valid_workflow_file)])

    workflow_path = Path(valid_workflow_file).resolve()
    mock_service.assert_called_once_with(
        workflow_path=workflow_path,
        resume_id=None,
        resume_after_block_name=None
    )

    assert result.exit_code == 0
    assert "Status: COMPLETED" in result.stdout
    assert "Workflow completed successfully" in result.stdout


@patch("kwargify_core.cli.services.run_registered_workflow_service")
def test_run_registered_workflow(mock_service, runner):
    """Test running a workflow by name from registry."""
    mock_service.return_value = {
        "run_id": "123",
        "workflow_name": "test_workflow",
        "status": "COMPLETED",
        "message": "Workflow 'test_workflow' (Version: 1) completed successfully"
    }

    result = runner.invoke(app, ["run", "--name", "test_workflow"])
    
    mock_service.assert_called_once_with(
        name="test_workflow",
        version=None,
        resume_id=None,
        resume_after_block_name=None
    )

    assert result.exit_code == 0
    assert "Workflow: test_workflow" in result.stdout
    assert "Status: COMPLETED" in result.stdout
    assert "completed successfully" in result.stdout


@patch("kwargify_core.cli.services.run_registered_workflow_service")
def test_run_specific_version(mock_service, runner):
    """Test running a specific version of a registered workflow."""
    mock_service.return_value = {
        "run_id": "123",
        "workflow_name": "test_workflow",
        "status": "COMPLETED",
        "message": "Workflow 'test_workflow' (Version: 1) completed successfully"
    }

    result = runner.invoke(app, ["run", "--name", "test_workflow", "--version", "1"])

    mock_service.assert_called_once_with(
        name="test_workflow",
        version=1,
        resume_id=None,
        resume_after_block_name=None
    )

    assert result.exit_code == 0
    assert "Workflow: test_workflow" in result.stdout
    assert "Status: COMPLETED" in result.stdout
    assert "completed successfully" in result.stdout


def test_run_nonexistent_workflow(runner):
    """Test running a non-existent registered workflow."""
    result = runner.invoke(app, ["run", "--name", "nonexistent"])
    assert result.exit_code == 1
    assert "Error running workflow:" in result.stdout


def test_run_invalid_version(runner, valid_workflow_file):
    """Test running a non-existent version of a workflow."""
    # Register workflow
    runner.invoke(app, ["register", str(valid_workflow_file)])
    
    # Try to run non-existent version
    result = runner.invoke(app, ["run", "--name", "test_workflow", "--version", "999"])
    assert result.exit_code == 1
    assert "Error running workflow:" in result.stdout


def test_run_missing_source_file(runner, valid_workflow_file, tmp_path):
    """Test running a registered workflow whose source file was moved/deleted."""
    # Register workflow
    runner.invoke(app, ["register", str(valid_workflow_file)])
    
    # Move the source file to simulate deletion/move
    new_path = tmp_path / "moved_workflow.py"
    valid_workflow_file.rename(new_path)
    
    # Try to run the workflow
    result = runner.invoke(app, ["run", "--name", "test_workflow"])
    assert result.exit_code == 1
    assert "Error running workflow" in result.stdout
    assert "not found" in result.stdout


def test_run_mutually_exclusive_args(runner, valid_workflow_file):
    """Test that file path and name cannot be used together."""
    result = runner.invoke(app, [
        "run",
        str(valid_workflow_file),
        "--name", "test_workflow"
    ])
    assert result.exit_code == 1
    assert "Cannot provide both" in result.stdout


@patch("kwargify_core.cli.services.register_workflow_service")
def test_register_workflow(mock_service, runner, valid_workflow_file):
    """Test registering a valid workflow."""
    mock_service.return_value = {
        "workflow_name": "test_workflow",
        "version": 1,
        "source_hash": "abcdef123456"
    }

    result = runner.invoke(app, ["register", str(valid_workflow_file)])

    workflow_path = Path(valid_workflow_file).resolve()
    mock_service.assert_called_once_with(workflow_path, None)

    assert result.exit_code == 0
    assert "Workflow registered successfully!" in result.stdout
    assert "Name: test_workflow" in result.stdout
    assert "Version: 1" in result.stdout


@patch("kwargify_core.cli.services.register_workflow_service")
def test_register_with_description(mock_service, runner, valid_workflow_file):
    """Test registering a workflow with description."""
    mock_service.return_value = {
        "workflow_name": "test_workflow",
        "version": 1,
        "source_hash": "abcdef123456"
    }

    result = runner.invoke(app, [
        "register",
        str(valid_workflow_file),
        "--description",
        "Test description"
    ])

    workflow_path = Path(valid_workflow_file).resolve()
    mock_service.assert_called_once_with(workflow_path, "Test description")

    assert result.exit_code == 0
    assert "Workflow registered successfully!" in result.stdout
    assert "Name: test_workflow" in result.stdout


def test_register_nonexistent_file(runner):
    """Test registering a non-existent workflow file."""
    result = runner.invoke(app, ["register", "nonexistent.py"])
    assert result.exit_code == 2  # Typer's error code for invalid arguments
    assert "does not exist" in result.stdout.lower()


@patch("kwargify_core.cli.services.list_workflows_service")
def test_list_workflows_empty(mock_service, runner):
    """Test listing workflows when none are registered."""
    mock_service.return_value = []

    result = runner.invoke(app, ["list"])

    mock_service.assert_called_once()
    assert result.exit_code == 0
    assert "Registered Workflows" in result.stdout


@patch("kwargify_core.cli.services.list_workflows_service")
def test_list_workflows(mock_service, runner):
    """Test listing workflows."""
    mock_service.return_value = [{
        "name": "test_workflow",
        "latest_version": 1,
        "description": "Test workflow",
        "created_at": "2025-01-01T10:00:00"
    }]

    result = runner.invoke(app, ["list"])

    mock_service.assert_called_once()
    assert result.exit_code == 0
    assert "test_workflow" in result.stdout
    assert "Latest Version" in result.stdout


@patch("kwargify_core.cli.services.list_workflow_versions_service")
def test_list_workflow_versions(mock_service, runner):
    """Test listing versions of a specific workflow."""
    mock_service.return_value = [{
        "version": 1,
        "created_at": "2025-01-01T10:00:00",
        "source_path": "/path/to/workflow.py",
        "source_hash": "abcdef123456"
    }]

    result = runner.invoke(app, ["list", "--name", "test_workflow"])

    mock_service.assert_called_once_with("test_workflow")
    assert result.exit_code == 0
    assert "Versions of Workflow: test_workflow" in result.stdout
    assert "Version" in result.stdout


@patch("kwargify_core.cli.services.list_workflow_versions_service")
def test_list_nonexistent_workflow(mock_service, runner):
    """Test listing versions of a non-existent workflow."""
    mock_service.side_effect = services.RegistryServiceError("Workflow not found")
    
    result = runner.invoke(app, ["list", "--name", "nonexistent"])
    assert result.exit_code == 1
    assert "Error listing workflows" in result.stdout


@patch("kwargify_core.cli.services.show_workflow_service")
def test_show_workflow_summary(mock_service, runner, valid_workflow_file):
    """Test showing workflow summary."""
    mock_service.return_value = {
        "name": "test_workflow",
        "total_blocks": 3,
        "execution_order": [
            {"order": 1, "name": "block1", "dependencies": []},
            {"order": 2, "name": "block2", "dependencies": ["block1"]}
        ],
        "block_details": [
            {
                "name": "block1",
                "config": {"param": "value1"},
                "input_map": {}
            },
            {
                "name": "block2",
                "config": {},
                "input_map": {"input": {"source_block": "block1", "output_key": "result"}}
            }
        ],
        "mermaid_diagram": "graph TD\nA-->B"
    }

    result = runner.invoke(app, ["show", str(valid_workflow_file)])

    workflow_path = Path(valid_workflow_file).resolve()
    mock_service.assert_called_once_with(workflow_path, False)

    assert result.exit_code == 0
    assert "Workflow Summary" in result.stdout
    assert "Total Blocks: 3" in result.stdout
    assert "block1" in result.stdout
    assert "param: value1" in result.stdout


@patch("kwargify_core.cli.services.show_workflow_service")
def test_show_workflow_diagram(mock_service, runner, valid_workflow_file):
    """Test showing workflow Mermaid diagram."""
    mock_service.return_value = {
        "mermaid_diagram": "graph TD\nA-->B"
    }

    result = runner.invoke(app, ["show", "--diagram", str(valid_workflow_file)])

    workflow_path = Path(valid_workflow_file).resolve()
    mock_service.assert_called_once_with(workflow_path, True)

    assert result.exit_code == 0
    assert "```mermaid" in result.stdout
    assert "graph TD" in result.stdout


def test_show_nonexistent_file(runner):
    """Test showing a non-existent workflow file."""
    result = runner.invoke(app, ["show", "nonexistent.py"])
    assert result.exit_code == 2  # Typer's error code for invalid arguments
    assert "does not exist" in result.stdout.lower()


@pytest.fixture
def valid_workflow_file(tmp_path):
    """Create a valid workflow file for testing."""
    content = '''
def get_workflow():
    # Content not important since we're mocking service layer
    pass
'''
    file_path = tmp_path / "valid_workflow.py"
    with open(file_path, "w") as f:
        f.write(content)
    return file_path


@pytest.fixture
def invalid_workflow_file(tmp_path):
    """Create an invalid workflow file for testing."""
    content = '''
def get_workflow():
    return "not a workflow object"
'''
    file_path = tmp_path / "invalid_workflow.py"
    with open(file_path, "w") as f:
        f.write(content)
    return file_path


@patch("kwargify_core.cli.services.run_workflow_file_service")
def test_run_invalid_workflow(mock_service, runner, invalid_workflow_file):
    """Test running an invalid workflow file."""
    mock_service.side_effect = services.WorkflowLoadErrorService("Invalid workflow object")

    result = runner.invoke(app, ["run", str(invalid_workflow_file)])
    assert result.exit_code == 1
    assert "Error loading workflow:" in result.stdout


def test_run_nonexistent_file(runner):
    """Test running a non-existent workflow file."""
    result = runner.invoke(app, ["run", "nonexistent.py"])
    assert result.exit_code == 2  # Typer's error code for invalid arguments
    assert "does not exist" in result.stdout.lower()


@patch("kwargify_core.cli.services.init_project_service")
def test_init_command_creates_config(mock_service, runner):
    """Test that the init command creates a new configuration."""
    mock_service.return_value = {
        "message": "Project 'my_project' initialized. Configuration saved."
    }
    
    result = runner.invoke(app, ["init"], input="my_project\nmy_data.db\n")
    
    mock_service.assert_called_once_with("my_project", "my_data.db")
    assert result.exit_code == 0
    assert "Project 'my_project' initialized." in result.stdout


@patch("kwargify_core.cli.services.init_project_service")
def test_init_command_handles_empty_input(mock_service, runner):
    """Test that the init command handles empty input."""
    result = runner.invoke(app, ["init"], input="\n\n")
    
    # Typer should exit with error since inputs are mandatory
    assert result.exit_code != 0
    assert "Error: Project name cannot be empty." in result.stdout


@patch("kwargify_core.cli.services.show_workflow_service")
def test_show_workflow_error(mock_service, runner, valid_workflow_file):
    """Test error handling when showing workflow fails."""
    mock_service.side_effect = services.WorkflowShowError("Failed to analyze workflow")

    result = runner.invoke(app, ["show", str(valid_workflow_file)])

    workflow_path = Path(valid_workflow_file).resolve()
    mock_service.assert_called_once_with(workflow_path, False)

    assert result.exit_code == 1
    assert "Error showing workflow: Failed to analyze workflow" in result.stdout


@patch("kwargify_core.cli.services.run_workflow_file_service")
def test_run_workflow_execution_error(mock_service, runner, valid_workflow_file):
    """Test error handling when workflow execution fails."""
    mock_service.side_effect = services.WorkflowRunError("Block execution failed")

    result = runner.invoke(app, ["run", str(valid_workflow_file)])

    workflow_path = Path(valid_workflow_file).resolve()
    mock_service.assert_called_once_with(
        workflow_path=workflow_path,
        resume_id=None,
        resume_after_block_name=None
    )

    assert result.exit_code == 1
    assert "Error running workflow: Block execution failed" in result.stdout
