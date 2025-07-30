from typing import Dict, List, Optional

from .base_model_service import BaseModelService
from ...infrastructure.llm.ollama.factories.nomic_factory import NomicModelFactory


class NomicService(BaseModelService):
    """
    Service for interacting with the Nomic model.
    Provides specialized methods for the Nomic model, focusing on embeddings.
    """

    def __init__(self, api_url: str, api_token: str = None):
        """
        Initialize a new NomicService.

        Args:
            api_url: The base URL of the LLM API.
            api_token: Optional API token for authentication.

        Raises:
            ValueError: If the api_url is empty or None.
        """
        if not api_url:
            raise ValueError("API URL cannot be empty or None")

        self.api_url = api_url
        self.api_token = api_token

        # Create the Nomic model factory
        self.factory = NomicModelFactory(
            api_url=api_url,
            api_token=api_token
        )

        # Create repositories
        self.embedding_repository = self.factory.create_embedding_repository()

    def generate(self, prompt: str, system_prompt: str = None, max_tokens: int = None) -> Optional[str]:
        """
        Generate text using the Nomic model.
        Nomic doesn't support text generation, so this always returns None.

        Args:
            prompt: The prompt to generate text from.
            system_prompt: Optional system prompt to use.
            max_tokens: Optional maximum number of tokens to generate.

        Returns:
            Optional[str]: Always None as Nomic doesn't support text generation.
        """
        return None

    def chat(self, message: str, session_id: str, chat_history: List[Dict[str, str]] = None) -> Optional[str]:
        """
        Chat with the Nomic model.
        Nomic doesn't support chat, so this always returns None.

        Args:
            message: The user's message.
            session_id: The ID of the chat session.
            chat_history: Optional chat history to include in the conversation.

        Returns:
            Optional[str]: Always None as Nomic doesn't support chat.
        """
        return None

    def embed(self, text: str) -> Optional[List[float]]:
        """
        Create an embedding for the given text using the Nomic model.

        Args:
            text: The text to create an embedding for.

        Returns:
            Optional[List[float]]: The embedding vector, or None if an error occurs.

        Raises:
            ValueError: If the text is empty or None.
        """
        if not text:
            raise ValueError("Text cannot be empty or None")

        return self.embedding_repository.embed(text)

    def batch_embed(self, texts: List[str]) -> Optional[List[List[float]]]:
        """
        Create embeddings for multiple texts in a single batch.

        Args:
            texts: List of texts to create embeddings for.

        Returns:
            Optional[List[List[float]]]: List of embedding vectors, or None if an error occurs.

        Raises:
            ValueError: If the texts list is empty or None.
        """
        if not texts:
            raise ValueError("Texts list cannot be empty or None")

        # Filter out empty texts
        valid_texts = [text for text in texts if text]
        if not valid_texts:
            raise ValueError("All texts in the list are empty")

        # Process each text individually
        # In a real implementation, this could be optimized to use batch processing if supported by the API
        embeddings = []
        for text in valid_texts:
            embedding = self.embedding_repository.embed(text)
            if embedding is None:
                return None  # If any embedding fails, return None
            embeddings.append(embedding)

        return embeddings