# Copyright (c) 2025, InfinityQ Technology, Inc.

import io
from typing import Iterable, List, Tuple, Union

import numpy as np

from titanq._model.array.arraybuilder import IndexKey, RealNumber
from titanq._model.array.arraylike import ArrayLike, util


class NumpyArray(ArrayLike):

    def __init__(self, array: np.ndarray):
        """
        Creates a NumpyArray implementing ArrayLike

        :param array: The numpy ndarray itself
        """
        self._array = array

    def shape(self) -> Tuple[int, int]:
        return self._array.shape

    def density(self) -> float:
        return np.count_nonzero(self._array) / self._array.size

    def non_null_items(self) -> Iterable[Tuple[IndexKey, RealNumber]]:
        non_zero_indices = np.nonzero(self._array)
        if len(non_zero_indices) == 1: # 1D
            for i in non_zero_indices:
                yield (0, i), self._array[i]
        else: # 2D
            for i, j in zip(non_zero_indices[0], non_zero_indices[1]):
                yield (i, j), self._array[i, j]

    def inner(self) -> np.ndarray:
        return self._array

    def ndim(self) -> int:
        return self._array.ndim

    def data_type(self) -> np.dtype:
        return self._array.dtype

    def is_binary(self) -> bool:
        return np.logical_xor((self._array == 1), (self._array == 0)).all()

    def sum(self, axis=None) -> Union[int, np.ndarray]:
        return np.sum(self._array, axis=axis)

    def to_bytes(self) -> bytes:
        buffer = io.BytesIO()
        np.save(buffer, self._array)
        return buffer.getvalue()

    def reshape_to_2d(self) -> None:
        if self.ndim() != 1:
            raise ValueError("Input array is not 1-D. Cannot reshape array.")

        self._array = self._array.reshape(1, -1)

    def repeat_rows(self) -> None:
        self._array = np.repeat(self._array, 2).reshape(-1, 2)

    def isnan(self) -> bool:
        return np.isnan(self._array).any()

    def isinf(self) -> bool:
        return np.isinf(self._array).any()

    def __iter__(self) -> Iterable[Union[RealNumber, 'NumpyArray']]:
        if self.ndim() == 1: # check for ndim only once for performance gains
            for value in self._array:
                yield value
        else:
            for row in self._array:
                yield NumpyArray(row)

    def iter_nonzero_row_values(self) -> Iterable[np.ndarray]:
        if self.ndim() == 1:
            raise NotImplementedError(f"{self.__class__.__name__}: 1D arrays are not iterable with 'iter_nonzero_row_values()'")

        for row in self._array:
            yield row[row != 0]

    def is_first_col_lower_second_col(self) -> bool:
        return util.compare_first_col_lower_second_col(self._array)

    def are_values_unsigned_integer(self) -> bool:
        return util.are_values_unsigned_integer(self._array)

    def row_sums_under_cardinality(self, numpy_array: np.ndarray) -> Tuple[List[int], List[int]]:
        return util.row_sums_under_cardinality(self.sum(axis=1), numpy_array)