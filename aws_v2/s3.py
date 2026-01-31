"""Enhanced S3 operations."""

import logging
from typing import Optional, Dict, Any, List
from pathlib import Path
import boto3
from botocore.exceptions import ClientError

from .retry import retry_with_backoff
from .exceptions import ValidationException

logger = logging.getLogger(__name__)


class S3Helper:
    """Enhanced S3 operations with retry logic and better error handling."""
    
    def __init__(self, session: boto3.Session, max_retries: int = 3, retry_delay: float = 1.0):
        """
        Initialize S3 helper.
        
        Args:
            session: Boto3 session
            max_retries: Maximum number of retries
            retry_delay: Initial delay for retries
        """
        self.client = session.client('s3')
        self.max_retries = max_retries
        self.retry_delay = retry_delay
    
    @retry_with_backoff(max_retries=3, initial_delay=1.0)
    def upload_with_retry(
        self,
        bucket: str,
        key: str,
        file_path: str,
        extra_args: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Upload a file to S3 with automatic retry on failure.
        
        Args:
            bucket: S3 bucket name
            key: Object key in S3
            file_path: Local file path to upload
            extra_args: Extra arguments for upload (e.g., ACL, metadata)
        
        Returns:
            Dictionary with upload information
        """
        path = Path(file_path)
        if not path.exists():
            raise ValidationException(f"File not found: {file_path}")
        
        logger.info(f"Uploading {file_path} to s3://{bucket}/{key}")
        
        try:
            self.client.upload_file(
                Filename=str(path),
                Bucket=bucket,
                Key=key,
                ExtraArgs=extra_args or {}
            )
            return {
                "bucket": bucket,
                "key": key,
                "file_path": file_path,
                "status": "success"
            }
        except ClientError as e:
            logger.error(f"Failed to upload to S3: {e}")
            raise
    
    @retry_with_backoff(max_retries=3, initial_delay=1.0)
    def download_with_retry(
        self,
        bucket: str,
        key: str,
        file_path: str
    ) -> Dict[str, Any]:
        """
        Download a file from S3 with automatic retry on failure.
        
        Args:
            bucket: S3 bucket name
            key: Object key in S3
            file_path: Local file path to save to
        
        Returns:
            Dictionary with download information
        """
        logger.info(f"Downloading s3://{bucket}/{key} to {file_path}")
        
        # Ensure parent directory exists
        Path(file_path).parent.mkdir(parents=True, exist_ok=True)
        
        try:
            self.client.download_file(
                Bucket=bucket,
                Key=key,
                Filename=file_path
            )
            return {
                "bucket": bucket,
                "key": key,
                "file_path": file_path,
                "status": "success"
            }
        except ClientError as e:
            logger.error(f"Failed to download from S3: {e}")
            raise
    
    def list_objects_smart(
        self,
        bucket: str,
        prefix: str = "",
        max_keys: int = 1000
    ) -> List[Dict[str, Any]]:
        """
        List objects in S3 bucket with pagination handling.
        
        Args:
            bucket: S3 bucket name
            prefix: Prefix to filter objects
            max_keys: Maximum number of keys to return
        
        Returns:
            List of object metadata dictionaries
        """
        logger.info(f"Listing objects in s3://{bucket}/{prefix}")
        
        objects = []
        paginator = self.client.get_paginator('list_objects_v2')
        
        try:
            for page in paginator.paginate(
                Bucket=bucket,
                Prefix=prefix,
                PaginationConfig={'MaxItems': max_keys}
            ):
                if 'Contents' in page:
                    objects.extend(page['Contents'])
        except ClientError as e:
            logger.error(f"Failed to list objects: {e}")
            raise
        
        return objects
    
    def object_exists(self, bucket: str, key: str) -> bool:
        """
        Check if an object exists in S3.
        
        Args:
            bucket: S3 bucket name
            key: Object key in S3
        
        Returns:
            True if object exists, False otherwise
        """
        try:
            self.client.head_object(Bucket=bucket, Key=key)
            return True
        except ClientError as e:
            if e.response['Error']['Code'] == '404':
                return False
            raise
