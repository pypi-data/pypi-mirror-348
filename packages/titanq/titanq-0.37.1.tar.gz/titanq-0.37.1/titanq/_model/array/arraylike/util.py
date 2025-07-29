# Copyright (c) 2025, InfinityQ Technology, Inc.


import logging
from typing import List, Tuple
import numpy as np

log = logging.getLogger("TitanQ")


def row_sums_under_cardinality(sum, numpy_array: np.ndarray) -> Tuple[List[int], List[int]]:
    """
    Returns all rows indices that their values sum is equal/less than the given
    cardinality in the `numpy_array`.

    :param sum: sum of all values in each row
    :param numpy_array: array to compare to the sum

    :return: A tuple of the equal indices and less indices
    """
    equal_indices = np.where(sum == numpy_array)[0]
    less_indices = np.where(sum < numpy_array)[0]

    return (equal_indices, less_indices)


def compare_first_col_lower_second_col(mask: np.ndarray) -> bool:
    """Returns if the numpy array has every first column lower than the second."""
    if mask.ndim != 2 or mask.shape[1] != 2:
        raise ValueError("`compare_first_col_lower_second_col()` can only be used with arrays of shape (N, 2)")

    # filter first np.nan and np.inf
    valid_mask = np.isfinite(mask[:, 0]) & np.isfinite(mask[:, 1])
    return np.all(mask[valid_mask, 0] < mask[valid_mask, 1])


def are_values_unsigned_integer(mask: np.ndarray) -> bool:
    """Returns if the numpy array if every value is an unsigned integer"""
    if not np.issubdtype(mask.dtype, np.integer):
        return False # not integer array

    if np.any(mask < 0):
        return False # negative values found

    return True