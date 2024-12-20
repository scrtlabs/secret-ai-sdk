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


    def get_models(self, priv_key: str) -> List[str]:
        """
        Method get_models returns a list of models known to the worker management smart contract
        
        Arguments:
        - `priv_key`:str - a base16 encoded user wallet's private key value to sign the request with
        
        Returns:
        - List[str] - a list of models known to the smart contract
        """
        secp_prk = secp256k1.PrivateKey(bytes.fromhex(priv_key))
        puk = secp_prk.pubkey.serialize()
        sig = secp_prk.ecdsa_serialize_compact(secp_prk.ecdsa_sign(puk))
        query = {"get_models": {"signature": sig.hex(), "subscriber_public_key": puk.hex()}}
        models = self.secret_client.wasm.contract_query(self.smart_contract, query)
        return models['models']


    def get_urls(self, priv_key: str, model: Optional[str] = None) -> List[str]:
        """
        Method get_urls returns a list of urls known to Secret worker management 
        smart contract that host the given model
        
        Arguments:
        - `priv_key`:str - a base16 encoded user wallet's private key value to sign the request with
        - `model`:str - a model to use when searching for the urls that host it

        Returns:
        - List[str]: - a list of urls that match the model search criteria, if provided,
                    or all urls known to Secret smart contract
        """
        secp_prk = secp256k1.PrivateKey(bytes.fromhex(priv_key))
        puk = secp_prk.pubkey.serialize()
        sig = secp_prk.ecdsa_serialize_compact(secp_prk.ecdsa_sign(puk))
        if not model:
            query = {"get_u_r_ls": {"signature": sig.hex(), \
                                    "subscriber_public_key": puk.hex()}}
        else:
            query = {"get_u_r_ls": {"signature": sig.hex(), \
                                    "subscriber_public_key": puk.hex(), "model": model}}
        urls = self.secret_client.wasm.contract_query(self.smart_contract, query)
        return urls['urls']
