# registry.py

"""
Module Claive AI SDK Registry
Module allows SDK clients to query Claive AI infrastructure 
for the deployed models and LLM instances
"""

from typing import List, Optional

from claive_sdk._config import DEFAULT_LLM_MODEL, DEFAULT_LLM_URL

class RegistryClaive():
    """
    RegistryClaive is a collection of registry query methods
    """

    @staticmethod
    def get_models() -> List[str]:
        """
        get_modles - returns a list of all registered models

        Returns:
        - List[str]: a list of models known to the registry
        """
        return [DEFAULT_LLM_MODEL]

    @staticmethod
    def get_urls(model: Optional[str]) -> List[str]:
        # pylint: disable=unused-argument
        """
        get_urls - returns a list of urls that match the specified model

        Arguments:
        - `model`: Optional[str] the name of of a model of interest

        Returns:
        - List[str]: a list of LLM URLs that implement this model 
        """
        return [DEFAULT_LLM_URL]