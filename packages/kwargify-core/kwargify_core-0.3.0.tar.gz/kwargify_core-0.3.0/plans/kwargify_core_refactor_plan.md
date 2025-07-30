# `kwargify-core` Refactoring Plan for Programmatic Consumption

**Date:** May 18, 2025
**Author:** Roo (AI Technical Leader)

## 1. Overview

**Goal:**
The primary goal of this refactoring effort is to modify the `kwargify-core` package to include a dedicated **service layer**. This layer will expose the core functionalities of `kwargify-core` in a way that is easily and cleanly consumable by other Python packages. Specifically, this will prepare `kwargify-core` to be used by a future, separate FastAPI application (`kwargify-server`).

This refactor focuses _only_ on changes within the `kwargify-core` package. The development of `kwargify-server` is out of scope for this plan.

**Key Decisions & Principles:**

- **Service Layer (`src/kwargify_core/services.py`)**: A new module will be created to house the core business logic, decoupled from the Command Line Interface (CLI).
- **Absolute Paths**: Functions within the service layer will expect **absolute file paths** as `pathlib.Path` objects for any file/directory arguments.
- **Synchronous Operations**: Service layer functions will be standard synchronous Python functions. The consuming application (e.g., `kwargify-server`) will be responsible for handling asynchronous execution if needed (e.g., via thread pools).
- **CLI Refactoring**: The existing CLI (`src/kwargify_core/cli.py`) will be refactored to use this new service layer. It will be responsible for converting any user-provided relative paths to absolute paths.
- **Error Handling**: The service layer will define and raise custom exceptions for clear error communication. The CLI will catch these and present user-friendly messages.
- **Testing**: Comprehensive unit tests will be written for the new service layer, and existing CLI tests will be updated.
- **No New External Dependencies**: This refactor aims to use existing project dependencies. Pydantic is not a requirement for service function signatures at this stage; standard type hints are sufficient.

## 2. Key Deliverables within `kwargify-core`

### A. Create Service Layer (`src/kwargify_core/services.py`)

**Guidance for Junior Developer:**

- Create a new file: `src/kwargify_core/services.py`.
- Import necessary modules: `Path` from `pathlib`, `Optional`, `List`, `Dict`, `Any`, `Union` from `typing`.
- Import relevant components from `kwargify_core` (e.g., `load_config`, `save_config` from `.config`; `load_workflow_from_py` from `.loader`; `WorkflowRegistry` from `.registry`; `SQLiteLogger`, `get_database_name` from `.logging.sqlite_logger` and `.config`; `Workflow` from `.core.workflow`).
- Your main task is to extract the core logic from `cli.py` functions, remove Typer-specific code (`typer.echo`, `typer.prompt`, `typer.Exit`, `rich.console` usage for direct output), and make it callable as a regular Python function.
- Ensure all file/directory path arguments in service functions are clearly documented to expect absolute `Path` objects.
- Service functions should return Python dictionaries or lists, not print directly to console.
- Raise custom exceptions (defined below) when errors occur.

**A.1. Define Custom Exceptions:**
Create these custom exceptions at the beginning of `src/kwargify_core/services.py`. They should inherit from `Exception`.

```python
# src/kwargify_core/services.py

class ServiceError(Exception):
    """Base class for service layer errors."""
    pass

class ProjectInitError(ServiceError):
    """Error during project initialization."""
    pass

class WorkflowLoadErrorService(ServiceError): # Differentiate from loader.WorkflowLoadError if needed
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

class RegistryServiceError(ServiceError): # Differentiate from registry.WorkflowRegistryError
    """Error interacting with the workflow registry."""
    pass

class HistoryError(ServiceError):
    """Error accessing run history."""
    pass
```

**A.2. Service Functions:**

For each function below, implement the logic as described.

1.  **`init_project_service(project_name: str, db_name: str) -> Dict[str, str]`**

    - **Purpose**: Initializes a Kwargify project by setting project name and database name in `config.toml`.
    - **Core Logic**: Adapt from [`cli.py::init_project()`](src/kwargify_core/cli.py:67). Uses [`load_config()`](src/kwargify_core/config.py:37) and [`save_config()`](src/kwargify_core/config.py:56).
    - **Input**:
      - `project_name: str`: The name of the project.
      - `db_name: str`: The name for the database file.
    - **Return**: `{"message": "Project '...' initialized. Configuration saved."}`
    - **Raises**: `ProjectInitError` if `project_name` or `db_name` is empty/whitespace, or if `save_config` fails.

2.  **`run_workflow_file_service(workflow_path: Path, resume_id: Optional[str] = None, resume_after_block_name: Optional[str] = None) -> Dict[str, Any]`**

    - **Purpose**: Runs a workflow from a given Python file path.
    - **Core Logic**: Adapt from the file-path-based execution part of [`cli.py::run_workflow()`](src/kwargify_core/cli.py:106). Uses [`load_workflow_from_py()`](src/kwargify_core/loader.py:15), `SQLiteLogger`, and `workflow.run()`.
    - **Input**:
      - `workflow_path: Path`: Absolute path to the workflow Python file.
      - `resume_id: Optional[str]`: ID of a previous run to resume from.
      - `resume_after_block_name: Optional[str]`: Name of the block after which to resume (requires `resume_id`).
    - **Return**: `{"run_id": str, "workflow_name": str, "status": str, "message": str, ...other relevant details}`
    - **Raises**:
      - `WorkflowLoadErrorService` if `workflow_path` doesn't exist or is invalid.
      - `WorkflowRunError` if `resume_after_block_name` is given without `resume_id`, if `resume_id` is not found, or if `workflow.run()` fails.
      - `HistoryError` if logger fails to fetch resume details.
    - **Note**: Handle the logic for auto-determining `resume_after_block_name` if only `resume_id` is provided, similar to `cli.py`.

3.  **`run_registered_workflow_service(name: str, version: Optional[int] = None, resume_id: Optional[str] = None, resume_after_block_name: Optional[str] = None) -> Dict[str, Any]`**

    - **Purpose**: Runs a registered workflow by its name and optional version.
    - **Core Logic**: Adapt from the registry-based execution part of [`cli.py::run_workflow()`](src/kwargify_core/cli.py:106). Uses `WorkflowRegistry`, `SQLiteLogger`, [`load_workflow_from_py()`](src/kwargify_core/loader.py:15) (with path from registry), and `workflow.run()`.
    - **Input**:
      - `name: str`: Name of the registered workflow.
      - `version: Optional[int]`: Version of the workflow (defaults to latest).
      - `resume_id: Optional[str]`: ID of a previous run to resume from.
      - `resume_after_block_name: Optional[str]`: Name of the block after which to resume.
    - **Return**: `{"run_id": str, "workflow_name": str, "status": str, "message": str, ...other relevant details}`
    - **Raises**:
      - `RegistryServiceError` if workflow/version not found in registry.
      - `WorkflowLoadErrorService` if registered workflow's source file is not found or invalid.
      - `WorkflowRunError` for issues during `workflow.run()` or resume logic.
      - `HistoryError` if logger fails to fetch resume details.

4.  **`validate_workflow_service(workflow_path: Path) -> Dict[str, Any]`**

    - **Purpose**: Validates a workflow definition from a Python file.
    - **Core Logic**: Adapt from [`cli.py::validate_workflow()`](src/kwargify_core/cli.py:222). Uses [`load_workflow_from_py()`](src/kwargify_core/loader.py:15) and `workflow.topological_sort()`, `workflow.to_mermaid()`.
    - **Input**:
      - `workflow_path: Path`: Absolute path to the workflow Python file.
    - **Return**: `{"is_valid": bool, "name": str, "blocks_count": int, "dependency_flow": str, "mermaid_diagram": str, "errors": Optional[List[str]]}`
    - **Raises**: `WorkflowLoadErrorService` if loading fails. `WorkflowValidationError` if validation checks (cycles, missing deps) fail.

5.  **`show_workflow_service(workflow_path: Path, diagram_only: bool = False) -> Dict[str, Any]`**

    - **Purpose**: Retrieves details or a Mermaid diagram of a workflow.
    - **Core Logic**: Adapt from [`cli.py::show_workflow()`](src/kwargify_core/cli.py:356). Uses [`load_workflow_from_py()`](src/kwargify_core/loader.py:15).
    - **Input**:
      - `workflow_path: Path`: Absolute path to the workflow Python file.
      - `diagram_only: bool`: If true, only returns the Mermaid diagram.
    - **Return**:
      - If `diagram_only`: `{"mermaid_diagram": str}`
      - Else: `{"name": str, "total_blocks": int, "execution_order": List[Dict], "block_details": List[Dict], "mermaid_diagram": str}` (Structure block details clearly).
    - **Raises**: `WorkflowLoadErrorService` if loading fails. `WorkflowShowError` for other issues.

6.  **`register_workflow_service(workflow_path: Path, description: Optional[str] = None) -> Dict[str, Any]`**

    - **Purpose**: Registers a workflow or creates a new version.
    - **Core Logic**: Uses `WorkflowRegistry().register()`.
    - **Input**:
      - `workflow_path: Path`: Absolute path to the workflow Python file.
      - `description: Optional[str]`: Description for the workflow.
    - **Return**: The dictionary returned by `registry.register()` (e.g., `{"workflow_id": ..., "workflow_name": ..., "version": ..., "source_hash": ...}`).
    - **Raises**: `WorkflowLoadErrorService` (if `load_workflow_from_py` within registry fails), `RegistryServiceError` (for other registry operation failures).

7.  **`list_workflows_service() -> List[Dict[str, Any]]`**

    - **Purpose**: Lists all registered workflows.
    - **Core Logic**: Uses `WorkflowRegistry().list_workflows()`.
    - **Return**: A list of dictionaries, each representing a workflow, as returned by `registry.list_workflows()`.
    - **Raises**: `RegistryServiceError`.

8.  **`list_workflow_versions_service(workflow_name: str) -> List[Dict[str, Any]]`**

    - **Purpose**: Lists all versions of a specific registered workflow.
    - **Core Logic**: Uses `WorkflowRegistry().list_versions()`.
    - **Input**:
      - `workflow_name: str`: The name of the workflow.
    - **Return**: A list of dictionaries, each representing a version, as returned by `registry.list_versions()`.
    - **Raises**: `RegistryServiceError` (e.g., if workflow name not found).

9.  **`get_workflow_version_details_service(workflow_name: str, version: Optional[int] = None) -> Dict[str, Any]`**

    - **Purpose**: Gets detailed information about a specific workflow version.
    - **Core Logic**: Uses `WorkflowRegistry().get_version_details()`.
    - **Input**:
      - `workflow_name: str`: The name of the workflow.
      - `version: Optional[int]`: The version number (latest if None).
    - **Return**: A dictionary with version details, as returned by `registry.get_version_details()`.
    - **Raises**: `RegistryServiceError` (e.g., if workflow or version not found).

10. **`list_run_history_service() -> List[Dict[str, Any]]`**

    - **Purpose**: Lists recent workflow runs.
    - **Core Logic**: Adapt from [`cli.py::show_history()`](src/kwargify_core/cli.py:528) (when `run_id` is None). Uses `SQLiteLogger(get_database_name()).list_runs()`.
    - **Return**: A list of dictionaries, each representing a run summary.
    - **Raises**: `HistoryError`.

11. **`get_run_details_service(run_id: str) -> Dict[str, Any]`**
    - **Purpose**: Gets detailed information for a specific workflow run.
    - **Core Logic**: Adapt from [`cli.py::show_history()`](src/kwargify_core/cli.py:528) (when `run_id` is provided). Uses `SQLiteLogger(get_database_name()).get_run_details()`.
    - **Input**:
      - `run_id: str`: The ID of the run.
    - **Return**: A dictionary containing detailed run information, including block executions, inputs, outputs, and errors.
    - **Raises**: `HistoryError` (e.g., if `run_id` not found).

### B. Refactor CLI (`src/kwargify_core/cli.py`)

**Guidance for Junior Developer:**

- Import the newly created service functions from `src.kwargify_core.services`.
- For each Typer command function in `cli.py`:
  1.  **Path Conversion**: If the command takes a file/directory path from the user, convert it to an absolute path _before_ calling the service function. Use `absolute_path = Path(user_provided_path).resolve()`.
  2.  **Call Service Function**: Replace the existing core logic with a call to the appropriate service function, passing the (now absolute) paths and other parameters.
  3.  **Handle Output**: Take the dictionary or list returned by the service function and use `typer.echo` or `rich.console` methods to format and print it to the console in a user-friendly way. This is where the CLI's presentation logic now resides.
  4.  **Error Handling**: Wrap the service function call in a `try...except` block. Catch the specific custom exceptions defined in `services.py` (e.g., `ProjectInitError`, `WorkflowRunError`). For each caught exception, print a user-friendly error message to `typer.echo(..., err=True)` and then `raise typer.Exit(code=1)`.

**Example (Conceptual for `run` command):**

```python
# src/kwargify_core/cli.py
# ... imports ...
from . import services # Assuming services.py is in the same directory for simplicity here
from pathlib import Path

# ...
@app.command("run")
def run_workflow(
    workflow_path_str: Optional[str] = typer.Argument(None, ...), # Keep as str for Typer
    name: Optional[str] = typer.Option(None, ...),
    # ... other CLI args
):
    try:
        if workflow_path_str:
            workflow_abs_path = Path(workflow_path_str).resolve()
            if not workflow_abs_path.exists():
                 typer.echo(f"Error: Workflow file not found at {workflow_abs_path}", err=True)
                 raise typer.Exit(code=1)
            result = services.run_workflow_file_service(
                workflow_path=workflow_abs_path,
                # ... pass other relevant args ...
            )
        elif name:
            result = services.run_registered_workflow_service(
                name=name,
                # ... pass other relevant args ...
            )
        else:
            typer.echo("Error: Must provide either a workflow path or --name.", err=True)
            raise typer.Exit(code=1)

        # Process and print 'result' dictionary using typer.echo / rich
        typer.echo(f"Run ID: {result.get('run_id')}")
        typer.echo(f"Status: {result.get('status')}")
        # ... more detailed output based on result structure ...

    except services.WorkflowLoadErrorService as e:
        typer.echo(f"Error loading workflow: {e}", err=True)
        raise typer.Exit(code=1)
    except services.WorkflowRunError as e:
        typer.echo(f"Error running workflow: {e}", err=True)
        raise typer.Exit(code=1)
    # ... other specific service exceptions ...
    except services.ServiceError as e: # Catch-all for other service errors
        typer.echo(f"An unexpected service error occurred: {e}", err=True)
        raise typer.Exit(code=1)
    except Exception as e:
        typer.echo(f"An unexpected CLI error occurred: {e}", err=True)
        raise typer.Exit(code=1)
```

### C. Testing

**Guidance for Junior Developer:**

- Use `pytest` for all tests.
- Remember to mock dependencies appropriately to isolate the unit under test.

**C.1. Service Layer Tests (`src/kwargify_core/tests/test_services.py`)**

- Create a new file: `src/kwargify_core/tests/test_services.py`.
- For _each function_ in `services.py`:
  - **Happy Path Test(s)**: Test successful execution with valid inputs. Assert the returned dictionary/list has the correct structure and values.
    - Use `tmp_path` fixture from `pytest` to create temporary files/directories for testing functions that interact with the file system (via mocks or real interactions if simple).
    - Ensure you pass absolute paths to the service functions during tests.
  - **Error/Exception Test(s)**: Test scenarios where specific custom exceptions (e.g., `WorkflowRunError`) are expected to be raised. Use `pytest.raises` for this.
    - Example: `with pytest.raises(services.ProjectInitError): services.init_project_service("", "test.db")`
  - **Mocking**:
    - Use `unittest.mock.patch` to mock calls to other parts of `kwargify-core` (e.g., `config.load_config`, `registry.WorkflowRegistry().register`, `loader.load_workflow_from_py`, `SQLiteLogger` methods).
    - Mock file system operations (`Path.exists`, `open`) if they are not part of what you are testing directly (e.g., if `load_workflow_from_py` is mocked, you might not need to mock `open` for that test).
    - Configure mocks to return specific values or raise exceptions to simulate different conditions.

**C.2. CLI Tests (`tests/test_cli.py`)**

- **Review Existing Tests**: Go through each test in [`tests/test_cli.py`](tests/test_cli.py:1).
- **Update Mocks**:
  - Many existing mocks might be targeting functions that are now part of the internal logic of service functions (e.g., direct calls to `SQLiteLogger` from `cli.py`).
  - Change these mocks to target the service layer functions instead (e.g., `@patch('kwargify_core.services.run_workflow_file_service')`).
  - The mocked service function should be configured to return a sample dictionary (simulating successful execution) or raise a service exception (simulating an error).
- **Test CLI Output**: Verify that the CLI correctly formats the output based on what the (mocked) service function returns.
- **Test CLI Error Handling**: Verify that the CLI catches service exceptions and prints the correct error messages and exits with the right code.
- **Test Path Handling**: Add tests to ensure CLI commands correctly handle user-provided relative and absolute paths, and that the service layer is called with an absolute path.

## 3. Conceptual Mermaid Diagram

```mermaid
graph TD
    subgraph kwargify-server (Separate Package - Future)
        FastAPIApp[FastAPI App]
    end

    subgraph kwargify-core (This Project)
        ServiceLayer[Service Layer (src/kwargify_core/services.py)\n- Expects absolute paths\n- Synchronous operations]
        CLILayer[CLI (src/kwargify_core/cli.py)\n- Converts relative paths to absolute]

        CoreComponents[Core Logic\n(loader.py, registry.py, core/*, config.py, logging/*)]
        Database[(SQLite Database)]
    end

    FastAPIApp -->|Imports & Calls with absolute paths| ServiceLayer;
    CLILayer -->|Calls with absolute paths| ServiceLayer;

    ServiceLayer -->|Uses| CoreComponents;
    CoreComponents -->|Accesses| Database;
```

## 4. Final Note for Developer

- Adhere to existing coding standards, including Ruff for formatting and linting, and comprehensive type hints for all functions and methods.
- Commit changes incrementally with clear messages.
- Run tests frequently (`pytest`) to catch issues early.
- If anything is unclear in this plan or in the existing codebase, please ask for clarification.

This plan should provide a solid foundation for the refactoring work.
