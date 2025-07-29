# Copyright (c) 2025, InfinityQ Technology, Inc.

"""
Array Transform module

This module provides functionality for checking various types of arrays and transform them in need.
It transforms them into different formats based on the chosen strategy.

It utilizes the strategy pattern, to provide a flexible approach for handling different array formats
and different check logic.

Example Usage
-------------
    factory = ArrayLikeFactory()

    # choose the strategy
    sprase_strategy = SparseStrategy()

    # create the transform checker with the strategy
    transform_checker = ArrayTransformChecker(sprase_strategy)

    # create the array
    array_builder = factory.create_numpy(np.array([[1, 0, 0], [0, 1, 0], [0, 0, 0]]))

    # use the transform checker
    convert_option = transform_checker.check(array)

    # convert_option is the type that you need to transform to
"""

from abc import ABC, abstractmethod

from titanq._model.array.arraybuilder import ArrayBuilder
from titanq._model.array.arraylike import ArrayLike


class ArrayTransformStrategy(ABC):
    """
    Abstract class that each strategy would implement.
    """

    @abstractmethod
    def check(self, array: ArrayBuilder) -> ArrayLike:
        """
        Checks the array if a transform is needed.

        :param array: The array to check if a transform is needed

        :returns: The type of array to transform to
        """
        pass


class ArrayTransformChecker:
    """Array transform checker class that would apply a given strategy."""

    def __init__(self, strategy: ArrayTransformStrategy):
        self._strategy = strategy


    def check(self, array: ArrayBuilder) -> ArrayLike:
        return self._strategy.check(array)