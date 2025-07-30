import sys
from pathlib import Path
from typing import Optional, Any
import os

if sys.version_info >= (3, 11):
    import tomllib
    import toml
else:
    try:
        import toml as tomllib # type: ignore
        import toml # type: ignore
    except ImportError:
        # Handle the case where 'toml' is not installed for Python < 3.11
        # For now, we can raise an informative error or log a warning.
        # A better solution would be to ensure 'toml' is a dependency.
        print("ERROR: 'toml' package is required for Python < 3.11. Please install it.", file=sys.stderr)
        # Or, to make the functions still somewhat work, have load_config return {}
        # and save_config do nothing if tomllib is not available.
        # For this task, let's make load_config return {} and save_config be a no-op
        # if the import fails, and print a warning.
        class TomlLibMissing:
            def loads(self, s): return {}
            def load(self, f): return {} # Added load method for file reading
            def dumps(self, o): return ""
            def dump(self, o, f): pass # Added dump method for file writing
            class TOMLDecodeError(Exception): pass

        tomllib = TomlLibMissing() # type: ignore
        toml = TomlLibMissing() # type: ignore # Also mock 'toml' for save_config
        print("WARNING: 'toml' package not found for Python < 3.11. TOML support will be limited.", file=sys.stderr)

def get_config_path() -> Path:
    """Returns the path to the configuration file."""
    return Path("config.toml")

def load_config() -> dict:
    """
    Reads config.toml, handles FileNotFoundError and tomllib.TOMLDecodeError,
    returns parsed data or an empty dictionary if errors occur or file not found.
    """
    config_path = get_config_path()
    try:
        with open(config_path, "rb") as f:
            # Assume Python 3.11+ for tomllib
            return tomllib.load(f)
    except FileNotFoundError:
        return {}
    except tomllib.TOMLDecodeError:
        print(f"Warning: Malformed config file at {config_path}. Returning empty config.")
        return {}
    except Exception as e:
        print(f"An unexpected error occurred while loading config: {e}")
        return {}

def save_config(config_data: dict) -> None:
    """Writes data to config.toml."""
    config_path = get_config_path()
    try:
        with open(config_path, "w") as f:
            toml.dump(config_data, f)
    except Exception as e:
        print(f"An unexpected error occurred while saving config: {e}")


def get_config_value(key_path: str, default: Optional[Any] = None) -> Any:
    """Retrieves a value from loaded config by dot-separated key."""
    config = load_config()
    keys = key_path.split('.')
    value = config
    try:
        for key in keys:
            value = value[key]
        return value
    except (KeyError, TypeError):
        return default

def get_database_name() -> str:
    """Uses get_config_value for "database.name", defaults to "kwargify_runs.db"."""
    return get_config_value("database.name", default="kwargify_runs.db")

def get_project_name() -> Optional[str]:
    """Uses get_config_value for "project.name"."""
    return get_config_value("project.name")