# Copyright (c) 2025, InfinityQ Technology, Inc.

import io
from typing import Iterable, List, Tuple, Union

import numpy as np
from scipy.sparse import coo_array, save_npz

from titanq._model.array.arraybuilder import IndexKey, RealNumber
from titanq._model.array.arraylike import ArrayLike, util


class ScipyCooArray(ArrayLike):

    def __init__(self, array: coo_array):
        """
        Creates a ScipyCooArray implementing ArrayLike

        :param array: The scipy COOrdinate array itself
        """
        self._array = array

    def shape(self) -> Tuple[int, int]:
        return self._array.shape

    def density(self) -> float:
        if self._array.ndim == 1:
            # non-zero elements divided by length of the 1D array
            return self._array.nnz / self._array.shape[0]
        else:
            # non-zero elements divided by the size of the 2D array
            return self._array.nnz / (self._array.shape[0] * self._array.shape[1])

    def non_null_items(self) -> Iterable[Tuple[IndexKey, RealNumber]]:
        if self.ndim() == 1:
            for col, data in zip(self._array.col, self._array.data):
                yield (0, col), data
        else:
            for row, col, data in zip(self._array.row, self._array.col, self._array.data):
                yield (row, col), data

    def inner(self) -> coo_array:
        return self._array

    def ndim(self) -> int:
        return self._array.ndim

    def data_type(self) -> np.dtype:
        return self._array.dtype

    def is_binary(self):
        return np.all((self._array.data == 1) | (self._array.data == 0))

    def sum(self, axis=None) -> Union[int, np.ndarray]:
        return self._array.sum(axis=axis)

    def to_bytes(self) -> bytes:
        buffer = io.BytesIO()
        save_npz(buffer, self._array)
        return buffer.getvalue()

    def reshape_to_2d(self) -> None:
        if self.ndim() != 1:
            raise ValueError("Input array is not 1-D. Cannot reshape array.")

        self._array = self._array.reshape(1, -1)

    def repeat_rows(self) -> None:
        self._array = coo_array(np.repeat(self._array.toarray(), 2).reshape(-1, 2))

    def isnan(self) -> bool:
        return np.isnan(self._array.data).any()

    def isinf(self) -> bool:
        return np.isinf(self._array.data).any()

    def is_first_col_lower_second_col(self) -> bool:
        return util.compare_first_col_lower_second_col(self._array.toarray())

    def are_values_unsigned_integer(self) -> bool:
        return util.are_values_unsigned_integer(self._array.toarray())

    def row_sums_under_cardinality(self, numpy_array: np.ndarray) -> List[int]:
        return util.row_sums_under_cardinality(self.sum(axis=1), numpy_array)