# Copyright (c) 2025, InfinityQ Technology, Inc.

"""
Some helping functions for the timeouts
"""

import time


def get_dynamic_wait_interval(start_time: float) -> float:
    """
    Returns a wait interval (in seconds) based on how much time
    has elapsed since `start_time`.

    [0,   10[ --> returns 0.25 seconds
    [10,  60[ --> returns 1 seconds
    [60, inf[ --> returns 5 seconds
    """
    elapsed = time.time() - start_time

    if elapsed < 10:
        return 0.25
    elif elapsed < 60:
        return 1
    return 5
