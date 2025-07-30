import unittest
from unittest.mock import patch, mock_open
import tomllib
import toml
from pathlib import Path
import os
import tempfile

# Assuming the config module is in src/kwargify_core
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from kwargify_core import config

class TestConfig(unittest.TestCase):

    def setUp(self):
        # Create a temporary directory for config files during tests
        self.test_dir = tempfile.TemporaryDirectory()
        self.original_get_config_path = config.get_config_path
        # Patch get_config_path to point to the temporary directory
        config.get_config_path = lambda: Path(self.test_dir.name) / "config.toml"

    def tearDown(self):
        # Clean up the temporary directory
        self.test_dir.cleanup()
        # Restore the original get_config_path
        config.get_config_path = self.original_get_config_path

    def test_save_and_load_config(self):
        """Test saving a sample configuration and loading it back."""
        sample_config = {
            "database": {
                "name": "my_test_db.db",
                "user": "test_user"
            },
            "project": {
                "name": "my_test_project"
            }
        }
        config.save_config(sample_config)
        loaded_config = config.load_config()
        self.assertEqual(loaded_config, sample_config)

    def test_get_config_value(self):
        """Test retrieving values, including nested ones and with defaults."""
        sample_config = {
            "database": {
                "name": "my_test_db.db",
                "user": "test_user"
            },
            "project": {
                "name": "my_test_project"
            },
            "settings": {
                "timeout": 30
            }
        }
        config.save_config(sample_config)

        self.assertEqual(config.get_config_value("database.name"), "my_test_db.db")
        self.assertEqual(config.get_config_value("project.name"), "my_test_project")
        self.assertEqual(config.get_config_value("settings.timeout"), 30)
        self.assertEqual(config.get_config_value("non_existent_key"), None)
        self.assertEqual(config.get_config_value("non_existent_key", default="default_value"), "default_value")
        self.assertEqual(config.get_config_value("database.password", default="default_password"), "default_password")
        self.assertEqual(config.get_config_value("database"), {"name": "my_test_db.db", "user": "test_user"})

    def test_get_database_name_with_config(self):
        """Test getting DB name when config.toml has it."""
        sample_config = {
            "database": {
                "name": "configured_db.db"
            }
        }
        config.save_config(sample_config)
        self.assertEqual(config.get_database_name(), "configured_db.db")

    def test_get_database_name_without_config(self):
        """Test getting default DB name when config.toml doesn't have it or doesn't exist."""
        # Test when file exists but no database.name
        sample_config = {"project": {"name": "test"}}
        config.save_config(sample_config)
        self.assertEqual(config.get_database_name(), "kwargify_runs.db")

        # Test when file does not exist
        os.remove(config.get_config_path())
        self.assertEqual(config.get_database_name(), "kwargify_runs.db")


    def test_get_project_name(self):
        """Test getting project name."""
        sample_config = {
            "project": {
                "name": "my_test_project"
            }
        }
        config.save_config(sample_config)
        self.assertEqual(config.get_project_name(), "my_test_project")

        # Test when project.name is not in config
        sample_config_no_project_name = {"database": {"name": "test"}}
        config.save_config(sample_config_no_project_name)
        self.assertEqual(config.get_project_name(), None)

        # Test when file does not exist
        os.remove(config.get_config_path())
        self.assertEqual(config.get_project_name(), None)


    @patch('kwargify_core.config.tomllib.load')
    @patch('builtins.open', new_callable=mock_open)
    def test_load_config_file_not_found(self, mock_file, mock_tomllib_load):
        """Test load_config() when config.toml is missing (should return empty dict)."""
        mock_file.side_effect = FileNotFoundError
        loaded_config = config.load_config()
        self.assertEqual(loaded_config, {})
        mock_tomllib_load.assert_not_called()

    @patch('kwargify_core.config.tomllib.load')
    @patch('builtins.open', new_callable=mock_open, read_data="[invalid toml")
    def test_load_config_malformed(self, mock_file, mock_tomllib_load):
        """Test load_config() with an invalid TOML file (should return empty dict)."""
        mock_tomllib_load.side_effect = tomllib.TOMLDecodeError("Malformed TOML", "", 0)
        loaded_config = config.load_config()
        self.assertEqual(loaded_config, {})
        mock_tomllib_load.assert_called_once()

if __name__ == '__main__':
    unittest.main()