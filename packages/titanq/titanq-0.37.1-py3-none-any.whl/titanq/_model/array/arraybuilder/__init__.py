# Copyright (c) 2025, InfinityQ Technology, Inc.

from abc import ABC, abstractmethod
from typing import Iterable, Tuple, Union


IndexKey = Tuple[int, int]
RealNumber = Union[int, float]


class ArrayBuilder(ABC):
    """
    ArrayBuilder allows data structures to be eventually converted into an ArrayLike.
    """

    @abstractmethod
    def density(self) -> float:
        """Returns the density of the array builder."""
        pass

    @abstractmethod
    def shape(self) -> Tuple[int, ...]:
        """Returns the shape of the array builder."""
        pass

    @abstractmethod
    def non_null_items(self) -> Iterable[Tuple[IndexKey, RealNumber]]:
        """
        Iterate over the non-null content of the array builder.

        :param start_row_index: appends it to the start of the row index, this is useful when iterating
        over multiple array builders.
        """
        pass