"""Main AWS V2 client."""

import logging
from typing import Optional
import boto3

from .config import Config
from .s3 import S3Helper
from .ec2 import EC2Helper

logger = logging.getLogger(__name__)


class AWSV2Client:
    """
    Enhanced AWS client with improved error handling and retry logic.
    
    This client provides a better interface to AWS services with:
    - Automatic retry with exponential backoff
    - Enhanced error messages
    - Simplified configuration
    - Type hints for better IDE support
    """
    
    def __init__(
        self,
        region: Optional[str] = None,
        access_key_id: Optional[str] = None,
        secret_access_key: Optional[str] = None,
        session_token: Optional[str] = None,
        profile_name: Optional[str] = None,
        max_retries: int = 3,
        retry_delay: float = 1.0,
        config: Optional[Config] = None
    ):
        """
        Initialize the AWS V2 client.
        
        Args:
            region: AWS region
            access_key_id: AWS access key ID
            secret_access_key: AWS secret access key
            session_token: AWS session token
            profile_name: AWS profile name
            max_retries: Maximum number of retries for operations
            retry_delay: Initial delay between retries
            config: Optional Config object (overrides other parameters)
        """
        # Use provided config or create new one
        if config is None:
            config = Config(
                region=region,
                access_key_id=access_key_id,
                secret_access_key=secret_access_key,
                session_token=session_token,
                profile_name=profile_name,
                max_retries=max_retries,
                retry_delay=retry_delay
            )
        
        self.config = config
        
        # Create boto3 session
        self._session = boto3.Session(**config.to_boto3_config())
        
        # Initialize service helpers
        self._s3 = None
        self._ec2 = None
        
        logger.info(f"Initialized AWS V2 client for region {config.region}")
    
    @property
    def s3(self) -> S3Helper:
        """Get S3 helper (lazy initialization)."""
        if self._s3 is None:
            self._s3 = S3Helper(
                self._session,
                max_retries=self.config.max_retries,
                retry_delay=self.config.retry_delay
            )
        return self._s3
    
    @property
    def ec2(self) -> EC2Helper:
        """Get EC2 helper (lazy initialization)."""
        if self._ec2 is None:
            self._ec2 = EC2Helper(
                self._session,
                max_retries=self.config.max_retries,
                retry_delay=self.config.retry_delay
            )
        return self._ec2
    
    @property
    def session(self) -> boto3.Session:
        """Get the underlying boto3 session."""
        return self._session
