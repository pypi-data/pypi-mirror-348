# Kwargify Core Services (`src/kwargify_core/services.py`)

## I. Module Overview

The `services.py` module acts as the primary service layer for the Kwargify core functionality. It provides a high-level API for interacting with various aspects of Kwargify, including project initialization, workflow execution (from file or registry), workflow validation, workflow registration, and accessing run history. This layer abstracts the underlying complexities of components like workflow loading, registry management, configuration, and logging.

## II. Custom Exceptions

This module defines a set of custom exceptions to handle specific error conditions within the service layer. All custom service exceptions inherit from the base `ServiceError` class.

- **`ServiceError(Exception)`**:
  - **Description**: Base class for all service layer errors.
- **`ProjectInitError(ServiceError)`**:
  - **Description**: Raised during errors in project initialization, such as invalid project/database names or failures in saving configuration.
- **`WorkflowLoadErrorService(ServiceError)`**:
  - **Description**: Raised when there's an error loading a workflow within the service context, often due to file not found or issues with the workflow definition itself.
- **`WorkflowRunError(ServiceError)`**:
  - **Description**: Raised during errors encountered while executing a workflow, including issues with resume logic or underlying block execution failures.
- **`WorkflowValidationError(ServiceError)`**:
  - **Description**: Raised when a workflow fails validation checks, such as cyclic dependencies or missing block dependencies.
- **`WorkflowShowError(ServiceError)`**:
  - **Description**: Raised when an error occurs while trying to display workflow details or generate its diagram.
- **`RegistryServiceError(ServiceError)`**:
  - **Description**: Raised for errors related to interactions with the `WorkflowRegistry`, such as failing to find a workflow, register a new one, or list existing workflows/versions.
- **`HistoryError(ServiceError)`**:
  - **Description**: Raised when there are errors accessing workflow run history, like a run ID not being found or issues with the logger.

## III. Service Functions

### 1. `init_project_service(project_name: str, db_name: str) -> Dict[str, str]`

- **Purpose**: Initializes a Kwargify project by setting up its configuration, including the project name and the database name.
- **Parameters**:
  - `project_name (str)`: The name to be assigned to the Kwargify project. Cannot be empty or whitespace.
  - `db_name (str)`: The name for the SQLite database file (e.g., "kwargify.db"). Cannot be empty or whitespace.
- **Returns**:
  - `Dict[str, str]`: A dictionary containing a success message, e.g., `{"message": "Project 'MyProject' initialized. Configuration saved."}`.
- **Raises**:
  - [`ProjectInitError`](src/kwargify_core/services.py:18): If `project_name` or `db_name` is empty/whitespace, or if saving the configuration via [`save_config()`](src/kwargify_core/config.py:0) fails.
- **Key Interactions**:
  - Uses [`load_config()`](src/kwargify_core/config.py:0) and [`save_config()`](src/kwargify_core/config.py:0) from [`src/kwargify_core/config.py`](src/kwargify_core/config.py).

### 2. `run_workflow_file_service(workflow_path: Path, resume_id: Optional[str] = None, resume_after_block_name: Optional[str] = None) -> Dict[str, Any]`

- **Purpose**: Executes a workflow defined in a specified Python file. Supports resuming a previous run.
- **Parameters**:
  - `workflow_path (Path)`: Absolute path to the Python file containing the workflow definition.
  - `resume_id (Optional[str])`: The ID of a previous workflow run to resume from.
  - `resume_after_block_name (Optional[str])`: The name of the block after which the workflow should resume. If `resume_id` is provided and this is `None`, it attempts to resume after the last successfully completed block of the `resume_id` run.
- **Returns**:
  - `Dict[str, Any]`: A dictionary containing run details, e.g., `{"run_id": "...", "workflow_name": "...", "status": "COMPLETED", "message": "Workflow completed successfully"}`.
- **Raises**:
  - [`WorkflowLoadErrorService`](src/kwargify_core/services.py:22): If the `workflow_path` does not exist or if [`load_workflow_from_py()`](src/kwargify_core/loader.py:0) fails.
  - [`WorkflowRunError`](src/kwargify_core/services.py:26): If `resume_after_block_name` is given without `resume_id`, if the `resume_id` run cannot be found, if no completed blocks are found for resumption, or if any other error occurs during [`workflow.run()`](src/kwargify_core/core/workflow.py:0).
  - [`HistoryError`](src/kwargify_core/services.py:42): If fetching details for `resume_id` from the logger fails.
- **Key Interactions**:
  - Uses [`SQLiteLogger`](src/kwargify_core/logging/sqlite_logger.py:0) for fetching resume details.
  - Uses [`load_workflow_from_py()`](src/kwargify_core/loader.py:0) from [`src/kwargify_core/loader.py`](src/kwargify_core/loader.py).
  - Calls the `run()` method on the loaded [`Workflow`](src/kwargify_core/core/workflow.py:0) instance.
  - Uses [`get_database_name()`](src/kwargify_core/config.py:0) from [`src/kwargify_core/config.py`](src/kwargify_core/config.py).

### 3. `run_registered_workflow_service(name: str, version: Optional[int] = None, resume_id: Optional[str] = None, resume_after_block_name: Optional[str] = None) -> Dict[str, Any]`

- **Purpose**: Executes a workflow that has been previously registered in the Kwargify registry, by its name and an optional version. Supports resuming a previous run.
- **Parameters**:
  - `name (str)`: The name of the registered workflow.
  - `version (Optional[int])`: The specific version of the workflow to run. If `None`, the latest version is used.
  - `resume_id (Optional[str])`: The ID of a previous workflow run to resume from.
  - `resume_after_block_name (Optional[str])`: The name of the block after which the workflow should resume. Auto-determines if `resume_id` is provided and this is `None`.
- **Returns**:
  - `Dict[str, Any]`: A dictionary containing run details, similar to `run_workflow_file_service`.
- **Raises**:
  - [`RegistryServiceError`](src/kwargify_core/services.py:38): If the workflow name/version is not found in the registry via [`registry.get_version_details()`](src/kwargify_core/registry.py:0).
  - [`WorkflowLoadErrorService`](src/kwargify_core/services.py:22): If the source file path obtained from the registry does not exist or if [`load_workflow_from_py()`](src/kwargify_core/loader.py:0) fails.
  - [`WorkflowRunError`](src/kwargify_core/services.py:26): Similar conditions as `run_workflow_file_service` regarding resume logic or general workflow execution failures.
  - [`HistoryError`](src/kwargify_core/services.py:42): If fetching details for `resume_id` from the logger fails.
- **Key Interactions**:
  - Uses [`WorkflowRegistry`](src/kwargify_core/registry.py:0) to fetch workflow details.
  - Uses [`SQLiteLogger`](src/kwargify_core/logging/sqlite_logger.py:0) for resume details.
  - Uses [`load_workflow_from_py()`](src/kwargify_core/loader.py:0).
  - Calls `run()` on the loaded [`Workflow`](src/kwargify_core/core/workflow.py:0) instance, passing `workflow_version_id`.
  - Uses [`get_database_name()`](src/kwargify_core/config.py:0).

### 4. `validate_workflow_service(workflow_path: Path) -> Dict[str, Any]`

- **Purpose**: Validates a workflow definition from a Python file without executing it. Checks for issues like cyclic dependencies and missing dependencies.
- **Parameters**:
  - `workflow_path (Path)`: Absolute path to the Python file containing the workflow definition.
- **Returns**:
  - `Dict[str, Any]`: A dictionary containing validation results.
    - On success: `{"is_valid": True, "name": "...", "blocks_count": ..., "dependency_flow": "blockA >> [blockB, blockC] >> blockD", "mermaid_diagram": "...", "errors": None}`.
    - On failure: `{"is_valid": False, "name": None, ..., "errors": ["Error message..."]}`.
- **Raises**:
  - [`WorkflowLoadErrorService`](src/kwargify_core/services.py:22): If [`load_workflow_from_py()`](src/kwargify_core/loader.py:0) fails.
  - [`WorkflowValidationError`](src/kwargify_core/services.py:30): If validation logic (e.g., cycle detection, dependency layer building) fails internally, or if specific validation rules (like missing dependencies) are violated.
- **Key Interactions**:
  - Uses [`load_workflow_from_py()`](src/kwargify_core/loader.py:0).
  - Calls [`workflow.topological_sort()`](src/kwargify_core/core/workflow.py:0) and [`workflow.to_mermaid()`](src/kwargify_core/core/workflow.py:0) on the [`Workflow`](src/kwargify_core/core/workflow.py:0) instance.
  - Implements logic to check for missing dependencies among blocks and to build a layer-based representation of the dependency flow.

### 5. `show_workflow_service(workflow_path: Path, diagram_only: bool = False) -> Dict[str, Any]`

- **Purpose**: Retrieves detailed information about a workflow from a Python file, including its structure, execution order, and optionally, just its Mermaid diagram.
- **Parameters**:
  - `workflow_path (Path)`: Absolute path to the Python file containing the workflow definition.
  - `diagram_only (bool)`: If `True`, returns only the Mermaid diagram string. Defaults to `False`.
- **Returns**:
  - `Dict[str, Any]`:
    - If `diagram_only` is `True`: `{"mermaid_diagram": "..."}`.
    - If `diagram_only` is `False`: A dictionary with comprehensive details like `{"name": "...", "total_blocks": ..., "execution_order": [...], "block_details": [...], "mermaid_diagram": "..."}`.
      - `execution_order`: List of blocks with their order and dependencies.
      - `block_details`: List of blocks with their name, config, and input mappings.
- **Raises**:
  - [`WorkflowLoadErrorService`](src/kwargify_core/services.py:22): If [`load_workflow_from_py()`](src/kwargify_core/loader.py:0) fails.
  - [`WorkflowShowError`](src/kwargify_core/services.py:34): For any other errors during the process of gathering workflow details.
- **Key Interactions**:
  - Uses [`load_workflow_from_py()`](src/kwargify_core/loader.py:0).
  - Calls [`workflow.topological_sort()`](src/kwargify_core/core/workflow.py:0) and [`workflow.to_mermaid()`](src/kwargify_core/core/workflow.py:0).
  - Iterates through sorted blocks to extract details like dependencies, config, and input mappings.

### 6. `register_workflow_service(workflow_path: Path, description: Optional[str] = None) -> Dict[str, Any]`

- **Purpose**: Registers a workflow defined in a Python file with the Kwargify registry. If the workflow (by name) already exists, this creates a new version.
- **Parameters**:
  - `workflow_path (Path)`: Absolute path to the Python file containing the workflow definition.
  - `description (Optional[str])`: An optional description for this workflow version.
- **Returns**:
  - `Dict[str, Any]`: A dictionary containing the result of the registration, typically including details like workflow ID, version number, and name. This structure is determined by [`registry.register()`](src/kwargify_core/registry.py:0).
- **Raises**:
  - [`WorkflowLoadErrorService`](src/kwargify_core/services.py:22): If an error occurs during the initial loading/parsing of the workflow file by the registry's internal mechanisms (which also use `load_workflow_from_py`).
  - [`RegistryServiceError`](src/kwargify_core/services.py:38): If the [`registry.register()`](src/kwargify_core/registry.py:0) operation fails for other reasons (e.g., database issues, invalid workflow structure for registration).
- **Key Interactions**:
  - Uses [`WorkflowRegistry().register()`](src/kwargify_core/registry.py:0).

### 7. `list_workflows_service() -> List[Dict[str, Any]]`

- **Purpose**: Lists all unique workflows registered in the Kwargify registry.
- **Returns**:
  - `List[Dict[str, Any]]`: A list of dictionaries, where each dictionary represents a registered workflow and contains details like its name, latest version, and description. Structure determined by [`registry.list_workflows()`](src/kwargify_core/registry.py:0).
- **Raises**:
  - [`RegistryServiceError`](src/kwargify_core/services.py:38): If [`registry.list_workflows()`](src/kwargify_core/registry.py:0) fails.
- **Key Interactions**:
  - Uses [`WorkflowRegistry().list_workflows()`](src/kwargify_core/registry.py:0).

### 8. `list_workflow_versions_service(workflow_name: str) -> List[Dict[str, Any]]`

- **Purpose**: Lists all registered versions for a specific workflow.
- **Parameters**:
  - `workflow_name (str)`: The name of the workflow for which to list versions.
- **Returns**:
  - `List[Dict[str, Any]]`: A list of dictionaries, each representing a version of the specified workflow, including details like version number, registration date, and description. Structure determined by [`registry.list_versions()`](src/kwargify_core/registry.py:0).
- **Raises**:
  - [`RegistryServiceError`](src/kwargify_core/services.py:38): If the workflow `workflow_name` is not found or if [`registry.list_versions()`](src/kwargify_core/registry.py:0) fails.
- **Key Interactions**:
  - Uses [`WorkflowRegistry().list_versions()`](src/kwargify_core/registry.py:0).

### 9. `get_workflow_version_details_service(workflow_name: str, version: Optional[int] = None) -> Dict[str, Any]`

- **Purpose**: Retrieves detailed information about a specific version of a registered workflow.
- **Parameters**:
  - `workflow_name (str)`: The name of the workflow.
  - `version (Optional[int])`: The specific version number. If `None`, details for the latest version are fetched.
- **Returns**:
  - `Dict[str, Any]`: A dictionary containing detailed information about the workflow version, such as its ID, name, version number, description, source path, and registration date. Structure determined by [`registry.get_version_details()`](src/kwargify_core/registry.py:0).
- **Raises**:
  - [`RegistryServiceError`](src/kwargify_core/services.py:38): If the specified workflow name or version is not found, or if [`registry.get_version_details()`](src/kwargify_core/registry.py:0) fails.
- **Key Interactions**:
  - Uses [`WorkflowRegistry().get_version_details()`](src/kwargify_core/registry.py:0).

### 10. `list_run_history_service() -> List[Dict[str, Any]]`

- **Purpose**: Lists a summary of recent workflow runs recorded by the logger.
- **Returns**:
  - `List[Dict[str, Any]]`: A list of dictionaries, each summarizing a workflow run (e.g., run ID, workflow name, start time, status). Structure determined by [`logger.list_runs()`](src/kwargify_core/logging/sqlite_logger.py:0).
- **Raises**:
  - [`HistoryError`](src/kwargify_core/services.py:42): If [`logger.list_runs()`](src/kwargify_core/logging/sqlite_logger.py:0) fails.
- **Key Interactions**:
  - Uses [`SQLiteLogger(get_database_name()).list_runs()`](src/kwargify_core/logging/sqlite_logger.py:0).
  - Uses [`get_database_name()`](src/kwargify_core/config.py:0).

### 11. `get_run_details_service(run_id: str) -> Dict[str, Any]`

- **Purpose**: Retrieves detailed information for a specific workflow run, identified by its run ID.
- **Parameters**:
  - `run_id (str)`: The unique ID of the workflow run.
- **Returns**:
  - `Dict[str, Any]`: A dictionary containing comprehensive details about the run, including workflow name, status, start/end times, parameters, and block-level execution details. Structure determined by [`logger.get_run_details()`](src/kwargify_core/logging/sqlite_logger.py:0).
- **Raises**:
  - [`HistoryError`](src/kwargify_core/services.py:42): If the `run_id` is not found by [`logger.get_run_details()`](src/kwargify_core/logging/sqlite_logger.py:0) or if the operation fails.
- **Key Interactions**:
  - Uses [`SQLiteLogger(get_database_name()).get_run_details()`](src/kwargify_core/logging/sqlite_logger.py:0).
  - Uses [`get_database_name()`](src/kwargify_core/config.py:0).
