"""
Enhanced IAM operations with better UX.
"""

import click
import boto3
from botocore.exceptions import ClientError, NoCredentialsError
from aws_v2.utils import (
    print_success, print_error, print_warning, print_info,
    print_table, confirm_action
)


@click.group(name='iam')
def iam_group():
    """Manage IAM users and roles with enhanced features."""
    pass


@iam_group.command(name='list-users')
def list_users():
    """
    List IAM users with better formatting.
    
    Shows username, user ID, creation date, and password last used.
    """
    try:
        iam = boto3.client('iam')
        response = iam.list_users()
        
        users = []
        for user in response['Users']:
            password_last_used = 'Never'
            if 'PasswordLastUsed' in user:
                password_last_used = user['PasswordLastUsed'].strftime('%Y-%m-%d %H:%M:%S')
            
            users.append([
                user['UserName'],
                user['UserId'],
                user['CreateDate'].strftime('%Y-%m-%d %H:%M:%S'),
                password_last_used
            ])
        
        if not users:
            print_warning("No IAM users found")
            return
        
        headers = ['Username', 'User ID', 'Created', 'Password Last Used']
        print_table(headers, users)
        print_info(f"Total users: {len(users)}")
        
    except NoCredentialsError:
        print_error("AWS credentials not configured. Run 'aws configure' first.")
    except ClientError as e:
        print_error(f"AWS API error: {e.response['Error']['Message']}")
    except Exception as e:
        print_error(f"Error: {str(e)}")


@iam_group.command(name='list-roles')
def list_roles():
    """
    List IAM roles with better formatting.
    
    Shows role name, role ID, and creation date.
    """
    try:
        iam = boto3.client('iam')
        response = iam.list_roles()
        
        roles = []
        for role in response['Roles']:
            roles.append([
                role['RoleName'],
                role['RoleId'],
                role['CreateDate'].strftime('%Y-%m-%d %H:%M:%S'),
                role.get('Description', 'N/A')[:50]  # Truncate description
            ])
        
        if not roles:
            print_warning("No IAM roles found")
            return
        
        headers = ['Role Name', 'Role ID', 'Created', 'Description']
        print_table(headers, roles)
        print_info(f"Total roles: {len(roles)}")
        
    except NoCredentialsError:
        print_error("AWS credentials not configured. Run 'aws configure' first.")
    except ClientError as e:
        print_error(f"AWS API error: {e.response['Error']['Message']}")
    except Exception as e:
        print_error(f"Error: {str(e)}")


@iam_group.command(name='whoami')
def whoami():
    """
    Display information about the current IAM identity.
    
    Shows the ARN, account ID, and user/role ID of the current credentials.
    """
    try:
        sts = boto3.client('sts')
        identity = sts.get_caller_identity()
        
        print_info("Current AWS Identity:")
        print(f"  Account: {identity['Account']}")
        print(f"  User/Role ARN: {identity['Arn']}")
        print(f"  User/Role ID: {identity['UserId']}")
        
    except NoCredentialsError:
        print_error("AWS credentials not configured. Run 'aws configure' first.")
    except ClientError as e:
        print_error(f"AWS API error: {e.response['Error']['Message']}")
    except Exception as e:
        print_error(f"Error: {str(e)}")
