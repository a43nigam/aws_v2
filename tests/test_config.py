"""Tests for AWS V2 configuration."""

import os
import pytest
from aws_v2.config import Config


class TestConfig:
    """Test configuration management."""
    
    def test_default_config(self):
        """Test default configuration values."""
        config = Config()
        assert config.max_retries == 3
        assert config.retry_delay == 1.0
        assert config.region is not None
    
    def test_custom_config(self):
        """Test custom configuration values."""
        config = Config(
            region='us-west-2',
            max_retries=5,
            retry_delay=2.0
        )
        assert config.region == 'us-west-2'
        assert config.max_retries == 5
        assert config.retry_delay == 2.0
    
    def test_config_from_env(self, monkeypatch):
        """Test configuration from environment variables."""
        monkeypatch.setenv('AWS_DEFAULT_REGION', 'eu-west-1')
        monkeypatch.setenv('AWS_ACCESS_KEY_ID', 'test-key')
        monkeypatch.setenv('AWS_SECRET_ACCESS_KEY', 'test-secret')
        monkeypatch.setenv('AWS_SESSION_TOKEN', 'test-token')
        monkeypatch.setenv('AWS_PROFILE', 'test-profile')
        
        config = Config()
        assert config.region == 'eu-west-1'
        assert config.access_key_id == 'test-key'
        assert config.secret_access_key == 'test-secret'
        assert config.session_token == 'test-token'
        assert config.profile_name == 'test-profile'
    
    def test_boto3_config_conversion(self):
        """Test conversion to boto3 config format."""
        config = Config(
            region='us-east-1',
            access_key_id='test-key',
            secret_access_key='test-secret'
        )
        boto3_config = config.to_boto3_config()
        
        assert boto3_config['region_name'] == 'us-east-1'
        assert boto3_config['aws_access_key_id'] == 'test-key'
        assert boto3_config['aws_secret_access_key'] == 'test-secret'
    
    def test_boto3_config_without_credentials(self):
        """Test boto3 config without explicit credentials."""
        config = Config(region='us-east-1')
        boto3_config = config.to_boto3_config()
        
        assert boto3_config['region_name'] == 'us-east-1'
        assert 'aws_access_key_id' not in boto3_config
        assert 'aws_secret_access_key' not in boto3_config
