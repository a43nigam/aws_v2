"""
Tests for AWS V2 CLI.
"""

import pytest
from click.testing import CliRunner
from aws_v2.cli import main


def test_cli_help():
    """Test that CLI help works."""
    runner = CliRunner()
    result = runner.invoke(main, ['--help'])
    assert result.exit_code == 0
    assert 'AWS V2' in result.output


def test_cli_version():
    """Test that CLI version works."""
    runner = CliRunner()
    result = runner.invoke(main, ['--version'])
    assert result.exit_code == 0
    assert '1.0.0' in result.output


def test_ec2_help():
    """Test that EC2 command help works."""
    runner = CliRunner()
    result = runner.invoke(main, ['ec2', '--help'])
    assert result.exit_code == 0
    assert 'ec2' in result.output.lower()


def test_s3_help():
    """Test that S3 command help works."""
    runner = CliRunner()
    result = runner.invoke(main, ['s3', '--help'])
    assert result.exit_code == 0
    assert 's3' in result.output.lower()


def test_iam_help():
    """Test that IAM command help works."""
    runner = CliRunner()
    result = runner.invoke(main, ['iam', '--help'])
    assert result.exit_code == 0
    assert 'iam' in result.output.lower()


if __name__ == '__main__':
    pytest.main([__file__])
