# AI Extractor Block

## Overview

The AI Extractor Block is a component within the `kwargify-core` framework designed to extract structured data from unstructured text content. It leverages a Large Language Model (LLM) through the `litellm` library to understand the text and pull out specific pieces of information based on a defined schema.

This block is particularly useful when you need to convert natural language text into a machine-readable format, such as JSON, for further processing in a workflow.

## Inputs

The AI Extractor Block requires the following inputs:

1.  **`content`** (`str`):

    - Description: The raw text content from which data needs to be extracted.
    - Example: `"John Doe is 30 years old and lives in New York. His email is john.doe@example.com."`

2.  **`extraction_fields`** (`Dict[str, Dict[str, str]]`):
    - Description: A dictionary defining the schema for data extraction. Each key in the dictionary represents a field to be extracted. The value for each key is another dictionary specifying the `type` of the field and a `description` of what to extract for that field.
    - Supported types: `string`, `number`, `boolean`, `array`.
    - Format:
      ```json
      {
        "field_name_1": {
          "type": "string|number|boolean|array",
          "description": "Detailed description of what to extract for this field."
        },
        "field_name_2": {
          "type": "string",
          "description": "Another field description."
        }
      }
      ```
    - Example:
      ```json
      {
        "name": {
          "type": "string",
          "description": "The full name of the person."
        },
        "age": {
          "type": "number",
          "description": "The age of the person."
        },
        "city": {
          "type": "string",
          "description": "The city where the person lives."
        },
        "email": {
          "type": "string",
          "description": "The email address of the person."
        }
      }
      ```

## Outputs

The block produces the following outputs:

1.  **`extracted_data`** (`Dict[str, Any]`):

    - Description: A dictionary containing the structured data extracted from the input `content` based on the `extraction_fields` schema. If a field cannot be extracted, its value will be `null`.
    - Example (based on the input example above):
      ```json
      {
        "name": "John Doe",
        "age": 30,
        "city": "New York",
        "email": "john.doe@example.com"
      }
      ```

2.  **`raw_response`** (`str`, Optional):
    - Description: The raw response string received from the LLM. This can be useful for debugging purposes to understand what the model returned before any cleaning or JSON parsing.

## Configuration Options

The AI Extractor Block can be configured with the following options:

1.  **`model`** (`str`):

    - Description: Specifies the LLM model to be used for extraction via `litellm`.
    - Default: `"gpt-4o-mini"`
    - Example: `"claude-3.5-sonnet"`, `"gpt-4"`

2.  **`temperature`** (`float`):
    - Description: Controls the randomness of the LLM's output. Lower values (e.g., 0.2) make the output more deterministic and focused, while higher values (e.g., 0.8) make it more creative. For extraction tasks, a lower temperature is generally preferred.
    - Default: `0.2`
    - Range: Typically between `0.0` and `1.0` (or `2.0` for some models).

## Interaction with AI Services

The AI Extractor Block interacts with AI services (LLMs) through the `litellm` library. `litellm` acts as a unified interface to various LLM providers (OpenAI, Anthropic, Cohere, etc.).

- **API Keys**: The block itself does not handle API keys directly. `litellm` is responsible for managing API key credentials. You typically set these as environment variables (e.g., `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`) which `litellm` will automatically pick up. Refer to the `litellm` documentation for details on how to configure API keys for different providers.
- **Prompt Engineering**: The block constructs a specific prompt for the LLM based on the input `content` and `extraction_fields`. The prompt instructs the LLM to act as a "precise data extraction assistant" and to return _only_ a valid JSON object.
  - The system prompt used is: `"You are a precise data extraction assistant. Your ONLY task is to extract the requested information and return it as a valid JSON object. DO NOT include any other text or explanation in your response."`
  - The user prompt includes the `content` and a description of the `extraction_fields`.
  - While the block handles basic prompt generation, advanced prompt engineering might involve carefully crafting the `description` for each field in `extraction_fields` to guide the LLM more effectively. For complex extractions, providing examples within the field descriptions or using a more sophisticated prompting strategy (if `litellm` and the chosen model support it) might be necessary, though this block currently uses a straightforward approach.

## Example Usage in a Workflow

Here's a conceptual example of how to configure and use the `AIExtractorBlock` within a `kwargify-core` workflow:

```python
from kwargify_core.core.workflow import Workflow
from kwargify_core.blocks.read_file import ReadFileBlock
from kwargify_core.blocks.ai_extractor import AIExtractorBlock
from kwargify_core.blocks.write_file import WriteFileBlock

# Define the workflow
extraction_workflow = Workflow(name="DocumentInformationExtraction")

# Step 1: Read content from a file
extraction_workflow.add_block(
    ReadFileBlock,
    name="read_document",
    config={"file_path": "path/to/your/document.txt"}
)

# Step 2: Extract structured data using AI
extraction_workflow.add_block(
    AIExtractorBlock,
    name="extract_data_from_text",
    config={
        "model": "gpt-4o-mini",  # Or your preferred model
        "temperature": 0.1
    },
    inputs={
        "content": extraction_workflow.blocks["read_document"].outputs["content"],
        "extraction_fields": {
            "invoice_number": {
                "type": "string",
                "description": "The unique identifier for the invoice, usually labeled as 'Invoice #', 'Invoice ID', or similar."
            },
            "total_amount": {
                "type": "number",
                "description": "The final total amount due on the invoice."
            },
            "due_date": {
                "type": "string",
                "description": "The date by which the invoice payment is due, in YYYY-MM-DD format if possible."
            },
            "client_name": {
                "type": "string",
                "description": "The name of the client or company being invoiced."
            }
        }
    }
)

# Step 3: Write the extracted data to a JSON file
extraction_workflow.add_block(
    WriteFileBlock,
    name="save_extracted_data",
    config={"file_path": "path/to/output/extracted_data.json"},
    inputs={
        "content": extraction_workflow.blocks["extract_data_from_text"].outputs["extracted_data"]
        # Assuming WriteFileBlock can handle dicts and serialize to JSON,
        # or a JsonToStringBlock might be needed in between.
    }
)

# To run the workflow (conceptual):
# result = extraction_workflow.run_all()
# print(result)
# print(extraction_workflow.blocks["extract_data_from_text"].outputs["extracted_data"])
# print(extraction_workflow.blocks["extract_data_from_text"].outputs.get("raw_response"))

```

**Note on `WriteFileBlock` with JSON:**
The example above assumes `WriteFileBlock` can directly handle a dictionary and serialize it to JSON. If not, you might need to insert a `JsonToStringBlock` before `WriteFileBlock` to convert the `extracted_data` dictionary into a JSON string.

```python
# ... (previous blocks)
from kwargify_core.blocks.json_to_string import JsonToStringBlock

# Intermediate step to convert dict to JSON string
extraction_workflow.add_block(
    JsonToStringBlock,
    name="format_data_as_json_string",
    inputs={
        "json_data": extraction_workflow.blocks["extract_data_from_text"].outputs["extracted_data"]
    }
)

# Step 3 (revised): Write the extracted data (as string) to a JSON file
extraction_workflow.add_block(
    WriteFileBlock,
    name="save_extracted_data",
    config={"file_path": "path/to/output/extracted_data.json"},
    inputs={
        "content": extraction_workflow.blocks["format_data_as_json_string"].outputs["string_data"]
    }
)
# ... (rest of the workflow execution)
```

This documentation provides a comprehensive guide to understanding and using the AI Extractor Block within your `kwargify-core` workflows.
