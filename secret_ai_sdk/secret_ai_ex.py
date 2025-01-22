# secret_ai_ex.py

""" 
Module Secret AI SDK custom exceptions
"""

# Exceptions
class SecretAIError(Exception):
    """Base exception class Secret AI SDK module."""
    def __init__(self, msg: str = 'Secret AI SDK error'):
        super().__init__(f'Secret AI SDK Error: {msg}')

class SecretAIInvalidInputError(SecretAIError):
    """Raised when invalid input is provided."""
    def __init__(self):
        super().__init__('Invalid value')

class SecretAIAPIKeyMissingError(SecretAIError):
    """Raised when no API key is provided."""
    def __init__(self):
        super().__init__('Missing API Key. Environment variable SECRET_AI_API_KEY must be set')

class SecretAISecretValueMissingError(SecretAIError):
    """Raised when no key mnemonic is provided."""
    def __init__(self, var: str):
        super().__init__(f'Missing environment variable {var} must be set')
