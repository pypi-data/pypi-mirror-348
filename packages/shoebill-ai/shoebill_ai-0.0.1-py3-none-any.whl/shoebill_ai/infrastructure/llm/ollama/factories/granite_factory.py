from typing import Optional

from .....domain.model_factory import ModelFactory
from .....domain.reasoning.llm_chat_repository import LlmChatRepository
from .....domain.reasoning.llm_embedding_repository import LlmEmbeddingRepository
from .....domain.reasoning.llm_generate_respository import LlmGenerateRepository
from ....llm.template_loader import TemplateLoader
from ..ollama_chat_repository import OllamaChatRepository
from ..ollama_generate_repository import OllamaGenerateRepository


class GraniteModelFactory(ModelFactory):
    """
    Factory for creating repositories for the Granite 3.3:8b model.
    """

    MODEL_NAME = "granite3.3:8b"

    def __init__(self, api_url: str, temperature: float = 0.6, max_tokens: int = 2500, 
                 api_token: str = None, use_templating: bool = True):
        """
        Initialize a new GraniteModelFactory.

        Args:
            api_url: The base URL of the Ollama API.
            temperature: The temperature to use for generation.
            max_tokens: The maximum number of tokens to generate.
            api_token: Optional API token for authentication.
            use_templating: Whether to use Jinja2 templating for prompt formatting.
        """
        self.api_url = api_url
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.api_token = api_token
        self.use_templating = use_templating

        # Create a template loader if templating is enabled
        if use_templating:
            self.template_loader = TemplateLoader()

    def create_chat_repository(self) -> LlmChatRepository:
        """
        Creates a chat repository for the Granite model.

        Returns:
            LlmChatRepository: A repository for chat interactions with the Granite model.
        """
        kwargs = {
            "api_url": self.api_url,
            "model_name": self.MODEL_NAME,
            "temperature": self.temperature,
            "api_token": self.api_token,
            "use_templating": self.use_templating
        }

        # Add template loader if templating is enabled
        if self.use_templating and hasattr(self, 'template_loader'):
            kwargs["template_loader"] = self.template_loader

        return OllamaChatRepository(**kwargs)

    def create_generate_repository(self) -> LlmGenerateRepository:
        """
        Creates a generate repository for the Granite model.

        Returns:
            LlmGenerateRepository: A repository for text generation with the Granite model.
        """
        kwargs = {
            "api_url": self.api_url,
            "model_name": self.MODEL_NAME,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "api_token": self.api_token,
            "use_templating": self.use_templating
        }

        # Add template loader if templating is enabled
        if self.use_templating and hasattr(self, 'template_loader'):
            kwargs["template_loader"] = self.template_loader

        return OllamaGenerateRepository(**kwargs)

    def create_embedding_repository(self) -> Optional[LlmEmbeddingRepository]:
        """
        Granite model doesn't support embeddings, so this returns None.

        Returns:
            Optional[LlmEmbeddingRepository]: None, as Granite doesn't support embeddings.
        """
        return None
