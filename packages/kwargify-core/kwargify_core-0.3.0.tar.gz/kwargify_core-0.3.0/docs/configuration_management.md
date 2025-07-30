# Configuration Management in kwargify-core

## Overview

Configuration in `kwargify-core` is managed through a central TOML file. This approach allows for easy customization of project settings, such as database names and project-specific parameters, without modifying the core codebase. The system is designed to be robust, gracefully handling missing or malformed configuration files by falling back to sensible defaults or empty configurations.

The primary module responsible for configuration is [`src/kwargify_core/config.py`](../src/kwargify_core/config.py:1).

## Configuration File

### Location and Name

The configuration file is named `config.toml` and is expected to be located in the root directory from which the `kwargify-core` application or script is executed. This is determined by the [`get_config_path()`](../src/kwargify_core/config.py:33) function, which returns `Path("config.toml")`.

### Format

The configuration file uses the **TOML (Tom's Obvious, Minimal Language)** format. TOML is designed to be a minimal configuration file format that is easy to read due to its simple semantics.

`kwargify-core` uses `tomllib` (available in Python 3.11+) for parsing TOML files. For Python versions older than 3.11, it attempts to use the `toml` package as a fallback. If the `toml` package is not installed in these older Python environments, TOML support will be limited (e.g., loading configuration might return an empty dictionary, and saving might be a no-op), and a warning will be printed to `stderr`.

### Structure

The `config.toml` file can have a flexible, nested structure. Users can define sections and key-value pairs as needed by their project.

**Example `config.toml` structure:**

```toml
[project]
name = "My Kwargify Project"
version = "1.0.0"

[database]
name = "project_specific_runs.db"
# Other database settings can be added here
# host = "localhost"
# port = 5432

[api_keys]
# It's generally recommended to use environment variables for sensitive keys,
# but they can be stored here if appropriate for the use case.
# service_x = "your_api_key_here"
```

## Handling Configuration

### Loading Configuration

Configuration is loaded into the application using the [`load_config()`](../src/kwargify_core/config.py:37) function.

- It reads the `config.toml` file.
- If the file is not found, it returns an empty dictionary (`{}`).
- If the file is found but is malformed (i.e., contains TOML syntax errors), a warning is printed to `stderr`, and an empty dictionary is returned.
- In case of other unexpected errors during loading, an error message is printed, and an empty dictionary is returned.

### Saving Configuration

Configuration data (as a Python dictionary) can be written back to the `config.toml` file using the [`save_config(config_data: dict)`](../src/kwargify_core/config.py:56) function.

- This function will overwrite the existing `config.toml` file or create it if it doesn't exist.
- If any unexpected error occurs during saving, an error message is printed.

## Accessing Configuration Settings

Individual configuration values are retrieved using the [`get_config_value(key_path: str, default: Optional[Any] = None)`](../src/kwargify_core/config.py:66) function.

- `key_path`: A dot-separated string representing the path to the desired value within the TOML structure (e.g., `"project.name"`, `"database.host"`).
- `default`: An optional value to return if the specified `key_path` is not found in the configuration or if the configuration file itself is missing or empty. If no default is provided and the key is not found, it will also return the default value passed (which is `None` by default for the `default` parameter itself).

**Example Usage:**

```python
from kwargify_core.config import get_config_value, get_database_name, get_project_name

# Assuming config.toml contains:
# [project]
# name = "My Project"
#
# [database]
# name = "my_data.db"

project_name = get_config_value("project.name")
print(f"Project Name: {project_name}") # Output: My Project

db_host = get_config_value("database.host", default="localhost")
print(f"Database Host: {db_host}") # Output: localhost (as it's not in config.toml)

# Using specialized getter functions
database_file = get_database_name()
print(f"Database File: {database_file}") # Output: my_data.db

current_project = get_project_name()
print(f"Current Project from specialized getter: {current_project}") # Output: My Project
```

## Modifying Configuration Settings Programmatically

To modify configuration settings:

1.  Load the current configuration using [`load_config()`](../src/kwargify_core/config.py:37).
2.  Modify the resulting Python dictionary.
3.  Save the updated dictionary back to `config.toml` using [`save_config()`](../src/kwargify_core/config.py:56).

**Example:**

```python
from kwargify_core.config import load_config, save_config

# Load existing configuration
current_config = load_config()

# Modify or add settings
if 'project' not in current_config:
    current_config['project'] = {}
current_config['project']['version'] = "1.1.0"
current_config['new_setting'] = {"enabled": True}

# Save the updated configuration
save_config(current_config)
print("Configuration updated and saved.")
```

## Default Configuration Values

Some parts of `kwargify-core` may have built-in default values if specific settings are not found in `config.toml`.

- **Database Name:** The [`get_database_name()`](../src/kwargify_core/config.py:78) function defaults to `"kwargify_runs.db"` if the `database.name` key is not found in the configuration.
- **Project Name:** The [`get_project_name()`](../src/kwargify_core/config.py:82) function will return `None` if `project.name` is not specified, as it calls [`get_config_value("project.name")`](../src/kwargify_core/config.py:84) without a specific default override (thus using the default `None` from `get_config_value`).

## Environment Variables

The configuration management provided by [`src/kwargify_core/config.py`](../src/kwargify_core/config.py:1) primarily focuses on the `config.toml` file. It does not inherently read or override settings from environment variables directly within this module. For sensitive information like API keys, or for environment-specific overrides, it is a common practice to use environment variables. While `kwargify-core`'s `config.py` doesn't implement this directly, users can integrate environment variable reading in their application logic before or after loading settings from `config.toml` if needed.

## Configuration Scenarios

### Scenario 1: Basic Project Setup

A user wants to define a project name and a custom database file for their `kwargify-core` workflows.

**`config.toml`:**

```toml
[project]
name = "Alpha Analysis"

[database]
name = "alpha_analysis_runs.db"
```

**Python code:**

```python
from kwargify_core.config import get_project_name, get_database_name

project = get_project_name() # "Alpha Analysis"
db = get_database_name()     # "alpha_analysis_runs.db"

print(f"Running project: {project} using database: {db}")
```

### Scenario 2: Missing Configuration File

A user runs `kwargify-core` without creating a `config.toml` file.

**Python code:**

```python
from kwargify_core.config import get_project_name, get_database_name, get_config_value

project = get_project_name() # None
db = get_database_name()     # "kwargify_runs.db" (default)
custom_setting = get_config_value("custom.setting", default="fallback") # "fallback"

print(f"Project: {project}, Database: {db}, Custom: {custom_setting}")
# Output: Project: None, Database: kwargify_runs.db, Custom: fallback
```

A warning about the missing file might not be printed by `load_config` itself if it just returns `{}`, but `get_config_value` will operate on this empty dict.

### Scenario 3: Malformed Configuration File

A user has a `config.toml` with syntax errors.

**`config.toml` (malformed):**

```toml
[project
name = "My Project" # Missing closing bracket for section
```

When [`load_config()`](../src/kwargify_core/config.py:37) is called (e.g., internally by [`get_config_value()`](../src/kwargify_core/config.py:66)), a warning like "Warning: Malformed config file at config.toml. Returning empty config." will be printed to `stderr`. Subsequent calls to [`get_config_value()`](../src/kwargify_core/config.py:66) will use default values or return `None` as if the file was empty.

This documentation provides a comprehensive guide to understanding and utilizing the configuration management features within `kwargify-core`.
