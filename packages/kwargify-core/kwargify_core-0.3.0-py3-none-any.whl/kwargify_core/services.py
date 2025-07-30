"""Service layer for Kwargify core functionality."""

from pathlib import Path
from typing import Optional, List, Dict, Any, Union
from datetime import datetime

from .loader import load_workflow_from_py, WorkflowLoadError
from .registry import WorkflowRegistry, WorkflowRegistryError
from .config import load_config, save_config, get_database_name
from .core.workflow import Workflow
from .logging.sqlite_logger import SQLiteLogger

# Custom Exceptions
class ServiceError(Exception):
    """Base class for service layer errors."""
    pass

class ProjectInitError(ServiceError):
    """Error during project initialization."""
    pass

class WorkflowLoadErrorService(ServiceError):
    """Error loading workflow in service context."""
    pass

class WorkflowRunError(ServiceError):
    """Error during workflow execution."""
    pass

class WorkflowValidationError(ServiceError):
    """Error during workflow validation."""
    pass

class WorkflowShowError(ServiceError):
    """Error displaying workflow details."""
    pass

class RegistryServiceError(ServiceError):
    """Error interacting with the workflow registry."""
    pass

class HistoryError(ServiceError):
    """Error accessing run history."""
    pass

def init_project_service(project_name: str, db_name: str) -> Dict[str, str]:
    """Initialize a Kwargify project with the given name and database configuration.
    
    Args:
        project_name: Name of the project
        db_name: Name for the database file
        
    Returns:
        Dict containing success message
        
    Raises:
        ProjectInitError: If project_name/db_name is empty or config save fails
    """
    if not project_name or not project_name.strip():
        raise ProjectInitError("Project name cannot be empty or whitespace")
    if not db_name or not db_name.strip():
        raise ProjectInitError("Database name cannot be empty or whitespace")

    try:
        config = load_config()
        
        if "project" not in config:
            config["project"] = {}
        if "database" not in config:
            config["database"] = {}

        config["project"]["name"] = project_name
        config["database"]["name"] = db_name

        save_config(config)
        return {"message": f"Project '{project_name}' initialized. Configuration saved."}
    except Exception as e:
        raise ProjectInitError(f"Failed to initialize project: {str(e)}")

def run_workflow_file_service(
    workflow_path: Path,
    resume_id: Optional[str] = None,
    resume_after_block_name: Optional[str] = None
) -> Dict[str, Any]:
    """Run a workflow from a Python file.
    
    Args:
        workflow_path: Absolute path to the workflow Python file
        resume_id: Optional ID of previous run to resume from
        resume_after_block_name: Optional name of block after which to resume
        
    Returns:
        Dict containing run details including run_id, workflow_name, status
        
    Raises:
        WorkflowLoadErrorService: If workflow file doesn't exist or is invalid
        WorkflowRunError: If workflow execution fails
        HistoryError: If resume details cannot be fetched
    """
    if not workflow_path.exists():
        raise WorkflowLoadErrorService(f"Workflow file not found: {workflow_path}")

    try:
        logger = SQLiteLogger(get_database_name())
        
        if resume_after_block_name and not resume_id:
            raise WorkflowRunError("Cannot specify resume_after_block_name without resume_id")

        if resume_id and not resume_after_block_name:
            # Auto-determine last successful block
            run_details = logger.get_run_details(resume_id)
            if not run_details:
                raise WorkflowRunError(f"Could not find run with ID: {resume_id}")

            completed_blocks = [block for block in run_details['blocks'] if block['status'] == 'COMPLETED']
            if not completed_blocks:
                raise WorkflowRunError("No successfully completed blocks found in the previous run")

            resume_after_block_name = completed_blocks[-1]['block_name']

        workflow = load_workflow_from_py(str(workflow_path))
        workflow.run(resume_from_run_id=resume_id, resume_after_block_name=resume_after_block_name)

        return {
            "run_id": workflow.run_id,
            "workflow_name": workflow.name,
            "status": "COMPLETED",
            "message": "Workflow completed successfully"
        }
    except WorkflowLoadError as e:
        raise WorkflowLoadErrorService(f"Error loading workflow: {str(e)}")
    except Exception as e:
        raise WorkflowRunError(f"Error running workflow: {str(e)}")

def run_registered_workflow_service(
    name: str,
    version: Optional[int] = None,
    resume_id: Optional[str] = None,
    resume_after_block_name: Optional[str] = None
) -> Dict[str, Any]:
    """Run a registered workflow by name and optional version.
    
    Args:
        name: Name of the registered workflow
        version: Optional version number (defaults to latest)
        resume_id: Optional ID of previous run to resume from
        resume_after_block_name: Optional name of block after which to resume
        
    Returns:
        Dict containing run details including run_id, workflow_name, status
        
    Raises:
        RegistryServiceError: If workflow/version not found in registry
        WorkflowLoadErrorService: If workflow file not found or invalid
        WorkflowRunError: If workflow execution fails
        HistoryError: If resume details cannot be fetched
    """
    try:
        registry = WorkflowRegistry()
        details = registry.get_version_details(name, version)
        workflow_version_id = details["id"]
        workflow_path = Path(details["source_path"])

        if not workflow_path.exists():
            raise WorkflowLoadErrorService(
                f"Source file for workflow '{name}' version {version or 'latest'} "
                f"not found at: {workflow_path}"
            )

        logger = SQLiteLogger(get_database_name())

        if resume_after_block_name and not resume_id:
            raise WorkflowRunError("Cannot specify resume_after_block_name without resume_id")

        if resume_id and not resume_after_block_name:
            # Auto-determine last successful block
            run_details = logger.get_run_details(resume_id)
            if not run_details:
                raise WorkflowRunError(f"Could not find run with ID: {resume_id}")

            completed_blocks = [block for block in run_details['blocks'] if block['status'] == 'COMPLETED']
            if not completed_blocks:
                raise WorkflowRunError("No successfully completed blocks found in the previous run")

            resume_after_block_name = completed_blocks[-1]['block_name']

        workflow = load_workflow_from_py(str(workflow_path))
        workflow.run(
            workflow_version_id=workflow_version_id,
            resume_from_run_id=resume_id,
            resume_after_block_name=resume_after_block_name
        )

        return {
            "run_id": workflow.run_id,
            "workflow_name": workflow.name,
            "status": "COMPLETED",
            "message": f"Workflow '{name}' (Version: {details['version']}) completed successfully"
        }
    except WorkflowRegistryError as e:
        raise RegistryServiceError(f"Error accessing registry: {str(e)}")
    except WorkflowLoadError as e:
        raise WorkflowLoadErrorService(f"Error loading workflow: {str(e)}")
    except Exception as e:
        raise WorkflowRunError(f"Error running workflow: {str(e)}")

def validate_workflow_service(workflow_path: Path) -> Dict[str, Any]:
    """Validate a workflow definition without executing it.
    
    Args:
        workflow_path: Absolute path to the workflow Python file
        
    Returns:
        Dict containing validation results and workflow details
        
    Raises:
        WorkflowLoadErrorService: If workflow file cannot be loaded
        WorkflowValidationError: If validation fails
    """
    try:
        workflow = load_workflow_from_py(str(workflow_path))
        
        # Check for cycles in the dependency graph
        workflow.topological_sort()
        
        # Check if all blocks have their dependencies added to the workflow
        missing_deps = []
        for block in workflow.blocks:
            for dep in block.dependencies:
                if dep not in workflow.blocks:
                    missing_deps.append(f"Block '{block.name}' depends on '{dep.name}' but it's not in the workflow")
        
        if missing_deps:
            raise WorkflowValidationError("Missing dependencies:\n" + "\n".join(f"- {dep}" for dep in missing_deps))

        # Generate layer-based dependency string
        layers = {}
        remaining_blocks = set(workflow.blocks)
        current_layer = 0

        # Build layers based on dependencies
        while remaining_blocks:
            current_layer_blocks = []

            for block in list(remaining_blocks):
                # A block can be in current layer if all its dependencies are in previous layers
                deps_satisfied = True
                for dep in block.dependencies:
                    found_in_prev = False
                    for layer_num in range(current_layer):
                        if dep in layers.get(layer_num, []):
                            found_in_prev = True
                            break
                    if not found_in_prev:
                        deps_satisfied = False
                        break

                if deps_satisfied:
                    current_layer_blocks.append(block)
                    remaining_blocks.remove(block)

            if not current_layer_blocks and remaining_blocks:
                # If we can't add any blocks but still have remaining ones,
                # there might be a cycle that topological_sort didn't catch
                raise WorkflowValidationError("Unable to build dependency layers. Possible cycle detected.")

            # Sort blocks within layer by name for consistent output
            current_layer_blocks.sort(key=lambda b: b.name)
            layers[current_layer] = current_layer_blocks
            current_layer += 1

        # Convert layers to dependency string
        dependency_parts = []
        for i in range(current_layer):
            blocks = layers[i]
            if len(blocks) > 1:
                dependency_parts.append(f"[{', '.join(b.name for b in blocks)}]")
            else:
                dependency_parts.append(blocks[0].name)

        return {
            "is_valid": True,
            "name": workflow.name,
            "blocks_count": len(workflow.blocks),
            "dependency_flow": " >> ".join(dependency_parts),
            "mermaid_diagram": workflow.to_mermaid(),
            "errors": None
        }
    except WorkflowLoadError as e:
        raise WorkflowLoadErrorService(f"Error loading workflow: {str(e)}")
    except WorkflowValidationError as e:
        return {
            "is_valid": False,
            "name": None,
            "blocks_count": None,
            "dependency_flow": None,
            "mermaid_diagram": None,
            "errors": [str(e)]
        }
    except Exception as e:
        raise WorkflowValidationError(f"Error validating workflow: {str(e)}")

def show_workflow_service(workflow_path: Path, diagram_only: bool = False) -> Dict[str, Any]:
    """Get details or Mermaid diagram of a workflow.
    
    Args:
        workflow_path: Absolute path to the workflow Python file
        diagram_only: If True, return only the Mermaid diagram
        
    Returns:
        Dict containing workflow details or just the diagram
        
    Raises:
        WorkflowLoadErrorService: If workflow cannot be loaded
        WorkflowShowError: For other display-related errors
    """
    try:
        workflow = load_workflow_from_py(str(workflow_path))
        
        if diagram_only:
            return {"mermaid_diagram": workflow.to_mermaid()}
        
        sorted_blocks = workflow.topological_sort()
        execution_order = []
        block_details = []
        
        for i, block in enumerate(sorted_blocks, 1):
            deps = [dep.name for dep in block.dependencies]
            execution_order.append({
                "order": i,
                "name": block.name,
                "dependencies": deps
            })
            
            block_detail = {
                "name": block.name,
                "config": getattr(block, 'config', {}),
                "input_map": {}
            }
            
            # Safely handle optional input_map attribute
            input_map = getattr(block, 'input_map', {})
            if input_map:
                for input_key, (source_block, output_key) in input_map.items():
                    block_detail["input_map"][input_key] = {
                        "source_block": source_block.name,
                        "output_key": output_key
                    }
            
            block_details.append(block_detail)
        
        return {
            "name": workflow.name,
            "total_blocks": len(workflow.blocks),
            "execution_order": execution_order,
            "block_details": block_details,
            "mermaid_diagram": workflow.to_mermaid()
        }
    except WorkflowLoadError as e:
        raise WorkflowLoadErrorService(f"Error loading workflow: {str(e)}")
    except Exception as e:
        raise WorkflowShowError(f"Error showing workflow: {str(e)}")

def register_workflow_service(workflow_path: Path, description: Optional[str] = None) -> Dict[str, Any]:
    """Register a workflow or create a new version.
    
    Args:
        workflow_path: Absolute path to the workflow Python file
        description: Optional description for the workflow
        
    Returns:
        Dict containing registration details
        
    Raises:
        WorkflowLoadErrorService: If workflow cannot be loaded
        RegistryServiceError: For registry operation failures
    """
    try:
        registry = WorkflowRegistry()
        result = registry.register(str(workflow_path), description)
        return result
    except WorkflowLoadError as e:
        raise WorkflowLoadErrorService(f"Error loading workflow: {str(e)}")
    except WorkflowRegistryError as e:
        raise RegistryServiceError(f"Error registering workflow: {str(e)}")

def list_workflows_service() -> List[Dict[str, Any]]:
    """List all registered workflows.
    
    Returns:
        List of dictionaries containing workflow details
        
    Raises:
        RegistryServiceError: If registry operations fail
    """
    try:
        registry = WorkflowRegistry()
        return registry.list_workflows()
    except WorkflowRegistryError as e:
        raise RegistryServiceError(f"Error listing workflows: {str(e)}")

def list_workflow_versions_service(workflow_name: str) -> List[Dict[str, Any]]:
    """List all versions of a specific workflow.
    
    Args:
        workflow_name: Name of the workflow
        
    Returns:
        List of dictionaries containing version details
        
    Raises:
        RegistryServiceError: If workflow not found or registry operations fail
    """
    try:
        registry = WorkflowRegistry()
        return registry.list_versions(workflow_name)
    except WorkflowRegistryError as e:
        raise RegistryServiceError(f"Error listing workflow versions: {str(e)}")

def get_workflow_version_details_service(workflow_name: str, version: Optional[int] = None) -> Dict[str, Any]:
    """Get detailed information about a specific workflow version.
    
    Args:
        workflow_name: Name of the workflow
        version: Optional version number (defaults to latest)
        
    Returns:
        Dict containing version details
        
    Raises:
        RegistryServiceError: If workflow/version not found or registry operations fail
    """
    try:
        registry = WorkflowRegistry()
        return registry.get_version_details(workflow_name, version)
    except WorkflowRegistryError as e:
        raise RegistryServiceError(f"Error getting workflow version details: {str(e)}")

def list_run_history_service() -> List[Dict[str, Any]]:
    """List recent workflow runs.
    
    Returns:
        List of dictionaries containing run summaries
        
    Raises:
        HistoryError: If history access fails
    """
    try:
        logger = SQLiteLogger(get_database_name())
        return logger.list_runs()
    except Exception as e:
        raise HistoryError(f"Error accessing run history: {str(e)}")

def get_run_details_service(run_id: str) -> Dict[str, Any]:
    """Get detailed information for a specific workflow run.
    
    Args:
        run_id: ID of the run to fetch details for
        
    Returns:
        Dict containing detailed run information
        
    Raises:
        HistoryError: If run_id not found or history access fails
    """
    try:
        logger = SQLiteLogger(get_database_name())
        run_details = logger.get_run_details(run_id)
        if not run_details:
            raise HistoryError(f"Run not found: {run_id}")
        return run_details
    except Exception as e:
        raise HistoryError(f"Error accessing run details: {str(e)}")