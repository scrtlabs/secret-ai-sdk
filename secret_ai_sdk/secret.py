# secret.py

"""
Module: secret enables interactions with Secret worker management smart contract
"""
import binascii
import os
from typing import Optional, List

from secret_sdk.client.lcd import LCDClient
from secret_sdk.key.mnemonic import MnemonicKey

import secret_ai_sdk._config as cfg
from secret_ai_sdk.secret_ai_ex import SecretAISecretValueMissingError

class Secret:
    """
    Secret supports interactions with the worker management smart contract
    """
    def __init__(self, chain_id: Optional[str] = None, node_url: Optional[str] = None):
        if not chain_id:
            self.chain_id = os.getenv(cfg.SECRET_CHAIN_ID, cfg.SECRET_CHAIN_ID_DEFAULT)
            if not self.chain_id:
                raise SecretAISecretValueMissingError(cfg.SECRET_CHAIN_ID)
        else:
            self.chain_id = chain_id

        if not node_url:
            self.node_url = os.getenv(cfg.SECRET_NODE_URL, cfg.SECRET_NODE_URL_DEFAULT)
            if not self.node_url:
                raise SecretAISecretValueMissingError(cfg.SECRET_NODE_URL)
        else:
            self.node_url = node_url

        self.secret_client = LCDClient(chain_id=self.chain_id, url=self.node_url)

        self.smart_contract = os.getenv(
            cfg.SECRET_WORKER_SMART_CONTRACT, cfg.SECRET_WORKER_SMART_CONTRACT_DEFAULT)

    def get_priv_key_from_mnemonic(self, mnemonic: str) -> str:
        """
        Method get_priv_key_from_mnemonic returns a base16 encoded private key

        Arguments:
        - `mnemonic`:str - mnemonic as string

        Returns:
        - str: base16 encoded priv key  
        """
        mk = MnemonicKey(mnemonic=mnemonic)
        hex_key = binascii.hexlify(mk.private_key)
        return hex_key.decode('utf8')

    def get_models(self) -> List[str]:
        """
        Method get_models returns a list of models known to the worker management smart contract
                
        Returns:
        - List[str] - a list of models known to the smart contract
        
        Raises:
        - SecretAINetworkError: If the query fails after retries
        - SecretAIResponseError: If the response is malformed
        """
        from secret_ai_sdk.secret_ai_ex import SecretAINetworkError, SecretAIResponseError
        from secret_ai_sdk._retry import retry_with_backoff
        
        @retry_with_backoff(max_retries=3)
        def _query_models():
            query = {"get_models": {}}
            try:
                response = self.secret_client.wasm.contract_query(self.smart_contract, query)
                if not isinstance(response, dict) or 'models' not in response:
                    raise SecretAIResponseError(
                        "Invalid response format from smart contract",
                        response
                    )
                return response['models']
            except Exception as e:
                if isinstance(e, SecretAIResponseError):
                    raise
                raise SecretAINetworkError(f"Failed to query models: {str(e)}", e)
        
        return _query_models()


    def get_urls(self, model: Optional[str] = None) -> List[str]:
        """
        Method get_urls returns a list of urls known to Secret worker management 
        smart contract that host the given model
        
        Arguments:
        - `model`:str - a model to use when searching for the urls that host it

        Returns:
        - List[str]: - a list of urls that match the model search criteria, if provided,
                    or all urls known to Secret smart contract
        
        Raises:
        - SecretAINetworkError: If the query fails after retries
        - SecretAIResponseError: If the response is malformed
        """
        from secret_ai_sdk.secret_ai_ex import SecretAINetworkError, SecretAIResponseError
        from secret_ai_sdk._retry import retry_with_backoff
        
        @retry_with_backoff(max_retries=3)
        def _query_urls():
            if not model:
                query = {"get_u_r_ls": {}}
            else:
                query = {"get_u_r_ls": {"model": model}}
            
            try:
                response = self.secret_client.wasm.contract_query(self.smart_contract, query)
                if not isinstance(response, dict) or 'urls' not in response:
                    raise SecretAIResponseError(
                        "Invalid response format from smart contract",
                        response
                    )
                return response['urls']
            except Exception as e:
                if isinstance(e, SecretAIResponseError):
                    raise
                raise SecretAINetworkError(f"Failed to query URLs: {str(e)}", e)
        
        return _query_urls()
