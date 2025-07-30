"""Tests for the workflow registry functionality."""

import pytest
import sqlite3
import tempfile
import os
import json
from pathlib import Path
import toml
from unittest.mock import patch

from kwargify_core.registry import WorkflowRegistry, WorkflowRegistryError


@pytest.fixture
def registry():
    """Create a registry with a temporary database."""
    with tempfile.NamedTemporaryFile(suffix=".db") as tmp:
        registry = WorkflowRegistry(db_path=tmp.name)
        yield registry


@pytest.fixture
def workflow_file(tmp_path):
    """Create a sample workflow file."""
    content = '''
from kwargify_core.core.workflow import Workflow
from kwargify_core.core.block import Block

class SimpleBlock(Block):
    def run(self) -> None:
        self.outputs = {"result": "success"}

def get_workflow():
    workflow = Workflow()
    workflow.name = "test_workflow"
    block = SimpleBlock(name="test_block")
    workflow.add_block(block)
    return workflow
'''
    file_path = tmp_path / "workflow.py"
    with open(file_path, "w") as f:
        f.write(content)
    return file_path


@pytest.fixture
def updated_workflow_file(tmp_path):
    """Create an updated version of the workflow file."""
    content = '''
from kwargify_core.core.workflow import Workflow
from kwargify_core.core.block import Block

class SimpleBlock(Block):
    def run(self) -> None:
        self.outputs = {"result": "success"}

def get_workflow():
    workflow = Workflow()
    workflow.name = "test_workflow"
    block1 = SimpleBlock(name="test_block")
    block2 = SimpleBlock(name="new_block")  # Added new block
    workflow.add_block(block1)
    workflow.add_block(block2)
    return workflow
'''
    file_path = tmp_path / "workflow_v2.py"
    with open(file_path, "w") as f:
        f.write(content)
    return file_path


def test_register_workflow(registry, workflow_file):
    """Test registering a new workflow."""
    result = registry.register(str(workflow_file), "Test workflow")
    
    assert result["workflow_name"] == "test_workflow"
    assert result["version"] == 1
    assert "source_hash" in result
    
    # Verify in database
    workflows = registry.list_workflows()
    assert len(workflows) == 1
    assert workflows[0]["name"] == "test_workflow"
    assert workflows[0]["latest_version"] == 1


def test_register_new_version(registry, workflow_file, updated_workflow_file):
    """Test registering a new version of an existing workflow."""
    # Register initial version
    v1 = registry.register(str(workflow_file))
    assert v1["version"] == 1
    
    # Register updated version
    v2 = registry.register(str(updated_workflow_file))
    assert v2["version"] == 2
    assert v2["workflow_id"] == v1["workflow_id"]
    
    # Get version details
    versions = registry.list_versions("test_workflow")
    assert len(versions) == 2
    assert versions[0]["version"] == 2  # Most recent first
    assert versions[1]["version"] == 1


def test_get_version_details(registry, workflow_file):
    """Test retrieving workflow version details."""
    registry.register(str(workflow_file))
    
    details = registry.get_version_details("test_workflow")
    assert details["version"] == 1
    
    # Check snapshot content
    snapshot = details["definition_snapshot"]
    assert snapshot["name"] == "test_workflow"
    assert len(snapshot["blocks"]) == 1
    assert snapshot["blocks"][0]["name"] == "test_block"
    
    # Check Mermaid diagram
    assert "graph TD" in details["mermaid_diagram"]
    assert "test_block" in details["mermaid_diagram"]


def test_list_workflows_empty(registry):
    """Test listing workflows when registry is empty."""
    workflows = registry.list_workflows()
    assert len(workflows) == 0


def test_list_versions_nonexistent(registry):
    """Test listing versions for non-existent workflow."""
    with pytest.raises(WorkflowRegistryError) as exc:
        registry.list_versions("nonexistent")
    assert "not found" in str(exc.value)


def test_get_version_details_specific_version(registry, workflow_file, updated_workflow_file):
    """Test getting details for a specific version."""
    registry.register(str(workflow_file))
    registry.register(str(updated_workflow_file))
    
    v1_details = registry.get_version_details("test_workflow", version=1)
    assert v1_details["version"] == 1
    assert len(v1_details["definition_snapshot"]["blocks"]) == 1
    
    v2_details = registry.get_version_details("test_workflow", version=2)
    assert v2_details["version"] == 2
    assert len(v2_details["definition_snapshot"]["blocks"]) == 2


def test_get_version_details_latest(registry, workflow_file, updated_workflow_file):
    """Test getting latest version details."""
    registry.register(str(workflow_file))
    registry.register(str(updated_workflow_file))
    
    latest = registry.get_version_details("test_workflow")  # No version specified
    assert latest["version"] == 2  # Should get latest version
    assert len(latest["definition_snapshot"]["blocks"]) == 2


def test_register_invalid_workflow(registry, tmp_path):
    """Test registering an invalid workflow file."""
    invalid_file = tmp_path / "invalid.py"
    invalid_file.write_text("def get_workflow(): return 'not a workflow'")
    
    with pytest.raises(WorkflowRegistryError) as exc:
        registry.register(str(invalid_file))
    assert "Failed to register workflow" in str(exc.value)


@pytest.fixture
def create_config_file(tmp_path):
    """Fixture to create a temporary config.toml file."""
    def _creator(config_data):
        config_path = tmp_path / "config.toml"
        with open(config_path, "w") as f:
            toml.dump(config_data, f)
        # Return the path and a cleanup function
        return config_path, lambda: os.remove(config_path)
    return _creator


@patch("kwargify_core.registry.get_database_name")
def test_registry_uses_configured_db(mock_get_database_name, tmp_path, create_config_file):
    """Test that WorkflowRegistry uses the configured database name if db_path is None."""
    custom_db_name = "configured_test_registry.db"
    mock_get_database_name.return_value = custom_db_name

    # Create a temporary config file (though get_database_name is mocked,
    # this simulates the environment where a config would exist)
    config_data = {"database": {"name": custom_db_name}}
    config_path, cleanup = create_config_file(config_data)

    # Change the current working directory to the temporary directory
    original_cwd = os.getcwd()
    os.chdir(tmp_path)

    try:
        # Instantiate WorkflowRegistry without db_path
        registry = WorkflowRegistry()

        # Assert that the logger was initialized with the configured DB name
        # We need to access the logger's db_path attribute, which is private.
        # A better approach would be to patch SQLiteLogger.__init__ as done in test_cli.py
        # Let's refactor this test to patch SQLiteLogger.__init__ instead.
        # assert registry.logger.db_path == custom_db_name # This won't work directly

        # Refactored test using patch on SQLiteLogger
        with patch("kwargify_core.registry.SQLiteLogger") as mock_sqlite_logger_class:
             # Instantiate WorkflowRegistry without db_path
             registry = WorkflowRegistry()

             # Assert that SQLiteLogger was instantiated with the configured DB name
             mock_sqlite_logger_class.assert_called_once_with(custom_db_name)


    finally:
        # Restore the original working directory and clean up the config file
        os.chdir(original_cwd)
        cleanup()