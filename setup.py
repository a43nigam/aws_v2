from setuptools import setup, find_packages

setup(
    name='aws-v2',
    version='1.0.0',
    description='AWS CLI wrapper with enhanced features and better UX',
    author='AWS V2 Contributors',
    packages=find_packages(),
    install_requires=[
        'boto3>=1.26.0',
        'click>=8.1.0',
        'colorama>=0.4.6',
        'tabulate>=0.9.0',
        'pyyaml>=6.0',
    ],
    entry_points={
        'console_scripts': [
            'aws-v2=aws_v2.cli:main',
        ],
    },
    python_requires='>=3.8',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
)
