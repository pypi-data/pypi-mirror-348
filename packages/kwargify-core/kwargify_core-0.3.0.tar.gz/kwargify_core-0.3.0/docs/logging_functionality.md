# Logging Functionality in kwargify-core

## Overview

Logging is a critical component of `kwargify-core`, providing a detailed record of workflow and block execution. This allows for monitoring, debugging, and auditing of processes. The primary logging mechanism in `kwargify-core` is the `SQLiteLogger`, which stores log data in a structured SQLite database.

This document details the `SQLiteLogger`, its data storage, configuration, usage, and methods for interacting with log data.

## `SQLiteLogger`

The [`SQLiteLogger`](../src/kwargify_core/logging/sqlite_logger.py:9) class is responsible for capturing and storing all relevant information during the execution of workflows and their constituent blocks. It uses a SQLite database, making the log data portable and easily queryable.

### Purpose

The main purposes of the `SQLiteLogger` are:

- To provide a persistent and structured record of every workflow run.
- To track the execution status (e.g., STARTED, COMPLETED, FAILED, SKIPPED) of individual blocks within a workflow.
- To store inputs, outputs, and error messages for each block execution, aiding in debugging and analysis.
- To capture custom log messages (INFO, DEBUG, WARNING, ERROR) generated during block execution.
- To maintain a version history of workflows, linking runs to specific workflow definitions.

### Database Structure

The `SQLiteLogger` initializes and manages a SQLite database file (specified by `db_path` during instantiation). It creates the following tables to store logging information:

1.  **`workflows`**: Registers unique workflows.

    - `id` (INTEGER, PRIMARY KEY, AUTOINCREMENT): Unique identifier for the workflow.
    - `name` (TEXT, UNIQUE, NOT NULL): The name of the workflow.
    - `description` (TEXT): An optional description of the workflow.
    - `created_at` (DATETIME, DEFAULT CURRENT_TIMESTAMP): Timestamp of when the workflow was first registered.

2.  **`workflow_versions`**: Tracks different versions of a workflow.

    - `id` (INTEGER, PRIMARY KEY, AUTOINCREMENT): Unique identifier for the workflow version.
    - `workflow_id` (INTEGER, NOT NULL): Foreign key referencing `workflows.id`.
    - `version_number` (INTEGER, NOT NULL): Version number for this workflow definition.
    - `definition_snapshot` (TEXT, NOT NULL): A snapshot (e.g., JSON) of the workflow definition for this version.
    - `mermaid_diagram` (TEXT): An optional Mermaid diagram representing the workflow structure.
    - `source_path` (TEXT, NOT NULL): The file system path to the workflow definition source.
    - `source_hash` (TEXT, NOT NULL): A hash of the workflow definition source file for integrity checking.
    - `created_at` (DATETIME, DEFAULT CURRENT_TIMESTAMP): Timestamp of when this version was created.
    - UNIQUE constraint on (`workflow_id`, `version_number`).

3.  **`run_summary`**: Stores a high-level summary for each workflow execution.

    - `run_id` (TEXT, PRIMARY KEY): Unique identifier for this specific workflow run.
    - `workflow_name` (TEXT, NOT NULL): Name of the workflow being run.
    - `workflow_version_id` (INTEGER): Foreign key referencing `workflow_versions.id`, if the run is associated with a registered version.
    - `start_time` (TIMESTAMP, NOT NULL): Timestamp when the workflow run started.
    - `end_time` (TIMESTAMP): Timestamp when the workflow run ended.
    - `status` (TEXT, NOT NULL): Final status of the run (e.g., "STARTED", "COMPLETED", "FAILED", "PARTIAL").
    - `resumed_from_run_id` (TEXT): If the run was resumed, this field stores the `run_id` of the original run.

4.  **`run_details`**: Stores detailed information about each block execution within a workflow run.

    - `block_execution_id` (TEXT, PRIMARY KEY): Unique identifier for this specific block execution instance.
    - `run_id` (TEXT, NOT NULL): Foreign key referencing `run_summary.run_id`.
    - `block_name` (TEXT, NOT NULL): Name of the block that was executed.
    - `start_time` (TIMESTAMP, NOT NULL): Timestamp when the block execution started.
    - `end_time` (TIMESTAMP): Timestamp when the block execution ended.
    - `status` (TEXT, NOT NULL): Status of the block execution (e.g., "STARTED", "COMPLETED", "FAILED", "SKIPPED").
    - `inputs` (TEXT): JSON string representing the input parameters for the block.
    - `outputs` (TEXT): JSON string representing the output data from the block.
    - `error_message` (TEXT): Error message if the block execution failed.
    - `retries_attempted` (INTEGER, DEFAULT 0): Number of retries attempted for this block.

5.  **`run_logs`**: Stores custom log messages generated during block executions.
    - `log_id` (INTEGER, PRIMARY KEY, AUTOINCREMENT): Unique identifier for the log entry.
    - `block_execution_id` (TEXT, NOT NULL): Foreign key referencing `run_details.block_execution_id`.
    - `run_id` (TEXT, NOT NULL): Foreign key referencing `run_summary.run_id`.
    - `timestamp` (TIMESTAMP, NOT NULL): Timestamp when the log message was generated.
    - `level` (TEXT, NOT NULL): Log level (e.g., "INFO", "DEBUG", "WARNING", "ERROR").
    - `message` (TEXT, NOT NULL): The actual log message.

### Configuration and Usage

To use the `SQLiteLogger`, an instance must be created by providing a path to the SQLite database file:

```python
from kwargify_core.logging import SQLiteLogger

# Configure the logger with a database path
logger = SQLiteLogger(db_path="path/to/kwargify_logs.db")
```

This `logger` instance is then typically passed to or made accessible by the workflow execution engine and individual blocks. The engine and blocks use the logger's methods to record events.

### Key Logging Methods

The `SQLiteLogger` provides several methods to log different aspects of workflow and block execution:

- **`log_run_start(run_id: str, workflow_name: str, resumed_from_run_id: Optional[str] = None, workflow_version_id: Optional[int] = None)`**:
  Logs the beginning of a workflow run. Records the `run_id`, `workflow_name`, start time, and initial "STARTED" status. Optionally logs `resumed_from_run_id` if the run is a resumption and `workflow_version_id` if linked to a registered version.

- **`log_run_end(run_id: str, status: str)`**:
  Logs the completion or failure of a workflow run. Updates the `run_summary` table with the end time and final `status` (e.g., "COMPLETED", "FAILED").

- **`log_block_start(block_execution_id: str, run_id: str, block_name: str, inputs: Dict)`**:
  Logs the start of an individual block's execution. Records the `block_execution_id`, `run_id`, `block_name`, start time, initial "STARTED" status, and a JSON representation of the block's `inputs`.

- **`log_block_end(block_execution_id: str, status: str, outputs: Optional[Dict] = None, error_message: Optional[str] = None, retries_attempted: int = 0)`**:
  Logs the end of a block's execution. Updates the `run_details` table with the end time, final `status`, a JSON representation of `outputs` (if successful), an `error_message` (if failed), and the number of `retries_attempted`.

- **`log_block_skipped(block_execution_id: str, run_id: str, block_name: str, outputs: Dict)`**:
  Logs when a block's execution is skipped, typically during a workflow resume operation where the block's previous output is reused. Records the block as "SKIPPED" along with its pre-computed `outputs`.

- **`log_message(block_execution_id: str, run_id: str, level: str, message: str)`**:
  Logs a custom message from within a block's execution. This is useful for detailed debugging or informational messages. Records the `level` (e.g., "INFO", "ERROR") and the `message` text, linking it to the specific `block_execution_id` and `run_id`.

### Retrieving and Querying Log Data

The `SQLiteLogger` also provides methods to retrieve and query the stored log data:

- **`get_run_outputs(run_id: str) -> Dict[str, Dict]`**:
  Retrieves the outputs of all successfully completed blocks for a given `run_id`. Returns a dictionary mapping block names to their output data.

- **`get_block_status(run_id: str, block_name: str) -> Optional[str]`**:
  Fetches the most recent execution status of a specific `block_name` within a given `run_id`.

- **`list_runs(limit: int = 50) -> List[Dict]`**:
  Lists recent workflow runs, ordered by start time (descending). Returns a list of dictionaries, each containing `run_id`, `workflow_name`, `start_time`, `end_time`, and `status`. The `limit` parameter controls the maximum number of runs returned.

- **`get_run_details(run_id: str) -> Optional[Dict]`**:
  Provides a comprehensive summary of a specific `run_id`. This includes the overall run information (workflow name, start/end times, status) and a list of all block executions within that run, detailing each block's name, start/end times, status, inputs, outputs, error messages, and retries.

Since the log data is stored in a SQLite database, users can also connect to the `db_path` directly using any SQLite client or library for custom queries and advanced analysis beyond the methods provided by `SQLiteLogger`.

## Other Logging Mechanisms

Currently, [`SQLiteLogger`](../src/kwargify_core/logging/sqlite_logger.py:9) is the primary and most comprehensive logging mechanism provided by `kwargify-core`. While standard Python logging (e.g., the `logging` module) might be used internally by some components or for console output, `SQLiteLogger` is the designated interface for persistent, structured logging of workflow and block execution details.
