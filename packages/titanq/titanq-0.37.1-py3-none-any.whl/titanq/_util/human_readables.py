# Copyright (c) 2025, InfinityQ Technology, Inc.

"""
Some helping functions to make some text human readable
"""

def bytes_size_human_readable(size: int) -> str:
    """
    Returns a human readable string from a bytes number (size).
    Will be maxed to Terabytes.

    ex: 1000 --> '1KB' or 1 500 000 --> '1.5MB'
    """
    two_power_ten = 1024.0
    for unit in ["B", "KB", "MB", "GB"]:
        if abs(size) < two_power_ten:
            return f"{size:3.1f}{unit}"
        size /= two_power_ten
    return f"{size:3.1f}TB" # return in terabytes if above