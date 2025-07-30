import uuid
from typing import Optional, Dict, Any, List

from ..llm_response_cleaner import clean_llm_response
from ..template_loader import TemplateLoader
from ....domain.reasoning.llm_generate_respository import LlmGenerateRepository
from .ollama_http_client import OllamaHttpClient


class OllamaGenerateRepository(LlmGenerateRepository):
    """
    Repository for generating text using the Ollama API.
    """

    def __init__(self, api_url: str, model_name: str, system_prompt: str = None, 
                 temperature: float = None, seed: int = None, max_tokens: int = 5000, 
                 api_token: str = None, template_loader: TemplateLoader = None, 
                 use_templating: bool = True):
        """
        Initialize a new OllamaGenerateRepository.

        Args:
            api_url: The base URL of the Ollama API.
            model_name: The name of the model to use.
            system_prompt: Optional system prompt to use for generation.
            temperature: The temperature to use for generation.
            seed: Optional seed for reproducible generation.
            max_tokens: The maximum number of tokens to generate.
            api_token: Optional API token for authentication.
            template_loader: Optional template loader to use for formatting prompts.
            use_templating: Whether to use Jinja2 templating for prompt formatting.
        """
        self.model_name = model_name
        self.system_prompt = system_prompt
        self.temperature = temperature
        self.seed = seed
        self.max_tokens = max_tokens
        self.http_client = OllamaHttpClient(api_url, api_token)
        self.use_templating = use_templating

        # Initialize template loader if not provided and templating is enabled
        if use_templating:
            self.template_loader = template_loader or TemplateLoader()

    def _format_with_template(self, user_prompt: str, system_prompt: str = None) -> str:
        """
        Format the prompt using a Jinja2 template appropriate for the model.

        Args:
            user_prompt: The user's prompt.
            system_prompt: Optional system prompt.

        Returns:
            str: The formatted prompt string.
        """
        # Get the appropriate template for this model
        template_name = self.template_loader.get_model_template(self.model_name)
        if not template_name:
            # If no template is available, return the user prompt with system prompt as prefix
            if system_prompt:
                return f"{system_prompt}\n\n{user_prompt}"
            return user_prompt

        # Prepare context for the template
        context = {
            "System": system_prompt or "",
            "Messages": [
                {"Role": "user", "Content": user_prompt}
            ],
            "Tools": []  # Can be extended later to support tools
        }

        # Render the template
        return self.template_loader.render_template(template_name, context)

    def generate(self, user_prompt: str, system_prompt: str = None, max_tokens: int = None) -> Optional[str]:
        """
        Generate text using the Ollama API.

        Args:
            user_prompt: The prompt to generate text from.
            system_prompt: Optional system prompt to override the default.
            max_tokens: Optional maximum number of tokens to generate.

        Returns:
            Optional[str]: The generated text, or None if the request failed.
        """
        system_prompt = system_prompt or self.system_prompt
        payload = {
            "model": self.model_name,
            "stream": False,
            "num_ctx": f"{self.max_tokens}"
        }

        # Add common parameters
        if self.seed:
            payload["seed"] = f"{self.seed}"
        if self.temperature:
            payload["temperature"] = f"{self.temperature}"
        if max_tokens:
            payload["num_ctx"] = f"{max_tokens}"

        # Use templating if enabled and available for this model
        if self.use_templating and hasattr(self, 'template_loader'):
            # Format with template
            formatted_prompt = self._format_with_template(user_prompt, system_prompt)
            payload["prompt"] = formatted_prompt
        else:
            # Use standard formatting
            payload["prompt"] = user_prompt
            if system_prompt:
                payload["system"] = system_prompt

        response_data = self.http_client.post("generate", payload)
        if response_data:
            response_content = response_data.get("response")
            return clean_llm_response(response_content)

        return None
