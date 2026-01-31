"""Tests for retry functionality."""

import pytest
from aws_v2.retry import retry_with_backoff
from aws_v2.exceptions import RetryException


class TestRetryWithBackoff:
    """Test retry decorator functionality."""
    
    def test_successful_call_no_retry(self):
        """Test that successful calls don't trigger retries."""
        call_count = 0
        
        @retry_with_backoff(max_retries=3)
        def successful_func():
            nonlocal call_count
            call_count += 1
            return "success"
        
        result = successful_func()
        assert result == "success"
        assert call_count == 1
    
    def test_retry_on_exception(self):
        """Test that function retries on exception."""
        call_count = 0
        
        @retry_with_backoff(max_retries=3, initial_delay=0.01)
        def failing_func():
            nonlocal call_count
            call_count += 1
            if call_count < 3:
                raise ValueError("Test error")
            return "success"
        
        result = failing_func()
        assert result == "success"
        assert call_count == 3
    
    def test_max_retries_exceeded(self):
        """Test that RetryException is raised after max retries."""
        call_count = 0
        
        @retry_with_backoff(max_retries=2, initial_delay=0.01)
        def always_failing_func():
            nonlocal call_count
            call_count += 1
            raise ValueError("Test error")
        
        with pytest.raises(RetryException) as exc_info:
            always_failing_func()
        
        assert call_count == 3  # Initial attempt + 2 retries
        assert exc_info.value.attempts == 2
        assert isinstance(exc_info.value.last_error, ValueError)
    
    def test_specific_exception_retry(self):
        """Test retrying only specific exceptions."""
        
        @retry_with_backoff(
            max_retries=2,
            initial_delay=0.01,
            retryable_exceptions=(ValueError,)
        )
        def specific_exception_func():
            raise TypeError("This should not be retried")
        
        # TypeError should not be retried, so it's raised immediately
        with pytest.raises(TypeError):
            specific_exception_func()
