# Core Workflow Engine

The Core Workflow Engine in `kwargify-core` is responsible for orchestrating the execution of a series of interconnected processing units called "Blocks." It manages the dependencies between these blocks, ensures they are run in the correct order, handles inputs and outputs, and provides logging and error management capabilities. The central component of this engine is the `Workflow` class.

## Overview of the `Workflow` Class

The [`Workflow`](../src/kwargify_core/core/workflow.py:8) class represents a Directed Acyclic Graph (DAG) of [`Block`](../src/kwargify_core/core/block.py:1) instances. Its primary role is to:

- **Define a sequence of operations:** By adding blocks and specifying their dependencies, a `Workflow` defines a complex data processing pipeline.
- **Orchestrate execution:** It determines the correct order of execution for blocks based on their dependencies (using a topological sort).
- **Manage data flow:** It facilitates the passing of outputs from one block to the inputs of another.
- **Handle errors and retries:** It provides mechanisms for retrying failed blocks and logging the execution status.
- **Support resumability:** Workflows can be resumed from a specific point if a previous run was interrupted.
- **Log execution details:** It integrates with a logging system (e.g., [`SQLiteLogger`](../src/kwargify_core/logging/sqlite_logger.py:1)) to record the lifecycle and results of workflow and block executions.

## Defining and Constructing a Workflow

A workflow is constructed by instantiating the `Workflow` class and then adding `Block` instances to it.

### Initialization

A `Workflow` object is initialized as follows:

```python
from kwargify_core.core.workflow import Workflow

# Initialize a new workflow
# Default max_retries for blocks can be set here
wf = Workflow(default_max_retries=2)

# The workflow is assigned a unique run_id upon initialization
print(f"Workflow Run ID: {wf.run_id}")

# By default, it uses a SQLiteLogger and a default name
print(f"Workflow Name: {wf.name}")
print(f"Logger: {wf.logger}")
```

### Adding Blocks

Blocks are added to the workflow using the [`add_block()`](../src/kwargify_core/core/workflow.py:34) method:

```python
from kwargify_core.core.block import Block

# Assume BlockA and BlockB are custom Block implementations
class BlockA(Block):
    def run_logic(self):
        self.outputs['data_a'] = "Output from Block A"
        print("Block A executed")

class BlockB(Block):
    def run_logic(self):
        input_from_a = self.inputs.get('input_b')
        self.outputs['data_b'] = f"Output from Block B, using: {input_from_a}"
        print(f"Block B executed with input: {input_from_a}")

block_a = BlockA(name="BlockA")
block_b = BlockB(name="BlockB")

wf.add_block(block_a)
wf.add_block(block_b)
```

### Defining Dependencies

Dependencies between blocks define the order of execution. A block will only run after all its dependencies have successfully completed. Dependencies are typically defined within the `Block` itself when it's instantiated, by passing other `Block` instances to its `dependencies` parameter.

The `Workflow` class uses these defined dependencies to perform a topological sort.

Additionally, explicit input mapping can define dependencies. If `block_b`'s `input_map` specifies that it takes an output from `block_a`, `block_a` implicitly becomes a dependency of `block_b`.

```python
# Example of defining dependency via input_map (conceptual)
# (Actual input_map is set on the block instance)
# block_b.input_map = {'input_b': (block_a, 'data_a')}
# This implies block_a must run before block_b.
```

The `Workflow`'s [`topological_sort()`](../src/kwargify_core/core/workflow.py:175) method handles resolving the execution order based on these direct dependencies and any implied by `input_map`.

## Workflow Execution Process

The [`run()`](../src/kwargify_core/core/workflow.py:39) method is the entry point for executing the workflow.

### 1. Topological Sort

Before execution, the workflow performs a [`topological_sort()`](../src/kwargify_core/core/workflow.py:175) of its blocks. This ensures that blocks are executed in an order that respects their dependencies. If a circular dependency is detected, a `ValueError` is raised.

### 2. Resume Capability

The `run` method supports resuming a workflow from a previous, partially completed run. This is useful for long-running workflows or recovering from transient failures.
To resume, `resume_from_run_id` (the ID of the previous run) and `resume_after_block_name` (the name of the last successfully completed block in the previous run) must be provided.
The workflow will:

- Fetch outputs from the specified previous run using the logger.
- Validate that all blocks up to and including `resume_after_block_name` were `COMPLETED`.
- Skip these blocks in the current run, using their previously logged outputs.
- Continue execution from the block immediately following `resume_after_block_name`.

### 3. Sequential Execution

Blocks are executed sequentially according to the topologically sorted order. (Parallel execution is not explicitly implemented in the base `Workflow` class but could be a feature of specialized block runners or workflow managers built on top of this core).

### 4. Block Execution Lifecycle

For each block in the sorted list (unless skipped due to resume):
a. **Log Block Start:** The logger records the start of the block execution, including its inputs.
b. **Collect Inputs:** The block calls [`collect_inputs_from_dependencies()`](../src/kwargify_core/core/block.py) to gather necessary inputs from its direct dependencies.
c. **Input Mapping:** If the block has an `input_map` defined, it wires outputs from specified source blocks to its own inputs.
d. **Run with Retries:** The block's [`run()`](../src/kwargify_core/core/block.py) method (which internally calls `run_logic`) is invoked.
_ If the block execution fails, it will be retried up to `block.max_retries` or `workflow.default_max_retries`.
_ A simple delay (`time.sleep(1)`) is introduced between retries.
e. **Log Block End:** The logger records the end of the block execution, its final status (`COMPLETED` or `FAILED`), its outputs, any exception if it failed, and the number of retries attempted.
f. **Error Handling:** If a block ultimately fails after all retry attempts, the exception is re-raised, and the overall workflow run is marked as `FAILED`.

### 5. Workflow Logging

- [`log_run_start()`](../src/kwargify_core/logging/sqlite_logger.py): Called at the beginning of the workflow `run` method.
- [`log_run_end()`](../src/kwargify_core/logging/sqlite_logger.py): Called when the workflow completes (either all blocks succeed or an error occurs), recording the final status (`COMPLETED` or `FAILED`).

## Key Methods and Properties of `Workflow`

- **`__init__(self, default_max_retries: int = 1)`**:

  - Initializes the workflow.
  - `default_max_retries`: Sets the default number of retries for blocks that don't specify their own.
  - `self.blocks: List[Block]`: A list to store blocks added to the workflow.
  - `self.name: str`: Name of the workflow (defaults to "DefaultWorkflow").
  - `self.logger: SQLiteLogger`: An instance of the logger, configured with the database name from `get_database_name()`.
  - `self.run_id: str`: A unique UUID hex string identifying this particular execution instance of the workflow.

- **`add_block(self, block: Block) -> None`**:

  - Adds a `Block` instance to the workflow's list of blocks if not already present.

- **`run(self, resume_from_run_id: Optional[str] = None, resume_after_block_name: Optional[str] = None, workflow_version_id: Optional[int] = None) -> None`**:

  - Executes all blocks in the workflow in topological order.
  - `resume_from_run_id`: ID of a previous run to resume from.
  - `resume_after_block_name`: Name of the block after which to resume.
  - `workflow_version_id`: Optional ID if this workflow run corresponds to a registered version.
  - Handles logging, retries, and error propagation.

- **`topological_sort(self) -> List[Block]`**:

  - Performs a topological sort on the blocks based on their `dependencies`.
  - Returns a list of blocks in the order they should be executed.
  - Raises a `ValueError` if a circular dependency is detected.

- **`to_mermaid(self) -> str`**:
  - Generates a string representation of the workflow in Mermaid graph syntax. This is useful for visualizing the workflow structure and dependencies.

### Accessing Block Outputs

The `Workflow` class itself does not have a dedicated `get_block_output` method. Block outputs are managed as follows:

1.  **During Execution:** After a block runs successfully, its outputs are stored in its `block.outputs` dictionary. Subsequent blocks that depend on it can access these outputs, typically via the `input_map` mechanism or by directly accessing `dependency.outputs`.
2.  **After Execution:**
    - The `block.outputs` attribute of each block instance will contain its final outputs.
    - The logger (e.g., `SQLiteLogger`) stores the outputs of each block execution. You can query the logger using the `run_id` and block name to retrieve historical outputs. For example, `logger.get_run_outputs(run_id)` can fetch all outputs for a given run.

## Workflow Inputs and Outputs Management

### Workflow Inputs

- **Initial Inputs:** The overall workflow doesn't have a single, explicit "input" dictionary in the same way individual blocks do. Inputs for the "entry-point" blocks (those with no dependencies within the workflow) must be set on those block instances _before_ the workflow's `run()` method is called. This can be done by directly setting their `inputs` attribute or by configuring them with parameters that define how they acquire their initial data (e.g., a `ReadFileBlock` might take a file path as a configuration parameter).
- **Dynamic Inputs (Inter-block):** As the workflow executes, outputs from completed blocks become available as inputs to subsequent dependent blocks. This data flow is managed by:
  - The `block.collect_inputs_from_dependencies()` method.
  - The `block.input_map` attribute, which allows fine-grained mapping of specific outputs from source blocks to specific inputs of target blocks.

### Workflow Outputs

- **Final Outputs:** Similar to inputs, the workflow doesn't have a single aggregated "output" dictionary. The results of the workflow are the collective outputs of its constituent blocks, particularly the "terminal" blocks (those not depended upon by any other block in the workflow).
- **Accessing Outputs:** After a workflow run, the outputs of any specific block can be accessed via `block_instance.outputs`.
- **Logged Outputs:** All block outputs are logged by the `SQLiteLogger`, providing a persistent record. These can be retrieved using methods like `logger.get_run_outputs(run_id)`.

## Lifecycle of a Workflow

1.  **Definition & Construction:**

    - A `Workflow` instance is created.
    - `Block` instances are created and configured.
    - Blocks are added to the workflow using `add_block()`. Dependencies are implicitly or explicitly defined.

2.  **Preparation for Execution:**

    - The `run()` method is called.
    - A unique `run_id` is already associated with the workflow instance.
    - The logger is notified of the run start (`log_run_start`).
    - Blocks are topologically sorted.
    - Resume logic is handled if `resume_from_run_id` is provided.

3.  **Execution:**

    - Blocks are iterated through in topological order.
    - For each block:
      - It's skipped if resuming and already completed in the previous run.
      - Inputs are collected/mapped.
      - `log_block_start` is called.
      - The block's `run()` method is executed (with retries if configured).
      - `log_block_end` is called with status, outputs, and any error.
      - If a block fails permanently, the exception propagates, and the workflow moves to the "Failed" state.

4.  **Completion:**

    - If all blocks execute successfully, the workflow run is marked `COMPLETED`.
    - The logger is notified of the run end (`log_run_end` with status `COMPLETED`).

5.  **Failure:**

    - If any block fails after retries, or if an error occurs during workflow orchestration (e.g., circular dependency):
      - The exception is typically raised.
      - The workflow run is marked `FAILED`.
      - The logger is notified of the run end (`log_run_end` with status `FAILED`).

6.  **Post-Execution:**
    - Outputs of individual blocks are available in their `outputs` attribute.
    - All execution details (status, inputs, outputs, errors, timings) are persisted by the logger for review and auditing.

## Examples of Defining and Running a Simple Workflow

### Example 1: Simple Sequential Workflow

```python
import time
from kwargify_core.core.workflow import Workflow
from kwargify_core.core.block import Block
from kwargify_core.config import set_database_name

# Configure a database for logging (optional, defaults to kwargify_runs.db)
set_database_name("my_workflow_runs.db")

# Define custom blocks
class ReadDataBlock(Block):
    def __init__(self, name: str, data_source: str, **kwargs):
        super().__init__(name, **kwargs)
        self.data_source = data_source

    def run_logic(self):
        print(f"Reading data from: {self.data_source}")
        time.sleep(0.1) # Simulate I/O
        self.outputs["raw_data"] = f"Content from {self.data_source}"

class ProcessDataBlock(Block):
    def run_logic(self):
        raw_data = self.inputs.get("raw_data_input")
        if raw_data is None:
            raise ValueError("Input 'raw_data_input' not found for ProcessDataBlock")
        print(f"Processing data: {raw_data}")
        time.sleep(0.2) # Simulate processing
        self.outputs["processed_data"] = raw_data.upper()

class WriteReportBlock(Block):
    def run_logic(self):
        processed_data = self.inputs.get("final_data")
        if processed_data is None:
            raise ValueError("Input 'final_data' not found for WriteReportBlock")
        print(f"Writing report with: {processed_data}")
        time.sleep(0.1) # Simulate I/O
        self.outputs["report_status"] = "SUCCESS"
        self.outputs["report_content"] = f"Report: {processed_data}"


# 1. Create workflow instance
wf = Workflow(name="SimpleETLWorkflow", default_max_retries=0)

# 2. Create block instances
reader = ReadDataBlock(name="DataReader", data_source="file.txt")
processor = ProcessDataBlock(name="DataProcessor")
writer = WriteReportBlock(name="ReportWriter")

# 3. Define dependencies and input/output mapping
# Processor depends on Reader
processor.add_dependency(reader)
processor.input_map = {"raw_data_input": (reader, "raw_data")}

# Writer depends on Processor
writer.add_dependency(processor)
writer.input_map = {"final_data": (processor, "processed_data")}

# 4. Add blocks to the workflow
wf.add_block(reader)
wf.add_block(processor)
wf.add_block(writer)

# 5. Run the workflow
try:
    print(f"Starting workflow: {wf.name} with Run ID: {wf.run_id}")
    wf.run()
    print(f"Workflow {wf.name} completed successfully.")
    print(f"Report Writer outputs: {writer.outputs}")
except Exception as e:
    print(f"Workflow {wf.name} failed: {e}")

# You can inspect the database 'my_workflow_runs.db' for logs.
# Example: Accessing outputs from the logger (conceptual)
# run_outputs = wf.logger.get_run_outputs(wf.run_id)
# print(f"All outputs from logger for run {wf.run_id}: {run_outputs}")
```

This example demonstrates:

- Creating a `Workflow`.
- Defining custom `Block`s.
- Adding blocks to the workflow.
- Defining dependencies explicitly using `add_dependency()` and implicitly via `input_map`.
- Running the workflow and handling potential exceptions.
- Accessing outputs from block instances after the run.

This documentation provides a comprehensive overview of the `kwargify-core` Workflow Engine, its components, and how to use them to build and execute data processing pipelines.
