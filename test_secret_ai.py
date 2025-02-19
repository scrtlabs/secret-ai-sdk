# test_secret_ai.py
"""
secret-ai sdk test module
"""
import os
import unittest
from secret_ai_sdk.secret import Secret
from secret_ai_sdk.secret_ai import ChatSecret

# pylint: disable=line-too-long
TEST_MNEMONIC = 'grant rice replace explain federal release fix clever romance raise often wild taxi quarter soccer fiber love must tape steak together observe swap guitar'

TEST_KNOWN_MODEL = 'deepseek-r1:70b' # a known confidential LLM model

TEST_KNOWN_API_KEY = 'bWFzdGVyQHNjcnRsYWJzLmNvbTpTZWNyZXROZXR3b3JrTWFzdGVyS2V5X18yMDI1' # a known to work API key

class TestSecretAIFunctions(unittest.TestCase):
    """
    Test class to test Secret AI SDK functionality
    """
    def test_secret_ai(self):
        """
        test - verify that a connection with a confidential LLM can be establsished
            and a query can be successfully processed
        """
        secret_client = Secret()
        models = secret_client.get_models()
        self.assertGreaterEqual(len(models), 1)
        urls = secret_client.get_urls(model=TEST_KNOWN_MODEL)
        self.assertGreaterEqual(len(urls), 1)

        secret_ai_llm = ChatSecret(
            base_url=urls[0],
            model=TEST_KNOWN_MODEL,
            temperature=1.
        )
        messages = [
            (
                "system",
                "You are a helpful assistant that translates English to French. Translate the user sentence.",
            ),
            ("human", "I love programming."),
        ]
        response = secret_ai_llm.invoke(messages, stream=False)
        self.assertIsNotNone(response)
        self.assertGreater(len(response.content), 0)
        print(response.content)

if __name__ == '__main__':
    unittest.main()