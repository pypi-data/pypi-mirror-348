# Copyright (c) 2025, InfinityQ Technology, Inc.

import numpy as np
from scipy.sparse import coo_array, csr_array

from titanq._model.array import _TITANQ_DTYPE
from titanq._model.array.arraybuilder import ArrayBuilder


def array_builder_to_numpy(array: ArrayBuilder) -> np.ndarray:
    numpy_array = np.zeros(array.shape(), dtype=_TITANQ_DTYPE)
    if len(array.shape()) == 1:
        for (_, y), value in array.non_null_items():
            numpy_array[y] = value
    else:
        for (x, y), value in array.non_null_items():
            numpy_array[x][y] = value
    return numpy_array


def array_builder_to_coo_array(array: ArrayBuilder) -> coo_array:
    rows = []
    cols = []
    data = []
    for (x, y), value in array.non_null_items():
        rows.append(x)
        cols.append(y)
        data.append(value)

    if len(array.shape()) == 1:
        numpy_array = np.zeros(array.shape()[0])
        for value in zip(cols, data):
            numpy_array[cols] = data

        # 1D coo_array can only be created through a list or a numpy object
        return coo_array(numpy_array, shape=array.shape(), dtype=_TITANQ_DTYPE)

    return coo_array((data, (rows, cols)), shape=array.shape(), dtype=_TITANQ_DTYPE)


def array_builder_to_csr_array(array: ArrayBuilder) -> csr_array:
    # convert the ArrayBuilder to a coo_array first, since it's naturally in coordinate format.
    # coo_array is efficient for incremental construction. Converting to csr_array is very efficient.
    coo_array = array_builder_to_coo_array(array)
    return coo_array.tocsr()