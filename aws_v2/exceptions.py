"""Custom exceptions for AWS V2."""


class AWSV2Exception(Exception):
    """Base exception for AWS V2 errors."""
    pass


class RetryException(AWSV2Exception):
    """Exception raised when retry attempts are exhausted."""
    
    def __init__(self, message: str, attempts: int, last_error: Exception):
        super().__init__(f"{message} after {attempts} attempts. Last error: {last_error}")
        self.attempts = attempts
        self.last_error = last_error


class ConfigurationException(AWSV2Exception):
    """Exception raised for configuration errors."""
    pass


class ValidationException(AWSV2Exception):
    """Exception raised for validation errors."""
    pass
