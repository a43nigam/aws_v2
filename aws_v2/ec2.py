"""
Enhanced EC2 operations with better UX.
"""

import click
import boto3
from botocore.exceptions import ClientError, NoCredentialsError
from aws_v2.utils import (
    print_success, print_error, print_warning, print_info,
    print_table, confirm_action
)


@click.group(name='ec2')
def ec2_group():
    """Manage EC2 instances with enhanced features."""
    pass


@ec2_group.command(name='list')
@click.option('--region', default=None, help='AWS region (defaults to configured region)')
@click.option('--state', type=click.Choice(['running', 'stopped', 'all']), default='all',
              help='Filter by instance state')
def list_instances(region, state):
    """
    List EC2 instances with better formatting.
    
    Shows instance ID, name, type, state, and public IP in a clean table.
    """
    try:
        ec2 = boto3.client('ec2', region_name=region) if region else boto3.client('ec2')
        
        # Build filters
        filters = []
        if state != 'all':
            filters.append({'Name': 'instance-state-name', 'Values': [state]})
        
        response = ec2.describe_instances(Filters=filters) if filters else ec2.describe_instances()
        
        instances = []
        for reservation in response['Reservations']:
            for instance in reservation['Instances']:
                # Get instance name from tags
                name = 'N/A'
                for tag in instance.get('Tags', []):
                    if tag['Key'] == 'Name':
                        name = tag['Value']
                        break
                
                instances.append([
                    instance['InstanceId'],
                    name,
                    instance['InstanceType'],
                    instance['State']['Name'],
                    instance.get('PublicIpAddress', 'N/A'),
                    instance.get('PrivateIpAddress', 'N/A')
                ])
        
        if not instances:
            print_warning(f"No instances found with state: {state}")
            return
        
        headers = ['Instance ID', 'Name', 'Type', 'State', 'Public IP', 'Private IP']
        print_table(headers, instances)
        print_info(f"Total instances: {len(instances)}")
        
    except NoCredentialsError:
        print_error("AWS credentials not configured. Run 'aws configure' first.")
    except ClientError as e:
        print_error(f"AWS API error: {e.response['Error']['Message']}")
    except Exception as e:
        print_error(f"Error: {str(e)}")


@ec2_group.command(name='start')
@click.argument('instance_ids', nargs=-1, required=True)
@click.option('--region', default=None, help='AWS region')
@click.option('--yes', is_flag=True, help='Skip confirmation')
def start_instances(instance_ids, region, yes):
    """
    Start one or more EC2 instances.
    
    INSTANCE_IDS: One or more instance IDs to start
    """
    if not yes and not confirm_action(f"Start {len(instance_ids)} instance(s)?"):
        print_warning("Operation cancelled")
        return
    
    try:
        ec2 = boto3.client('ec2', region_name=region) if region else boto3.client('ec2')
        response = ec2.start_instances(InstanceIds=list(instance_ids))
        
        for instance in response['StartingInstances']:
            print_success(f"Starting instance {instance['InstanceId']} "
                        f"({instance['PreviousState']['Name']} → {instance['CurrentState']['Name']})")
        
    except NoCredentialsError:
        print_error("AWS credentials not configured. Run 'aws configure' first.")
    except ClientError as e:
        print_error(f"AWS API error: {e.response['Error']['Message']}")
    except Exception as e:
        print_error(f"Error: {str(e)}")


@ec2_group.command(name='stop')
@click.argument('instance_ids', nargs=-1, required=True)
@click.option('--region', default=None, help='AWS region')
@click.option('--yes', is_flag=True, help='Skip confirmation')
def stop_instances(instance_ids, region, yes):
    """
    Stop one or more EC2 instances.
    
    INSTANCE_IDS: One or more instance IDs to stop
    """
    if not yes and not confirm_action(f"Stop {len(instance_ids)} instance(s)?"):
        print_warning("Operation cancelled")
        return
    
    try:
        ec2 = boto3.client('ec2', region_name=region) if region else boto3.client('ec2')
        response = ec2.stop_instances(InstanceIds=list(instance_ids))
        
        for instance in response['StoppingInstances']:
            print_success(f"Stopping instance {instance['InstanceId']} "
                        f"({instance['PreviousState']['Name']} → {instance['CurrentState']['Name']})")
        
    except NoCredentialsError:
        print_error("AWS credentials not configured. Run 'aws configure' first.")
    except ClientError as e:
        print_error(f"AWS API error: {e.response['Error']['Message']}")
    except Exception as e:
        print_error(f"Error: {str(e)}")
