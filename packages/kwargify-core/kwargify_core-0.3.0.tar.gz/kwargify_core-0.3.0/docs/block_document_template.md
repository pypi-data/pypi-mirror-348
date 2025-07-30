# Document Template Block

## Overview

The `DocumentTemplateBlock` is a component within the `kwargify-core` project designed to generate formatted documents by populating a template with provided data. It utilizes the Jinja2 templating engine to achieve this. This block is useful when you need to create dynamic content based on a predefined structure, such as generating reports, emails, or configuration files.

## Inputs

The `DocumentTemplateBlock` requires the following inputs:

- **`template` (str):** This is a string containing the Jinja2 template. The template can include variables (e.g., `{{ variable_name }}`), control structures like loops (`{% for item in items %}`), and conditionals (`{% if condition %}`).
- **`data` (Dict[str, Any]):** This is a Python dictionary where keys correspond to the variable names used in the `template` string, and values are the data to be inserted into those variables.

## Outputs

The block produces a single output:

- **`document` (str):** This is a string containing the rendered document. It's the result of the Jinja2 template being processed with the provided `data`.

## Configuration Options

The `DocumentTemplateBlock` uses a default Jinja2 environment with the following settings:

- **`StrictUndefined`:** This is enabled by default. If the template tries to access a variable that is not provided in the `data` dictionary, a `jinja2.exceptions.UndefinedError` (wrapped in a `RuntimeError`) will be raised. This helps in catching missing data errors early.
- **`trim_blocks=True`:** This option removes the first newline character after a Jinja2 block tag (e.g., `{% ... %}`).
- **`lstrip_blocks=True`:** This option strips leading whitespace (tabs and spaces) from the start of a line up to the beginning of a block tag.

There are no other external configuration options specific to this block beyond the standard Jinja2 syntax and features.

## Example Usage

Here's an example of how to configure and use the `DocumentTemplateBlock` in a workflow:

**Sample Template (`template` input):**

```jinja2
Report for {{ user_profile.name }} ({{ user_profile.email }})
==================================================

Account ID: {{ account.id }}
Account Type: {{ account.type }}

Recent Activity:
{% if recent_activities %}
  {% for activity in recent_activities %}
  - {{ activity.timestamp }}: {{ activity.description }}
  {% endfor %}
{% else %}
  No recent activity.
{% endif %}

{% if notes %}
Additional Notes:
{{ notes }}
{% endif %}
```

**Sample Context Data (`data` input):**

```python
{
    "user_profile": {
        "name": "Alice Wonderland",
        "email": "alice@example.com"
    },
    "account": {
        "id": "acc_12345",
        "type": "Premium"
    },
    "recent_activities": [
        {"timestamp": "2024-05-10 10:00:00", "description": "Logged in"},
        {"timestamp": "2024-05-10 10:05:00", "description": "Viewed dashboard"},
        {"timestamp": "2024-05-09 15:30:00", "description": "Updated profile"}
    ],
    "notes": "User has requested a follow-up call regarding their subscription."
}
```

**Workflow Configuration (Conceptual):**

```python
# Assuming 'workflow' is an instance of a Workflow class
# and DocumentTemplateBlock is registered with the name 'document_templater'

workflow.add_block(
    name="generate_user_report",
    block_type="document_templater", # Or whatever name it's registered under
    inputs={
        "template": """
Report for {{ user_profile.name }} ({{ user_profile.email }})
==================================================

Account ID: {{ account.id }}
Account Type: {{ account.type }}

Recent Activity:
{% if recent_activities %}
  {% for activity in recent_activities %}
  - {{ activity.timestamp }}: {{ activity.description }}
  {% endfor %}
{% else %}
  No recent activity.
{% endif %}

{% if notes %}
Additional Notes:
{{ notes }}
{% endif %}
""",
        "data": { # This data would typically come from previous blocks or external sources
            "user_profile": {
                "name": "Alice Wonderland",
                "email": "alice@example.com"
            },
            "account": {
                "id": "acc_12345",
                "type": "Premium"
            },
            "recent_activities": [
                {"timestamp": "2024-05-10 10:00:00", "description": "Logged in"},
                {"timestamp": "2024-05-10 10:05:00", "description": "Viewed dashboard"},
                {"timestamp": "2024-05-09 15:30:00", "description": "Updated profile"}
            ],
            "notes": "User has requested a follow-up call regarding their subscription."
        }
    }
)

# To get the output:
# report_output = workflow.run()["generate_user_report"]["document"]
# print(report_output)
```

**Expected Output (`document` output):**

```text
Report for Alice Wonderland (alice@example.com)
==================================================

Account ID: acc_12345
Account Type: Premium

Recent Activity:
  - 2024-05-10 10:00:00: Logged in
  - 2024-05-10 10:05:00: Viewed dashboard
  - 2024-05-09 15:30:00: Updated profile

Additional Notes:
User has requested a follow-up call regarding their subscription.
```

This example demonstrates how the `DocumentTemplateBlock` can be used to dynamically generate a structured text document by merging a template with specific data.
