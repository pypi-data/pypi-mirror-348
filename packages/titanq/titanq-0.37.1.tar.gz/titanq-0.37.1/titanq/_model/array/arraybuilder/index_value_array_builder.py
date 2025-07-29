# Copyright (c) 2025, InfinityQ Technology, Inc.

from typing import Iterable, List, Tuple, Union

from titanq._model.array.arraybuilder import ArrayBuilder, IndexKey, RealNumber


class IndexValueArrayBuilder(ArrayBuilder):
    """
    IndexValueArrayBuilder is an implementation of the ArrayBuilder interface that stores data in a dictionary
    where the keys are tuples of indices (x, y) and the values are real numbers (int or float).

    The additional methods keys() and values() make it faster to retrieve arrays from this builder in some cases.
    """

    def __init__(self, shape: Tuple[int, ...]):
        """
        Initialize an IndexValueArrayBuilder.

        :param shape: Determine the shape of the IndexValueArrayBuilder, this is needed to calculate the density.
        """
        self._shape = shape
        self._data = {}

    def shape(self) -> Tuple[int, ...]:
        return self._shape

    def density(self) -> float:
        return len(self._data) / (self.shape()[0] * self.shape()[1])

    def non_null_items(self) -> Iterable[Tuple[IndexKey, RealNumber]]:
        return self._data.items()

    def is_empty(self) -> bool:
        """Returns True if no value is stored, otherwise False."""
        return not self._data

    def append(self, x: int, y: int, value: Union[int, float]) -> None:
        """Adds or update a value at the given (x, y) index."""
        self._data[(x, y)] = self._data.get((x, y), 0) + value

    def keys(self) -> List[IndexKey]:
        """Returns the coordinates of the stored data."""
        return self._data.keys()

    def values(self) -> List[RealNumber]:
        """Returns the values of the stored data"""
        return self._data.values()