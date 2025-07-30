from typing import Dict, List, Optional

from .base_model_service import BaseModelService
from ...infrastructure.llm.ollama.factories.granite_factory import GraniteModelFactory
from ...infrastructure.llm.ollama.models.ollama_chat_message import OllamaChatMessage


class GraniteService(BaseModelService):
    """
    Service for interacting with the Granite model.
    Provides specialized methods for the Granite model, including document support.
    """

    def __init__(self, api_url: str, api_token: str = None, temperature: float = 0.6, max_tokens: int = 2500):
        """
        Initialize a new GraniteService.

        Args:
            api_url: The base URL of the LLM API.
            api_token: Optional API token for authentication.
            temperature: The temperature to use for generation.
            max_tokens: The maximum number of tokens to generate.

        Raises:
            ValueError: If the api_url is empty or None, or if temperature or max_tokens are invalid.
        """
        if not api_url:
            raise ValueError("API URL cannot be empty or None")
        if temperature < 0:
            raise ValueError("Temperature must be non-negative")
        if max_tokens <= 0:
            raise ValueError("Max tokens must be positive")

        self.api_url = api_url
        self.api_token = api_token
        self.temperature = temperature
        self.max_tokens = max_tokens

        # Create the Granite model factory
        self.factory = GraniteModelFactory(
            api_url=api_url,
            temperature=temperature,
            max_tokens=max_tokens,
            api_token=api_token,
            use_templating=True
        )

        # Create repositories
        self.chat_repository = self.factory.create_chat_repository()
        self.generate_repository = self.factory.create_generate_repository()

    def generate(self, prompt: str, system_prompt: str = None, max_tokens: int = None) -> Optional[str]:
        """
        Generate text using the Granite model.

        Args:
            prompt: The prompt to generate text from.
            system_prompt: Optional system prompt to use.
            max_tokens: Optional maximum number of tokens to generate.

        Returns:
            Optional[str]: The generated text, or None if an error occurs.

        Raises:
            ValueError: If the prompt is empty or None.
        """
        if not prompt:
            raise ValueError("Prompt cannot be empty or None")

        return self.generate_repository.generate(prompt, system_prompt, max_tokens)

    def chat(self, message: str, session_id: str, chat_history: List[Dict[str, str]] = None) -> Optional[str]:
        """
        Chat with the Granite model.

        Args:
            message: The user's message.
            session_id: The ID of the chat session.
            chat_history: Optional chat history to include in the conversation.

        Returns:
            Optional[str]: The model's response, or None if an error occurs.

        Raises:
            ValueError: If the message is empty or None, or if the session_id is empty or None.
        """
        if not message:
            raise ValueError("Message cannot be empty or None")
        if not session_id:
            raise ValueError("Session ID cannot be empty or None")

        return self.chat_repository.chat(message, session_id, chat_history)

    def chat_with_documents(self, message: str, session_id: str, documents: List[Dict[str, str]],
                           chat_history: List[Dict[str, str]] = None) -> Optional[str]:
        """
        Chat with the Granite model using provided documents as context.

        Args:
            message: The user's message.
            session_id: The ID of the chat session.
            documents: List of documents to use as context. Each document should have 'id' and 'content' keys.
            chat_history: Optional chat history to include in the conversation.

        Returns:
            Optional[str]: The model's response, or None if an error occurs.

        Raises:
            ValueError: If the message is empty or None, or if the session_id is empty or None.
        """
        if not message:
            raise ValueError("Message cannot be empty or None")
        if not session_id:
            raise ValueError("Session ID cannot be empty or None")
        if not documents:
            raise ValueError("Documents list cannot be empty or None")

        # Start with system prompts and user message
        messages = []

        # Add document messages
        for doc in documents:
            doc_id = doc.get('id', '')
            content = doc.get('content', '')
            if content:
                # Use the document role with optional ID
                role = f"document{doc_id}" if doc_id else "document"
                messages.append(OllamaChatMessage(role, content))

        # Add chat history if provided
        if chat_history:
            for msg in chat_history:
                messages.append(OllamaChatMessage(msg.get("role", "user"), msg.get("content", "")))

        # Add the current user message
        messages.append(OllamaChatMessage("user", message))

        # Call the chat repository with the prepared messages
        return self.chat_repository.chat_with_messages(messages)
