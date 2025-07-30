# Write File Block

## Overview

The `WriteFileBlock` is a component within the `kwargify-core` framework responsible for writing provided content to a specified file. It allows for configuring the destination path, encoding, and write mode (overwrite or append).

## Inputs

The block expects the following input:

- `content` (str): The string content that needs to be written to the file. This input is mandatory.

## Outputs

Upon successful execution, the block produces the following output:

- `path` (str): The absolute path of the file to which the content was written.

## Configuration Options

The `WriteFileBlock` can be configured with the following options:

- `path` (str): **Required**. The destination file path where the content will be written.
- `encoding` (str, optional): The character encoding to be used when writing the file. Defaults to `'utf-8'`.
- `mode` (str, optional): The mode in which the file should be opened.
  - `'w'`: Write mode. If the file exists, it will be overwritten. If it does not exist, it will be created. This is the default mode.
  - `'a'`: Append mode. If the file exists, new content will be appended to the end. If it does not exist, it will be created.

## Example Usage

Below is an example of how to configure and use the `WriteFileBlock` within a workflow definition (e.g., in a Python script or a YAML configuration file, depending on how workflows are defined in your `kwargify-core` setup).

```python
from kwargify_core.core.workflow import Workflow
from kwargify_core.core.block import Block
from kwargify_core.blocks.write_file import WriteFileBlock

# Define a simple custom block that produces static text content
class StaticContentBlock(Block):
    def __init__(self, name="static_content_producer", content="Hello, Kwargify!"):
        super().__init__(name)
        self._content = content
        self.outputs = {"text_output": None} # Declare an output port

    def run(self):
        print(f"Running {self.name}...")
        self.outputs["text_output"] = self._content
        print(f"{self.name} produced: '{self.outputs['text_output']}'")

# 1. Instantiate the Workflow
wf = Workflow(name="file_writer_workflow")

# 2. Instantiate the blocks
content_block = StaticContentBlock(name="my_content_generator", content="This is a test content for WriteFileBlock.")
write_block = WriteFileBlock(
    name="my_file_writer",
    config={
        "path": "output/example_output.txt", # Ensure 'output/' directory exists or is creatable
        "mode": "w",
        "encoding": "utf-8"
    }
)

# 3. Add blocks to the workflow
wf.add_block(content_block)
wf.add_block(write_block)

# 4. Set up input dependency
# The 'content' input for WriteFileBlock comes from the 'text_output' of StaticContentBlock
write_block.set_input("content", content_block.get_output("text_output"))

# 5. Run the workflow
print("Starting workflow...")
wf.run()
print("Workflow finished.")

# To verify, check the contents of 'output/example_output.txt'.
# It should contain: "This is a test content for WriteFileBlock."
# You might need to create the 'output/' directory manually if it doesn't exist
# and the block/workflow doesn't handle its creation.
```

This example demonstrates how the `WriteFileBlock` can be integrated into a larger workflow to persist data to the filesystem. The specific syntax for referencing outputs from previous steps (`{{ ... }}`) might vary based on the workflow engine's templating capabilities.
