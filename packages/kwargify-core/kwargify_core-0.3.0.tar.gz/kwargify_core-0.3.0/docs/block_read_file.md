# Read File Block

## Overview

The `ReadFileBlock` is a component within the `kwargify-core` project designed to read the content of a specified file. It is typically used in workflows where data needs to be ingested from the file system. This block can handle plain text and markdown files.

## Inputs

This block does not take direct inputs from preceding blocks in a standard workflow data flow. Its primary input is configured through its configuration options.

## Outputs

The `ReadFileBlock` produces the following outputs:

- `content` (str): The full content of the file read, as a single string.
- `filename` (str): The name of the file (e.g., `example.txt`), extracted from the provided path. This is the base name of the file, not the full path.

## Configuration Options

The behavior of the `ReadFileBlock` is controlled by the following configuration parameters:

- **`path`** (str): **Required**. The absolute or relative path to the file that needs to be read.
  - Example: `"./data/input.txt"` or `"/path/to/your/file.md"`
- **`encoding`** (str): _Optional_. The file encoding to use when reading the file.
  - Default value: `"utf-8"`
  - Other common values: `"ascii"`, `"latin-1"`, etc.

## Example Usage

Below is an example of how to configure and use the `ReadFileBlock` within a hypothetical workflow definition (e.g., in a Python script using `kwargify-core`):

```python
from kwargify_core.core.workflow import Workflow
from kwargify_core.blocks.read_file import ReadFileBlock
from kwargify_core.blocks.write_file import WriteFileBlock # Assuming a WriteFileBlock for demonstration

# Define a workflow
my_workflow = Workflow(name="file_processing_example")

# Configure the ReadFileBlock
my_workflow.add_block(
    ReadFileBlock,
    name="read_source_document",
    config={
        "path": "examples/contract.txt",  # Path to the file to be read
        "encoding": "utf-8"              # Optional: specify encoding
    }
)

# Example: Using the output of ReadFileBlock in another block
# This assumes a WriteFileBlock that takes 'content' and 'filename' as inputs
my_workflow.add_block(
    WriteFileBlock,
    name="write_processed_document",
    config={
        "output_path": "examples/processed_contract.txt",
        "content_input": "{{ read_source_document.outputs.content }}", # Referencing output
        "filename_input": "{{ read_source_document.outputs.filename }}" # Referencing output
    },
    dependencies=["read_source_document"]
)

# To run this workflow (simplified):
# my_workflow.run()

# After execution, the 'read_source_document' block would have populated:
# - outputs['content']: with the text from 'examples/contract.txt'
# - outputs['filename']: with 'contract.txt'
```

### Explanation of the Example:

1.  We import the necessary classes, including `Workflow` and `ReadFileBlock`.
2.  A `Workflow` instance named `"file_processing_example"` is created.
3.  The `ReadFileBlock` is added to the workflow with the name `"read_source_document"`.
    - Its `config` dictionary specifies the `path` to the file `"examples/contract.txt"`.
    - The `encoding` is explicitly set to `"utf-8"`, though this is the default.
4.  (Illustrative) A `WriteFileBlock` is added, named `"write_processed_document"`.
    - It is configured to use the `content` and `filename` outputs from the `"read_source_document"` block. This demonstrates how the output of `ReadFileBlock` can be consumed by subsequent blocks in a workflow.
    - The `dependencies` field ensures `read_source_document` runs before `write_processed_document`.

When this workflow runs, the `ReadFileBlock` will attempt to read the file specified by `path`. If successful, its `outputs` dictionary will be populated with the file's content and filename, which can then be used by other blocks in the workflow. If the file is not found or cannot be read (e.g., due to permission issues or incorrect encoding), the block will raise an appropriate error.
