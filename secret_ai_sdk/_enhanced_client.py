# _enhanced_client.py

"""
Module: Enhanced Secret AI SDK Clients with retry logic and better error handling
"""

import os
import logging
from typing import Optional, Dict, Any
import httpx
from httpx import Timeout

from ollama import AsyncClient as OllamaAsyncClient, Client as OllamaClient

import secret_ai_sdk._config as _config
from secret_ai_sdk.secret_ai_ex import (
    SecretAIAPIKeyMissingError,
    SecretAIConnectionError,
    SecretAITimeoutError,
    SecretAIResponseError,
    SecretAINetworkError
)
from secret_ai_sdk._retry import (
    retry_with_backoff,
    get_timeout_config,
    get_retry_config
)

logger = logging.getLogger(__name__)


class EnhancedSecretAIClient(OllamaClient):
    """
    Enhanced Ollama client with retry logic, timeouts, and better error handling.
    
    Arguments:
    - `host`: optional, Ollama URL
    - `api_key`: optional, Secret AI API Key. If none, will access the env var SECRET_AI_API_KEY
    - `timeout`: optional, request timeout in seconds
    - `connect_timeout`: optional, connection timeout in seconds
    - `max_retries`: optional, maximum number of retry attempts
    - `retry_delay`: optional, initial retry delay in seconds
    - `retry_backoff`: optional, retry backoff multiplier
    - `validate_responses`: optional, whether to validate response format (default: True)
    `kwargs` are passed to the parent class + Authorization: Bearer API_KEY.
    """
    
    def __init__(
        self,
        host: Optional[str] = None,
        api_key: Optional[str] = None,
        timeout: Optional[float] = None,
        connect_timeout: Optional[float] = None,
        max_retries: Optional[int] = None,
        retry_delay: Optional[float] = None,
        retry_backoff: Optional[float] = None,
        validate_responses: bool = True,
        **kwargs
    ) -> None:
        # Get API key
        if api_key is None:
            api_key = os.getenv(_config.API_KEY)
        
        if not api_key:
            raise SecretAIAPIKeyMissingError()
        
        # Get timeout configuration
        timeout_config = get_timeout_config()
        self.request_timeout = timeout if timeout is not None else timeout_config['request_timeout']
        self.connect_timeout = connect_timeout if connect_timeout is not None else timeout_config['connect_timeout']
        
        # Get retry configuration
        retry_config = get_retry_config()
        self.max_retries = max_retries if max_retries is not None else retry_config['max_retries']
        self.retry_delay = retry_delay if retry_delay is not None else retry_config['initial_delay']
        self.retry_backoff = retry_backoff if retry_backoff is not None else retry_config['backoff_multiplier']
        
        self.validate_responses = validate_responses
        self.host = host
        
        # Set up authentication header
        auth: Dict[str, str] = {'Authorization': f'Bearer {api_key}'}
        kwargs['headers'] = {**kwargs.get('headers', {}), **auth}
        
        # Configure timeout for the underlying client
        kwargs['timeout'] = Timeout(
            timeout=self.request_timeout,
            connect=self.connect_timeout
        )
        
        try:
            super().__init__(host, **kwargs)
        except Exception as e:
            logger.error(f"Failed to initialize client for host {host}: {e}")
            raise SecretAIConnectionError(host or "default", e)
        
        logger.info(f"Initialized EnhancedSecretAIClient with host: {host}, "
                   f"timeout: {self.request_timeout}s, max_retries: {self.max_retries}")
    
    def _validate_response(self, response: Any) -> None:
        """
        Validate the response format and content.
        
        Args:
            response: The response to validate
            
        Raises:
            SecretAIResponseError: If the response is invalid
        """
        if not self.validate_responses:
            return
        
        if response is None:
            raise SecretAIResponseError("Received null response", response)
        
        # Check for common error indicators
        if isinstance(response, dict):
            if 'error' in response:
                raise SecretAIResponseError(f"Server returned error: {response['error']}", response)
            
            # Validate expected fields based on response type
            if 'message' in response and 'content' not in response.get('message', {}):
                logger.warning("Response message missing 'content' field")
    
    @retry_with_backoff()
    def generate(self, *args, **kwargs) -> Any:
        """
        Generate a response with retry logic and error handling.
        """
        try:
            response = super().generate(*args, **kwargs)
            self._validate_response(response)
            return response
        except httpx.TimeoutException as e:
            logger.error(f"Request timed out: {e}")
            raise SecretAITimeoutError(self.request_timeout, "generate")
        except httpx.ConnectError as e:
            logger.error(f"Connection failed: {e}")
            raise SecretAIConnectionError(self.host or "default", e)
        except Exception as e:
            if isinstance(e, (SecretAITimeoutError, SecretAIConnectionError, SecretAIResponseError)):
                raise
            logger.error(f"Unexpected error during generate: {e}")
            raise SecretAINetworkError(f"Generate failed: {str(e)}", e)
    
    @retry_with_backoff()
    def chat(self, *args, **kwargs) -> Any:
        """
        Chat with retry logic and error handling.
        """
        try:
            response = super().chat(*args, **kwargs)
            self._validate_response(response)
            return response
        except httpx.TimeoutException as e:
            logger.error(f"Chat request timed out: {e}")
            raise SecretAITimeoutError(self.request_timeout, "chat")
        except httpx.ConnectError as e:
            logger.error(f"Chat connection failed: {e}")
            raise SecretAIConnectionError(self.host or "default", e)
        except Exception as e:
            if isinstance(e, (SecretAITimeoutError, SecretAIConnectionError, SecretAIResponseError)):
                raise
            logger.error(f"Unexpected error during chat: {e}")
            raise SecretAINetworkError(f"Chat failed: {str(e)}", e)
    
    def _handle_stream_error(self, error: Exception, operation: str = "stream"):
        """Handle errors during streaming operations."""
        if isinstance(error, httpx.TimeoutException):
            raise SecretAITimeoutError(self.request_timeout, operation)
        elif isinstance(error, httpx.ConnectError):
            raise SecretAIConnectionError(self.host or "default", error)
        elif not isinstance(error, (SecretAITimeoutError, SecretAIConnectionError, SecretAIResponseError)):
            raise SecretAINetworkError(f"{operation} failed: {str(error)}", error)
        raise error


class EnhancedSecretAIAsyncClient(OllamaAsyncClient):
    """
    Enhanced async Ollama client with retry logic, timeouts, and better error handling.
    
    Arguments:
    - `host`: optional, Ollama URL
    - `api_key`: optional, Secret AI API Key. If none, will access the env var SECRET_AI_API_KEY
    - `timeout`: optional, request timeout in seconds
    - `connect_timeout`: optional, connection timeout in seconds
    - `max_retries`: optional, maximum number of retry attempts
    - `retry_delay`: optional, initial retry delay in seconds
    - `retry_backoff`: optional, retry backoff multiplier
    - `validate_responses`: optional, whether to validate response format (default: True)
    `kwargs` are passed to the parent class + Authorization: Bearer API_KEY.
    """
    
    def __init__(
        self,
        host: Optional[str] = None,
        api_key: Optional[str] = None,
        timeout: Optional[float] = None,
        connect_timeout: Optional[float] = None,
        max_retries: Optional[int] = None,
        retry_delay: Optional[float] = None,
        retry_backoff: Optional[float] = None,
        validate_responses: bool = True,
        **kwargs
    ) -> None:
        # Get API key
        if api_key is None:
            api_key = os.getenv(_config.API_KEY)
        
        if not api_key:
            raise SecretAIAPIKeyMissingError()
        
        # Get timeout configuration
        timeout_config = get_timeout_config()
        self.request_timeout = timeout if timeout is not None else timeout_config['request_timeout']
        self.connect_timeout = connect_timeout if connect_timeout is not None else timeout_config['connect_timeout']
        
        # Get retry configuration
        retry_config = get_retry_config()
        self.max_retries = max_retries if max_retries is not None else retry_config['max_retries']
        self.retry_delay = retry_delay if retry_delay is not None else retry_config['initial_delay']
        self.retry_backoff = retry_backoff if retry_backoff is not None else retry_config['backoff_multiplier']
        
        self.validate_responses = validate_responses
        self.host = host
        
        # Set up authentication header
        auth: Dict[str, str] = {'Authorization': f'Bearer {api_key}'}
        kwargs['headers'] = {**kwargs.get('headers', {}), **auth}
        
        # Configure timeout for the underlying client
        kwargs['timeout'] = Timeout(
            timeout=self.request_timeout,
            connect=self.connect_timeout
        )
        
        try:
            super().__init__(host, **kwargs)
        except Exception as e:
            logger.error(f"Failed to initialize async client for host {host}: {e}")
            raise SecretAIConnectionError(host or "default", e)
        
        logger.info(f"Initialized EnhancedSecretAIAsyncClient with host: {host}, "
                   f"timeout: {self.request_timeout}s, max_retries: {self.max_retries}")
    
    def _validate_response(self, response: Any) -> None:
        """
        Validate the response format and content.
        
        Args:
            response: The response to validate
            
        Raises:
            SecretAIResponseError: If the response is invalid
        """
        if not self.validate_responses:
            return
        
        if response is None:
            raise SecretAIResponseError("Received null response", response)
        
        # Check for common error indicators
        if isinstance(response, dict):
            if 'error' in response:
                raise SecretAIResponseError(f"Server returned error: {response['error']}", response)
            
            # Validate expected fields based on response type
            if 'message' in response and 'content' not in response.get('message', {}):
                logger.warning("Response message missing 'content' field")
    
    @retry_with_backoff()
    async def generate(self, *args, **kwargs) -> Any:
        """
        Generate a response with retry logic and error handling.
        """
        try:
            response = await super().generate(*args, **kwargs)
            self._validate_response(response)
            return response
        except httpx.TimeoutException as e:
            logger.error(f"Request timed out: {e}")
            raise SecretAITimeoutError(self.request_timeout, "generate")
        except httpx.ConnectError as e:
            logger.error(f"Connection failed: {e}")
            raise SecretAIConnectionError(self.host or "default", e)
        except Exception as e:
            if isinstance(e, (SecretAITimeoutError, SecretAIConnectionError, SecretAIResponseError)):
                raise
            logger.error(f"Unexpected error during generate: {e}")
            raise SecretAINetworkError(f"Generate failed: {str(e)}", e)
    
    @retry_with_backoff()
    async def chat(self, *args, **kwargs) -> Any:
        """
        Chat with retry logic and error handling.
        """
        try:
            response = await super().chat(*args, **kwargs)
            self._validate_response(response)
            return response
        except httpx.TimeoutException as e:
            logger.error(f"Chat request timed out: {e}")
            raise SecretAITimeoutError(self.request_timeout, "chat")
        except httpx.ConnectError as e:
            logger.error(f"Chat connection failed: {e}")
            raise SecretAIConnectionError(self.host or "default", e)
        except Exception as e:
            if isinstance(e, (SecretAITimeoutError, SecretAIConnectionError, SecretAIResponseError)):
                raise
            logger.error(f"Unexpected error during chat: {e}")
            raise SecretAINetworkError(f"Chat failed: {str(e)}", e)
    
    def _handle_stream_error(self, error: Exception, operation: str = "stream"):
        """Handle errors during streaming operations."""
        if isinstance(error, httpx.TimeoutException):
            raise SecretAITimeoutError(self.request_timeout, operation)
        elif isinstance(error, httpx.ConnectError):
            raise SecretAIConnectionError(self.host or "default", error)
        elif not isinstance(error, (SecretAITimeoutError, SecretAIConnectionError, SecretAIResponseError)):
            raise SecretAINetworkError(f"{operation} failed: {str(error)}", error)
        raise error