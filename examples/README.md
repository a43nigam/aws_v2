# AWS V2 Examples

This directory contains example scripts demonstrating how to use AWS V2.

## Examples

- `s3_example.py` - S3 operations (upload, download, list)
- `ec2_example.py` - EC2 operations (list, start, stop instances)

## Running Examples

Make sure you have AWS credentials configured:

```bash
export AWS_ACCESS_KEY_ID=your_access_key
export AWS_SECRET_ACCESS_KEY=your_secret_key
export AWS_DEFAULT_REGION=us-east-1
```

Then run any example:

```bash
python s3_example.py
python ec2_example.py
```
