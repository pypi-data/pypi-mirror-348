from typing import Optional, List, Dict, Any

from ....domain.reasoning.llm_chat_repository import LlmChatRepository
from ....infrastructure.llm.llm_response_cleaner import clean_llm_response
from ....infrastructure.llm.ollama.models.ollama_chat_message import OllamaChatMessage
from ....infrastructure.llm.ollama.models.ollama_chat_session import OllamaChatSession
from ....infrastructure.llm.template_loader import TemplateLoader
from .ollama_http_client import OllamaHttpClient


class OllamaChatRepository(LlmChatRepository):
    """
    Repository for chat interactions using the Ollama API.
    """

    def __init__(self, api_url: str, model_name: str, system_prompts: list[str] = None, 
                 temperature: float = None, seed: int = None, api_token: str = None,
                 template_loader: TemplateLoader = None, use_templating: bool = True):
        """
        Initialize a new OllamaChatRepository.

        Args:
            api_url: The base URL of the Ollama API.
            model_name: The name of the model to use.
            system_prompts: Optional list of system prompts to use for the chat.
            temperature: The temperature to use for generation.
            seed: Optional seed for reproducible generation.
            api_token: Optional API token for authentication.
            template_loader: Optional template loader to use for formatting prompts.
            use_templating: Whether to use Jinja2 templating for prompt formatting.
        """
        self.model_name = model_name
        self.temperature = temperature
        self.seed = seed
        self.system_prompts = system_prompts or []
        self.http_client = OllamaHttpClient(api_url, api_token)
        self.use_templating = use_templating

        # Initialize template loader if not provided and templating is enabled
        if use_templating:
            self.template_loader = template_loader or TemplateLoader()

    def chat(self, user_message: str, session_id: str, chat_history: List[dict] = None) -> Optional[str]:
        """
        Chat with the model using the Ollama API.

        Args:
            user_message: The user's message.
            session_id: The ID of the chat session.
            chat_history: Optional chat history to include in the conversation.

        Returns:
            Optional[str]: The model's response, or None if the request failed.
        """
        # Start with system prompts and user message
        messages = []
        for system_prompt in self.system_prompts:
            messages.append(OllamaChatMessage("system", system_prompt))

        # Add chat history if provided
        if chat_history:
            for message in chat_history:
                messages.append(OllamaChatMessage(message.get("role", "user"), message.get("content", "")))

        # Add the current user message
        messages.append(OllamaChatMessage("user", user_message))

        # Create a session
        session = OllamaChatSession(session_id, messages)

        return self.chat_with_messages(session.messages)

    def chat_with_messages(self, messages: List[Any]) -> Optional[str]:
        """
        Chat with the model using a custom list of messages.

        This method allows for more flexibility in message formatting, such as including
        document messages or other special message types.

        Args:
            messages: The list of messages to send to the model. Each message should have
                     'role' and 'content' attributes or keys.

        Returns:
            Optional[str]: The model's response, or None if the request failed.
        """
        return self._call_ollama_api(messages)

    def _format_with_template(self, messages: List[Any]) -> str:
        """
        Format messages using a Jinja2 template appropriate for the model.

        Args:
            messages: The messages to format. Each message should have 'role' and 'content' attributes.

        Returns:
            str: The formatted prompt string.
        """
        # Get the appropriate template for this model
        template_name = self.template_loader.get_model_template(self.model_name)
        if not template_name:
            # Fall back to standard formatting if no template is available
            return self._format_standard(messages)

        # Extract system messages
        system_content = ""
        for msg in messages:
            if msg.role == "system":
                if system_content:
                    system_content += "\n\n"
                system_content += msg.content

        # Prepare context for the template
        context = {
            "System": system_content,
            "Messages": [{"Role": msg.role, "Content": msg.content} for msg in messages],
            "Tools": []  # Can be extended later to support tools
        }

        # Render the template
        return self.template_loader.render_template(template_name, context)

    def _format_standard(self, messages: List[Any]) -> List[Dict[str, str]]:
        """
        Format messages in the standard Ollama API format.

        Args:
            messages: The messages to format. Each message should have 'role' and 'content' attributes.

        Returns:
            List[Dict[str, str]]: The formatted messages.
        """
        result = []
        for message in messages:
            # Handle OllamaChatMessage objects
            if hasattr(message, 'to_dict'):
                result.append(message.to_dict())
            # Handle dict-like objects
            elif hasattr(message, 'get'):
                result.append({
                    "role": message.get("role", "user"),
                    "content": message.get("content", "")
                })
            # Handle objects with role and content attributes
            else:
                result.append({
                    "role": getattr(message, "role", "user"),
                    "content": getattr(message, "content", "")
                })
        return result

    def _call_ollama_api(self, messages: List[Any]) -> Optional[str]:
        """
        Call the Ollama API with the given messages.

        Args:
            messages: The messages to send to the API. Each message should have 'role' and 'content' attributes.

        Returns:
            Optional[str]: The model's response, or None if the request failed.
        """
        payload = {
            "model": self.model_name,
            "stream": False
        }

        # Add temperature and seed if provided
        if self.temperature:
            payload["temperature"] = self.temperature
        if self.seed:
            payload["seed"] = self.seed

        # Use templating if enabled and available for this model
        if self.use_templating and hasattr(self, 'template_loader'):
            # Format with template and use the prompt API
            formatted_prompt = self._format_with_template(messages)
            payload["prompt"] = formatted_prompt
            endpoint = "generate"
        else:
            # Use standard message formatting and the chat API
            payload["messages"] = self._format_standard(messages)
            endpoint = "chat"

        # Call the appropriate API endpoint
        response_data = self.http_client.post(endpoint, payload)
        if response_data:
            # Extract response based on the endpoint used
            if endpoint == "generate":
                full_response = response_data.get("response")
            else:
                full_response = response_data.get("message", {}).get("content")

            return clean_llm_response(full_response)

        return None
