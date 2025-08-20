# _retry.py

"""
Module: Retry logic and error handling utilities for Secret AI SDK
"""

import asyncio
import time
import logging
from typing import TypeVar, Callable, Optional, Any, Type, Tuple
from functools import wraps
import os

import secret_ai_sdk._config as _config
from secret_ai_sdk.secret_ai_ex import (
    SecretAINetworkError,
    SecretAITimeoutError,
    SecretAIRetryExhaustedError,
    SecretAIConnectionError
)

logger = logging.getLogger(__name__)

T = TypeVar('T')

def get_retry_config() -> dict:
    """
    Get retry configuration from environment variables or defaults.
    
    Returns:
        dict: Configuration dictionary with retry settings
    """
    return {
        'max_retries': int(os.getenv(_config.MAX_RETRIES, _config.MAX_RETRIES_DEFAULT)),
        'initial_delay': float(os.getenv(_config.RETRY_DELAY, _config.RETRY_DELAY_DEFAULT)),
        'backoff_multiplier': float(os.getenv(_config.RETRY_BACKOFF, _config.RETRY_BACKOFF_DEFAULT)),
        'max_delay': float(os.getenv(_config.MAX_RETRY_DELAY, _config.MAX_RETRY_DELAY_DEFAULT)),
    }

def get_timeout_config() -> dict:
    """
    Get timeout configuration from environment variables or defaults.
    
    Returns:
        dict: Configuration dictionary with timeout settings
    """
    return {
        'request_timeout': float(os.getenv(_config.REQUEST_TIMEOUT, _config.REQUEST_TIMEOUT_DEFAULT)),
        'connect_timeout': float(os.getenv(_config.CONNECT_TIMEOUT, _config.CONNECT_TIMEOUT_DEFAULT)),
    }

def calculate_delay(attempt: int, initial_delay: float, multiplier: float, max_delay: float) -> float:
    """
    Calculate exponential backoff delay for retry attempt.
    
    Args:
        attempt: Current retry attempt number (0-based)
        initial_delay: Initial delay in seconds
        multiplier: Backoff multiplier
        max_delay: Maximum delay in seconds
        
    Returns:
        float: Calculated delay in seconds
    """
    delay = initial_delay * (multiplier ** attempt)
    return min(delay, max_delay)

def is_retryable_error(error: Exception) -> bool:
    """
    Determine if an error is retryable.
    
    Args:
        error: The exception to check
        
    Returns:
        bool: True if the error is retryable, False otherwise
    """
    from secret_ai_sdk.secret_ai_ex import SecretAIResponseError
    
    # Response errors are not retryable (bad data format)
    if isinstance(error, SecretAIResponseError):
        return False
    
    # Network errors are generally retryable
    if isinstance(error, (SecretAINetworkError, SecretAITimeoutError, SecretAIConnectionError)):
        return True
    
    # Check for common retryable HTTP/network errors
    error_msg = str(error).lower()
    retryable_keywords = [
        'timeout', 'timed out', 'connection', 'network',
        'temporarily unavailable', 'service unavailable',
        '502', '503', '504', 'gateway timeout'
    ]
    
    return any(keyword in error_msg for keyword in retryable_keywords)

def retry_with_backoff(
    max_retries: Optional[int] = None,
    initial_delay: Optional[float] = None,
    backoff_multiplier: Optional[float] = None,
    max_delay: Optional[float] = None,
    retryable_exceptions: Optional[Tuple[Type[Exception], ...]] = None
):
    """
    Decorator for retrying functions with exponential backoff.
    
    Args:
        max_retries: Maximum number of retry attempts
        initial_delay: Initial delay between retries in seconds
        backoff_multiplier: Multiplier for exponential backoff
        max_delay: Maximum delay between retries in seconds
        retryable_exceptions: Tuple of exception types to retry on
        
    Returns:
        Decorated function with retry logic
    """
    config = get_retry_config()
    
    max_retries = max_retries if max_retries is not None else config['max_retries']
    initial_delay = initial_delay if initial_delay is not None else config['initial_delay']
    backoff_multiplier = backoff_multiplier if backoff_multiplier is not None else config['backoff_multiplier']
    max_delay = max_delay if max_delay is not None else config['max_delay']
    
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        def sync_wrapper(*args, **kwargs) -> T:
            last_error = None
            
            for attempt in range(max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_error = e
                    
                    # Check if this is the last attempt
                    if attempt >= max_retries:
                        logger.error(f"All {max_retries + 1} attempts failed for {func.__name__}")
                        raise SecretAIRetryExhaustedError(max_retries + 1, last_error)
                    
                    # Check if error is retryable
                    if retryable_exceptions:
                        if not isinstance(e, retryable_exceptions):
                            logger.debug(f"Non-retryable error in {func.__name__}: {e}")
                            raise
                    elif not is_retryable_error(e):
                        logger.debug(f"Non-retryable error in {func.__name__}: {e}")
                        raise
                    
                    # Calculate delay and wait
                    delay = calculate_delay(attempt, initial_delay, backoff_multiplier, max_delay)
                    logger.warning(
                        f"Attempt {attempt + 1}/{max_retries + 1} failed for {func.__name__}: {e}. "
                        f"Retrying in {delay:.2f} seconds..."
                    )
                    time.sleep(delay)
            
            # This should not be reached, but just in case
            raise SecretAIRetryExhaustedError(max_retries + 1, last_error)
        
        @wraps(func)
        async def async_wrapper(*args, **kwargs) -> T:
            last_error = None
            
            for attempt in range(max_retries + 1):
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    last_error = e
                    
                    # Check if this is the last attempt
                    if attempt >= max_retries:
                        logger.error(f"All {max_retries + 1} attempts failed for {func.__name__}")
                        raise SecretAIRetryExhaustedError(max_retries + 1, last_error)
                    
                    # Check if error is retryable
                    if retryable_exceptions:
                        if not isinstance(e, retryable_exceptions):
                            logger.debug(f"Non-retryable error in {func.__name__}: {e}")
                            raise
                    elif not is_retryable_error(e):
                        logger.debug(f"Non-retryable error in {func.__name__}: {e}")
                        raise
                    
                    # Calculate delay and wait
                    delay = calculate_delay(attempt, initial_delay, backoff_multiplier, max_delay)
                    logger.warning(
                        f"Attempt {attempt + 1}/{max_retries + 1} failed for {func.__name__}: {e}. "
                        f"Retrying in {delay:.2f} seconds..."
                    )
                    await asyncio.sleep(delay)
            
            # This should not be reached, but just in case
            raise SecretAIRetryExhaustedError(max_retries + 1, last_error)
        
        # Return appropriate wrapper based on function type
        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        else:
            return sync_wrapper
    
    return decorator

class RetryableSession:
    """
    A session wrapper that provides retry logic for HTTP requests.
    """
    
    def __init__(
        self,
        session: Any,
        max_retries: Optional[int] = None,
        initial_delay: Optional[float] = None,
        backoff_multiplier: Optional[float] = None,
        max_delay: Optional[float] = None
    ):
        """
        Initialize RetryableSession.
        
        Args:
            session: The underlying session object
            max_retries: Maximum number of retry attempts
            initial_delay: Initial delay between retries
            backoff_multiplier: Multiplier for exponential backoff
            max_delay: Maximum delay between retries
        """
        self.session = session
        config = get_retry_config()
        
        self.max_retries = max_retries if max_retries is not None else config['max_retries']
        self.initial_delay = initial_delay if initial_delay is not None else config['initial_delay']
        self.backoff_multiplier = backoff_multiplier if backoff_multiplier is not None else config['backoff_multiplier']
        self.max_delay = max_delay if max_delay is not None else config['max_delay']
    
    def _should_retry(self, error: Exception) -> bool:
        """Check if an error should trigger a retry."""
        return is_retryable_error(error)
    
    def request_with_retry(self, method: str, url: str, **kwargs) -> Any:
        """
        Make an HTTP request with retry logic.
        
        Args:
            method: HTTP method
            url: Request URL
            **kwargs: Additional request parameters
            
        Returns:
            Response object
            
        Raises:
            SecretAIRetryExhaustedError: When all retries are exhausted
        """
        last_error = None
        
        for attempt in range(self.max_retries + 1):
            try:
                response = self.session.request(method, url, **kwargs)
                response.raise_for_status()
                return response
            except Exception as e:
                last_error = e
                
                if attempt >= self.max_retries:
                    logger.error(f"All {self.max_retries + 1} attempts failed for {method} {url}")
                    raise SecretAIRetryExhaustedError(self.max_retries + 1, last_error)
                
                if not self._should_retry(e):
                    logger.debug(f"Non-retryable error for {method} {url}: {e}")
                    raise
                
                delay = calculate_delay(attempt, self.initial_delay, self.backoff_multiplier, self.max_delay)
                logger.warning(
                    f"Attempt {attempt + 1}/{self.max_retries + 1} failed for {method} {url}: {e}. "
                    f"Retrying in {delay:.2f} seconds..."
                )
                time.sleep(delay)
        
        raise SecretAIRetryExhaustedError(self.max_retries + 1, last_error)