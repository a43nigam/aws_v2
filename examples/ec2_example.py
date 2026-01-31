#!/usr/bin/env python3
"""
Example script demonstrating AWS V2 usage for EC2 instances.
"""

import sys
import os

# Add parent directory to path to import aws_v2
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from aws_v2.utils import print_info, print_success, print_warning

def main():
    print_info("AWS V2 EC2 Example")
    print_info("=" * 50)
    
    print_info("\nTo list all EC2 instances:")
    print("  aws-v2 ec2 list\n")
    
    print_info("To list only running instances:")
    print("  aws-v2 ec2 list --state running\n")
    
    print_info("To start an instance:")
    print("  aws-v2 ec2 start i-1234567890abcdef0\n")
    
    print_info("To stop an instance:")
    print("  aws-v2 ec2 stop i-1234567890abcdef0\n")
    
    print_success("AWS V2 provides better formatting and user experience!")
    print_warning("Make sure to configure AWS credentials first: aws configure")

if __name__ == '__main__':
    main()
