# client.py

"""
Module: Secret AI SDK Clients
"""

# base imports
from typing import Optional
import os
import logging

# third party imports
from ollama import AsyncClient as OllamaAsyncClient, Client as OllamaClient

# local imports
import secret_ai_sdk._config as _config
from secret_ai_sdk.secret_ai_ex import SecretAIAPIKeyMissingError

logger = logging.getLogger(__name__)

# Try to import enhanced clients, fall back to basic if not available
try:
    from secret_ai_sdk._enhanced_client import (
        EnhancedSecretAIClient,
        EnhancedSecretAIAsyncClient
    )
    ENHANCED_CLIENTS_AVAILABLE = True
except ImportError:
    logger.debug("Enhanced clients not available, using basic clients")
    ENHANCED_CLIENTS_AVAILABLE = False


class SecretAIClient(OllamaClient):
    """
    Creates an ollama client with optional enhanced error handling.

    Arguments:
    - `host`: optional, Ollama URL
    - `api_key`: optional, Secret AI API Key. If none, will access the env var SECRET_AI_API_KEY
    - `use_enhanced`: optional, use enhanced client with retry logic (default: True if available)
    `kwargs` are passed to the parent class + Authorization: Bearer API_KEY.
    """
    def __new__(cls, host: Optional[str] = None, api_key: Optional[str] = None, 
                use_enhanced: bool = True, **kwargs):
        """
        Create either enhanced or basic client based on availability and preference.
        """
        if use_enhanced and ENHANCED_CLIENTS_AVAILABLE:
            logger.debug("Using enhanced SecretAI client with retry logic")
            return EnhancedSecretAIClient(host=host, api_key=api_key, **kwargs)
        else:
            # Return instance of current class using basic implementation
            return super().__new__(cls)
    
    def __init__(self, host: Optional[str] = None, api_key: Optional[str] = None, 
                 use_enhanced: bool = True, **kwargs) -> None:
        # Skip init if enhanced client was created
        if use_enhanced and ENHANCED_CLIENTS_AVAILABLE:
            return
            
        if api_key is None:
            api_key = os.getenv(_config.API_KEY)

        if not api_key:
            raise SecretAIAPIKeyMissingError()

        auth: dict = {'Authorization':f'Bearer {api_key}'}
        kwargs['headers'] = auth
        super().__init__(host, **kwargs)


class SecretAIAsyncClient(OllamaAsyncClient):
    """
    Creates an async ollama client with optional enhanced error handling.

    Arguments:
    - `host`: optional, Ollama URL
    - `api_key`: optional, Secret AI API Key. If none, will access the env var SECRET_AI_API_KEY
    - `use_enhanced`: optional, use enhanced client with retry logic (default: True if available)
    `kwargs` are passed to the parent class + Authorization: Bearer API_KEY.
    """
    def __new__(cls, host: Optional[str] = None, api_key: Optional[str] = None,
                use_enhanced: bool = True, **kwargs):
        """
        Create either enhanced or basic async client based on availability and preference.
        """
        if use_enhanced and ENHANCED_CLIENTS_AVAILABLE:
            logger.debug("Using enhanced SecretAI async client with retry logic")
            return EnhancedSecretAIAsyncClient(host=host, api_key=api_key, **kwargs)
        else:
            # Return instance of current class using basic implementation
            return super().__new__(cls)
    
    def __init__(self, host: Optional[str] = None, api_key: Optional[str] = None,
                 use_enhanced: bool = True, **kwargs) -> None:
        # Skip init if enhanced client was created
        if use_enhanced and ENHANCED_CLIENTS_AVAILABLE:
            return
            
        if api_key is None:
            api_key = os.getenv(_config.API_KEY)

        if not api_key:
            raise SecretAIAPIKeyMissingError()

        auth: dict = {'Authorization':f'Bearer {api_key}'}
        kwargs['headers'] = auth
        super().__init__(host, **kwargs)
