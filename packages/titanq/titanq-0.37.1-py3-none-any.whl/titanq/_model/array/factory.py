# Copyright (c) 2025, InfinityQ Technology, Inc.

from typing import Type, Union

import numpy as np
from scipy.sparse import coo_array, csr_array

from titanq._model.array import _TITANQ_DTYPE, Array, conversion_util
from titanq._model.array.arraybuilder import ArrayBuilder
from titanq._model.array.arraylike import ArrayLike
from titanq._model.array.arraylike.numpy_array import NumpyArray
from titanq._model.array.arraylike.scipy_coo_array import ScipyCooArray
from titanq._model.array.arraylike.scipy_csr_array import ScipyCsrArray
from titanq._model.array.transform import ArrayTransformChecker
from titanq._model.array.transform.sparse_threshold import SparseThresholdStrategy


_SPARSE_THRESHOLD = 0.2 # 20%

ArrayLikeFactoryInputs = Union[Array, ArrayBuilder]


class ArrayLikeFactory:
    """
    `ArrayLikeFactory` handles the creation of ArrayLike objects in the array module.

    Methods
    -------
    `create_numpy()` will create a numpy array like object.

    `create_scipy_coo_array()` will create a scipy coo array like object.

    `create_minimal()` will create a resource efficient array like object. It focuses
    on minimizing memory usage.
    """
    def __init__(self):
        self._sparse_transform_checker = ArrayTransformChecker(SparseThresholdStrategy(_SPARSE_THRESHOLD))

    def create_numpy(self, array: ArrayLikeFactoryInputs, data_type: np.dtype = _TITANQ_DTYPE) -> NumpyArray:
        """Creates a `NumpyArray` array like object."""
        array_builder = self._as_array_builder(array, data_type)

        return self._array_like_from_array_builder(array_builder, NumpyArray)

    def create_minimal(self, array: ArrayLikeFactoryInputs) -> ArrayLike:
        """
        Returns the corresponding `ArrayLike` based on the instance type, optimizing for
        minimal memory usage.
        """
        array_builder = self._as_array_builder(array)

        # apply the sparse threshold strategy
        array_like_type = self._sparse_transform_checker.check(array_builder)

        return self._array_like_from_array_builder(array_builder, array_like_type)

    def _as_array_builder(self, array: ArrayLikeFactoryInputs, data_type: np.dtype = _TITANQ_DTYPE) -> ArrayBuilder:
        """Creates and returns the `ArrayBuilder` based on the instance type."""
        if isinstance(array, np.ndarray):
            return NumpyArray(array.astype(data_type))

        elif isinstance(array, coo_array):
            return ScipyCooArray(array.astype(data_type))

        elif isinstance(array, csr_array):
            return ScipyCsrArray(array.astype(data_type))

        elif isinstance(array, ArrayBuilder): # Already an array builder
            return array

        else:
            raise ValueError(f"Unsupported array type: {type(array)}")

    def _array_like_from_array_builder(self, array: ArrayBuilder, type: Type[ArrayLike]) -> ArrayLike:
        """Converts an `ArrayBuilder` into an `ArrayLike` depending on the provided `type`."""
        if isinstance(array, type):
            return array # there is no need to convert it to itself

        if type is NumpyArray:
            numpy_array = conversion_util.array_builder_to_numpy(array)
            return self._as_array_builder(numpy_array)

        elif type is ScipyCooArray:
            coo_array = conversion_util.array_builder_to_coo_array(array)
            return self._as_array_builder(coo_array)

        elif type is ScipyCsrArray:
            csr_array = conversion_util.array_builder_to_csr_array(array)
            return self._as_array_builder(csr_array)
