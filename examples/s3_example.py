#!/usr/bin/env python3
"""
Example script demonstrating AWS V2 usage for S3 buckets.
"""

import sys
import os

# Add parent directory to path to import aws_v2
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from aws_v2.utils import print_info, print_success, print_warning

def main():
    print_info("AWS V2 S3 Example")
    print_info("=" * 50)
    
    print_info("\nTo list all S3 buckets:")
    print("  aws-v2 s3 list-buckets\n")
    
    print_info("To list objects in a bucket:")
    print("  aws-v2 s3 list-objects my-bucket\n")
    
    print_info("To create a new bucket:")
    print("  aws-v2 s3 create-bucket my-new-bucket --region us-east-1\n")
    
    print_info("To delete a bucket:")
    print("  aws-v2 s3 delete-bucket my-bucket\n")
    
    print_success("AWS V2 shows human-readable sizes and better formatted output!")
    print_warning("Make sure to configure AWS credentials first: aws configure")

if __name__ == '__main__':
    main()
