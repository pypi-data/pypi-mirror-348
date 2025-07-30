from abc import ABC, abstractmethod
from typing import Dict, List, Optional


class BaseModelService(ABC):
    """
    Base class for model-specific services.
    Defines the common interface that all model services must implement.
    """

    @abstractmethod
    def generate(self, prompt: str, system_prompt: str = None, max_tokens: int = None) -> Optional[str]:
        """
        Generate text using the model.

        Args:
            prompt: The prompt to generate text from.
            system_prompt: Optional system prompt to use.
            max_tokens: Optional maximum number of tokens to generate.

        Returns:
            Optional[str]: The generated text, or None if an error occurs.
        """
        pass

    @abstractmethod
    def chat(self, message: str, session_id: str, chat_history: List[Dict[str, str]] = None) -> Optional[str]:
        """
        Chat with the model.

        Args:
            message: The user's message.
            session_id: The ID of the chat session.
            chat_history: Optional chat history to include in the conversation.

        Returns:
            Optional[str]: The model's response, or None if an error occurs.
        """
        pass

    def embed(self, text: str) -> Optional[List[float]]:
        """
        Create an embedding for the given text.
        Default implementation returns None as not all models support embeddings.

        Args:
            text: The text to create an embedding for.

        Returns:
            Optional[List[float]]: The embedding vector, or None if the model doesn't support embeddings.
        """
        return None

    def chat_with_documents(self, message: str, session_id: str, documents: List[Dict[str, str]], 
                           chat_history: List[Dict[str, str]] = None) -> Optional[str]:
        """
        Chat with the model using provided documents as context.
        Default implementation returns None as not all models support document-based chat.

        Args:
            message: The user's message.
            session_id: The ID of the chat session.
            documents: List of documents to use as context.
            chat_history: Optional chat history to include in the conversation.

        Returns:
            Optional[str]: The model's response, or None if the model doesn't support document-based chat.
        """
        return None