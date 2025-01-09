# test_claive.py 
"""
claive sdk test module
"""
import os
import unittest
from claive_sdk.secret import SecretClaive
from claive_sdk.claive import ChatClaive

# pylint: disable=line-too-long
TEST_MNEMONIC = 'grant rice replace explain federal release fix clever romance raise often wild taxi quarter soccer fiber love must tape steak together observe swap guitar'

TEST_KNOWN_MODEL = 'llama3.1:70b' # a known confidential LLM model

TEST_KNOWN_API_KEY = 'dGVzdEBzY3J0bGFicy5jb206Q0xBSVZFLUFJLUFQSS1LRVktMTIzNC01Njc4OTAtMDAwMAo=' # a known to work API key

class TestClaiveFunctions(unittest.TestCase):
    """
    Test class to test Claive SDK functionality
    """
    def test_claive(self):
        """
        test - verify that a connection with a confidential LLM can be establsished
            and a query can be successfully processed
        """
        secret_client = SecretClaive()
        models = secret_client.get_models()
        self.assertGreaterEqual(len(models), 1)
        urls = secret_client.get_urls(model=TEST_KNOWN_MODEL)
        self.assertGreaterEqual(len(urls), 1)

        claive_llm = ChatClaive(
            base_url=urls[0],
            model=TEST_KNOWN_MODEL,
            temperature=1.
        )
        attestation = claive_llm.get_attestation()
        self.assertIsNotNone(attestation)
        messages = [
            (
                "system",
                "You are a helpful assistant that translates English to French. Translate the user sentence.",
            ),
            ("human", "I love programming."),
        ]
        response = claive_llm.invoke(messages, stream=False)
        self.assertIsNotNone(response)
        self.assertGreater(len(response.content), 0)
        print(response.content)

if __name__ == '__main__':
    unittest.main()