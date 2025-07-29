# Copyright (c) 2024, InfinityQ Technology, Inc.

import logging
from typing import Optional

from titanq._model.array.arraybuilder.array_builder_collection import ArrayBuilderCollection
from titanq._model.array.arraylike import ArrayLike

from .base_constraints import BaseConstraints
from ...errors import ConstraintSizeError


log = logging.getLogger("TitanQ")


class QuadConstraints(BaseConstraints):
    def __init__(self) -> None:
        super().__init__()

        self._quad_constraint_weights: ArrayBuilderCollection = ArrayBuilderCollection()
        self._quad_constraint_bounds: ArrayBuilderCollection = ArrayBuilderCollection()
        self._quad_constraint_linear_weights: ArrayBuilderCollection = ArrayBuilderCollection()

    def is_empty(self) -> bool:
        """return if all constraints are empty"""

        return (
            self._quad_constraint_weights.is_empty() and
            self._quad_constraint_bounds.is_empty() and
            self._quad_constraint_linear_weights.is_empty()
        )


    def add_constraint(
        self,
        num_variables: int,
        quad_constraint_weights: ArrayLike,
        quad_constraint_bounds: ArrayLike,
        quad_constraint_linear_weights: Optional[ArrayLike] = None
    ) -> None:
        """
        Add a quadratic constraint to the existing ones

        :param num_variables: the number of variables from the model
        :param quad_constraint_weights: quadratic constraint weights to append to the existing ones.
        :param quad_constraint_bounds: quadratic constraint bounds to append to the existing ones.
        :param quad_constraint_linear_weights: quadratic constraint linear weights to append to the existing ones.

        :raises ConstraintSizeError:
            Number of constraints is different than the number of
            variables.
        """
        # shape validation
        if quad_constraint_weights.shape() != (num_variables, num_variables):
            raise ConstraintSizeError(
                "Invalid constraint_mask shape: expected (N,N) where N is the number of variables "
                + f"({num_variables},{num_variables}), but got {quad_constraint_weights.shape()}.")

        if quad_constraint_linear_weights is not None and quad_constraint_linear_weights.shape() != (1, num_variables):
                raise ValueError(
                    "Invalid constraint_linear_weights shape: expected (N,) where N is "
                    + f"the number of variables ({num_variables}), "
                    + f"but got {quad_constraint_linear_weights.shape()}.")

        self._quad_constraint_weights.append(quad_constraint_weights)
        self._quad_constraint_bounds.append(quad_constraint_bounds)

        if quad_constraint_linear_weights is not None:
            self._quad_constraint_linear_weights.append(quad_constraint_linear_weights)


    def weights(self) -> Optional[ArrayLike]:
        """Returns the quadratic weights constraints."""
        if self._quad_constraint_weights.is_empty():
            return None
        return self._array_like_factory.create_minimal(self._quad_constraint_weights)


    def bounds(self) -> Optional[ArrayLike]:
        """Returns the quadratic bounds constraints."""
        if self._quad_constraint_bounds.is_empty():
            return None
        return self._array_like_factory.create_numpy(self._quad_constraint_bounds)

    def linear_weights(self) -> Optional[ArrayLike]:
        """Return the quadratic linear weights constraints."""
        if self._quad_constraint_linear_weights is None:
            return None
        if self._quad_constraint_linear_weights.is_empty():
            return None
        return self._array_like_factory.create_minimal(self._quad_constraint_linear_weights)
