# Error Handling Improvements for Secret AI SDK

## Overview

This document outlines the comprehensive error handling improvements implemented to address the following gaps:

- Limited retry logic for network failures
- No timeout configurations for HTTP requests  
- Missing error handling for malformed responses
- Inconsistent error handling patterns

## Key Improvements

### 1. Enhanced Exception Classes

Added comprehensive custom exceptions in `secret_ai_ex.py`:

- **SecretAINetworkError**: Base class for network-related failures
- **SecretAITimeoutError**: Specific timeout errors with timeout details
- **SecretAIRetryExhaustedError**: When all retry attempts fail
- **SecretAIResponseError**: Malformed or invalid responses
- **SecretAIConnectionError**: Connection establishment failures

### 2. Retry Logic with Exponential Backoff

Created `_retry.py` module with:

- Configurable retry attempts (default: 3)
- Exponential backoff with jitter protection
- Smart error classification (retryable vs non-retryable)
- Support for both sync and async operations
- Decorator-based retry logic for easy application

### 3. Timeout Configuration

Extended `_config.py` with timeout settings:

```python
# Environment Variables
SECRET_AI_REQUEST_TIMEOUT=30      # Request timeout (seconds)
SECRET_AI_CONNECT_TIMEOUT=10      # Connection timeout (seconds)
SECRET_AI_MAX_RETRIES=3           # Maximum retry attempts
SECRET_AI_RETRY_DELAY=1           # Initial retry delay (seconds)
SECRET_AI_RETRY_BACKOFF=2         # Backoff multiplier
SECRET_AI_MAX_RETRY_DELAY=30      # Maximum retry delay (seconds)
```

### 4. Enhanced Clients

Created `_enhanced_client.py` with:

- Automatic retry logic for network failures
- Configurable timeouts for HTTP operations
- Response validation and error detection
- Graceful fallback to basic clients if enhanced features unavailable
- Comprehensive logging for debugging

### 5. Improved Secret Class

Updated `secret.py` methods:

- Added retry logic to `get_models()` and `get_urls()`
- Response format validation
- Proper error propagation with context
- Network failure resilience

## Configuration Options

All settings can be configured via environment variables:

| Variable | Default | Description |
|----------|---------|-------------|
| `SECRET_AI_REQUEST_TIMEOUT` | 30 | Request timeout in seconds |
| `SECRET_AI_CONNECT_TIMEOUT` | 10 | Connection timeout in seconds |
| `SECRET_AI_MAX_RETRIES` | 3 | Maximum retry attempts |
| `SECRET_AI_RETRY_DELAY` | 1 | Initial retry delay in seconds |
| `SECRET_AI_RETRY_BACKOFF` | 2 | Backoff multiplier |
| `SECRET_AI_MAX_RETRY_DELAY` | 30 | Maximum retry delay in seconds |

## Usage Examples

### Basic Usage (Automatic Enhancement)

```python
from secret_ai_sdk import ChatSecret, Secret

# Enhanced clients are used automatically
secret_client = Secret()
models = secret_client.get_models()  # Automatic retry on failure

# Enhanced ChatSecret with retry logic
chat_client = ChatSecret(base_url=url, model=model)
response = chat_client.invoke(messages)  # Automatic retry and validation
```

### Custom Configuration

```python
# Custom timeout and retry settings
from secret_ai_sdk._enhanced_client import EnhancedSecretAIClient

client = EnhancedSecretAIClient(
    host="https://api.example.com",
    timeout=60,           # 60 second timeout
    max_retries=5,        # 5 retry attempts
    retry_delay=2,        # 2 second initial delay
    validate_responses=True
)
```

### Error Handling

```python
from secret_ai_sdk import (
    ChatSecret,
    SecretAINetworkError,
    SecretAITimeoutError,
    SecretAIRetryExhaustedError
)

try:
    chat_client = ChatSecret(base_url=url, model=model)
    response = chat_client.invoke(messages)
except SecretAITimeoutError as e:
    print(f"Request timed out after {e.timeout} seconds")
except SecretAIRetryExhaustedError as e:
    print(f"All {e.attempts} retry attempts failed")
except SecretAINetworkError as e:
    print(f"Network error: {e}")
```

## Backwards Compatibility

- All existing APIs remain unchanged
- Enhanced features are opt-in via environment variables
- Basic clients remain available as fallback
- No breaking changes to public interfaces

## Testing

Comprehensive test suite in `test_error_handling.py` covers:

- Exception class functionality
- Retry logic with various scenarios
- Timeout configuration
- Enhanced client behavior
- Smart contract interaction resilience
- Response validation

## Error Classification

The system intelligently classifies errors:

### Retryable Errors
- Network timeouts
- Connection failures  
- Temporary service unavailability (502, 503, 504)
- Infrastructure errors

### Non-Retryable Errors
- Authentication failures (API key issues)
- Invalid response formats
- Client-side validation errors
- Permanent server errors (400, 401, 403)

## Monitoring and Logging

Enhanced logging provides:

- Retry attempt details with delays
- Error classification decisions
- Performance metrics
- Configuration information
- Debug traces for troubleshooting

This comprehensive error handling system significantly improves the SDK's reliability and user experience while maintaining full backwards compatibility.