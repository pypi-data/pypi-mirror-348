from typing import Optional, List

from ....domain.reasoning.llm_embedding_repository import LlmEmbeddingRepository
from .ollama_http_client import OllamaHttpClient


class OllamaEmbeddingRepository(LlmEmbeddingRepository):
    """
    Repository for creating embeddings using the Ollama API.
    """

    def __init__(self, api_url: str, model_name: str, api_token: str = None):
        """
        Initialize a new OllamaEmbeddingRepository.

        Args:
            api_url: The base URL of the Ollama API.
            model_name: The name of the model to use.
            api_token: Optional API token for authentication.
        """
        self.model_name = model_name
        self.http_client = OllamaHttpClient(api_url, api_token)

    def embed(self, text: str) -> Optional[List[float]]:
        """
        Create an embedding for the given text using the Ollama API.

        Args:
            text: The text to create an embedding for.

        Returns:
            Optional[List[float]]: The embedding vector, or None if the request failed.
        """
        payload = {
            "model": self.model_name,
            "prompt": text
        }

        response_data = self.http_client.post("embeddings", payload)
        if response_data:
            return response_data.get("embedding")

        return None
