"""
Utility functions for AWS V2.
"""

from colorama import Fore, Style
from tabulate import tabulate
import sys


def print_success(message):
    """Print a success message in green."""
    print(f"{Fore.GREEN}✓ {message}{Style.RESET_ALL}")


def print_error(message):
    """Print an error message in red."""
    print(f"{Fore.RED}✗ {message}{Style.RESET_ALL}", file=sys.stderr)


def print_warning(message):
    """Print a warning message in yellow."""
    print(f"{Fore.YELLOW}⚠ {message}{Style.RESET_ALL}")


def print_info(message):
    """Print an info message in blue."""
    print(f"{Fore.BLUE}ℹ {message}{Style.RESET_ALL}")


def print_table(headers, rows, tablefmt='simple'):
    """
    Print data in a formatted table.
    
    Args:
        headers: List of column headers
        rows: List of row data
        tablefmt: Table format (default: 'simple')
    """
    print(tabulate(rows, headers=headers, tablefmt=tablefmt))


def format_bytes(bytes_value):
    """
    Format bytes into human-readable format.
    
    Args:
        bytes_value: Size in bytes
        
    Returns:
        Formatted string (e.g., "1.5 GB")
    """
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes_value < 1024.0:
            return f"{bytes_value:.2f} {unit}"
        bytes_value /= 1024.0
    return f"{bytes_value:.2f} PB"


def confirm_action(message, default=False):
    """
    Prompt user for confirmation.
    
    Args:
        message: Confirmation message
        default: Default value if user just presses Enter
        
    Returns:
        Boolean indicating user's choice
    """
    suffix = " [Y/n]" if default else " [y/N]"
    response = input(f"{Fore.YELLOW}? {message}{suffix}: {Style.RESET_ALL}").lower().strip()
    
    if not response:
        return default
    
    return response in ('y', 'yes')
