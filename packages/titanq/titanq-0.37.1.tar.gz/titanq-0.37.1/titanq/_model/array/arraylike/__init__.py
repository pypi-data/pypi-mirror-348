# Copyright (c) 2025, InfinityQ Technology, Inc.

from abc import ABC, abstractmethod
from typing import Any, Iterable, List, Tuple, Union

import numpy as np

from titanq._model.array.arraybuilder import ArrayBuilder


class ArrayLike(ArrayBuilder, ABC):
    """
    ArrayLike represents an array like passed in by a user. We support different formats (e.g. sparse, dense),
    so this class will hide the specific format and allow different array formats to behave the same.
    """

    @abstractmethod
    def inner(self) -> Any:
        """Returns the data of the instance itself of the array like."""
        pass

    @abstractmethod
    def ndim(self) -> int:
        """Returns the dimension count of the array like"""
        pass

    @abstractmethod
    def data_type(self) -> np.dtype:
        """
        Returns the data type of the elements contained in the ArrayBuilder.

        Currently, this is represented using numpy's dtype.
        """
        pass

    @abstractmethod
    def is_binary(self) -> bool:
        """Returns if the array like has only 0s and 1s values (binary)."""
        pass

    @abstractmethod
    def sum(self, axis=None) -> Union[int, np.ndarray]:
        """Returns the sum of the array elements."""
        pass

    @abstractmethod
    def to_bytes(self) -> bytes:
        """Returns the np type array as bytes."""
        pass

    @abstractmethod
    def reshape_to_2d(self) -> None:
        """
        Reshapes the array to a 2D array.

        ex: [1, 2] ->> [[1, 2]]
        """
        pass

    @abstractmethod
    def repeat_rows(self) -> None:
        """
        Reshapes the array to a 2D array and repeats the rows.

        ex: [1, 2] --> [[1, 1], [2, 2]]
        """
        pass

    @abstractmethod
    def isnan(self) -> bool:
        """True if one of the array elements is not a number."""
        pass

    @abstractmethod
    def isinf(self) -> bool:
        """True if one of the array elements is infinity."""
        pass

    @abstractmethod
    def is_first_col_lower_second_col(self) -> bool:
        """
        Can only be used with arrays shaped as (N, 2).

        Will return if every row has their first value lower
        than the second value.

        ex: [[0, 1], [0, 1]] -> True
        ex: [[0, 0], [0, 1]] -> True
        ex: [[1, 0], [0, 1]] -> False
        """
        pass

    @abstractmethod
    def are_values_unsigned_integer(self) -> bool:
        """Returns if all contained values are unsigned integer"""
        pass

    @abstractmethod
    def row_sums_under_cardinality(self, numpy_array: np.ndarray) -> Tuple[List[int], List[int]]:
        """
        Returns all rows indices that their values sum is equal/less than the given
        cardinality in the `numpy_array`.

        :param numpy_array: array to compare to the array like sum

        :return: A tuple of the equal indices and less indices
        """
        pass

    def __iter__(self) -> Iterable['ArrayLike']:
        """Iterates over the array like and will yield a new array like on each iteration."""
        raise NotImplementedError(
            f"{self.__class__.__name__}: not implemented with '__iter__'."
        )

    def iter_nonzero_row_values(self) -> Iterable[np.ndarray]:
        """
        Iterates over a 2D array like object, and will yield non null items only
        for each row into a new numpy array
        """
        raise NotImplementedError(
            f"{self.__class__.__name__}: not implemented with 'non_null_values_row()'."
        )