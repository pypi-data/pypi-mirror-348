from typing import Optional

from .....domain.model_factory import ModelFactory
from .....domain.reasoning.llm_chat_repository import LlmChatRepository
from .....domain.reasoning.llm_embedding_repository import LlmEmbeddingRepository
from .....domain.reasoning.llm_generate_respository import LlmGenerateRepository
from ..ollama_embed_repository import OllamaEmbeddingRepository


class NomicModelFactory(ModelFactory):
    """
    Factory for creating repositories for the Nomic Embed Text model.
    This model is specifically for embeddings and doesn't support chat or generation.
    """
    
    MODEL_NAME = "nomic-embed-text:137m-v1.5-fp16"
    
    def __init__(self, api_url: str, api_token: str = None):
        """
        Initialize a new NomicModelFactory.
        
        Args:
            api_url: The base URL of the Ollama API.
            api_token: Optional API token for authentication.
        """
        self.api_url = api_url
        self.api_token = api_token
    
    def create_chat_repository(self) -> Optional[LlmChatRepository]:
        """
        Nomic model doesn't support chat, so this returns None.
        
        Returns:
            Optional[LlmChatRepository]: None, as Nomic doesn't support chat.
        """
        return None
    
    def create_generate_repository(self) -> Optional[LlmGenerateRepository]:
        """
        Nomic model doesn't support generation, so this returns None.
        
        Returns:
            Optional[LlmGenerateRepository]: None, as Nomic doesn't support generation.
        """
        return None
    
    def create_embedding_repository(self) -> LlmEmbeddingRepository:
        """
        Creates an embedding repository for the Nomic model.
        
        Returns:
            LlmEmbeddingRepository: A repository for creating embeddings with the Nomic model.
        """
        return OllamaEmbeddingRepository(
            api_url=self.api_url,
            model_name=self.MODEL_NAME,
            api_token=self.api_token
        )