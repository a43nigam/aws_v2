"""Enhanced EC2 operations."""

import logging
from typing import Optional, Dict, Any, List
import boto3
from botocore.exceptions import ClientError

from .retry import retry_with_backoff

logger = logging.getLogger(__name__)


class EC2Helper:
    """Enhanced EC2 operations with retry logic and better error handling."""
    
    def __init__(self, session: boto3.Session, max_retries: int = 3, retry_delay: float = 1.0):
        """
        Initialize EC2 helper.
        
        Args:
            session: Boto3 session
            max_retries: Maximum number of retries
            retry_delay: Initial delay for retries
        """
        self.client = session.client('ec2')
        self.max_retries = max_retries
        self.retry_delay = retry_delay
    
    def list_instances_smart(
        self,
        filters: Optional[Dict[str, str]] = None,
        max_results: int = 100
    ) -> List[Dict[str, Any]]:
        """
        List EC2 instances with smart filtering.
        
        Args:
            filters: Dictionary of filters (e.g., {'tag:Environment': 'production'})
            max_results: Maximum number of results to return
        
        Returns:
            List of instance information dictionaries
        """
        logger.info("Listing EC2 instances")
        
        # Convert dict filters to AWS filter format
        aws_filters = []
        if filters:
            for key, value in filters.items():
                aws_filters.append({
                    'Name': key,
                    'Values': [value] if isinstance(value, str) else value
                })
        
        instances = []
        
        try:
            paginator = self.client.get_paginator('describe_instances')
            for page in paginator.paginate(
                Filters=aws_filters,
                PaginationConfig={'MaxItems': max_results}
            ):
                for reservation in page.get('Reservations', []):
                    for instance in reservation.get('Instances', []):
                        instances.append({
                            'id': instance.get('InstanceId'),
                            'type': instance.get('InstanceType'),
                            'state': instance.get('State', {}).get('Name'),
                            'private_ip': instance.get('PrivateIpAddress'),
                            'public_ip': instance.get('PublicIpAddress'),
                            'tags': {tag['Key']: tag['Value'] for tag in instance.get('Tags', [])}
                        })
        except ClientError as e:
            logger.error(f"Failed to list instances: {e}")
            raise
        
        return instances
    
    @retry_with_backoff(max_retries=3, initial_delay=1.0)
    def start_instance(self, instance_id: str) -> Dict[str, Any]:
        """
        Start an EC2 instance with retry logic.
        
        Args:
            instance_id: Instance ID to start
        
        Returns:
            Dictionary with operation result
        """
        logger.info(f"Starting instance {instance_id}")
        
        try:
            response = self.client.start_instances(InstanceIds=[instance_id])
            return {
                'instance_id': instance_id,
                'status': 'starting',
                'response': response
            }
        except ClientError as e:
            logger.error(f"Failed to start instance: {e}")
            raise
    
    @retry_with_backoff(max_retries=3, initial_delay=1.0)
    def stop_instance(self, instance_id: str) -> Dict[str, Any]:
        """
        Stop an EC2 instance with retry logic.
        
        Args:
            instance_id: Instance ID to stop
        
        Returns:
            Dictionary with operation result
        """
        logger.info(f"Stopping instance {instance_id}")
        
        try:
            response = self.client.stop_instances(InstanceIds=[instance_id])
            return {
                'instance_id': instance_id,
                'status': 'stopping',
                'response': response
            }
        except ClientError as e:
            logger.error(f"Failed to stop instance: {e}")
            raise
    
    def get_instance_status(self, instance_id: str) -> str:
        """
        Get the current status of an EC2 instance.
        
        Args:
            instance_id: Instance ID to check
        
        Returns:
            Instance state (e.g., 'running', 'stopped', 'pending')
        """
        try:
            response = self.client.describe_instances(InstanceIds=[instance_id])
            if response['Reservations']:
                instance = response['Reservations'][0]['Instances'][0]
                return instance['State']['Name']
            return 'not-found'
        except ClientError as e:
            logger.error(f"Failed to get instance status: {e}")
            raise
