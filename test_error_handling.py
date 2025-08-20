#!/usr/bin/env python3
"""
Test module for Secret AI SDK error handling and retry logic
"""

import unittest
import os
import time
from unittest.mock import Mock, patch, MagicMock
import asyncio

# Import the modules we're testing
from secret_ai_sdk.secret_ai_ex import (
    SecretAIError,
    SecretAINetworkError,
    SecretAITimeoutError,
    SecretAIRetryExhaustedError,
    SecretAIResponseError,
    SecretAIConnectionError,
    SecretAIAPIKeyMissingError
)
from secret_ai_sdk._retry import (
    calculate_delay,
    is_retryable_error,
    retry_with_backoff,
    get_retry_config,
    get_timeout_config
)
from secret_ai_sdk._config import (
    MAX_RETRIES_DEFAULT,
    RETRY_DELAY_DEFAULT,
    RETRY_BACKOFF_DEFAULT,
    REQUEST_TIMEOUT_DEFAULT,
    CONNECT_TIMEOUT_DEFAULT
)


class TestErrorClasses(unittest.TestCase):
    """Test custom exception classes"""
    
    def test_network_error(self):
        """Test SecretAINetworkError"""
        original_error = ValueError("Original error")
        error = SecretAINetworkError("Network failed", original_error)
        self.assertIn("Network error: Network failed", str(error))
        self.assertEqual(error.original_error, original_error)
    
    def test_timeout_error(self):
        """Test SecretAITimeoutError"""
        error = SecretAITimeoutError(30.0, "chat")
        self.assertIn("chat timed out after 30.0 seconds", str(error))
        self.assertEqual(error.timeout, 30.0)
    
    def test_retry_exhausted_error(self):
        """Test SecretAIRetryExhaustedError"""
        last_error = ValueError("Last attempt failed")
        error = SecretAIRetryExhaustedError(3, last_error)
        self.assertIn("All 3 retry attempts failed", str(error))
        self.assertEqual(error.attempts, 3)
        self.assertEqual(error.original_error, last_error)
    
    def test_response_error(self):
        """Test SecretAIResponseError"""
        response_data = {"error": "Invalid format"}
        error = SecretAIResponseError("Bad response", response_data)
        self.assertIn("Invalid response: Bad response", str(error))
        self.assertEqual(error.response_data, response_data)
    
    def test_connection_error(self):
        """Test SecretAIConnectionError"""
        original_error = ConnectionError("Connection refused")
        error = SecretAIConnectionError("localhost:8080", original_error)
        self.assertIn("Failed to connect to localhost:8080", str(error))
        self.assertEqual(error.host, "localhost:8080")


class TestRetryLogic(unittest.TestCase):
    """Test retry logic utilities"""
    
    def test_calculate_delay(self):
        """Test exponential backoff delay calculation"""
        # Test basic exponential backoff
        self.assertEqual(calculate_delay(0, 1.0, 2.0, 100.0), 1.0)
        self.assertEqual(calculate_delay(1, 1.0, 2.0, 100.0), 2.0)
        self.assertEqual(calculate_delay(2, 1.0, 2.0, 100.0), 4.0)
        self.assertEqual(calculate_delay(3, 1.0, 2.0, 100.0), 8.0)
        
        # Test max delay cap
        self.assertEqual(calculate_delay(10, 1.0, 2.0, 10.0), 10.0)
    
    def test_is_retryable_error(self):
        """Test error retryability detection"""
        # Retryable errors
        self.assertTrue(is_retryable_error(SecretAINetworkError("Network error")))
        self.assertTrue(is_retryable_error(SecretAITimeoutError(30.0)))
        self.assertTrue(is_retryable_error(SecretAIConnectionError("host")))
        self.assertTrue(is_retryable_error(Exception("Connection timeout")))
        self.assertTrue(is_retryable_error(Exception("502 Bad Gateway")))
        self.assertTrue(is_retryable_error(Exception("Service temporarily unavailable")))
        
        # Non-retryable errors
        self.assertFalse(is_retryable_error(SecretAIAPIKeyMissingError()))
        self.assertFalse(is_retryable_error(ValueError("Invalid input")))
        self.assertFalse(is_retryable_error(KeyError("Missing key")))
    
    def test_retry_decorator_sync_success(self):
        """Test retry decorator with successful sync function"""
        call_count = 0
        
        @retry_with_backoff(max_retries=3, initial_delay=0.01)
        def succeeds_on_third_try():
            nonlocal call_count
            call_count += 1
            if call_count < 3:
                raise SecretAINetworkError("Network error")
            return "success"
        
        result = succeeds_on_third_try()
        self.assertEqual(result, "success")
        self.assertEqual(call_count, 3)
    
    def test_retry_decorator_sync_exhausted(self):
        """Test retry decorator when retries are exhausted"""
        call_count = 0
        
        @retry_with_backoff(max_retries=2, initial_delay=0.01)
        def always_fails():
            nonlocal call_count
            call_count += 1
            raise SecretAINetworkError("Network error")
        
        with self.assertRaises(SecretAIRetryExhaustedError) as context:
            always_fails()
        
        self.assertEqual(call_count, 3)  # initial + 2 retries
        self.assertEqual(context.exception.attempts, 3)
    
    def test_retry_decorator_non_retryable(self):
        """Test retry decorator with non-retryable error"""
        call_count = 0
        
        @retry_with_backoff(max_retries=3, initial_delay=0.01)
        def raises_non_retryable():
            nonlocal call_count
            call_count += 1
            raise SecretAIResponseError("Invalid response")  # Non-retryable error
        
        with self.assertRaises(SecretAIResponseError):
            raises_non_retryable()
        
        self.assertEqual(call_count, 1)  # Should not retry
    
    async def test_retry_decorator_async_success(self):
        """Test retry decorator with successful async function"""
        call_count = 0
        
        @retry_with_backoff(max_retries=3, initial_delay=0.01)
        async def async_succeeds_on_second_try():
            nonlocal call_count
            call_count += 1
            if call_count < 2:
                raise SecretAITimeoutError(1.0)
            return "async_success"
        
        result = await async_succeeds_on_second_try()
        self.assertEqual(result, "async_success")
        self.assertEqual(call_count, 2)


class TestConfiguration(unittest.TestCase):
    """Test configuration loading"""
    
    def test_get_retry_config_defaults(self):
        """Test getting default retry configuration"""
        config = get_retry_config()
        self.assertEqual(config['max_retries'], MAX_RETRIES_DEFAULT)
        self.assertEqual(config['initial_delay'], RETRY_DELAY_DEFAULT)
        self.assertEqual(config['backoff_multiplier'], RETRY_BACKOFF_DEFAULT)
    
    @patch.dict(os.environ, {
        'SECRET_AI_MAX_RETRIES': '5',
        'SECRET_AI_RETRY_DELAY': '2.5',
        'SECRET_AI_RETRY_BACKOFF': '3.0'
    })
    def test_get_retry_config_from_env(self):
        """Test getting retry configuration from environment"""
        config = get_retry_config()
        self.assertEqual(config['max_retries'], 5)
        self.assertEqual(config['initial_delay'], 2.5)
        self.assertEqual(config['backoff_multiplier'], 3.0)
    
    def test_get_timeout_config_defaults(self):
        """Test getting default timeout configuration"""
        config = get_timeout_config()
        self.assertEqual(config['request_timeout'], REQUEST_TIMEOUT_DEFAULT)
        self.assertEqual(config['connect_timeout'], CONNECT_TIMEOUT_DEFAULT)
    
    @patch.dict(os.environ, {
        'SECRET_AI_REQUEST_TIMEOUT': '60',
        'SECRET_AI_CONNECT_TIMEOUT': '15'
    })
    def test_get_timeout_config_from_env(self):
        """Test getting timeout configuration from environment"""
        config = get_timeout_config()
        self.assertEqual(config['request_timeout'], 60.0)
        self.assertEqual(config['connect_timeout'], 15.0)


class TestEnhancedClient(unittest.TestCase):
    """Test enhanced client functionality"""
    
    @patch.dict(os.environ, {'SECRET_AI_API_KEY': 'test_api_key'})
    def test_enhanced_client_initialization(self):
        """Test enhanced client initialization"""
        from secret_ai_sdk._enhanced_client import EnhancedSecretAIClient
        
        with patch('secret_ai_sdk._enhanced_client.OllamaClient.__init__') as mock_init:
            mock_init.return_value = None
            client = EnhancedSecretAIClient(host="http://test.com")
            
            self.assertEqual(client.host, "http://test.com")
            self.assertEqual(client.request_timeout, REQUEST_TIMEOUT_DEFAULT)
            self.assertEqual(client.max_retries, MAX_RETRIES_DEFAULT)
            self.assertTrue(client.validate_responses)
    
    def test_enhanced_client_missing_api_key(self):
        """Test enhanced client with missing API key"""
        from secret_ai_sdk._enhanced_client import EnhancedSecretAIClient
        
        # Ensure API key is not set
        os.environ.pop('SECRET_AI_API_KEY', None)
        
        with self.assertRaises(SecretAIAPIKeyMissingError):
            EnhancedSecretAIClient(host="http://test.com")
    
    @patch.dict(os.environ, {'SECRET_AI_API_KEY': 'test_api_key'})
    def test_response_validation(self):
        """Test response validation"""
        from secret_ai_sdk._enhanced_client import EnhancedSecretAIClient
        
        with patch('secret_ai_sdk._enhanced_client.OllamaClient.__init__') as mock_init:
            mock_init.return_value = None
            client = EnhancedSecretAIClient(host="http://test.com")
            
            # Test null response
            with self.assertRaises(SecretAIResponseError):
                client._validate_response(None)
            
            # Test error response
            with self.assertRaises(SecretAIResponseError):
                client._validate_response({"error": "Server error"})
            
            # Test valid response (should not raise)
            client._validate_response({"message": {"content": "test"}})
            
            # Test with validation disabled
            client.validate_responses = False
            client._validate_response(None)  # Should not raise


class TestSecretClassRetry(unittest.TestCase):
    """Test Secret class with retry logic"""
    
    @patch('secret_ai_sdk.secret.LCDClient')
    def test_get_models_with_retry(self, mock_lcd_client):
        """Test get_models with retry on failure"""
        from secret_ai_sdk.secret import Secret
        
        # Setup mock
        mock_instance = MagicMock()
        mock_lcd_client.return_value = mock_instance
        
        # First two calls fail, third succeeds
        mock_instance.wasm.contract_query.side_effect = [
            Exception("Network error"),
            Exception("Timeout"),
            {"models": ["model1", "model2"]}
        ]
        
        secret = Secret()
        with patch('time.sleep'):  # Speed up test by mocking sleep
            models = secret.get_models()
        
        self.assertEqual(models, ["model1", "model2"])
        self.assertEqual(mock_instance.wasm.contract_query.call_count, 3)
    
    @patch('secret_ai_sdk.secret.LCDClient')
    def test_get_models_invalid_response(self, mock_lcd_client):
        """Test get_models with invalid response format"""
        from secret_ai_sdk.secret import Secret
        
        # Setup mock
        mock_instance = MagicMock()
        mock_lcd_client.return_value = mock_instance
        
        # Return invalid response format (response errors are not retried)
        mock_instance.wasm.contract_query.return_value = {"invalid": "response"}
        
        secret = Secret()
        with self.assertRaises(SecretAIResponseError) as context:
            secret.get_models()
        
        self.assertIn("Invalid response format", str(context.exception))
        # Should only be called once since response errors are not retryable
        self.assertEqual(mock_instance.wasm.contract_query.call_count, 1)


if __name__ == '__main__':
    # Run async tests properly
    unittest.main(verbosity=2)