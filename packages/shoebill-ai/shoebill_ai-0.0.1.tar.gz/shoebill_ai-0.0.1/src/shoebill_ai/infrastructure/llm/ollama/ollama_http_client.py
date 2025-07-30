import requests
from typing import Dict, Any, Optional


class OllamaHttpClient:
    """
    Base HTTP client for the Ollama API.
    Handles authentication and common request functionality.
    """
    
    def __init__(self, api_url: str, api_token: str = None):
        """
        Initialize a new OllamaHttpClient.
        
        Args:
            api_url: The base URL of the Ollama API.
            api_token: Optional API token for authentication.
        """
        self.api_url = api_url.rstrip('/')
        self.api_token = api_token
    
    def _get_headers(self) -> Dict[str, str]:
        """
        Get the headers for the request, including authentication if available.
        
        Returns:
            Dict[str, str]: The headers for the request.
        """
        headers = {}
        if self.api_token:
            headers["Authorization"] = f"Bearer {self.api_token}"
        return headers
    
    def post(self, endpoint: str, payload: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Send a POST request to the Ollama API.
        
        Args:
            endpoint: The endpoint to send the request to (without the base URL).
            payload: The payload to send with the request.
            
        Returns:
            Optional[Dict[str, Any]]: The JSON response from the API, or None if the request failed.
        """
        url = f"{self.api_url}/{endpoint}"
        headers = self._get_headers()
        
        try:
            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error during Ollama API call to {endpoint}: {e}")
            return None