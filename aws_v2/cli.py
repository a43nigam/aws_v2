"""
AWS V2 CLI - Enhanced command-line interface for AWS operations.
"""

import click
from colorama import init, Fore, Style
import sys

# Initialize colorama for cross-platform colored output
init(autoreset=True)

from aws_v2.ec2 import ec2_group
from aws_v2.s3 import s3_group
from aws_v2.iam import iam_group
from aws_v2.utils import print_success, print_error


@click.group()
@click.version_option(version='1.0.0')
def main():
    """
    AWS V2 - Enhanced AWS CLI with better UX and features.
    
    This tool provides an improved interface for common AWS operations with:
    - Better error messages and handling
    - Colored output for improved readability
    - Simplified commands for common tasks
    - Smart defaults and interactive prompts
    """
    pass


# Register command groups
main.add_command(ec2_group)
main.add_command(s3_group)
main.add_command(iam_group)


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print_error(f"Unexpected error: {str(e)}")
        sys.exit(1)
