import os
from kwargify_core.core.block import Block
from kwargify_core.core.workflow import Workflow

# Define a simple input file
INPUT_FILE_PATH = "examples/test_input.txt"

class BlockA(Block):
    def run(self):
        print(f"Running Block A: Reading from {INPUT_FILE_PATH}")
        try:
            with open(INPUT_FILE_PATH, 'r') as f:
                content = f.read()
            self.outputs['file_content'] = content
            print(f"Block A output: file_content='{content[:50]}...'")
        except FileNotFoundError:
            print(f"Error: Input file not found at {INPUT_FILE_PATH}")
            self.outputs['file_content'] = "" # Provide empty content on error
            # In a real scenario, you might want to raise the exception
            # raise

class BlockB(Block):
    def run(self):
        print("Running Block B: Processing data from Block A")
        file_content = self.inputs.get('file_content', '')
        processed_data_b = file_content.upper()
        self.outputs['processed_b'] = processed_data_b
        print(f"Block B output: processed_b='{processed_data_b[:50]}...'")

class BlockC(Block):
    def run(self):
        print("Running Block C: Processing data from Block A differently")
        file_content = self.inputs.get('file_content', '')
        processed_data_c = file_content.lower().replace(' ', '_')
        self.outputs['processed_c'] = processed_data_c
        print(f"Block C output: processed_c='{processed_data_c[:50]}...'")

class BlockD(Block):
    def run(self):
        print("Running Block D: Combining results from Block B and Block C")
        processed_b = self.inputs.get('processed_b', '')
        processed_c = self.inputs.get('processed_c', '')
        combined_data = f"Combined: B=[{processed_b[:20]}] C=[{processed_c[:20]}]"
        self.outputs['combined'] = combined_data
        print(f"Block D output: combined='{combined_data}'")

def get_workflow() -> Workflow:
    """Creates and returns the multi-dependency example workflow."""
    # Instantiate blocks
    block_a = BlockA(name="Read File Block")
    block_b = BlockB(name="Uppercase Processor")
    block_c = BlockC(name="Lowercase and Underscore Processor")
    block_d = BlockD(name="Combiner Block")

    # Define dependencies
    block_b.add_dependency(block_a)
    block_c.add_dependency(block_a)
    block_d.add_dependency(block_b)
    block_d.add_dependency(block_c)

    # Create workflow
    workflow = Workflow() # Instantiate with default parameters
    workflow.name = "MultiDependencyExample" # Give the workflow a name for registration

    # Add blocks to workflow (order doesn't strictly matter due to topological sort)
    workflow.add_block(block_d) # Add D first to show topological sort works
    workflow.add_block(block_b)
    workflow.add_block(block_a)
    workflow.add_block(block_c)

    return workflow

# --- Workflow Setup for direct execution ---
if __name__ == "__main__":
    # Create the input file if it doesn't exist
    if not os.path.exists(INPUT_FILE_PATH):
        os.makedirs(os.path.dirname(INPUT_FILE_PATH), exist_ok=True)
        with open(INPUT_FILE_PATH, "w") as f:
            f.write("This is a test file for the multi-dependency workflow example.")
        print(f"Created input file: {INPUT_FILE_PATH}")

    workflow = get_workflow()

    print("\n--- Running Workflow ---")
    workflow.run()
    print("--- Workflow Finished ---")

    # Access final output (assuming block_d is still accessible or retrieved from workflow)
    # Note: When run via CLI, you'd typically access outputs via the logger/registry
    # For direct run, we can access the block instance if we keep track of it
    # A better way for direct run might be to retrieve the block from workflow.blocks
    # Find block_d by name for accessing output after run
    block_d_instance = next((b for b in workflow.blocks if b.name == "Combiner Block"), None)
    if block_d_instance:
        print(f"\nFinal result from Block D: {block_d_instance.get_output('combined')}")

    # Generate and print Mermaid diagram
    print("\n--- Workflow Diagram (Mermaid) ---")
    print(workflow.to_mermaid())
    print("----------------------------------")