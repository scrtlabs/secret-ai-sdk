# secret.py

"""
Module: secret enables interactions with Secret worker management smart contract
"""
import os
from typing import Optional, List

from secret_sdk.client.lcd import LCDClient
from secret_sdk.key.mnemonic import MnemonicKey
import secp256k1

import claive_sdk._config as cfg
from claive_sdk.claive_ex import ClaiveSecretValueMissingError

class SecretClaive:
    """
    SecretClaive supports interactions with the worker management smart contract
    """
    def __init__(self, chain_id: Optional[str] = None, node_url: Optional[str] = None):
        if not chain_id:
            self.chain_id = os.getenv(cfg.SECRET_CHAIN_ID, cfg.SECRET_CHAIN_ID_DEFAULT)
            if not self.chain_id:
                raise ClaiveSecretValueMissingError(cfg.SECRET_CHAIN_ID)
        else:
            self.chain_id = chain_id

        if not node_url:
            self.node_url = os.getenv(cfg.SECRET_NODE_URL, cfg.SECRET_NODE_URL_DEFAULT)
            if not self.node_url:
                raise ClaiveSecretValueMissingError(cfg.SECRET_NODE_URL)
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
        pk = secp256k1.PrivateKey(mk.private_key)
        return pk.serialize()

    def get_models(self) -> List[str]:
        """
        Method get_models returns a list of models known to the worker management smart contract
                
        Returns:
        - List[str] - a list of models known to the smart contract
        """
        query = {"get_models": {}}
        models = self.secret_client.wasm.contract_query(self.smart_contract, query)
        return models['models']


    def get_urls(self, model: Optional[str] = None) -> List[str]:
        """
        Method get_urls returns a list of urls known to Secret worker management 
        smart contract that host the given model
        
        Arguments:
        - `model`:str - a model to use when searching for the urls that host it

        Returns:
        - List[str]: - a list of urls that match the model search criteria, if provided,
                    or all urls known to Secret smart contract
        """
        if not model:
            query = {"get_u_r_ls": {}}
        else:
            query = {"get_u_r_ls": {"model": model}}
        urls = self.secret_client.wasm.contract_query(self.smart_contract, query)
        return urls['urls']
