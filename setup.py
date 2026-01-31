from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="aws_v2",
    version="2.0.0",
    author="AWS V2 Contributors",
    description="Enhanced AWS utilities with better error handling and retry logic",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=[
        "boto3>=1.26.0",
        "botocore>=1.29.0",
        "python-dotenv>=0.19.0",
    ],
)
