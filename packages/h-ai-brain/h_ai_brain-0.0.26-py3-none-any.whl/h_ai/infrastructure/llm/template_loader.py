import os
import importlib.util
from typing import Dict, Any, Optional, List
from jinja2 import Environment, FileSystemLoader, PackageLoader, ChoiceLoader, select_autoescape


class TemplateLoader:
    """
    Loader for Jinja2 templates.

    This class provides functionality to load and render Jinja2 templates for model-specific prompt formatting.

    Templates are stored in the resources/templates directory and should have a .j2 extension.
    Different models can have different templates to format prompts according to their specific requirements.

    The default template (default.j2) is used for models without specific formatting needs.
    Model-specific templates (like granite3.j2) provide tailored formatting for particular models.

    Usage:
        # Create a template loader
        loader = TemplateLoader()

        # Get a list of available templates
        templates = loader.get_template_names()

        # Render a template with context
        context = {
            "System": "You are a helpful assistant.",
            "Messages": [
                {"Role": "user", "Content": "Hello!"}
            ]
        }
        formatted_prompt = loader.render_template("default.j2", context)

        # Get the appropriate template for a model
        template_name = loader.get_model_template("granite3.3:8b")
    """

    def __init__(self, templates_dir: str = None, package_name: str = None, package_path: str = None):
        """
        Initialize a new TemplateLoader.

        Args:
            templates_dir: Directory containing Jinja2 templates. If None, defaults to 'resources/templates'.
            package_name: Python package name containing templates. If None, defaults to 'h_ai'.
            package_path: Path within the package to templates. If None, defaults to 'resources/templates'.
        """
        # Get the base directory of the package
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

        # Set default directories if not provided
        if templates_dir is None:
            templates_dir = os.path.join(base_dir, 'resources', 'templates')
        if package_name is None:
            package_name = 'h_ai_brain'
        if package_path is None:
            package_path = 'resources/templates'

        # Create a list of loaders to try in order
        loaders = []

        # First try to load from package
        try:
            # Check if the package exists and has the specified path
            if importlib.util.find_spec(package_name) is not None:
                loaders.append(PackageLoader(package_name, package_path))
        except (ImportError, ModuleNotFoundError):
            # If package loading fails, we'll fall back to file system
            pass

        # Then try to load from file system
        if os.path.exists(templates_dir):
            loaders.append(FileSystemLoader(templates_dir))

        # If no loaders were added, raise an error
        if not loaders:
            raise ValueError(f"No valid template sources found. Tried package '{package_name}' and directory '{templates_dir}'")

        # Initialize Jinja2 environment with a ChoiceLoader
        self.env = Environment(
            loader=ChoiceLoader(loaders),
            autoescape=select_autoescape(['html', 'xml']),
            trim_blocks=True,
            lstrip_blocks=True
        )

        self.templates_dir = templates_dir
        self.package_name = package_name
        self.package_path = package_path

    def get_template_names(self) -> list[str]:
        """
        Get a list of available template names.

        Returns:
            list[str]: List of template filenames.
        """
        return self.env.list_templates()

    def render_template(self, template_name: str, context: Dict[str, Any]) -> str:
        """
        Render a template with the given context.

        Args:
            template_name: Name of the template file.
            context: Dictionary of variables to pass to the template.

        Returns:
            str: The rendered template.
        """
        template = self.env.get_template(template_name)
        return template.render(**context)


    def get_model_template(self, model_name: str) -> Optional[str]:
        """
        Get the appropriate template name for a given model.

        Args:
            model_name: The name of the model.

        Returns:
            Optional[str]: The template name for the model, or None if no specific template exists.
        """
        # Map model names to template names
        model_templates = {
            "granite3.3:8b": "granite3.j2",
            # Add more model-to-template mappings as needed
        }

        # Check if there's a specific template for this model
        template_name = model_templates.get(model_name)

        # If no specific template, use default
        if template_name is None:
            template_name = "default.j2"

        # Verify the template exists
        if template_name in self.get_template_names():
            return template_name

        # Fall back to default if the specific template doesn't exist
        if "default.j2" in self.get_template_names():
            return "default.j2"

        return None
