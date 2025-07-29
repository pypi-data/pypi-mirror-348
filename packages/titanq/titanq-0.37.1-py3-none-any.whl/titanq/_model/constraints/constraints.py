# Copyright (c) 2024, InfinityQ Technology, Inc.

import logging
from typing import Optional

from titanq._model.array.arraybuilder.array_builder_collection import ArrayBuilderCollection
from titanq._model.array.arraylike import ArrayLike

from .base_constraints import BaseConstraints
from ...errors import ConstraintSizeError


log = logging.getLogger("TitanQ")


class Constraints(BaseConstraints):
    def __init__(self) -> None:
        super().__init__()

        self._constraint_weights: ArrayBuilderCollection = ArrayBuilderCollection()
        self._constraint_bounds: ArrayBuilderCollection = ArrayBuilderCollection()


    def is_empty(self) -> bool:
        """Return if all constraints are empty."""
        return self._constraint_weights.is_empty() and self._constraint_bounds.is_empty()


    def add_constraint(self, num_variables: int, constraint_weights: ArrayLike, constraint_bounds: ArrayLike) -> None:
        """
        Add a constraint to the existing ones

        :param num_variables: the number of variables from the model
        :param constraint_weights: constraint_weights to append to the existing ones.
        :param constraint_bounds: constraint_bounds to append to the existing ones.

        :raises ConstraintSizeError:
            Number of constraints is different than the number of
            variables.
        """
        # shape validation
        if constraint_weights.shape()[1] != num_variables:
            raise ConstraintSizeError(
                "Constraint mask shape does not match the number of variables. "
                + f"Number of constraints: {constraint_weights.shape()[1]}, "
                + f"Number of variables: {num_variables}")


        self._constraint_weights.append(constraint_weights)
        self._constraint_bounds.append(constraint_bounds)


    def weights(self) -> Optional[ArrayLike]:
        """Returns the weights constraints."""
        if self._constraint_weights.is_empty():
            return None
        return self._array_like_factory.create_minimal(self._constraint_weights)


    def bounds(self) -> Optional[ArrayLike]:
        """Returns the bounds constraints."""
        if self._constraint_bounds.is_empty():
            return None
        return self._array_like_factory.create_numpy(self._constraint_bounds)
