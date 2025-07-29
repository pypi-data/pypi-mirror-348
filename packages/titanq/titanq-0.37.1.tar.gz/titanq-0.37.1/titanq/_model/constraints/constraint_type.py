# Copyright (c) 2025, InfinityQ Technology, Inc.
from enum import Enum

import numpy as np

from titanq._model.array.arraylike.numpy_array import NumpyArray



class ConstraintType(str, Enum):
    SET_PARTITIONING = "set_partitioning"
    CARDINALITY = "cardinality"
    EQUALITY = "equality"
    INEQUALITY = "inequality"


def get_constraint_type(mask: NumpyArray, bounds: NumpyArray) -> ConstraintType:
    """Returns the type of the constraint using the mask and bounds.

    :param mask: 1D Constraint mask
    :param bounds: 1D Constraint bounds

    :raises ValueError: If the shape of the mask or bounds doesn't match

    :return: The constraint type
    :rtype: ConstraintType
    """
    if bounds.ndim() != 1 or bounds.shape()[0] != 2:
        raise ValueError(f"constraint bounds has an invalid shape: {bounds.shape()}, expected: (2,)")


    if mask.ndim() != 1:
        raise ValueError(f"constraint mask has an invalid dimension: {mask.ndim()}, expected: 1")

    # use directly the numpy data
    bounds = bounds.inner()

    # detect inequality constraints
    if any(np.isnan(bounds)) or bounds[0] != bounds[1]:
        return ConstraintType.INEQUALITY

    # both bounds are equal from now on

    # any non-binary is an equality
    if not mask.is_binary():
        return ConstraintType.EQUALITY

    # any non-integer bounds or lower than 1 is an equality
    if bounds[0] % 1 != 0 or bounds[0] < 1:
        return ConstraintType.EQUALITY

    # equality value is equal to one
    if bounds[0] == 1:
        return ConstraintType.SET_PARTITIONING

    # equality value is lower or equal to the sum of the mask elements
    if bounds[0] <= mask.sum():
        return ConstraintType.CARDINALITY
    else:
        return ConstraintType.EQUALITY
