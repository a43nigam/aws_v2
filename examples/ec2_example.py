"""
Example: Basic EC2 operations with AWS V2
"""

from aws_v2 import AWSV2Client


def main():
    # Initialize the client
    client = AWSV2Client(region='us-east-1')
    
    # List all running instances
    print("Listing running instances...")
    instances = client.ec2.list_instances_smart(
        filters={'instance-state-name': 'running'}
    )
    print(f"Found {len(instances)} running instances")
    for instance in instances:
        print(f"  - {instance['id']} ({instance['type']}) - {instance['state']}")
        print(f"    Private IP: {instance['private_ip']}")
        print(f"    Public IP: {instance['public_ip']}")
        print(f"    Tags: {instance['tags']}")
    
    # List instances by tag
    print("\nListing production instances...")
    prod_instances = client.ec2.list_instances_smart(
        filters={'tag:Environment': 'production'}
    )
    print(f"Found {len(prod_instances)} production instances")
    
    # Get instance status
    if instances:
        instance_id = instances[0]['id']
        status = client.ec2.get_instance_status(instance_id)
        print(f"\nStatus of {instance_id}: {status}")
    
    # Start/stop instances (commented out for safety)
    # client.ec2.start_instance('i-1234567890abcdef0')
    # client.ec2.stop_instance('i-1234567890abcdef0')


if __name__ == '__main__':
    main()
