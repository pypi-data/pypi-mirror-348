import json
from .json_resource_loader import JsonResourceLoader


class PromptLoader:
    """
    Loader for prompt configuration files.

    This class provides functionality to load prompt configuration files from JSON resources.
    It uses JsonResourceLoader to handle loading from either a package or the file system.

    Usage:
        # Create a prompt loader for a specific file
        loader = PromptLoader("autonomous_agent")

        # Get a specific config value
        system_prompt = loader.get_config_value("system_prompt")

        # Get the entire config as a JSON string
        config_json = loader.get_entire_config()
    """

    def __init__(self, resource_name):
        """
        Initialize a new PromptLoader.

        Args:
            resource_name: Name of the JSON resource file (with or without .json extension).
        """
        # Use JsonResourceLoader to load the resource
        json_loader = JsonResourceLoader()
        self.config = json_loader.load_json_resource(resource_name)

    def get_config_value(self, key):
        """
        Get a specific value from the config.

        Args:
            key: The key to look up in the config.

        Returns:
            The value associated with the key, or None if the key doesn't exist.
        """
        return self.config.get(key)

    def get_entire_config(self):
        """
        Get the entire config as a JSON string.

        Returns:
            str: The entire config as a formatted JSON string.
        """
        return json.dumps(self.config, indent=2)
