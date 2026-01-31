"""
Tests for AWS V2 utility functions.
"""

import pytest
from aws_v2.utils import format_bytes, print_success, print_error, print_warning, print_info
from io import StringIO
import sys


def test_format_bytes():
    """Test byte formatting function."""
    assert format_bytes(0) == "0.00 B"
    assert format_bytes(512) == "512.00 B"
    assert format_bytes(1024) == "1.00 KB"
    assert format_bytes(1536) == "1.50 KB"
    assert format_bytes(1048576) == "1.00 MB"
    assert format_bytes(1073741824) == "1.00 GB"
    assert format_bytes(1099511627776) == "1.00 TB"


def test_print_functions_no_crash(capsys):
    """Test that print functions don't crash."""
    print_success("Success message")
    print_error("Error message")
    print_warning("Warning message")
    print_info("Info message")
    
    captured = capsys.readouterr()
    assert "Success message" in captured.out or "Success message" in captured.err
    assert "Error message" in captured.out or "Error message" in captured.err
    assert "Warning message" in captured.out or "Warning message" in captured.err
    assert "Info message" in captured.out or "Info message" in captured.err


if __name__ == '__main__':
    pytest.main([__file__])
