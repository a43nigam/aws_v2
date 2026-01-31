"""Retry utility with exponential backoff."""

import time
import logging
from typing import Callable, TypeVar, Optional
from functools import wraps

from .exceptions import RetryException

logger = logging.getLogger(__name__)

T = TypeVar('T')


def retry_with_backoff(
    max_retries: int = 3,
    initial_delay: float = 1.0,
    backoff_factor: float = 2.0,
    max_delay: float = 60.0,
    retryable_exceptions: tuple = (Exception,)
):
    """
    Decorator to retry a function with exponential backoff.
    
    Args:
        max_retries: Maximum number of retry attempts
        initial_delay: Initial delay in seconds
        backoff_factor: Factor to multiply delay by after each retry
        max_delay: Maximum delay between retries
        retryable_exceptions: Tuple of exception types to retry on
    """
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        def wrapper(*args, **kwargs) -> T:
            delay = initial_delay
            last_exception = None
            
            for attempt in range(max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except retryable_exceptions as e:
                    last_exception = e
                    if attempt == max_retries:
                        logger.error(
                            f"Failed after {max_retries} retries: {func.__name__}"
                        )
                        raise RetryException(
                            f"Operation {func.__name__} failed",
                            attempts=max_retries,
                            last_error=e
                        )
                    
                    logger.warning(
                        f"Attempt {attempt + 1}/{max_retries} failed for {func.__name__}. "
                        f"Retrying in {delay}s... Error: {e}"
                    )
                    time.sleep(delay)
                    delay = min(delay * backoff_factor, max_delay)
            
            # This should never be reached, but just in case
            raise RetryException(
                f"Operation {func.__name__} failed",
                attempts=max_retries,
                last_error=last_exception or Exception("Unknown error")
            )
        
        return wrapper
    return decorator
