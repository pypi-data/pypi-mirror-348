# Workflow Registry

## Overview

The Workflow Registry in `kwargify-core` provides a centralized system for managing and versioning workflows. It allows users to register workflows defined in Python files, track their different versions, and retrieve information about them. This is crucial for maintaining a history of workflow changes, ensuring reproducibility, and managing complex data processing pipelines.

The registry uses an SQLite database (managed via `SQLiteLogger`) to store metadata about workflows, including their definitions, source file paths, content hashes, and version history.

## Key Classes and Functions

### `WorkflowRegistry`

This is the primary class responsible for all registry operations.

- **Initialization**:

  ```python
  from kwargify_core.registry import WorkflowRegistry

  # Initializes with a default database path (from config)
  registry = WorkflowRegistry()

  # Or specify a custom database path
  # registry = WorkflowRegistry(db_path="path/to/your/workflows.db")
  ```

### `WorkflowRegistryError`

A custom exception class raised when workflow registry operations fail.

```python
from kwargify_core.registry import WorkflowRegistryError

try:
    # Some registry operation
    pass
except WorkflowRegistryError as e:
    print(f"Registry operation failed: {e}")
```

## Registering Workflows

Workflows are registered from their Python definition files. When a workflow is registered, the registry:

1.  Loads the workflow using `load_workflow_from_py`.
2.  Calculates a SHA-256 hash of the source file's content.
3.  Serializes the workflow's structure (name, blocks, configurations, dependencies) into a JSON snapshot.
4.  Generates a Mermaid diagram representation of the workflow.
5.  Stores this information in the database.

If a workflow with the same name already exists, a new version is created. Otherwise, a new entry for the workflow is created with version 1.

### `register(workflow_path: str, description: Optional[str] = None) -> Dict[str, Any]`

- **`workflow_path`**: The path to the Python file containing the workflow definition.
- **`description`**: An optional textual description for the workflow (primarily used when registering a workflow for the first time).
- **Returns**: A dictionary containing `workflow_id`, `workflow_name`, `version` number, and `source_hash`.

**Example:**

```python
# Assuming 'my_workflow.py' defines a kwargify Workflow
# and 'registry' is an instance of WorkflowRegistry

try:
    registration_details = registry.register(
        workflow_path="examples/simple_workflow.py",
        description="A simple example workflow for demonstration."
    )
    print(f"Registered Workflow: ID={registration_details['workflow_id']}, "
          f"Name='{registration_details['workflow_name']}', "
          f"Version={registration_details['version']}")
except WorkflowRegistryError as e:
    print(f"Failed to register workflow: {e}")
```

## Retrieving Workflow Information

### Listing All Registered Workflows

#### `list_workflows() -> List[Dict[str, Any]]`

Returns a list of all registered workflows, including their ID, name, description, creation date, latest version number, and the source path of the latest version.

**Example:**

```python
all_workflows = registry.list_workflows()
for wf in all_workflows:
    print(f"ID: {wf['id']}, Name: {wf['name']}, Latest Version: {wf['latest_version']}, "
          f"Source: {wf['source_path']}")
```

### Listing Versions of a Specific Workflow

#### `list_versions(workflow_name: str) -> List[Dict[str, Any]]`

Returns a list of all versions for a given workflow name, ordered by version number in descending order. Each entry includes version ID, version number, source path, source hash, and creation date.

- **`workflow_name`**: The name of the workflow.

**Example:**

```python
try:
    versions = registry.list_versions(workflow_name="SimpleWorkflow") # Use the actual name from your workflow file
    for v in versions:
        print(f"Version ID: {v['id']}, Version: {v['version']}, "
              f"Source: {v['source_path']}, Hash: {v['source_hash']}")
except WorkflowRegistryError as e:
    print(f"Error listing versions: {e}") # e.g., if workflow_name not found
```

### Getting Details of a Specific Workflow Version

#### `get_version_details(workflow_name: str, version: Optional[int] = None) -> Dict[str, Any]`

Retrieves detailed information for a specific version of a workflow. If `version` is not provided, it fetches the latest version.

- **`workflow_name`**: The name of the workflow.
- **`version`**: The specific version number (optional).
- **Returns**: A dictionary containing the version ID, version number, the JSON definition snapshot, the Mermaid diagram, source path, source hash, and creation date.

**Example:**

```python
try:
    # Get latest version details
    latest_details = registry.get_version_details(workflow_name="SimpleWorkflow")
    print(f"Latest Version ({latest_details['version']}) Details for SimpleWorkflow:")
    # print(json.dumps(latest_details['definition_snapshot'], indent=2))
    # print(latest_details['mermaid_diagram'])

    # Get specific version details (e.g., version 1)
    # version_1_details = registry.get_version_details(workflow_name="SimpleWorkflow", version=1)
    # print(f"\nVersion 1 Details for SimpleWorkflow:")
    # print(json.dumps(version_1_details['definition_snapshot'], indent=2))
except WorkflowRegistryError as e:
    print(f"Error getting version details: {e}")
```

## Version Management

- **Versioning**: Each time a workflow is registered using the `register` method, if a workflow with that name already exists, its version number is incremented. This allows tracking changes to a workflow over time.
- **Source Hashing**: The SHA-256 hash of the workflow's source file (`source_hash`) is stored with each version. This can be used to verify if the source file for a particular version has been modified since registration.
- **Definition Snapshot**: A JSON representation (`definition_snapshot`) of the workflow's structure (blocks, connections, configurations) is stored for each version. This allows for inspecting the exact structure of a workflow at a specific version, independent of the source file.
- **Namespaces**: Workflows are primarily namespaced by their `name` attribute, as defined within the workflow Python file. The registry does not currently implement explicit, separate namespacing beyond the workflow name itself.

## Internal Helper Methods

The `WorkflowRegistry` class also uses internal helper methods:

- `_calculate_file_hash(file_path: str) -> str`: Calculates the SHA-256 hash of a file.
- `_serialize_workflow(workflow: Workflow) -> str`: Converts a `Workflow` object into a JSON string representation for storage.

These methods support the public API by handling the underlying mechanics of hashing and serialization.
