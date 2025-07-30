from abc import ABC, abstractmethod
from typing import List, Optional

class LlmEmbeddingRepository(ABC):
    """
    Repository for creating embeddings with an LLM.
    """

    @abstractmethod
    def embed(self, text: str) -> Optional[List[float]]:
        """
        Create an embedding for the given text.

        Args:
            text: The text to create an embedding for.

        Returns:
            Optional[List[float]]: The embedding vector, or None if the request failed.
        """
        pass
