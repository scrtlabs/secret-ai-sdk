# secret_ai.py

"""
Module Secret AI SDK
================

Secret AI SDK module serves the purpose of connecting to Secret AI Confidential LLM.

Author: Alex H
Email: alexh@scrtlabs.com
Version: 0.1
"""

# base imports
from typing import Self, Dict
import logging
import os

# third party imports
from pydantic import model_validator
from langchain_ollama.chat_models import ChatOllama

# local imports
from secret_ai_sdk._enhanced_client import EnhancedSecretAIClient, EnhancedSecretAIAsyncClient
import secret_ai_sdk._config as _config

# Get the log level from the environment variable
log_level_name = os.environ.get(_config.LOG_LEVEL, 'info').lower()

# Set the logging level
if log_level_name in _config.LOG_LEVELS:
    logging.basicConfig(level=_config.LOG_LEVELS[log_level_name])
else:
    print(f"Invalid log level: {log_level_name}. Defaulting to INFO.")
    logging.basicConfig(level=logging.INFO)

# Test the logging levels
logger = logging.getLogger(__name__)

logger.fatal = logger.critical  # Add a fatal method to the logger

class ChatSecret(ChatOllama):
    """
    Secret AI Chat client
    """
    @model_validator(mode="after")
    def _set_clients(self) -> Self:
        """Override the _set_clients method."""
        # Call the parent class method
        super()._set_clients()
        client_kwargs = self.client_kwargs or {}
        # Secret AI Client
        self._client = EnhancedSecretAIClient(host=self.base_url, **client_kwargs)
        # Secret AI Async Client
        self._async_client = EnhancedSecretAIAsyncClient(host=self.base_url, **client_kwargs)

        return self

    def get_attestation(self) -> Dict:
        """ method returns the attestation report"""
        return {} # Not implemented yet

# Main entry point (if applicable)
if __name__ == "__main__":
    # example usage
    pass