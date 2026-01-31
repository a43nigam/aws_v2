"""
Example: Basic S3 operations with AWS V2
"""

from aws_v2 import AWSV2Client


def main():
    # Initialize the client
    client = AWSV2Client(region='us-east-1')
    
    # Upload a file with automatic retry
    print("Uploading file to S3...")
    result = client.s3.upload_with_retry(
        bucket='my-bucket',
        key='data/file.txt',
        file_path='/path/to/local/file.txt'
    )
    print(f"Upload result: {result}")
    
    # Download a file with automatic retry
    print("\nDownloading file from S3...")
    result = client.s3.download_with_retry(
        bucket='my-bucket',
        key='data/file.txt',
        file_path='/path/to/download/file.txt'
    )
    print(f"Download result: {result}")
    
    # List objects in a bucket
    print("\nListing objects...")
    objects = client.s3.list_objects_smart(
        bucket='my-bucket',
        prefix='data/',
        max_keys=100
    )
    print(f"Found {len(objects)} objects")
    for obj in objects[:5]:  # Show first 5
        print(f"  - {obj['Key']} ({obj['Size']} bytes)")
    
    # Check if an object exists
    exists = client.s3.object_exists(bucket='my-bucket', key='data/file.txt')
    print(f"\nObject exists: {exists}")


if __name__ == '__main__':
    main()
