"""
Maiten AI - Learn better
API Client for Anthropic Claude

Cliente para comunicarse con la API de Claude.
"""

import os
import logging
from typing import List, Dict, Optional
from anthropic import Anthropic

logger = logging.getLogger(__name__)


class ClaudeAPIClient:
    """
    Cliente para la API de Anthropic Claude
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Inicializa el cliente de Claude API.
        
        Args:
            api_key: API key de Anthropic (si no se provee, se busca en env)
        """
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY not found. Set it in .env file")
        
        self.client = Anthropic(api_key=self.api_key)
        self.model = os.getenv("AI_MODEL", "claude-sonnet-4-20250514")
        self.max_tokens = int(os.getenv("AI_MAX_TOKENS", "2000"))
        self.temperature = float(os.getenv("AI_TEMPERATURE", "0.7"))
        
        logger.info(f"Claude API Client initialized with model: {self.model}")
    
    def create_message(
        self,
        messages: List[Dict[str, str]],
        system_prompt: Optional[str] = None,
        max_tokens: Optional[int] = None,
        temperature: Optional[float] = None
    ) -> Dict:
        """
        Crea un mensaje usando la API de Claude.
        
        Args:
            messages: Lista de mensajes en formato [{"role": "user", "content": "..."}]
            system_prompt: Prompt del sistema (opcional)
            max_tokens: Máximo de tokens en la respuesta
            temperature: Temperatura para la generación (0.0 a 1.0)
            
        Returns:
            Dict con la respuesta de Claude
        """
        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=max_tokens or self.max_tokens,
                temperature=temperature or self.temperature,
                system=system_prompt,
                messages=messages
            )
            
            logger.info(f"API call successful. Model: {response.model}, Tokens: {response.usage.input_tokens + response.usage.output_tokens}")
            
            return {
                "content": response.content[0].text,
                "role": response.role,
                "model": response.model,
                "stop_reason": response.stop_reason,
                "usage": {
                    "input_tokens": response.usage.input_tokens,
                    "output_tokens": response.usage.output_tokens
                }
            }
            
        except Exception as e:
            logger.error(f"Error calling Claude API: {e}")
            raise
    
    def create_streaming_message(
        self,
        messages: List[Dict[str, str]],
        system_prompt: Optional[str] = None,
        max_tokens: Optional[int] = None,
        temperature: Optional[float] = None
    ):
        """
        Crea un mensaje con streaming usando la API de Claude.
        
        Args:
            messages: Lista de mensajes
            system_prompt: Prompt del sistema
            max_tokens: Máximo de tokens
            temperature: Temperatura
            
        Yields:
            Chunks de texto a medida que se generan
        """
        try:
            with self.client.messages.stream(
                model=self.model,
                max_tokens=max_tokens or self.max_tokens,
                temperature=temperature or self.temperature,
                system=system_prompt,
                messages=messages
            ) as stream:
                for text in stream.text_stream:
                    yield text
                    
        except Exception as e:
            logger.error(f"Error in streaming API call: {e}")
            raise


# Singleton instance
_api_client: Optional[ClaudeAPIClient] = None


def get_api_client(api_key: Optional[str] = None) -> ClaudeAPIClient:
    """
    Obtiene la instancia singleton del ClaudeAPIClient.
    
    Args:
        api_key: API key de Anthropic
        
    Returns:
        ClaudeAPIClient: Instancia del cliente
    """
    global _api_client
    
    if _api_client is None:
        _api_client = ClaudeAPIClient(api_key)
    
    return _api_client
