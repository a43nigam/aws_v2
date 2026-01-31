"""
Enhanced S3 operations with better UX.
"""

import click
import boto3
from botocore.exceptions import ClientError, NoCredentialsError
from datetime import datetime
from aws_v2.utils import (
    print_success, print_error, print_warning, print_info,
    print_table, format_bytes, confirm_action
)


@click.group(name='s3')
def s3_group():
    """Manage S3 buckets and objects with enhanced features."""
    pass


@s3_group.command(name='list-buckets')
def list_buckets():
    """
    List all S3 buckets with better formatting.
    
    Shows bucket name, creation date, and region in a clean table.
    """
    try:
        s3 = boto3.client('s3')
        response = s3.list_buckets()
        
        buckets = []
        for bucket in response['Buckets']:
            # Get bucket region
            try:
                location = s3.get_bucket_location(Bucket=bucket['Name'])
                region = location['LocationConstraint'] or 'us-east-1'
            except ClientError:
                region = 'N/A'
            
            buckets.append([
                bucket['Name'],
                bucket['CreationDate'].strftime('%Y-%m-%d %H:%M:%S'),
                region
            ])
        
        if not buckets:
            print_warning("No S3 buckets found")
            return
        
        headers = ['Bucket Name', 'Created', 'Region']
        print_table(headers, buckets)
        print_info(f"Total buckets: {len(buckets)}")
        
    except NoCredentialsError:
        print_error("AWS credentials not configured. Run 'aws configure' first.")
    except ClientError as e:
        print_error(f"AWS API error: {e.response['Error']['Message']}")
    except Exception as e:
        print_error(f"Error: {str(e)}")


@s3_group.command(name='list-objects')
@click.argument('bucket')
@click.option('--prefix', default='', help='Filter objects by prefix')
@click.option('--max-items', default=100, help='Maximum number of objects to display')
def list_objects(bucket, prefix, max_items):
    """
    List objects in an S3 bucket.
    
    BUCKET: Name of the S3 bucket
    """
    try:
        s3 = boto3.client('s3')
        
        kwargs = {'Bucket': bucket, 'MaxKeys': max_items}
        if prefix:
            kwargs['Prefix'] = prefix
        
        response = s3.list_objects_v2(**kwargs)
        
        if 'Contents' not in response:
            print_warning(f"No objects found in bucket '{bucket}' with prefix '{prefix}'")
            return
        
        objects = []
        total_size = 0
        for obj in response['Contents']:
            objects.append([
                obj['Key'],
                format_bytes(obj['Size']),
                obj['LastModified'].strftime('%Y-%m-%d %H:%M:%S'),
                obj.get('StorageClass', 'STANDARD')
            ])
            total_size += obj['Size']
        
        headers = ['Key', 'Size', 'Last Modified', 'Storage Class']
        print_table(headers, objects)
        print_info(f"Total objects: {len(objects)} | Total size: {format_bytes(total_size)}")
        
        if response.get('IsTruncated'):
            print_warning(f"Results truncated. Use --max-items to see more.")
        
    except NoCredentialsError:
        print_error("AWS credentials not configured. Run 'aws configure' first.")
    except ClientError as e:
        print_error(f"AWS API error: {e.response['Error']['Message']}")
    except Exception as e:
        print_error(f"Error: {str(e)}")


@s3_group.command(name='create-bucket')
@click.argument('bucket')
@click.option('--region', default='us-east-1', help='AWS region for the bucket')
def create_bucket(bucket, region):
    """
    Create a new S3 bucket.
    
    BUCKET: Name of the S3 bucket to create
    """
    try:
        s3 = boto3.client('s3', region_name=region)
        
        # S3 bucket creation differs for us-east-1
        if region == 'us-east-1':
            s3.create_bucket(Bucket=bucket)
        else:
            s3.create_bucket(
                Bucket=bucket,
                CreateBucketConfiguration={'LocationConstraint': region}
            )
        
        print_success(f"Bucket '{bucket}' created successfully in region '{region}'")
        
    except NoCredentialsError:
        print_error("AWS credentials not configured. Run 'aws configure' first.")
    except ClientError as e:
        print_error(f"AWS API error: {e.response['Error']['Message']}")
    except Exception as e:
        print_error(f"Error: {str(e)}")


@s3_group.command(name='delete-bucket')
@click.argument('bucket')
@click.option('--force', is_flag=True, help='Delete bucket even if it contains objects')
@click.option('--yes', is_flag=True, help='Skip confirmation')
def delete_bucket(bucket, force, yes):
    """
    Delete an S3 bucket.
    
    BUCKET: Name of the S3 bucket to delete
    """
    if not yes and not confirm_action(f"Delete bucket '{bucket}'?"):
        print_warning("Operation cancelled")
        return
    
    try:
        s3 = boto3.client('s3')
        
        if force:
            # Delete all objects first
            print_info(f"Deleting all objects in bucket '{bucket}'...")
            s3_resource = boto3.resource('s3')
            bucket_obj = s3_resource.Bucket(bucket)
            bucket_obj.objects.all().delete()
        
        s3.delete_bucket(Bucket=bucket)
        print_success(f"Bucket '{bucket}' deleted successfully")
        
    except NoCredentialsError:
        print_error("AWS credentials not configured. Run 'aws configure' first.")
    except ClientError as e:
        print_error(f"AWS API error: {e.response['Error']['Message']}")
    except Exception as e:
        print_error(f"Error: {str(e)}")
