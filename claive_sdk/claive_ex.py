# claive_ex.py

""" 
Module Claive AI SDK custom exceptions
"""

# Exceptions
class ClaiveError(Exception):
    """Base exception class Claive SDK module."""
    def __init__(self, msg: str = 'Claive SDK error'):
        super().__init__(f'Claive SDK Error: {msg}')

class ClaiveInvalidInputError(ClaiveError):
    """Raised when invalid input is provided."""
    def __init__(self):
        super().__init__('Invalid value')

class ClaiveAPIKeyMissingError(ClaiveError):
    """Raised when no API key is provided."""
    def __init__(self):
        super().__init__('Missing API Key. Environment varialbe CLAIVE_AI_API_KEY must be set')

class ClaiveSecretValueMissingError(ClaiveError):
    """Raised when no key mnemonic is provided."""
    def __init__(self, var: str):
        super().__init__(f'Missing environment varialbe {var} must be set')
