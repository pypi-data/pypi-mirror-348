"""Tests for Kwargify core service layer functionality."""

from pathlib import Path
import pytest
from unittest.mock import patch, MagicMock

from kwargify_core import services
from kwargify_core.core.workflow import Workflow
from kwargify_core.logging.sqlite_logger import SQLiteLogger
from kwargify_core.loader import WorkflowLoadError
from kwargify_core.registry import WorkflowRegistry, WorkflowRegistryError

# ===== Test init_project_service =====

def test_init_project_service_success():
    """Test successful project initialization."""
    with patch("kwargify_core.services.load_config") as mock_load_config, \
         patch("kwargify_core.services.save_config") as mock_save_config:
        
        mock_load_config.return_value = {"project": {}, "database": {}}
        
        result = services.init_project_service("test_project", "test.db")
        
        assert result == {"message": "Project 'test_project' initialized. Configuration saved."}
        mock_save_config.assert_called_once()
        config = mock_save_config.call_args[0][0]
        assert config["project"]["name"] == "test_project"
        assert config["database"]["name"] == "test.db"

def test_init_project_service_empty_name():
    """Test project initialization with empty project name."""
    with pytest.raises(services.ProjectInitError, match="Project name cannot be empty"):
        services.init_project_service("", "test.db")

def test_init_project_service_empty_db():
    """Test project initialization with empty database name."""
    with pytest.raises(services.ProjectInitError, match="Database name cannot be empty"):
        services.init_project_service("test_project", "")

def test_init_project_service_save_error():
    """Test project initialization with config save error."""
    with patch("kwargify_core.services.load_config") as mock_load_config, \
         patch("kwargify_core.services.save_config") as mock_save_config:
        
        mock_load_config.return_value = {}
        mock_save_config.side_effect = Exception("Save failed")
        
        with pytest.raises(services.ProjectInitError, match="Failed to initialize project"):
            services.init_project_service("test_project", "test.db")

# ===== Test run_workflow_file_service =====

def test_run_workflow_file_service_success(tmp_path):
    """Test successful workflow file execution."""
    workflow_path = Path(tmp_path) / "test_workflow.py"
    workflow_path.touch()
    
    mock_workflow = MagicMock(spec=Workflow)
    mock_workflow.run_id = "test_run_id"
    mock_workflow.name = "test_workflow"
    
    with patch("kwargify_core.services.load_workflow_from_py") as mock_load, \
         patch("kwargify_core.services.SQLiteLogger"):
        
        mock_load.return_value = mock_workflow
        
        result = services.run_workflow_file_service(workflow_path)
        
        assert result["run_id"] == "test_run_id"
        assert result["workflow_name"] == "test_workflow"
        assert result["status"] == "COMPLETED"

def test_run_workflow_file_service_missing_file(tmp_path):
    """Test workflow execution with missing file."""
    workflow_path = Path(tmp_path) / "nonexistent.py"
    
    with pytest.raises(services.WorkflowLoadErrorService, match="Workflow file not found"):
        services.run_workflow_file_service(workflow_path)

def test_run_workflow_file_service_load_error(tmp_path):
    """Test workflow execution with load error."""
    workflow_path = Path(tmp_path) / "test_workflow.py"
    workflow_path.touch()
    
    with patch("kwargify_core.services.load_workflow_from_py") as mock_load, \
         patch("kwargify_core.services.SQLiteLogger"):
        
        mock_load.side_effect = WorkflowLoadError("Load failed")
        
        with pytest.raises(services.WorkflowLoadErrorService, match="Error loading workflow"):
            services.run_workflow_file_service(workflow_path)

# ===== Test run_registered_workflow_service =====

def test_run_registered_workflow_service_success():
    """Test successful registered workflow execution."""
    mock_workflow = MagicMock(spec=Workflow)
    mock_workflow.run_id = "test_run_id"
    mock_workflow.name = "test_workflow"
    
    with patch("kwargify_core.services.WorkflowRegistry") as MockRegistry, \
         patch("kwargify_core.services.load_workflow_from_py") as mock_load, \
         patch("kwargify_core.services.Path.exists") as mock_exists, \
         patch("kwargify_core.services.SQLiteLogger"):
        
        mock_registry = MockRegistry.return_value
        mock_registry.get_version_details.return_value = {
            "id": "test_version_id",
            "source_path": "/path/to/workflow.py",
            "version": 1
        }
        mock_exists.return_value = True
        mock_load.return_value = mock_workflow
        
        result = services.run_registered_workflow_service("test_workflow", version=1)
        
        assert result["run_id"] == "test_run_id"
        assert result["workflow_name"] == "test_workflow"
        assert result["status"] == "COMPLETED"

def test_run_registered_workflow_service_not_found():
    """Test registered workflow execution with non-existent workflow."""
    with patch("kwargify_core.services.WorkflowRegistry") as MockRegistry:
        mock_registry = MockRegistry.return_value
        mock_registry.get_version_details.side_effect = WorkflowRegistryError("Not found")
        
        with pytest.raises(services.RegistryServiceError, match="Error accessing registry"):
            services.run_registered_workflow_service("nonexistent")

# ===== Test validate_workflow_service =====

def test_validate_workflow_service_success(tmp_path):
    """Test successful workflow validation."""
    workflow_path = Path(tmp_path) / "test_workflow.py"
    workflow_path.touch()
    
    mock_workflow = MagicMock(spec=Workflow)
    mock_workflow.name = "test_workflow"
    mock_workflow.blocks = []
    mock_workflow.topological_sort.return_value = []
    mock_workflow.to_mermaid.return_value = "graph TD;"
    
    with patch("kwargify_core.services.load_workflow_from_py") as mock_load:
        mock_load.return_value = mock_workflow
        
        result = services.validate_workflow_service(workflow_path)
        
        assert result["is_valid"] is True
        assert result["name"] == "test_workflow"
        assert result["blocks_count"] == 0
        assert result["mermaid_diagram"] == "graph TD;"

def test_validate_workflow_service_invalid():
    """Test workflow validation with invalid workflow."""
    path = Path("test_workflow.py")
    
    with patch("kwargify_core.services.load_workflow_from_py") as mock_load:
        mock_load.side_effect = WorkflowLoadError("Invalid workflow")
        
        with pytest.raises(services.WorkflowLoadErrorService, match="Error loading workflow"):
            services.validate_workflow_service(path)

# ===== Test show_workflow_service =====

def test_show_workflow_service_success(tmp_path):
    """Test successful workflow display."""
    workflow_path = Path(tmp_path) / "test_workflow.py"
    workflow_path.touch()
    
    mock_workflow = MagicMock(spec=Workflow)
    mock_workflow.name = "test_workflow"
    mock_workflow.blocks = []
    mock_workflow.topological_sort.return_value = []
    mock_workflow.to_mermaid.return_value = "graph TD;"
    
    with patch("kwargify_core.services.load_workflow_from_py") as mock_load:
        mock_load.return_value = mock_workflow
        
        result = services.show_workflow_service(workflow_path)
        
        assert result["name"] == "test_workflow"
        assert result["total_blocks"] == 0
        assert result["mermaid_diagram"] == "graph TD;"

def test_show_workflow_service_diagram_only(tmp_path):
    """Test workflow display with diagram only."""
    workflow_path = Path(tmp_path) / "test_workflow.py"
    workflow_path.touch()
    
    mock_workflow = MagicMock(spec=Workflow)
    mock_workflow.to_mermaid.return_value = "graph TD;"
    
    with patch("kwargify_core.services.load_workflow_from_py") as mock_load:
        mock_load.return_value = mock_workflow
        
        result = services.show_workflow_service(workflow_path, diagram_only=True)
        
        assert result == {"mermaid_diagram": "graph TD;"}

# ===== Test register_workflow_service =====

def test_register_workflow_service_success(tmp_path):
    """Test successful workflow registration."""
    workflow_path = Path(tmp_path) / "test_workflow.py"
    workflow_path.touch()
    
    expected_result = {
        "workflow_name": "test_workflow",
        "version": 1,
        "message": "Workflow registered successfully"
    }
    
    with patch("kwargify_core.services.WorkflowRegistry") as MockRegistry:
        mock_registry = MockRegistry.return_value
        mock_registry.register.return_value = expected_result
        
        result = services.register_workflow_service(workflow_path, "Test description")
        
        assert result == expected_result
        mock_registry.register.assert_called_once_with(
            str(workflow_path), "Test description"
        )

def test_register_workflow_service_error():
    """Test workflow registration with error."""
    path = Path("test_workflow.py")
    
    with patch("kwargify_core.services.WorkflowRegistry") as MockRegistry:
        mock_registry = MockRegistry.return_value
        mock_registry.register.side_effect = WorkflowRegistryError("Registration failed")
        
        with pytest.raises(services.RegistryServiceError, match="Error registering workflow"):
            services.register_workflow_service(path)

# ===== Test list_workflows_service =====

def test_list_workflows_service_success():
    """Test successful workflow listing."""
    expected_workflows = [
        {"name": "workflow1", "versions": 2},
        {"name": "workflow2", "versions": 1}
    ]
    
    with patch("kwargify_core.services.WorkflowRegistry") as MockRegistry:
        mock_registry = MockRegistry.return_value
        mock_registry.list_workflows.return_value = expected_workflows
        
        result = services.list_workflows_service()
        
        assert result == expected_workflows

def test_list_workflows_service_error():
    """Test workflow listing with error."""
    with patch("kwargify_core.services.WorkflowRegistry") as MockRegistry:
        mock_registry = MockRegistry.return_value
        mock_registry.list_workflows.side_effect = WorkflowRegistryError("Listing failed")
        
        with pytest.raises(services.RegistryServiceError, match="Error listing workflows"):
            services.list_workflows_service()

# ===== Test list_workflow_versions_service =====

def test_list_workflow_versions_service_success():
    """Test successful workflow versions listing."""
    expected_versions = [
        {"version": 1, "created_at": "2025-01-01"},
        {"version": 2, "created_at": "2025-01-02"}
    ]
    
    with patch("kwargify_core.services.WorkflowRegistry") as MockRegistry:
        mock_registry = MockRegistry.return_value
        mock_registry.list_versions.return_value = expected_versions
        
        result = services.list_workflow_versions_service("test_workflow")
        
        assert result == expected_versions
        mock_registry.list_versions.assert_called_once_with("test_workflow")

def test_list_workflow_versions_service_error():
    """Test workflow versions listing with error."""
    with patch("kwargify_core.services.WorkflowRegistry") as MockRegistry:
        mock_registry = MockRegistry.return_value
        mock_registry.list_versions.side_effect = WorkflowRegistryError("Listing failed")
        
        with pytest.raises(services.RegistryServiceError, match="Error listing workflow versions"):
            services.list_workflow_versions_service("test_workflow")

# ===== Test get_workflow_version_details_service =====

def test_get_workflow_version_details_service_success():
    """Test successful workflow version details retrieval."""
    expected_details = {
        "id": "version_id",
        "version": 1,
        "created_at": "2025-01-01"
    }
    
    with patch("kwargify_core.services.WorkflowRegistry") as MockRegistry:
        mock_registry = MockRegistry.return_value
        mock_registry.get_version_details.return_value = expected_details
        
        result = services.get_workflow_version_details_service("test_workflow", version=1)
        
        assert result == expected_details
        mock_registry.get_version_details.assert_called_once_with("test_workflow", 1)

def test_get_workflow_version_details_service_error():
    """Test workflow version details retrieval with error."""
    with patch("kwargify_core.services.WorkflowRegistry") as MockRegistry:
        mock_registry = MockRegistry.return_value
        mock_registry.get_version_details.side_effect = WorkflowRegistryError("Not found")
        
        with pytest.raises(services.RegistryServiceError, match="Error getting workflow version details"):
            services.get_workflow_version_details_service("test_workflow")

# ===== Test list_run_history_service =====

def test_list_run_history_service_success():
    """Test successful run history listing."""
    expected_runs = [
        {"run_id": "run1", "status": "COMPLETED"},
        {"run_id": "run2", "status": "FAILED"}
    ]
    
    with patch("kwargify_core.services.SQLiteLogger") as MockLogger, \
         patch("kwargify_core.services.get_database_name"):
        
        mock_logger = MockLogger.return_value
        mock_logger.list_runs.return_value = expected_runs
        
        result = services.list_run_history_service()
        
        assert result == expected_runs

def test_list_run_history_service_error():
    """Test run history listing with error."""
    with patch("kwargify_core.services.SQLiteLogger") as MockLogger, \
         patch("kwargify_core.services.get_database_name"):
        
        mock_logger = MockLogger.return_value
        mock_logger.list_runs.side_effect = Exception("Database error")
        
        with pytest.raises(services.HistoryError, match="Error accessing run history"):
            services.list_run_history_service()

# ===== Test get_run_details_service =====

def test_get_run_details_service_success():
    """Test successful run details retrieval."""
    expected_details = {
        "run_id": "test_run",
        "status": "COMPLETED",
        "blocks": []
    }
    
    with patch("kwargify_core.services.SQLiteLogger") as MockLogger, \
         patch("kwargify_core.services.get_database_name"):
        
        mock_logger = MockLogger.return_value
        mock_logger.get_run_details.return_value = expected_details
        
        result = services.get_run_details_service("test_run")
        
        assert result == expected_details
        mock_logger.get_run_details.assert_called_once_with("test_run")

def test_get_run_details_service_not_found():
    """Test run details retrieval with non-existent run."""
    with patch("kwargify_core.services.SQLiteLogger") as MockLogger, \
         patch("kwargify_core.services.get_database_name"):
        
        mock_logger = MockLogger.return_value
        mock_logger.get_run_details.return_value = None
        
        with pytest.raises(services.HistoryError, match="Run not found"):
            services.get_run_details_service("nonexistent")