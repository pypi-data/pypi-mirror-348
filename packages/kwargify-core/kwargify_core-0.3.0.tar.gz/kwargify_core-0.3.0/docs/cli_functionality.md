# Kwargify CLI Functionality

## Overview

The Kwargify Command Line Interface (CLI) provides a suite of tools for defining, running, managing, and inspecting workflows built with the `kwargify-core` library. It allows users to interact with their workflows directly from the terminal, streamlining development, execution, and monitoring processes.

The CLI is built using Typer and leverages Rich for enhanced terminal output, providing clear and user-friendly information.

## Prerequisites

- **Python:** A compatible version of Python must be installed.
- **kwargify-core:** The `kwargify-core` package must be installed in your Python environment.
  ```bash
  pip install kwargify-core
  # Or using Poetry
  poetry add kwargify-core
  ```
- **Workflow Files:** Workflows should be defined in Python (`.py`) files, each containing a `get_workflow()` function that returns a `kwargify_core.core.workflow.Workflow` instance.
- **Project Initialization (Optional but Recommended):** For features like workflow registration, versioning, and run history, it's recommended to initialize a Kwargify project using the `kwargify init` command. This creates a `config.toml` file.

## General Usage

The base command for the CLI is `kwargify`.

```bash
kwargify [OPTIONS] COMMAND [ARGS]...
```

To see the list of available commands and global options:

```bash
kwargify --help
```

To get help for a specific command:

```bash
kwargify <COMMAND_NAME> --help
```

### Global Options

- `--version`, `-v`: Show the application version and exit.

## Commands

The Kwargify CLI offers the following commands:

### 1. `init`

Initializes a new Kwargify project or updates an existing configuration. This command creates a `config.toml` file in the current directory (or updates it if it exists) to store project-specific settings, such as the project name and the database file name for logging.

**Usage:**

```bash
kwargify init [OPTIONS]
```

**Options:**

- `--project-name TEXT`: Your project's name. If not provided, you will be prompted.
- `--db-name TEXT`: Database file name (e.g., `my_project_runs.db`). If not provided, you will be prompted.

**Example:**

```bash
kwargify init --project-name "ContractAnalysis" --db-name "contract_analysis.db"
```

Or interactively:

```bash
kwargify init
# Project name: ContractAnalysis
# Database file name (e.g., my_data.db): contract_analysis.db
```

This will create or update `config.toml` with:

```toml
[project]
name = "ContractAnalysis"

[database]
name = "contract_analysis.db"
```

### 2. `run`

Executes a Kwargify workflow. The workflow can be specified either by providing a path to its Python definition file or by its registered name and optional version. This command also supports resuming workflows from a previous run.

**Usage:**

```bash
kwargify run [OPTIONS] [WORKFLOW_PATH]
```

**Arguments:**

- `WORKFLOW_PATH` (Optional): Path to the workflow Python file (`.py`).

**Options:**

- `--name TEXT`, `-n TEXT`: Name of the registered workflow to run.
- `--version INTEGER`, `-v INTEGER`: Version of the registered workflow to run (defaults to the latest if not specified).
- `--resume-id TEXT`: ID of a previous run to resume from. If `--resume-after` is not specified, it resumes after the last successfully completed block of that run.
- `--resume-after TEXT`: Name of the last successfully completed block after which to resume. Requires `--resume-id`.

**Key Features:**

- **Flexible Workflow Source:** Run workflows directly from `.py` files for development and testing, or run registered workflows for production or shared use.
- **Resumability:** If a workflow run is interrupted or fails, it can be resumed from the point of failure (or a specific block), saving computation time and resources. The CLI automatically determines the last successful block if only `--resume-id` is provided.
- **Logging:** Workflow execution is logged to the SQLite database specified in `config.toml`.

**Examples:**

- **Run a workflow from a file:**
  ```bash
  kwargify run examples/simple_workflow.py
  ```
- **Run a registered workflow by name (latest version):**
  ```bash
  kwargify run --name "MyRegisteredWorkflow"
  ```
- **Run a specific version of a registered workflow:**
  ```bash
  kwargify run --name "MyRegisteredWorkflow" --version 2
  ```
- **Resume a workflow run after the last successful block:**
  ```bash
  kwargify run --name "MyRegisteredWorkflow" --resume-id "run_abc123"
  ```
- **Resume a workflow run after a specific block:**
  ```bash
  kwargify run --name "MyRegisteredWorkflow" --resume-id "run_abc123" --resume-after "data_processing_block"
  ```

**Note:** You must provide either `WORKFLOW_PATH` or `--name`. Providing both will result in an error.

### 3. `validate`

Validates the structure and integrity of a workflow defined in a Python file without actually executing it. This is useful for catching errors early in the development process.

**Usage:**

```bash
kwargify validate WORKFLOW_PATH
```

**Arguments:**

- `WORKFLOW_PATH` (Required): Path to the workflow Python file (`.py`).

**Checks Performed:**

- The Python file can be loaded successfully.
- A `get_workflow()` function exists within the file and returns a `Workflow` instance.
- There are no circular dependencies among the blocks in the workflow.
- All dependencies declared by blocks are present in the workflow.

**Output:**

- A success or error message.
- Workflow name and number of blocks.
- A textual representation of the dependency flow (e.g., `block_A >> [block_B, block_C] >> block_D`).
- A Mermaid diagram definition for visualizing the workflow graph.

**Example:**

```bash
kwargify validate examples/contract_analysis_workflow.py
```

### 4. `show`

Displays a summary or a Mermaid diagram definition of a workflow from a Python file. This helps in understanding the workflow's structure and components.

**Usage:**

```bash
kwargify show [OPTIONS] WORKFLOW_PATH
```

**Arguments:**

- `WORKFLOW_PATH` (Required): Path to the workflow Python file (`.py`).

**Options:**

- `--diagram`, `-d`: If set, shows the Mermaid diagram definition instead of the summary.

**Output (Default Summary):**

- Workflow name.
- Total number of blocks.
- Execution order of blocks, including their dependencies.
- Details for each block:
  - Configuration parameters.
  - Input mappings (how block inputs are connected to outputs of other blocks).

**Output (with `--diagram`):**

- A Mermaid diagram definition string that can be used with tools like the Mermaid Live Editor to visualize the workflow.

**Examples:**

- **Show workflow summary:**
  ```bash
  kwargify show examples/simple_workflow.py
  ```
- **Show workflow Mermaid diagram definition:**
  ```bash
  kwargify show --diagram examples/simple_workflow.py
  ```

### 5. `register`

Registers a workflow in the Kwargify registry or creates a new version if the workflow (by name derived from the file) is already registered. The registry stores metadata about workflows, allowing them to be run by name and version.

**Usage:**

```bash
kwargify register [OPTIONS] WORKFLOW_PATH
```

**Arguments:**

- `WORKFLOW_PATH` (Required): Path to the workflow Python file (`.py`).

**Options:**

- `--description TEXT`, `-d TEXT`: An optional description for the workflow version.

**Functionality:**

- Loads the workflow from the specified file.
- Calculates a hash of the source file to detect changes.
- If a workflow with the same name and source hash already exists, it's considered the same version.
- If the name exists but the hash is different, a new version is created.
- Stores workflow metadata (name, version, source path, source hash, description, creation timestamp) in the SQLite database.

**Output:**

- Success message.
- Registered workflow name.
- Assigned version number.
- Source hash of the workflow file.

**Example:**

```bash
kwargify register examples/contract_report_workflow.py --description "Generates reports from contracts"
```

### 6. `list`

Lists all registered workflows or all versions of a specific registered workflow.

**Usage:**

```bash
kwargify list [OPTIONS]
```

**Options:**

- `--name TEXT`, `-n TEXT`: If provided, shows versions for this specific workflow name.

**Output:**

- **Without `--name`:** A table of all registered workflows, including their name, latest version number, description, and creation date of the workflow entry.
- **With `--name`:** A table of all versions for the specified workflow, including version number, creation date, source path, and source hash.

**Examples:**

- **List all registered workflows:**
  ```bash
  kwargify list
  ```
- **List versions of a specific workflow:**
  ```bash
  kwargify list --name "ContractReportWorkflow"
  ```

### 7. `history`

Shows the history of workflow runs or detailed information about a specific past run. This command queries the run log stored in the SQLite database.

**Usage:**

```bash
kwargify history [RUN_ID]
```

**Arguments:**

- `RUN_ID` (Optional): The specific ID of a workflow run to show details for.

**Output:**

- **Without `RUN_ID`:** A table listing recent workflow runs, including their Run ID, Workflow Name, Status (e.g., COMPLETED, FAILED), Start Time, and Duration.
- **With `RUN_ID`:**
  - A summary panel with overall run details (Workflow Name, Run ID, Status, Start Time, End Time).
  - A table of block executions within that run, showing each block's name, status, start time, duration, and retries attempted.
  - Detailed inputs, outputs, and error messages (if any) for each block in the run.

**Examples:**

- **Show recent workflow run history:**
  ```bash
  kwargify history
  ```
- **Show details for a specific run:**
  ```bash
  kwargify history "run_xyz789"
  ```

## Key Features and Capabilities Summary

- **Project Initialization:** Set up project-specific configurations.
- **Workflow Execution:** Run workflows from files or a central registry.
- **Resumable Runs:** Continue interrupted workflows, saving time and resources.
- **Validation:** Check workflow integrity before execution.
- **Visualization & Inspection:** Understand workflow structure with summaries and Mermaid diagrams.
- **Registration & Versioning:** Manage different versions of workflows in a registry.
- **Run History:** Track and review past workflow executions with detailed logs.
- **Rich CLI Output:** User-friendly tables and panels for clear information display.
- **Centralized Logging:** Uses SQLite for persistent storage of workflow metadata and run logs.

This CLI aims to provide a comprehensive toolkit for developers working with `kwargify-core`, facilitating an efficient and manageable workflow development lifecycle.
