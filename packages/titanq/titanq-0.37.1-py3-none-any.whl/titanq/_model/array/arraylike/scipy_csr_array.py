# Copyright (c) 2025, InfinityQ Technology, Inc.

from typing import Iterable, Tuple

import numpy as np
from scipy.sparse import csr_array

from titanq._model.array.arraybuilder import IndexKey, RealNumber
from titanq._model.array.arraylike.scipy_coo_array import ScipyCooArray


class ScipyCsrArray(ScipyCooArray):

    def __init__(self, array: csr_array):
        """
        Creates a ScipyCsrArray implementing ArrayLike

        :param array: The scipy Compressed Sparse Row array itself
        """
        self._array = array

    def non_null_items(self) -> Iterable[Tuple[IndexKey, RealNumber]]:
        # converting to coo_array is very quick and efficient, there is no need to re-implement this
        # as coo_array already handles this.
        scipy_coo_array = ScipyCooArray(self._array.tocoo())
        return iter(scipy_coo_array.non_null_items())

    def iter_nonzero_row_values(self) -> Iterable[np.ndarray]:
        if self.ndim() == 1:
            raise NotImplementedError(f"{self.__class__.__name__}: 1D arrays are not iterable with 'iter_nonzero_row_values()'")

        indptr = self._array.indptr
        data = self._array.data

        num_rows = self._array.shape[0]
        for i in range(num_rows):
            start = indptr[i]
            end = indptr[i + 1]
            nnz = data[start:end]
            yield nnz