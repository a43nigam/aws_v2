"""Configuration management for AWS V2."""

import os
from typing import Optional, Dict, Any
from dotenv import load_dotenv


class Config:
    """Enhanced configuration management with environment variable support."""
    
    def __init__(
        self,
        region: Optional[str] = None,
        access_key_id: Optional[str] = None,
        secret_access_key: Optional[str] = None,
        session_token: Optional[str] = None,
        profile_name: Optional[str] = None,
        max_retries: int = 3,
        retry_delay: float = 1.0,
    ):
        """
        Initialize configuration.
        
        Args:
            region: AWS region (defaults to env AWS_DEFAULT_REGION)
            access_key_id: AWS access key ID (defaults to env AWS_ACCESS_KEY_ID)
            secret_access_key: AWS secret access key (defaults to env AWS_SECRET_ACCESS_KEY)
            session_token: AWS session token (defaults to env AWS_SESSION_TOKEN)
            profile_name: AWS profile name (defaults to env AWS_PROFILE)
            max_retries: Maximum number of retries for failed operations
            retry_delay: Initial delay in seconds between retries
        """
        # Load environment variables from .env file if present
        load_dotenv()
        
        self.region = region or os.getenv("AWS_DEFAULT_REGION", "us-east-1")
        self.access_key_id = access_key_id or os.getenv("AWS_ACCESS_KEY_ID")
        self.secret_access_key = secret_access_key or os.getenv("AWS_SECRET_ACCESS_KEY")
        self.session_token = session_token or os.getenv("AWS_SESSION_TOKEN")
        self.profile_name = profile_name or os.getenv("AWS_PROFILE")
        self.max_retries = max_retries
        self.retry_delay = retry_delay
    
    def to_boto3_config(self) -> Dict[str, Any]:
        """Convert configuration to boto3 session parameters."""
        config = {
            "region_name": self.region,
        }
        
        if self.access_key_id:
            config["aws_access_key_id"] = self.access_key_id
        if self.secret_access_key:
            config["aws_secret_access_key"] = self.secret_access_key
        if self.session_token:
            config["aws_session_token"] = self.session_token
        if self.profile_name:
            config["profile_name"] = self.profile_name
            
        return config
