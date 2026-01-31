# AWS V2 - Enhanced AWS CLI

A better AWS CLI wrapper with improved user experience, better error handling, and useful features that make working with AWS services more pleasant.

## 🚀 Features

- **Better UX**: Colored output, formatted tables, and clear success/error messages
- **Improved Error Handling**: User-friendly error messages instead of cryptic API errors
- **Smart Defaults**: Sensible defaults for common operations
- **Interactive Prompts**: Confirmation dialogs for destructive operations
- **Enhanced Formatting**: Human-readable output with tables and formatted data
- **Simplified Commands**: Easier-to-use commands for common AWS operations

## 📦 Installation

```bash
# Clone the repository
git clone https://github.com/a43nigam/aws_v2.git
cd aws_v2

# Install dependencies
pip install -r requirements.txt

# Install the package
pip install -e .
```

## 🔧 Prerequisites

- Python 3.8 or higher
- AWS credentials configured (run `aws configure` with the standard AWS CLI)

## 📖 Usage

### EC2 Commands

#### List EC2 Instances
```bash
# List all instances
aws-v2 ec2 list

# List only running instances
aws-v2 ec2 list --state running

# List instances in a specific region
aws-v2 ec2 list --region us-west-2
```

#### Start EC2 Instances
```bash
# Start one or more instances
aws-v2 ec2 start i-1234567890abcdef0

# Start multiple instances
aws-v2 ec2 start i-1234567890abcdef0 i-0987654321fedcba0

# Skip confirmation prompt
aws-v2 ec2 start i-1234567890abcdef0 --yes
```

#### Stop EC2 Instances
```bash
# Stop one or more instances
aws-v2 ec2 stop i-1234567890abcdef0

# Stop multiple instances with confirmation skip
aws-v2 ec2 stop i-1234567890abcdef0 i-0987654321fedcba0 --yes
```

### S3 Commands

#### List S3 Buckets
```bash
# List all buckets with regions
aws-v2 s3 list-buckets
```

#### List Objects in a Bucket
```bash
# List objects in a bucket
aws-v2 s3 list-objects my-bucket

# List objects with a prefix
aws-v2 s3 list-objects my-bucket --prefix logs/

# Limit number of results
aws-v2 s3 list-objects my-bucket --max-items 50
```

#### Create S3 Bucket
```bash
# Create a bucket in us-east-1 (default)
aws-v2 s3 create-bucket my-new-bucket

# Create a bucket in a specific region
aws-v2 s3 create-bucket my-new-bucket --region eu-west-1
```

#### Delete S3 Bucket
```bash
# Delete an empty bucket
aws-v2 s3 delete-bucket my-bucket

# Force delete a bucket with objects
aws-v2 s3 delete-bucket my-bucket --force --yes
```

### IAM Commands

#### List IAM Users
```bash
# List all IAM users
aws-v2 iam list-users
```

#### List IAM Roles
```bash
# List all IAM roles
aws-v2 iam list-roles
```

#### Get Current Identity
```bash
# Show current AWS identity
aws-v2 iam whoami
```

## 🎨 Key Improvements Over Standard AWS CLI

1. **Colored Output**: Green for success, red for errors, yellow for warnings, blue for info
2. **Formatted Tables**: Clean, readable tables instead of JSON dumps
3. **Human-Readable Sizes**: Displays "1.5 GB" instead of "1610612736 bytes"
4. **Smart Confirmations**: Asks for confirmation on destructive operations
5. **Better Error Messages**: Clear, actionable error messages
6. **Simplified Syntax**: Shorter, more intuitive command names

## 🛡️ Security

- Uses AWS credentials from your standard AWS CLI configuration
- Never stores or logs credentials
- Prompts for confirmation on destructive operations
- Supports all standard AWS security features (MFA, temporary credentials, etc.)

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

MIT License - feel free to use this project however you'd like.

## 🔗 Related Projects

- [AWS CLI](https://aws.amazon.com/cli/) - The official AWS command-line interface
- [boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html) - AWS SDK for Python

## 📞 Support

For issues and questions, please open an issue on GitHub.