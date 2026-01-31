# AWS V2 - Enhanced AWS Utilities

A better way to interact with AWS services. This library provides simplified, enhanced utilities for common AWS operations with built-in error handling, retry logic, and improved configuration management.

## Features

- 🚀 **Simple API**: Easy-to-use interface for common AWS operations
- 🔄 **Auto-retry**: Built-in exponential backoff retry logic
- ⚙️ **Smart Configuration**: Flexible configuration management with environment variable support
- 🛡️ **Error Handling**: Comprehensive error handling and meaningful error messages
- 📊 **Logging**: Detailed logging for debugging and monitoring
- ✨ **Type Hints**: Full type hint support for better IDE integration

## Installation

```bash
pip install -r requirements.txt
```

## Quick Start

```python
from aws_v2 import AWSV2Client

# Initialize the client
client = AWSV2Client(region='us-east-1')

# Use enhanced S3 operations
client.s3.upload_with_retry('my-bucket', 'file.txt', '/path/to/file.txt')

# Use enhanced EC2 operations
instances = client.ec2.list_instances_smart(filters={'tag:Environment': 'production'})
```

## Configuration

Set your AWS credentials using environment variables or AWS credentials file:

```bash
export AWS_ACCESS_KEY_ID=your_access_key
export AWS_SECRET_ACCESS_KEY=your_secret_key
export AWS_DEFAULT_REGION=us-east-1
```

## Examples

See the `examples/` directory for more usage examples.

## Testing

```bash
python -m pytest tests/
```

## License

MIT License