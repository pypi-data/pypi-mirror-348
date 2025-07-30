from abc import ABC, abstractmethod
from typing import Optional, List, Dict, Any, Protocol


class ChatMessage(Protocol):
    """Protocol for chat messages."""
    role: str
    content: str


class LlmChatRepository(ABC):
    """
    Repository for chat interactions with an LLM.
    """

    @abstractmethod
    def chat(self, user_message: str, session_id: str, chat_history: List[Dict[str, str]] = None) -> Optional[str]:
        """
        Chat with the LLM.

        Args:
            user_message: The user's message.
            session_id: The ID of the chat session.
            chat_history: Optional chat history to include in the conversation.

        Returns:
            Optional[str]: The LLM's response, or None if the request failed.
        """
        ...

    @abstractmethod
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
        ...
