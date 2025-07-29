# Copyright (c) 2025, InfinityQ Technology, Inc.

from typing import Iterable, List, Tuple

from titanq._model.array.arraybuilder import ArrayBuilder, IndexKey, RealNumber


class ArrayBuilderCollection(ArrayBuilder):
    """
    ArrayBuilderCollection is an implementation of the ArrayBuilder interface that contains a
    list of other ArrayBuilder instances, effectively stacking them together and ordered.
    """

    def __init__(self):
        self._collection: List[ArrayBuilder] = []

    def shape(self) -> Tuple[int, ...]:
        # We need to iterate here through the collection and manually calculate the shape
        rows_counter = 0
        last_col_shape = 0
        for item in self._collection:
            rows_counter += item.shape()[0]
            last_col_shape = item.shape()[1]

        return (rows_counter, last_col_shape)

    def density(self) -> float:
        if len(self._collection) == 0:
            return 0

        # density needs to be calculated manually. In summary, each item
        # has a weight (number of rows), we multiply the weight by it's actual
        # density. Total is the sum of density by the total number of rows.
        density = 0
        rows_counter = 0
        for item in self._collection:
            # density for each array is it's density itself mulitiplied by a weight
            # which is the number of rows
            rows = item.shape()[0]
            density += item.density() * rows
            rows_counter += rows

        return density / rows_counter

    def non_null_items(self) -> Iterable[Tuple[IndexKey, RealNumber]]:
        offset = 0
        for arr in self._collection:
            for (x, y), value in arr.non_null_items():
                yield (x + offset, y), value
            offset += arr.shape()[0]

    def is_empty(self) -> bool:
        """Returns True if no value is stored, otherwise False."""
        return len(self._collection) == 0

    def append(self, array: ArrayBuilder) -> None:
        """Appends a new array builder object to the collection."""
        if not isinstance(array, ArrayBuilder):
            raise ValueError(
                f"{self.__class__.__name__}: append() only accepts 'ArrayBuilder' objects"
            )

        if len(array.shape()) != 2:
            raise ValueError(f"{self.__class__.__name__} should only be used with 2D Arrays")

        self._collection.append(array)