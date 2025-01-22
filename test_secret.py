# test_secret.py 
"""
secret test module
"""

import unittest
from secret_ai_sdk.secret import SecretWorker

# pylint: disable=line-too-long
TEST_MNEMONIC = 'grant rice replace explain federal release fix clever romance raise often wild taxi quarter soccer fiber love must tape steak together observe swap guitar'
TEST_PK = 'f0a7b67eb9a719d54f8a9bfbfb187d8c296b97911a05bf5ca30494823e46beb6'
TEST_KNOWN_MODEL = 'llama3.1:70b'
TEST_KNOWN_URL = 'https://ai1.myclaive.com:21434'

class TestSecretFunctions(unittest.TestCase):
    """
    Test class to test Secret smart contract interactions functionality
    """
    def test_priv_key_from_mnemonic(self):
        """
        Test: priv_key_from_mnemonic - check if private key can be successfully
            generated from the provided mnemonic
        """
        secret_client = SecretWorker()
        pk_hex = secret_client.get_priv_key_from_mnemonic(mnemonic=TEST_MNEMONIC)
        self.assertEqual(pk_hex, TEST_PK)

    def test_get_models(self):
        """
        Test: get_models - check if we can successfully obtain a list of known
            confidential LLM models
        """
        secret_client = SecretWorker()
        models = secret_client.get_models()
        self.assertGreaterEqual(len(models), 1)
        self.assertTrue(TEST_KNOWN_MODEL in models)

    def test_get_urls(self):
        """
        Test: get_urls - check if we can successfully obtain a list of known
            confidential LLM urls
        """
        secret_client = SecretWorker()
        pk_hex = secret_client.get_priv_key_from_mnemonic(mnemonic=TEST_MNEMONIC)
        urls = secret_client.get_urls(pk_hex)
        self.assertGreaterEqual(len(urls), 1)
        self.assertTrue(TEST_KNOWN_URL in urls)

    def test_get_urls_for_model(self):
        """
        Test: get_urls_for_model - check if we can successfully obtain a list of known
            confidential LLM urls based on the given model
        """
        secret_client = SecretWorker()
        urls = secret_client.get_urls(model=TEST_KNOWN_MODEL)
        self.assertGreaterEqual(len(urls), 1)
        self.assertTrue(TEST_KNOWN_URL in urls)

if __name__ == '__main__':
    unittest.main()