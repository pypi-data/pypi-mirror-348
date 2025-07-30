# Workflow Loading in kwargify-core

This document describes how workflows are defined and loaded within the `kwargify-core` project.

## Overview

In `kwargify-core`, workflows are defined as Python modules. Each workflow module must provide a specific entry point for the system to discover and load the workflow configuration. The primary mechanism for loading these workflows is handled by the `loader` module, specifically the [`load_workflow_from_py`](../src/kwargify_core/loader.py:15) function.

## Workflow Definition Format

Workflows are defined in standard Python files (`.py`). There isn't a separate YAML or JSON configuration file for defining the workflow structure itself; instead, the workflow is constructed programmatically within the Python file.

A key requirement for a Python file to be recognized as a valid workflow definition is that it **must contain a function named `get_workflow()`**. This function is expected to return an instance of the [`Workflow`](../src/kwargify_core/core/workflow.py) class (specifically, `kwargify_core.core.Workflow`).

### Example Workflow Definition (`my_workflow.py`):

```python
from kwargify_core.core.workflow import Workflow
from kwargify_core.core.block import Block

# Define custom blocks or import existing ones
class MyCustomBlock(Block):
    def execute(self, **kwargs):
        print(f"Executing MyCustomBlock with: {kwargs}")
        return {"output_data": "result from custom block"}

def get_workflow() -> Workflow:
    """
    Defines and returns the workflow.
    """
    workflow = Workflow(name="My Sample Workflow", description="A simple example workflow.")

    # Define blocks
    block1 = MyCustomBlock(name="custom_step_1")
    # Add more blocks and configure their dependencies as needed

    workflow.add_block(block1)
    # workflow.add_dependency(block_dependent, block_dependency, {"input_arg": "output_arg"})

    return workflow
```

## How the Loader Parses Workflow Files

The [`load_workflow_from_py(file_path: str)`](../src/kwargify_core/loader.py:15) function in [`src/kwargify_core/loader.py`](../src/kwargify_core/loader.py:1) is responsible for loading a workflow from a given Python file path. The process involves the following steps:

1.  **Path Validation**:

    - The function first converts the input `file_path` string to a `pathlib.Path` object and resolves it to an absolute path.
    - It checks if the file exists. If not, a [`WorkflowLoadError`](../src/kwargify_core/loader.py:10) is raised.
    - It verifies that the file has a `.py` extension. If not, a [`WorkflowLoadError`](../src/kwargify_core/loader.py:10) is raised.

2.  **Dynamic Module Loading**:

    - A unique module name is generated based on the file's stem (e.g., `workflow_module_my_workflow` for `my_workflow.py`).
    - `importlib.util.spec_from_file_location()` is used to create a module specification from the file path.
    - If a spec cannot be created, a [`WorkflowLoadError`](../src/kwargify_core/loader.py:10) is raised.
    - `importlib.util.module_from_spec()` creates a new module object from the specification.
    - `spec.loader.exec_module(module)` executes the module's code in the newly created module object's namespace. This is where the Python file is actually "run" and its contents (functions, classes) become available.

3.  **Workflow Retrieval**:

    - After the module is loaded, the function checks if the module has an attribute named `get_workflow` using `hasattr(module, 'get_workflow')`.
    - If the `get_workflow` function is not found, a [`WorkflowLoadError`](../src/kwargify_core/loader.py:10) is raised.
    - If found, `module.get_workflow()` is called to obtain the workflow object.

4.  **Workflow Validation**:

    - The object returned by `get_workflow()` is checked to ensure it is an instance of the [`Workflow`](../src/kwargify_core/core/workflow.py) class.
    - If the type is incorrect, a [`WorkflowLoadError`](../src/kwargify_core/loader.py:10) is raised.

5.  **Return Workflow**:
    - If all checks pass, the loaded and validated [`Workflow`](../src/kwargify_core/core/workflow.py) object is returned.

## Key Classes and Functions

- **[`load_workflow_from_py(file_path: str) -> Workflow`](../src/kwargify_core/loader.py:15)**: The main function responsible for loading a workflow from a Python file.
- **[`Workflow`](../src/kwargify_core/core/workflow.py)**: The core class representing a workflow. The `get_workflow()` function in a workflow definition file must return an instance of this class.
- **[`WorkflowLoadError(Exception)`](../src/kwargify_core/loader.py:10)**: A custom exception class raised for various errors encountered during the workflow loading process.

## Error Handling

The workflow loading process includes robust error handling:

- **File Not Found**: If the specified Python file does not exist, [`WorkflowLoadError`](../src/kwargify_core/loader.py:10) is raised with the message `File not found: {file_path}`.
- **Incorrect File Type**: If the file is not a Python file (i.e., does not end with `.py`), [`WorkflowLoadError`](../src/kwargify_core/loader.py:10) is raised with the message `File must be a Python file (.py): {file_path}`.
- **Module Loading Issues**: If `importlib.util` fails to create a module specification or load the module, a [`WorkflowLoadError`](../src/kwargify_core/loader.py:10) is raised (e.g., `Could not load module spec from {file_path}`).
- **Missing `get_workflow` Function**: If the loaded module does not contain a function named `get_workflow`, [`WorkflowLoadError`](../src/kwargify_core/loader.py:10) is raised with the message `Module {file_path} must contain a function named 'get_workflow'`.
- **Incorrect Workflow Object Type**: If the `get_workflow()` function does not return an instance of the [`Workflow`](../src/kwargify_core/core/workflow.py) class, [`WorkflowLoadError`](../src/kwargify_core/loader.py:10) is raised with the message `get_workflow() must return a Workflow object, got {type(workflow)}`.
- **General Exceptions**: Any other exceptions that occur during the loading process (e.g., `ImportError` within the workflow file itself, `AttributeError` if `get_workflow` is not callable) are caught and re-raised as a [`WorkflowLoadError`](../src/kwargify_core/loader.py:10), wrapping the original exception message for context.

## Example of Loading a Workflow

Assuming you have the `my_workflow.py` file defined as in the example above, you can load it as follows:

```python
from kwargify_core.loader import load_workflow_from_py, WorkflowLoadError

workflow_file = "path/to/your/my_workflow.py" # Replace with the actual path

try:
    loaded_workflow = load_workflow_from_py(workflow_file)
    print(f"Successfully loaded workflow: {loaded_workflow.name}")
    # Now you can execute the workflow or inspect its blocks
    # loaded_workflow.execute_sequentially(initial_data={})
except WorkflowLoadError as e:
    print(f"Error loading workflow: {e}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")

```

This example demonstrates how to use the [`load_workflow_from_py`](../src/kwargify_core/loader.py:15) function and handle potential [`WorkflowLoadError`](../src/kwargify_core/loader.py:10) exceptions.
