# Copyright (c) 2024, InfinityQ Technology, Inc.

from abc import abstractmethod, ABC

from titanq._model.array.factory import ArrayLikeFactory


class BaseConstraints(ABC):

    def __init__(self):
        self._array_like_factory = ArrayLikeFactory()

    @abstractmethod
    def is_empty(self):
        """Return if all constraints are empty."""
        pass