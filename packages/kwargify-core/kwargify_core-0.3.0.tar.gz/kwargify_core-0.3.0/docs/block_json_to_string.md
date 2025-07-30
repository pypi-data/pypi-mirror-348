# JSON to String Block

## Overview

The `JsonToStringBlock` is a component within the `kwargify-core` framework responsible for converting a Python object (such as a dictionary, list, or other JSON-serializable types) into its JSON string representation. This block is useful when you need to serialize data into a JSON format for storage, transmission, or further processing by other systems or blocks that expect JSON strings.

## Inputs

The block expects a single input:

- **`data`**:
  - **Type**: `Any` (e.g., `dict`, `list`, `str`, `int`, `float`, `bool`, `None`)
  - **Description**: The Python object that needs to be converted into a JSON string. The object must be serializable by Python's `json` module.
  - **Required**: Yes

## Outputs

The block produces a single output:

- **`json_string`**:
  - **Type**: `str`
  - **Description**: The JSON string representation of the input `data`.

## Configuration Options

The `JsonToStringBlock` supports the following configuration options to customize the JSON output:

- **`indent`**:

  - **Type**: `int`
  - **Optional**: Yes
  - **Default**: `None` (output is a compact JSON string with no extra whitespace)
  - **Description**: If specified, this integer value defines the number of spaces to use for indentation in the output JSON string, making it more human-readable. For example, an `indent` value of `2` or `4` is common.

- **`ensure_ascii`**:
  - **Type**: `bool`
  - **Optional**: Yes
  - **Default**: `True`
  - **Description**: If `ensure_ascii` is `True` (the default), the output is guaranteed to have all incoming non-ASCII characters escaped. If `ensure_ascii` is `False`, these characters will be output as-is.

## Example Usage

Below is an example of how to configure and use the `JsonToStringBlock` within a hypothetical workflow definition.

```python
from kwargify_core.core.workflow import Workflow
from kwargify_core.blocks.json_to_string import JsonToStringBlock

# Define a workflow
my_workflow = Workflow(name="data_serialization_workflow")

# Sample Python dictionary
sample_data = {
    "name": "Example Workflow",
    "version": 1.0,
    "details": {
        "author": "John Doe",
        "tags": ["serialization", "json", "example"]
    },
    "unicode_char": "é" # Example with a non-ASCII character
}

# Add and configure the JsonToStringBlock
my_workflow.add_block(
    JsonToStringBlock,
    name="serialize_data_to_json",
    inputs={"data": sample_data},
    config={
        "indent": 2,          # Indent the JSON output with 2 spaces
        "ensure_ascii": False # Allow non-ASCII characters (like 'é')
    }
)

# To execute the workflow (simplified for example purposes):
# In a real scenario, you would run the workflow and access outputs.
# For instance, if this block was part of a larger flow,
# its output 'json_string' could be used by a subsequent block.

# Simulate running the block to see the output
# (In a real workflow, you'd call my_workflow.run())
json_converter = JsonToStringBlock(
    name="serialize_data_to_json_standalone",
    inputs={"data": sample_data},
    config={
        "indent": 2,
        "ensure_ascii": False
    }
)
json_converter.run()
output_json_string = json_converter.outputs.get("json_string")

print("---- Configured JsonToStringBlock ----")
print(f"Input data: {sample_data}")
print(f"Output JSON string:\n{output_json_string}")

# Example with default configuration (compact, ASCII escaped)
default_json_converter = JsonToStringBlock(
    name="serialize_data_to_json_default",
    inputs={"data": sample_data}
    # No config provided, so defaults (indent=None, ensure_ascii=True) are used
)
default_json_converter.run()
default_output_json_string = default_json_converter.outputs.get("json_string")

print("\n---- Default JsonToStringBlock ----")
print(f"Input data: {sample_data}")
print(f"Output JSON string (default config):\n{default_output_json_string}")

```

### Expected Output from the Example:

```
---- Configured JsonToStringBlock ----
Input data: {'name': 'Example Workflow', 'version': 1.0, 'details': {'author': 'John Doe', 'tags': ['serialization', 'json', 'example']}, 'unicode_char': 'é'}
Output JSON string:
{
  "name": "Example Workflow",
  "version": 1.0,
  "details": {
    "author": "John Doe",
    "tags": [
      "serialization",
      "json",
      "example"
    ]
  },
  "unicode_char": "é"
}

---- Default JsonToStringBlock ----
Input data: {'name': 'Example Workflow', 'version': 1.0, 'details': {'author': 'John Doe', 'tags': ['serialization', 'json', 'example']}, 'unicode_char': 'é'}
Output JSON string (default config):
{"name": "Example Workflow", "version": 1.0, "details": {"author": "John Doe", "tags": ["serialization", "json", "example"]}, "unicode_char": "\u00e9"}
```

This example demonstrates how the `indent` and `ensure_ascii` configurations affect the final JSON string output. The first part shows a pretty-printed JSON with non-ASCII characters preserved, while the second part shows the default compact output with non-ASCII characters escaped.
