# Copyright (c) 2025, InfinityQ Technology, Inc.

"""
Some decorators used across the module.
"""

from functools import wraps
from typing import Callable, TypeVar


T = TypeVar("T")


def chainable(method: Callable[[T], None]) -> Callable[[T], T]:
    """
    Decorator that would return self when used with a method.
    This is useful when you want to make chained methods.

    Usage:
        data = some_method().another_mother().even_another_method()
    """
    @wraps(method)
    def wrapper(self: T, *args, **kwargs) -> T:
        method(self, *args, **kwargs)
        return self
    return wrapper
