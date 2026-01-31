"""
AWS V2 - Enhanced AWS Utilities

A better way to interact with AWS services with improved error handling,
retry logic, and configuration management.
"""

__version__ = "2.0.0"

from .client import AWSV2Client
from .config import Config
from .exceptions import AWSV2Exception, RetryException

__all__ = [
    "AWSV2Client",
    "Config", 
    "AWSV2Exception",
    "RetryException",
]
