# secret_ai_ex.py

""" 
Module Secret AI SDK custom exceptions
"""

from typing import Optional, Any

# Exceptions
class SecretAIError(Exception):
    """Base exception class Secret AI SDK module."""
    def __init__(self, msg: str = 'Secret AI SDK error'):
        super().__init__(f'Secret AI SDK Error: {msg}')

class SecretAINotImplementedError(SecretAIError):
    """Raised when an unimplemented API is called."""
    def __init__(self):
        super().__init__('Not implemented')


class SecretAIInvalidInputError(SecretAIError):
    """Raised when invalid input is provided."""
    def __init__(self, msg: Optional[str] = None):
        super().__init__(msg or 'Invalid value')

class SecretAIAPIKeyMissingError(SecretAIError):
    """Raised when no API key is provided."""
    def __init__(self):
        super().__init__('Missing API Key. Environment variable SECRET_AI_API_KEY must be set')

class SecretAISecretValueMissingError(SecretAIError):
    """Raised when no key mnemonic is provided."""
    def __init__(self, var: str):
        super().__init__(f'Missing environment variable {var} must be set')

class SecretAINetworkError(SecretAIError):
    """Raised when a network operation fails."""
    def __init__(self, msg: str, original_error: Optional[Exception] = None):
        self.original_error = original_error
        super().__init__(f'Network error: {msg}')

class SecretAITimeoutError(SecretAINetworkError):
    """Raised when a request times out."""
    def __init__(self, timeout: float, operation: str = 'request'):
        super().__init__(f'{operation} timed out after {timeout} seconds')
        self.timeout = timeout

class SecretAIRetryExhaustedError(SecretAINetworkError):
    """Raised when all retry attempts have been exhausted."""
    def __init__(self, attempts: int, last_error: Optional[Exception] = None):
        self.attempts = attempts
        super().__init__(f'All {attempts} retry attempts failed', last_error)

class SecretAIResponseError(SecretAIError):
    """Raised when the response from the server is invalid or unexpected."""
    def __init__(self, msg: str, response_data: Optional[Any] = None):
        self.response_data = response_data
        super().__init__(f'Invalid response: {msg}')

class SecretAIConnectionError(SecretAINetworkError):
    """Raised when unable to establish a connection."""
    def __init__(self, host: str, original_error: Optional[Exception] = None):
        self.host = host
        super().__init__(f'Failed to connect to {host}', original_error)
