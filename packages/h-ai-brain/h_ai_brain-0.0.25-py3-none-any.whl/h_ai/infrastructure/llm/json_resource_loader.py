import os
import json
import importlib.util
import importlib.resources
from typing import Dict, Any


class JsonResourceLoader:
    """
    Loader for JSON configuration files.

    This class provides functionality to load JSON configuration files from the resources directory.
    It can load files from either a package or the file system, with fallback behavior.

    Usage:
        # Create a JSON resource loader
        loader = JsonResourceLoader()

        # Load a JSON resource
        config = loader.load_json_resource("autonomous_agent.json")
    """

    def __init__(self, resources_dir: str = None, package_name: str = None, resources_path: str = None):
        """
        Initialize a new JsonResourceLoader.

        Args:
            resources_dir: Directory containing JSON resources. If None, defaults to 'resources'.
            package_name: Python package name containing resources. If None, defaults to 'h_ai'.
            resources_path: Path within the package to resources. If None, defaults to 'resources'.
        """
        # Get the base directory of the package
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

        # Set default directories if not provided
        if resources_dir is None:
            resources_dir = os.path.join(base_dir, 'resources')
        if package_name is None:
            package_name = 'h_ai'
        if resources_path is None:
            resources_path = 'resources'

        self.resources_dir = resources_dir
        self.package_name = package_name
        self.resources_path = resources_path

    def load_json_resource(self, filename: str) -> Dict[str, Any]:
        """
        Load a JSON resource file from package or file system.

        Args:
            filename: Name of the JSON file (with or without .json extension).

        Returns:
            Dict[str, Any]: The loaded JSON data.

        Raises:
            ValueError: If the resource file cannot be found in either the package or file system.
        """
        # Add .json extension if not present
        if not filename.endswith('.json'):
            filename = f"{filename}.json"

        # First try to load from package
        try:
            # Construct the resource path within the package
            resource_path = os.path.join(self.resources_path, filename)
            resource_path = resource_path.replace('\\', '/')  # Ensure forward slashes for package paths

            # Try to get the resource from the package
            package_spec = importlib.util.find_spec(self.package_name)
            if package_spec is not None:
                # Use importlib.resources to get the resource content
                resource_package = f"{self.package_name}.{os.path.dirname(resource_path)}"
                resource_name = os.path.basename(resource_path)

                # Handle different importlib.resources APIs based on Python version
                try:
                    # Python 3.9+
                    with importlib.resources.files(resource_package).joinpath(resource_name).open('r') as f:
                        return json.load(f)
                except (AttributeError, ImportError):
                    # Fallback for older Python versions
                    resource_text = importlib.resources.read_text(resource_package, resource_name)
                    return json.loads(resource_text)
        except (ImportError, ModuleNotFoundError, FileNotFoundError, ValueError):
            # If package loading fails, fall back to file system
            pass

        # Fall back to file system
        file_path = os.path.join(self.resources_dir, filename)
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                return json.load(f)

        # If we get here, the resource wasn't found in either location
        raise ValueError(f"Resource file not found: {filename} (tried package '{self.package_name}' and directory '{self.resources_dir}')")