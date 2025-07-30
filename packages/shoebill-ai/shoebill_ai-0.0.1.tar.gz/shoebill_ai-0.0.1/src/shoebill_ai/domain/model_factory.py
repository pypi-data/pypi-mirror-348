from abc import ABC, abstractmethod
from typing import Optional

from .reasoning.llm_chat_repository import LlmChatRepository
from .reasoning.llm_embedding_repository import LlmEmbeddingRepository
from .reasoning.llm_generate_respository import LlmGenerateRepository


class ModelFactory(ABC):
    """
    Abstract factory for creating model-specific repositories.
    This factory is responsible for creating the appropriate repositories for a given model.
    """
    
    @abstractmethod
    def create_chat_repository(self) -> LlmChatRepository:
        """
        Creates a chat repository for the model.
        
        Returns:
            LlmChatRepository: A repository for chat interactions with the model.
        """
        pass
    
    @abstractmethod
    def create_generate_repository(self) -> LlmGenerateRepository:
        """
        Creates a generate repository for the model.
        
        Returns:
            LlmGenerateRepository: A repository for text generation with the model.
        """
        pass
    
    @abstractmethod
    def create_embedding_repository(self) -> Optional[LlmEmbeddingRepository]:
        """
        Creates an embedding repository for the model.
        
        Returns:
            Optional[LlmEmbeddingRepository]: A repository for creating embeddings with the model,
                                             or None if the model doesn't support embeddings.
        """
        pass