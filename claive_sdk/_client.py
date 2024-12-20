# client.py

"""
Module: Claive AI SDK Clients
"""

# base imports
from typing import Optional
import os

# third party imports
from ollama import AsyncClient as OllamaAsyncClient, Client as OllamaClient

# local imports
import claive_sdk._config as _config
from claive_sdk.claive_ex import ClaiveAPIKeyMissingError


class ClaiveClient(OllamaClient):
    """
    Creates an ollama client.

    Arguments:
    - `host`: optional, Ollama URL
    - `api_key`: optional, Claive AI API Key. If none, will access the env var CLAIVE_AI_API_KEY
    `kwargs` are passed to the parent class + Authorization: Bearer API_KEY.
    """
    def __init__(self, host: Optional[str] = None, api_key: Optional[str] = None, **kwargs) -> None:
        if api_key is None:
            api_key = os.getenv(_config.API_KEY)

        if not api_key:
            raise ClaiveAPIKeyMissingError()

        auth: dict = {'Authorization':f'Bearer {api_key}'}
        kwargs['headers'] = auth
        super().__init__(host, **kwargs)


class ClaiveAsyncClient(OllamaAsyncClient):
    """
    Creates an async ollama client.

    Arguments:
    - `host`: optional, Ollama URL
    - `api_key`: optional, Claive AI API Key. If none, will access the env var CLAIVE_AI_API_KEY
    `kwargs` are passed to the parent class + Authorization: Bearer API_KEY.
    """
    def __init__(self, host: Optional[str] = None, api_key: Optional[str] = None, **kwargs) -> None:
        if api_key is None:
            api_key = os.getenv(_config.API_KEY)

        if not api_key:
            raise ClaiveAPIKeyMissingError()

        auth: dict = {'Authorization':f'Bearer {api_key}'}
        kwargs['headers'] = auth
        super().__init__(host, **kwargs)
