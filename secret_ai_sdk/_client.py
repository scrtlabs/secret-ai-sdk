# client.py

"""
Module: Secret AI SDK Clients
"""

# base imports
from typing import Optional
import os

# third party imports
from ollama import AsyncClient as OllamaAsyncClient, Client as OllamaClient

# local imports
import secret_ai_sdk._config as _config
from secret_ai_sdk.secret_ai_ex import SecretAIAPIKeyMissingError


class SecretAIClient(OllamaClient):
    """
    Creates an ollama client.

    Arguments:
    - `host`: optional, Ollama URL
    - `api_key`: optional, Secret AI API Key. If none, will access the env var SECRET_AI_API_KEY
    `kwargs` are passed to the parent class + Authorization: Bearer API_KEY.
    """
    def __init__(self, host: Optional[str] = None, api_key: Optional[str] = None, **kwargs) -> None:
        if api_key is None:
            api_key = os.getenv(_config.API_KEY)

        if not api_key:
            raise SecretAIAPIKeyMissingError()

        auth: dict = {'Authorization':f'Bearer {api_key}'}
        kwargs['headers'] = auth
        super().__init__(host, **kwargs)


class SecretAIAsyncClient(OllamaAsyncClient):
    """
    Creates an async ollama client.

    Arguments:
    - `host`: optional, Ollama URL
    - `api_key`: optional, Secret AI API Key. If none, will access the env var SECRET_AI_API_KEY
    `kwargs` are passed to the parent class + Authorization: Bearer API_KEY.
    """
    def __init__(self, host: Optional[str] = None, api_key: Optional[str] = None, **kwargs) -> None:
        if api_key is None:
            api_key = os.getenv(_config.API_KEY)

        if not api_key:
            raise SecretAIAPIKeyMissingError()

        auth: dict = {'Authorization':f'Bearer {api_key}'}
        kwargs['headers'] = auth
        super().__init__(host, **kwargs)
