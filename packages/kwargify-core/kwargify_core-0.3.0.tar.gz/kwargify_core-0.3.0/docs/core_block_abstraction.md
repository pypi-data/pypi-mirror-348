# Core Block Abstraction

The `Block` class, found in [`src/kwargify_core/core/block.py`](../src/kwargify_core/core/block.py:5), serves as the fundamental building block for creating modular and reusable components within the `kwargify-core` system. It defines an abstract base class (ABC) that all custom processing units, or "blocks," must inherit from.

## Overview

The `Block` abstraction provides a standardized interface and lifecycle for individual units of work within a larger workflow. Each block encapsulates a specific piece of logic, takes defined inputs, processes them, and produces outputs. This design promotes modularity, making workflows easier to construct, understand, and maintain.

## Purpose and Role

The primary purpose of the `Block` abstraction is to:

- **Standardize Component Interaction:** Define a common way for different processing units to connect and exchange data.
- **Encapsulate Logic:** Allow complex operations to be broken down into smaller, manageable, and testable units.
- **Enable Reusability:** Create blocks that can be reused across different workflows.
- **Facilitate Workflow Orchestration:** Provide a clear structure for how blocks are executed and how data flows between them.

In the `kwargify-core` system, blocks are the atomic units that form a directed acyclic graph (DAG) representing a workflow. They handle data transformation, external API calls, file operations, or any other discrete task.

## Key Methods and Properties

Concrete block implementations must define or can override the following key methods and properties:

### Properties

- **`name: str`**: A string identifier for the block instance. If not provided during initialization, it defaults to the class name.
- **`config: Dict[str, Any]`**: A dictionary to hold any configuration parameters specific to the block's operation. Initialized as an empty dictionary if not provided.
- **`max_retries: Optional[int]`**: An optional integer specifying the maximum number of times the block's `run` method should be retried in case of failure. (Note: Retry logic is not explicitly implemented in the base `Block` class shown but is a common pattern for such abstractions).
- **`inputs: Dict[str, Any]`**: A dictionary to store the input data for the block. Inputs can be set manually using `set_input()` or collected from dependencies.
- **`outputs: Dict[str, Any]`**: A dictionary where the block stores its results after execution.
- **`dependencies: List["Block"]`**: A list of other `Block` instances that this block depends on. The outputs of these dependencies are typically used as inputs for the current block.
- **`has_run: bool`**: A boolean flag indicating whether the block's `run()` method has been executed.

### Methods

- **`__init__(self, name: str = "", config: Dict[str, Any] = None, max_retries: Optional[int] = None)`**:
  The constructor initializes the block's `name`, `config`, `max_retries`, `inputs`, `outputs`, `dependencies`, and `has_run` status.

- **`add_dependency(self, block: "Block") -> None`**:
  [`src/kwargify_core/core/block.py:27`](../src/kwargify_core/core/block.py:27)
  Declares a dependency on another block. This means the current block will likely consume outputs from the specified dependency.

  ```python
  block_a = MyBlock(name="A")
  block_b = AnotherBlock(name="B")
  block_b.add_dependency(block_a) # block_b depends on block_a
  ```

- **`set_input(self, key: str, value: Any) -> None`**:
  [`src/kwargify_core/core/block.py:31`](../src/kwargify_core/core/block.py:31)
  Allows manually setting a specific input value for the block. This can be used to provide initial data or override data that might come from dependencies.

  ```python
  my_block.set_input("api_key", "your_secret_key")
  my_block.set_input("user_id", 123)
  ```

- **`get_output(self, key: str) -> Any`**:
  [`src/kwargify_core/core/block.py:35`](../src/kwargify_core/core/block.py:35)
  Retrieves a specific output value produced by the block after it has run.

  ```python
  result = my_block.get_output("processed_data")
  ```

- **`collect_inputs_from_dependencies(self) -> None`**:
  [`src/kwargify_core/core/block.py:39`](../src/kwargify_core/core/block.py:39)
  This crucial method gathers outputs from all declared dependencies and merges them into the current block's `inputs` dictionary. If a dependency has not run yet, its `run()` method is called first.

  ```python
  # Assuming block_b depends on block_a
  # block_a produces {"output_a": "value_a"}
  block_b.collect_inputs_from_dependencies()
  # block_b.inputs will now contain {"output_a": "value_a"}
  ```

- **`run(self) -> None` (Abstract Method)**:
  [`src/kwargify_core/core/block.py:48`](../src/kwargify_core/core/block.py:48)
  This is the core logic method that **must be implemented by all concrete subclasses**. It defines the actual processing task of the block. Inside this method, the block should:
  1.  Access its necessary inputs from `self.inputs`.
  2.  Perform its specific operations.
  3.  Store its results in `self.outputs`.
  ```python
  @abstractmethod
  def run(self) -> None:
      """Run the block's logic. Must be implemented by subclasses."""
      raise NotImplementedError("Each block must implement its own `run()` method.")
  ```

## Input and Output Data Handling

- **Inputs:** Blocks receive data through their `inputs` dictionary. This dictionary is populated in two main ways:

  1.  **Manually:** Using the [`set_input(key, value)`](../src/kwargify_core/core/block.py:31) method. This is useful for providing initial parameters or configuration that isn't derived from other blocks.
  2.  **From Dependencies:** The [`collect_inputs_from_dependencies()`](../src/kwargify_core/core/block.py:39) method automatically pulls all key-value pairs from the `outputs` of its dependency blocks and merges them into its own `inputs`. If multiple dependencies produce outputs with the same key, the output from the dependency processed later in the `self.dependencies` list will overwrite earlier ones. Careful naming of output keys or custom merging logic within a block's `run` method might be necessary in such cases.

- **Outputs:** After a block executes its [`run()`](../src/kwargify_core/core/block.py:48) method, it should store any results or data it produces in its `outputs` dictionary. These outputs can then be consumed by other blocks that depend on it or accessed directly after the workflow (or block) execution.
  ```python
  # Inside a custom block's run method
  def run(self):
      input_value = self.inputs.get("data")
      processed_value = input_value * 2
      self.outputs["result"] = processed_value
  ```

## Lifecycle of a Block within a Workflow

The typical lifecycle of a block when executed as part of a workflow (often managed by a workflow orchestrator) is as follows:

1.  **Initialization:** A block instance is created with a `name` and optional `config`.
    ```python
    my_block = CustomBlock(name="Processor", config={"threshold": 0.5})
    ```
2.  **Dependency Declaration:** Dependencies on other blocks are established using [`add_dependency()`](../src/kwargify_core/core/block.py:27).
    ```python
    data_source_block = ReadFileBlock(name="Source")
    my_block.add_dependency(data_source_block)
    ```
3.  **Input Collection (Implicit or Explicit):**
    - Manual inputs can be set via [`set_input()`](../src/kwargify_core/core/block.py:31).
    - When the workflow determines it's time for the block to run, it will typically ensure [`collect_inputs_from_dependencies()`](../src/kwargify_core/core/block.py:39) is called. This method ensures that:
      - Each dependency block is run (if it hasn't run already).
      - The outputs from these dependencies are copied into the current block's `inputs`.
4.  **Execution:** The block's [`run()`](../src/kwargify_core/core/block.py:48) method is called. This is where the block performs its main task using the data in `self.inputs` and populates `self.outputs`.
5.  **Output Consumption:** After execution, the block's `outputs` are available for downstream blocks or for final workflow results. The `has_run` flag is set to `True`.

A workflow orchestrator would typically manage this lifecycle for all blocks in a workflow, respecting the declared dependencies to ensure blocks are run in the correct order.

## Guidance on Creating New Custom Blocks

To create a new custom block, you need to inherit from the `Block` base class and implement the `run()` method.

1.  **Import `Block`:**

    ```python
    from kwargify_core.core.block import Block
    from typing import Any, Dict
    ```

2.  **Define Your Custom Block Class:** Inherit from `Block`.

    ```python
    class MyCustomBlock(Block):
        def __init__(self, name: str = "", config: Dict[str, Any] = None):
            super().__init__(name=name, config=config)
            # Add any custom initialization for your block here
            # For example, setting up a client for an external service
            self.api_key = self.config.get("api_key")
    ```

3.  **Implement the `run()` Method:** This is where your block's unique logic resides.

    - Access inputs from `self.inputs`.
    - Perform processing.
    - Store results in `self.outputs`.

    ```python
    class MyCustomBlock(Block):
        def __init__(self, name: str = "", config: Dict[str, Any] = None):
            super().__init__(name=name, config=config)
            self.greeting_template = self.config.get("greeting", "Hello, {name}!")

        def run(self) -> None:
            # Example: Get 'user_name' from inputs (possibly from a previous block)
            user_name = self.inputs.get("user_name", "World")

            # Process the input
            message = self.greeting_template.format(name=user_name)

            # Store the result in outputs
            self.outputs["greeting_message"] = message
            print(f"Block '{self.name}' executed: {message}") # Optional: for logging/debugging
    ```

4.  **(Optional) Define Expected Inputs/Outputs or Schema:** While not enforced by the base `Block` class directly, it's good practice to document or even validate the expected input keys and types, and the output keys and types your block will produce. This can be done via docstrings or by adding methods like `get_input_schema()` or `validate_inputs()`.

## Example of a Minimal Block Implementation

Here's a very simple block that takes a number as input, multiplies it by a factor defined in its configuration, and outputs the result.

```python
from kwargify_core.core.block import Block
from typing import Any, Dict

class MultiplierBlock(Block):
    def __init__(self, name: str = "", config: Dict[str, Any] = None):
        super().__init__(name=name, config=config)
        # Default factor if not provided in config
        self.factor = self.config.get("factor", 2)

    def run(self) -> None:
        # Get 'number_input' from self.inputs
        # Provide a default value (e.g., 0) if 'number_input' is not found
        input_value = self.inputs.get("number_input", 0)

        if not isinstance(input_value, (int, float)):
            print(f"Warning: Input 'number_input' for block '{self.name}' is not a number. Got: {input_value}")
            self.outputs["multiplied_value"] = None # Or handle error appropriately
            return

        # Perform the multiplication
        result = input_value * self.factor

        # Store the result in self.outputs
        self.outputs["multiplied_value"] = result
        print(f"Block '{self.name}' processed {input_value} * {self.factor} = {result}")

# How to use it (simplified example, not full workflow):
if __name__ == "__main__":
    # Create a block instance with configuration
    multiplier = MultiplierBlock(name="DoubleIt", config={"factor": 2})

    # Set an input manually
    multiplier.set_input("number_input", 10)

    # Run the block
    multiplier.run()

    # Get the output
    output = multiplier.get_output("multiplied_value")
    print(f"Output from '{multiplier.name}': {output}") # Expected: 20

    # Another instance with different config
    tripler = MultiplierBlock(name="TripleIt", config={"factor": 3})
    tripler.set_input("number_input", 5)
    tripler.run()
    output_tripler = tripler.get_output("multiplied_value")
    print(f"Output from '{tripler.name}': {output_tripler}") # Expected: 15
```

This example demonstrates the basic structure: inheriting from `Block`, using `__init__` to handle configuration, and implementing `run` to process inputs and produce outputs.
