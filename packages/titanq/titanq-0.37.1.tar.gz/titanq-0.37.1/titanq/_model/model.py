# Copyright (c) 2024, InfinityQ Technology, Inc.

from contextlib import contextmanager
import logging
from scipy.sparse import coo_array, csr_array
from typing import Any, Dict, Generator, List, Literal, Optional, Tuple, Union

import numpy as np
import numpy.typing as npt

from titanq import errors
from titanq._api.client import Client
from titanq._api.model.solve import Parameters, Manifest, Request, Response
from titanq._event import EventEmitter, create_sink
from titanq._event.milestone import (
    ComputationFailedEvent,
    GotComputationIDEvent,
    UploadStartEvent,
    OptimizationCompletedEvent,
)
from titanq._event.defined_progress import DownloadResultEvent, UploadEvent
from titanq._event.undefined_progress import (
    PreparingDataEvent,
    SendingProblemEvent,
    WaitingForResultEvent
)
from titanq._model.array import Array
from titanq._model.array.arraybuilder.index_value_array_builder import IndexValueArrayBuilder
from titanq._model.array.arraylike import ArrayLike
from titanq._model.array.factory import ArrayLikeFactory
from titanq._model.bytes_reader import BytesReaderWithCallback
from titanq._model.math_object import Equation, Expression
from titanq._storage import StorageClient
from titanq._storage.temp_storage import TempStorage
from titanq._util.api_key import get_and_validate_api_key

from .constraints import (
    Constraints,
    get_constraint_type,
    QuadConstraints,
)
from titanq.errors import (
    ConstraintAlreadySetError,
    EmptyResultError,
    ComputationFailedError,
    MissingFinishedStatusError,
    MissingVariableError,
    ObjectiveAlreadySetError,
    UnknownError,
    titanq_error_including_computation_id,
)
from .manifest import ManifestBuilder
from .objective import Objective, Target
from .optimize_response import OptimizeResponse
from .precision import Precision
from .variables import BinaryVariable, ContinuousVariable, IntegerVariable, Variable, Vtype

log = logging.getLogger("TitanQ")


class Model:
    """
    Root object to define a problem to be optimized
    """

    def __init__(
        self,
        *,
        api_key: str = None,
        storage_client: StorageClient = None,
        base_server_url: str = "https://titanq.infinityq.io",
        log_mode: Optional[Literal["pretty", "text", "off"]] = "pretty"
        ) -> None:
        """
        Initiate the model with a storage client. If the storage_client is missing, the storage will be managed by TitanQ.

        Notes
        -----
        If the storage is managed by TitanQ, the total input files size is limited to 1GB.

        Parameters
        ----------
        api_key
            TitanQ API key to access the service.
            If not set, it will use the environment variable ``TITANQ_API_KEY``
        storage_client
            Storage to choose in order to store some items.
        base_server_url
            TitanQ API server url, default set to ``https://titanq.infinityq.io``.
        log_mode
            Specifies the logging mode.

        Raises
        ------
        MissingTitanqApiKey
            If no API key is set and is also not set as an environment variable

        Examples
        --------
        With an S3 storage client
            >>> from titanq import Model, S3Storage
            >>> storage_client = S3Storage(
                access_key="{insert aws bucket access key here}",
                secret_key="{insert aws bucket secret key here}",
                bucket_name="{insert bucket name here}"
            )
            >>> model = Model(storage_client)

        Managed storage client
            >>> from titanq import Model, S3Storage
            >>> model = Model()
        """
        # model related
        self._variables: List[Variable] = []
        self._objective: Objective = None
        self._constraints = Constraints()
        self._quad_constraints = QuadConstraints()
        self._array_like_factory = ArrayLikeFactory()
        self._manifest_builder: ManifestBuilder = ManifestBuilder()

        # TitanQ communication related
        from titanq import __title__ as titanq_title, __version__ as titanq_version
        self._titanq_client = Client(
            base_server_address=base_server_url,
            api_key=get_and_validate_api_key(api_key),
            name=titanq_title,
            version=titanq_version
        )
        if storage_client is None:
            self._storage_client = TempStorage(self._titanq_client)
        else:
            self._storage_client = storage_client

        # miscellaneous
        self._log_mode = log_mode

    @contextmanager
    def _event_scope(self, is_optimization: bool = False) -> Generator[EventEmitter, Any, Any]:
        """
        Returns a context manager to emit events with.

        :param is_optimization: If the events are part of an optimization process, the sinks will have
        a different behaviour
        """
        self._event_emitter = create_sink(self._log_mode, is_optimization)
        try:
            self._event_emitter.start()
            yield self._event_emitter
        finally:
            self._event_emitter.stop()

    def get_objective_matrices(self) -> Tuple[Optional[Union[np.ndarray, csr_array]], Optional[np.ndarray]]:
        """
        Retrieve the weights and bias vector from the model's objective. Both will be None
        if not set.

        Return
        ------
        Weights matrix and the bias vector if the objective has been set, else both will be None
        """
        if self._objective is not None:
            weights = self._objective.weights().inner() if self._objective.weights() else None
            bias = self._objective.bias().inner()
            return weights, bias

        return (None, None)


    def get_objective_constant_term(self) -> float:
        """
        Retrieve the objective constant term.

        Refer to :meth:`set_objective_matrices` for the explanation of the objective constant term.

        Return
        ------
        Objective constant term
        """
        return self._objective.constant_term()


    def get_constraints_weights_and_bounds(self) -> Tuple[Optional[Union[np.ndarray, csr_array]], Optional[np.ndarray]]:
        """
        Retrieve the weights and bounds of all constraints from the model.

        Return
        ------
        Constraints weights if not None and constraints bounds if not None
        """
        weights = self._constraints.weights()
        bounds = self._constraints.bounds()
        return weights.inner() if weights else None, bounds.inner() if bounds else None


    def get_quad_constraints_weights_and_bounds(self) -> Tuple[Optional[Union[np.ndarray, csr_array]], Optional[np.ndarray]]:
        """
        Retrieve the quadratic constraints weights and bounds.

        Return
        ------
        Quadratic constraints weights if not None and quadratic constraints bounds if not None
        """
        weights = self._quad_constraints.weights()
        bounds = self._quad_constraints.bounds()
        return weights.inner() if weights else None, bounds.inner() if bounds else None


    def get_quad_constraints_linear_weights(self) -> Optional[Union[np.ndarray, csr_array]]:
        """
        Retrieve the quadratic constraints linear weights.

        Return
        ------
        Quadratic constraints linear weights if not None
        """
        lin_weights = self._quad_constraints.linear_weights()
        return lin_weights.inner() if lin_weights else None


    def add_variable_vector(
        self,
        name: str = '',
        size: int = 1,
        vtype: Vtype = Vtype.BINARY,
        variable_bounds:
            Optional[
                Union[
                    List[Tuple[int, int]],
                    List[Tuple[float, float]],
                ]
            ]=None,
    ) -> npt.NDArray[Any]:
        """
        Add a vector of variable to the model. Multiple variables vector can be added but with different names.

        Notes
        -----
        If Vtype is set to ``Vtype.INTEGER`` or ``Vtype.CONTINUOUS``, variable_bounds need to be set.

        Parameters
        ----------
        name
            The name given to this variable vector.
        size
            The size of the vector.
        vtype
            Type of the variables inside the vector.
        variable_bounds
            Lower and upper bounds for the variable vector. A list of tuples (can be either integers or continuous)

        Return
        ------
        variable
            The variable vector created.

        Raises
        ------
        MaximumVariableLimitError
            If the total size of variables exceed the limit.
        ValueError
            If the size of the vector is < 1

        Examples
        --------
        >>> from titanq import Model, Vtype
        >>> model.add_variable_vector('x', 3, Vtype.BINARY)
        >>> model.add_variable_vector('y', 2, Vtype.INTEGER, [[0, 5], [1, 6]])
        >>> model.add_variable_vector('z', 3, Vtype.CONTINUOUS, [[2.3, 4.6], [3.1, 5.3], [1.1, 4]])
        """

        if variable_bounds is None:
            variable_bounds = []

        # validation
        if not self._constraints.is_empty() or not self._quad_constraints.is_empty():
            raise ConstraintAlreadySetError(
                "Cannot add additional variables once linear or quadratic " \
                "constraints have been defined")

        if self._objective is not None:
            raise ObjectiveAlreadySetError("Cannot add additional variable once objective have been defined")

        if vtype is Vtype.BINARY and variable_bounds:
            raise ValueError("variable_bounds is not supported with Vtype.BINARY")

        if size < 1:
            raise ValueError("Variable vector size cannot be less than 1")

        # create the variable
        variables = []
        if vtype is Vtype.BINARY:
            variables = [BinaryVariable(name, i, len(self._variables) + i) for i in range(size) ]
        elif vtype is Vtype.INTEGER:
            variables = [IntegerVariable(name, i, len(self._variables) + i, variable_bounds[i]) for i in range(size)]
        elif vtype is Vtype.CONTINUOUS:
            variables = [ContinuousVariable(name, i, len(self._variables)+i, variable_bounds[i]) for i in range(size)]
        else:
            raise NotImplementedError(f"Unsupported variable type: {vtype}")

        self._variables.extend(variables)
        log.debug(f"add variable name='{name}', type={str(vtype)}, size={size}.")

        return np.array([Expression(v) for v in variables])


    def add_constraint_from_expression(self, equation: Equation):
        """
        Adds a constraint to the model using the given expression.

        This method processes the provided constraint expression to add it as a constraint to the
        optimization problem. Only linear constraints of the following types are supported:

        - `A == B`
        - `A <  B`
        - `A <= B`
        - `A >  B`
        - `A >= B`

        Constraints involving quadratic terms cannot be added as
        expressions and will raise an error.
        Instead, use :meth:`add_quadratic_equality_constraint` or
        :meth:`add_quadratic_inequality_constraint`.

        Parameters
        ----------
        expression
            The constraint expression. This should be an instance of `Equation`.

        Raises
        ------
        ValueError
            If the provided expression contains quadratic terms.
        TypeError
            If the provided expression is of an invalid or unsupported type.

        Examples
        --------
        >>> from titanq import Model, Vtype
        >>> x = model.add_variable_vector('x', 2, Vtype.BINARY)
        >>> y = model.add_variable_vector('y', 2, Vtype.BINARY)
        >>> expr = sum(x+y) == 1
        >>> model.add_constraint_from_expression(expr)
        """
        if not isinstance(equation, Equation):
            raise TypeError(f"The given constraint equation is not of type {str(Equation)}.")

        n_variable = len(self._variables)
        mask, bounds = equation.generate_constraint(n_variable)

        constraint_weights_arr_like = self._array_like_factory.create_minimal(mask)

        constraint_bounds_arr_like = self._array_like_factory.create_numpy(bounds)
        constraint_bounds_arr_like.reshape_to_2d()

        self._constraints.add_constraint(
            num_variables=n_variable,
            constraint_weights=constraint_weights_arr_like,
            constraint_bounds=constraint_bounds_arr_like
        )


    def set_objective_expression(self, expr: Expression, target=Target.MINIMIZE):
        """
        Sets the objective function for the optimization problem using the given expression.

        This method processes the provided expression to extract the bias vector and weight matrix,
        and then sets these as the objective matrices for the optimization problem.

        Parameters
        ----------
        expr
            The expression defining the objective function.
        target
            The target of this objective matrix.

        Raises
        ------
        TypeError
            if the provided expression contains any invalid/unsupported input

        Examples
        --------
        >>> from titanq import Model, Vtype
        >>> x = model.add_variable_vector('x', 2, Vtype.BINARY)
        >>> y = model.add_variable_vector('y', 2, Vtype.BINARY)
        >>> expr = (np.array([3, 4]) * x + (x * y) - 5 * y)[0]
        >>> model.set_objective_expression(expr)
        """
        if not isinstance(expr, Expression):
            raise TypeError(f"The given objective expression is not of type {str(Expression)}.")

        constant, bias, weights = expr.split_into_component(len(self._variables))
        self._objective = self._create_objective(weights, bias, target, constant)


    def set_objective_matrices(
        self,
        weights: Optional[Union[np.ndarray, coo_array, csr_array]],
        bias: np.ndarray,
        target: Target = Target.MINIMIZE,
        constant_term: float = 0.0
    ) -> None:
        """
        Set the objective matrices for the model.

        Parameters
        ----------
        weights
            The quadratic objective matrix, **this matrix needs to be symmetrical**.
            A 2-D array (must be float32).
            Weights matrix can be set to **None** if it is a linear problem with no quadratic elements.
        bias
            The linear constraint vector. A 1-D array.
        target
            The target of this objective matrix.
        constant_term
            This parameter represents a fixed value added to the final computed objective value.

            Example: Suppose the objective function to minimize is 'f(x) = x^2 + 2x + 4' and 'x' is a binary variable.

            The optimal solution would be x = 0 resulting in an optimal objective function value of f(x)=4.
            However, the solver ignores constant terms and only seeks to minimize f(x) = x^2 + 2x.
            This would typically yield f(x)=0 by default with the optimal solution of x=0.
            constant_term should be set to 4 to yield an objective function value of f(x)=4.

        Raises
        ------
        MissingVariableError
            If no variable have been added to the model.
        ObjectiveAlreadySetError
            If an objective has already been set in this model.
        ValueError
            If the weights shape or the bias shape does not fit the variables in the model.
            If the weights or bias data type is not float32.

        Examples
        --------
        >>> from titanq import Model, Target
        >>> edges = {0:[4,5,6,7], 1:[4,5,6,7], 2:[4,5,6,7], 3:[4,5,6,7], 4:[0,1,2,3], 5:[0,1,2,3], 6:[0,1,2,3], 7:[0,1,2,3]}
        >>> size = len(edges)
        >>> weights = np.zeros((size, size), dtype=np.float32)
        >>> for root, connections in edges.items():
        >>>     for c in connections:
        >>>         weights[root][c] = 1
        >>> # construct the bias vector (Uniform weighting across all nodes)
        >>> bias = np.asarray([0]*size, dtype=np.float32)
        >>> model.set_objective_matrices(weights, bias, Target.MINIMIZE)
        """
        self._objective = self._create_objective(weights, bias, target, constant_term)


    def _create_objective(
        self,
        weights: Optional[Union[Array, IndexValueArrayBuilder]],
        bias: Array,
        target: Target = Target.MINIMIZE,
        constant_term: float = 0.0
    ) -> Objective:
        """Creates the Objective object"""
        if len(self._variables) == 0:
            raise MissingVariableError("Cannot set objective before adding a variable to the model.")

        if self._objective is not None:
            raise ObjectiveAlreadySetError("An objective has already have been set for this model.")

        if bias is None:
            raise ValueError("Bias cannot be set to None")

        log.debug("set objective matrix and bias vector.")

        bias = self._array_like_factory.create_numpy(bias)

        if weights is not None:
            weights = self._array_like_factory.create_minimal(weights)

        return Objective(
            var_size=len(self._variables),
            bias=bias,
            weights=weights,
            target=target,
            constant_term=constant_term,
        )


    def add_set_partitioning_constraints_matrix(
        self,
        constraint_mask: Union[np.ndarray, coo_array, csr_array]
    ) -> None:
        """
        Adds set partitioning constraints in matrix format to the model.

        Parameters
        ----------
        constraint_mask
            A 2-D array (must be binary).
            The constraint_mask matrix of shape (M, N) where M the number of constraints and N is the number of variables.

        Raises
        ------
        MissingVariableError
            If no variable have been added to the model.
        ConstraintSizeError
            If the constraint_mask shape does not fit the expected shape of this model.
        ValueError
            If the constraint_mask data type is not binary.

        Examples
        --------
        >>> constraint_mask = np.array([[1, 1, 1, 0, 1], [1, 1, 1, 1, 0]])
        >>> model.add_set_partitioning_constraints_matrix(constraint_mask)
        """
        constraint_mask_arr_like = self._array_like_factory.create_minimal(constraint_mask)

        if len(self._variables) == 0:
            raise MissingVariableError("Cannot set constraints before adding a variable to the model.")

        if constraint_mask_arr_like.ndim() == 1:
            raise ValueError(
                "Cannot use add_set_partitioning_constraints_matrix() function with a vector, " \
                "please use add_set_partitioning_constraint() instead")

        if not constraint_mask_arr_like.is_binary():
            raise ValueError("Cannot add a constraint if the values are not in binary.")

        self._constraints.add_constraint(
            num_variables=len(self._variables),
            constraint_weights=constraint_mask_arr_like,
            constraint_bounds=self._array_like_factory.create_numpy(np.ones((constraint_mask_arr_like.shape()[0], 2)))
        )


    def add_set_partitioning_constraint(
        self,
        constraint_mask: Union[np.ndarray, coo_array]
    ) -> None:
        """
        Adds set partitioning constraint vector to the model.

        Parameters
        ----------
        constraint_mask
            A 1-D array (must be binary).
            The constraint_mask vector of shape (N,) where N is the number of variables.

        Raises
        ------
        MissingVariableError
            If no variable have been added to the model.
        ConstraintSizeError
            If the constraint_mask shape does not fit the expected shape of this model.
        ValueError
            If the constraint_mask data type is not binary.

        Examples
        --------
        >>> constraint_mask = np.array([1, 1, 1, 0, 1])
        >>> model.add_set_partitioning_constraint(constraint_mask)
        """
        constraint_mask_arr_like = self._array_like_factory.create_minimal(constraint_mask)

        if constraint_mask_arr_like.ndim() > 1:
            raise ValueError(
                "Cannot use this add_set_partitioning_constraint() function with a matrix, " \
                "please use add_set_partitioning_constraints_matrix() instead")

        constraint_mask_arr_like.reshape_to_2d()

        self.add_set_partitioning_constraints_matrix(constraint_mask=constraint_mask_arr_like)


    def add_cardinality_constraints_matrix(
        self,
        constraint_mask: Union[np.ndarray, coo_array, csr_array],
        cardinalities: Union[np.ndarray, coo_array]
    ) -> None:
        """
        Adds cardinality constraints in matrix format to the model.

        Parameters
        ----------
        constraint_mask
            A 2-D array (must be binary).
            The constraint_mask matrix of shape (M, N) where M the number of constraints and N is the number of variables.
        cardinalities
            A 1-D array (must be non-zero unsigned integer).
            The constraint_rhs vector of shape (M,) where M is the number of constraints.

        Raises
        ------
        MissingVariableError
            If no variable have been added to the model.
        ConstraintSizeError
            If the constraint_mask shape or the constraint_rhs shape does not fit the expected shape of this model.
        ValueError
            If the constraint_mask is not binary or cardinalities data type are not unsigned integers.

        Examples
        --------
        >>> constraint_mask = np.array([[1, 1, 1, 0, 1], [1, 1, 1, 1, 0]])
        >>> cardinalities = np.array([3, 2])
        >>> model.add_cardinality_constraints_matrix(constraint_mask, cardinalities)
        """
        constraint_mask_arr_like = self._array_like_factory.create_minimal(constraint_mask)
        cardinalities_arr_like = self._array_like_factory.create_numpy(cardinalities, data_type=np.int64)

        if len(self._variables) == 0:
            raise MissingVariableError("Cannot set constraints before adding a variable to the model.")

        if constraint_mask_arr_like.ndim() == 1:
            raise ValueError(
                "Cannot use add_cardinality_constraints_matrix() function with a vector, " \
                "please use add_cardinality_constraint() instead")

        if not cardinalities_arr_like.are_values_unsigned_integer():
            raise ValueError("Found cardinalities data types not unsigned intergers.")

        if not constraint_mask_arr_like.is_binary():
            raise ValueError("Cannot add a constraint if the values are not in binary.")

        if cardinalities_arr_like.shape()[0] != constraint_mask_arr_like.shape()[0]:
            raise ValueError(
                f"Cannot set constraints if cardinalities shape is not the same as the expected shape of this model." \
                f" Got cardinalities shape: {cardinalities_arr_like.shape()}, constraint mask shape: {constraint_mask_arr_like.shape()}.")

        equal_indices, less_indices = constraint_mask_arr_like.row_sums_under_cardinality(cardinalities_arr_like.inner())

        if len(equal_indices) > 0:
            log.warning(
                f" The sum of rows '{', '.join(map(str, equal_indices))}' in the binary array equals its corresponding cardinality."
            )

        if len(less_indices) > 0:
            raise ValueError(
                f"The sum of rows '{', '.join(map(str, less_indices))}' in the binary array is less than its corresponding cardinality."
            )

        cardinalities_arr_like.repeat_rows()

        self._constraints.add_constraint(
            num_variables=len(self._variables),
            constraint_weights=constraint_mask_arr_like,
            constraint_bounds=cardinalities_arr_like
        )


    def add_cardinality_constraint(
        self,
        constraint_mask: Union[np.ndarray, coo_array],
        cardinality: int
    ) -> None:
        """
        Adds cardinality constraint vector to the model.

        Parameters
        ----------
        constraint_mask
            A 1-D array (must be binary).
            The constraint_mask vector of shape (N,) where N is the number of variables.
        cardinality
            The constraint_rhs cardinality.
            This value has to be a non-zero unsigned integer.

        Raises
        ------
        MissingVariableError
            If no variable have been added to the model.
        ConstraintSizeError
            If the constraint_mask shape or the constraint_rhs shape does not fit
            the expected shape of this model.
        ValueError
            If the constraint_mask is not in binary or the cardinality is not an unsigned integer.

        Examples
        --------
        >>> constraint_mask = np.array([1, 1, 1, 0, 1])
        >>> cardinality = 3
        >>> model.add_cardinality_constraint(constraint_mask, cardinality)
        """
        constraint_mask_arr_like = self._array_like_factory.create_minimal(constraint_mask)

        if constraint_mask_arr_like.ndim() > 1:
            raise ValueError(
                "Cannot use add_cardinality_constraint() function with a matrix, " \
                "please use add_cardinality_constraints_matrix() instead")

        constraint_mask_arr_like.reshape_to_2d()

        self.add_cardinality_constraints_matrix(
            constraint_mask=constraint_mask_arr_like,
            cardinalities=np.full((1,), cardinality)
        )


    def add_equality_constraints_matrix(
        self,
        constraint_mask: Union[np.ndarray, coo_array, csr_array],
        limit: Union[np.ndarray, coo_array]
    ) -> None:
        """
        Adds an equality constraint matrix to the model.

        Parameters
        ----------
        constraint_mask
            A 2-D array (float32).
            The constraint_mask vector of shape (M, N) where M the number of constraints and N is the number of variables.
        limit
            A 1-D array (float32).
            The limit vector of shape (M,) where M is the number of constraints.

        Raises
        ------
        MissingVariableError
            If no variable have been added to the model.
        ValueError
            If the constraint_mask shape does not fit the expected shape of this model.
            If the constraint_mask or limit contains irregular format ('NaN' or 'inf').

        Examples
        --------
        >>> constraint_mask = np.array([[-3.51, 0, 0, 0], [10, 0, 0, 0]], dtype=np.float32)
        >>> limit = np.array([2, 10], dtype=np.float32)
        >>> model.add_equality_constraints_matrix(constraint_mask, limit)
        """
        constraint_mask_arr_like = self._array_like_factory.create_minimal(constraint_mask)
        limit_arr_like = self._array_like_factory.create_numpy(limit)

        if len(self._variables) == 0:
            raise MissingVariableError("Cannot set constraints before adding a variable to the model.")

        if constraint_mask_arr_like.data_type() != np.float32 or limit_arr_like.data_type() != np.float32:
            raise ValueError(
                f"Input parameters must be float32, got Constraint mask: {constraint_mask_arr_like.data_type()}, " \
                f"Limit: {limit.data_type()}"
            )

        if constraint_mask_arr_like.ndim() == 1:
            raise ValueError(
                "Cannot use add_equality_constraint_matrix() function with a vector, " \
                "please use add_equality_constraint() instead")

        if constraint_mask_arr_like.isnan() or constraint_mask_arr_like.isinf():
            raise ValueError("Constraint mask contains NaN or inf values")

        if limit_arr_like.isnan() or limit_arr_like.isinf():
            raise ValueError("Limit contains NaN or inf values")

        # convert to the constraint bounds format
        limit_arr_like.repeat_rows()

        self._constraints.add_constraint(
            num_variables=len(self._variables),
            constraint_weights=constraint_mask_arr_like,
            constraint_bounds=limit_arr_like
        )


    def add_equality_constraint(
        self,
        constraint_mask: Union[np.ndarray, coo_array],
        limit: np.float32
    ) -> None:
        """
        Adds an equality constraint vector to the model.

        Parameters
        ----------
        constraint_mask
            A 1-D array (float32).
            The constraint_mask vector of shape (N,) where N is the number of variables.
        limit
            Limit value to the constraint mask.

        Raises
        ------
        MissingVariableError
            If no variable have been added to the model.
        ValueError
            If the constraint_mask shape does not fit the expected shape of this model.
            If the constraint_mask or limit contains irregular format ('NaN' or 'inf').

        Examples
        --------
        >>> constraint_mask = np.array([1.05, -1.1], dtype=np.float32)
        >>> limit = -3.45
        >>> model.add_equality_constraint(constraint_mask, limit)
        """
        constraint_mask_arr_like = self._array_like_factory.create_minimal(constraint_mask)

        if constraint_mask_arr_like.ndim() > 1:
            raise ValueError(
                "Cannot use add_equality_constraint() function with a matrix, " \
                "please use add_equality_constraint_matrix() instead")

        # for equality constraints matrix, each limit is the equality bounds for each constraint
        limit_repeated = np.full((1,), limit, dtype=np.float32)
        constraint_mask_arr_like.reshape_to_2d()

        self.add_equality_constraints_matrix(
            constraint_mask=constraint_mask_arr_like,
            limit=limit_repeated
        )


    def add_inequality_constraints_matrix(
        self,
        constraint_mask: Union[np.ndarray, coo_array, csr_array],
        constraint_bounds: Union[np.ndarray, coo_array, csr_array]
    ) -> None:
        """
        Adds inequality constraint matrix to the model.

        Parameters
        ----------
        constraint_mask
            A 2-D array (float32).
            The constraint_mask vector of shape (M, N) where N is the number of variables.
        constraint_bounds
            A 2-D array (float32).
            Vector of shape (M, 2) where M is the number of constraints.

        Raises
        ------
        MissingVariableError
            If no variable have been added to the model.
        ValueError
            If the constraint_mask shape does not fit the expected shape of this model.
            If the constraint_mask contains irregular format ('NaN' or 'inf').
            If the lowerbound is equal or higher than its given upperbound.

        Examples
        --------
        >>> constraint_mask = np.array([[-3.51, 0], [10, 0]], dtype=np.float32)
        >>> constraint_bounds = np.array([[8, 9], [np.nan, 100_000]], dtype=np.float32)
        >>> model.add_inequality_constraints_matrix(constraint_mask, constraint_bounds)
        """
        constraint_mask_arr_like = self._array_like_factory.create_minimal(constraint_mask)
        constraint_bounds_arr_like = self._array_like_factory.create_numpy(constraint_bounds)

        if len(self._variables) == 0:
            raise MissingVariableError("Cannot set constraints before adding a variable to the model.")

        if constraint_mask_arr_like.data_type() != np.float32 or constraint_bounds_arr_like.data_type() != np.float32:
            raise ValueError(
                f"Input parameters must be float32, got Constraint mask: {constraint_mask_arr_like.data_type()}, " \
                f"Limit: {constraint_bounds_arr_like.data_type()}")

        if constraint_mask_arr_like.ndim() == 1:
            raise ValueError(
                "Cannot use add_inequality_constraint_matrix() function with a vector, " \
                "please use add_inequality_constraint() instead")

        if constraint_mask_arr_like.isnan() or constraint_mask_arr_like.isinf():
            raise ValueError("Constraint mask contains NaN or inf values.")

        if not constraint_bounds_arr_like.is_first_col_lower_second_col():
            raise ValueError("Constraint bounds contains lowerbounds equal or larger than their upperbound.")

        self._constraints.add_constraint(
            num_variables=len(self._variables),
            constraint_weights=constraint_mask_arr_like,
            constraint_bounds=constraint_bounds_arr_like
        )


    def add_inequality_constraint(
        self,
        constraint_mask: Union[np.ndarray, coo_array],
        constraint_bounds: Union[np.ndarray, coo_array]
    ) -> None:
        """
        Adds inequality constraint vector to the model. At least one bound must be set.

        Parameters
        ----------
        constraint_mask
            A 1-D array (float32).
            The constraint_mask vector of shape (N,) where N is the number of variables.
        constraint_bounds
            A 1-D array (float32).
            Vector of shape (2,)

        Raises
        ------
        MissingVariableError
            If no variable have been added to the model.
        ValueError
            If the constraint_mask shape does not fit the expected shape of this model.
            If the constraint_mask contains irregular format ('NaN' or 'inf').
            If the lowerbound is equal or higher than the upperbound.

        Examples
        --------
        >>> constraint_mask = np.array([1.05, -1.1], dtype=np.float32)
        >>> constraint_bounds = np.array([1.0, np.nan], dtype=np.float32)
        >>> model.add_inequality_constraint(constraint_mask, constraint_bounds)
        """
        constraint_mask_arr_like = self._array_like_factory.create_minimal(constraint_mask)
        constraint_bounds_arr_like = self._array_like_factory.create_numpy(constraint_bounds)

        if constraint_mask_arr_like.ndim() > 1:
            raise ValueError(
                "Cannot use add_inequality_constraint() function with a matrix, " \
                "please use add_inequality_constraint_matrix() instead")

        constraint_mask_arr_like.reshape_to_2d()
        constraint_bounds_arr_like.reshape_to_2d()

        self.add_inequality_constraints_matrix(
            constraint_mask=constraint_mask_arr_like,
            constraint_bounds=constraint_bounds_arr_like)


    def add_quadratic_equality_constraint(
        self,
        constraint_mask: Union[np.ndarray, coo_array, csr_array],
        limit: np.float32,
        constraint_linear_weights: Optional[Union[np.ndarray, coo_array]] = None
    ) -> None:
        """
        Adds an equality quadratic constraint to the model.

        Parameters
        ----------
        constraint_mask
            A 2-D array (float32).
            The constraint_mask vector of shape (N, N) where N is the number of variables.
        limit
            Limit value to the constraint mask.
        constraint_linear_weights
            A 1-D array (float32).
            The constraint_linear_weights vector of shape (N,) where N is the number of variables.

        Raises
        ------
        MissingVariableError
            If no variable have been added to the model.
        ValueError
            If the constraint_mask shape does not fit the expected shape of this model.
            If the constraint_mask or limit contains irregular format ('NaN' or 'inf').

        Examples
        --------
        >>> constraint_mask = np.array([[0.1, 0.1], [0.1, 0.1]], dtype=np.float32)
        >>> limit = 1.0
        >>> constraint_linear_weights = np.array([0, 0.2], dtype=np.float32)
        >>> model.add_quadratic_equality_constraint(constraint_mask, limit, constraint_linear_weights)
        """
        self.add_quadratic_inequality_constraint(
            constraint_mask=constraint_mask,
            constraint_bounds=np.full((2,), limit, dtype=np.float32),
            constraint_linear_weights=constraint_linear_weights
        )


    def add_quadratic_inequality_constraint(
        self,
        constraint_mask: Union[np.ndarray, coo_array, csr_array],
        constraint_bounds: Union[np.ndarray, coo_array],
        constraint_linear_weights: Optional[Union[np.ndarray, coo_array]] = None
    ) -> None:
        """
        Adds an inequality quadratic constraint to the model.

        Parameters
        ----------
        constraint_mask
            A 2-D array (float32).
            The constraint_mask vector of shape (N, N) where N is the number of variables.
        constraint_bounds
            A 1-D array (float32).
            Vector of shape (2,).
        constraint_linear_weights
            A 1-D array (float32).
            The constraint_linear_weights vector of shape (N,) where N is the number of variables.

        Raises
        ------
        MissingVariableError
            If no variable have been added to the model.
        ValueError
            If the constraint_mask shape does not fit the expected shape of this model.
            If the constraint_mask or limit contains irregular format ('NaN' or 'inf').
            If the constraint_bounds' shape is not (2,).

        Examples
        --------
        >>> constraint_mask = np.array([[1.05, -1.1], [0, 0]], dtype=np.float32)
        >>> constraint_bounds = np.array([np.nan, 10], dtype=np.float32)
        >>> constraint_linear_weights = np.array([4.0, 4.0], dtype=np.float32)
        >>> model.add_quadratic_inequality_constraint(constraint_mask, constraint_bounds, constraint_linear_weights)
        """
        constraint_mask_arr_like = self._array_like_factory.create_minimal(constraint_mask)
        constraint_bounds_arr_like = self._array_like_factory.create_numpy(constraint_bounds)

        if len(self._variables) == 0:
            raise MissingVariableError("Cannot set constraints before adding a variable to the model.")

        EXPECTED_BOUNDS_SHAPE = (2,)
        if constraint_bounds_arr_like.shape() != EXPECTED_BOUNDS_SHAPE:
            raise ValueError(
                "Invalid constraint_bounds shape: "
                + f"expected {EXPECTED_BOUNDS_SHAPE}, got {constraint_bounds_arr_like.shape()}")

        if constraint_bounds_arr_like.inner()[0] > constraint_bounds_arr_like.inner()[1]:
            raise ValueError("Input constraint_bounds lowerbound is higher than its upperbound.")

        if constraint_mask_arr_like.data_type() != np.float32:
            raise ValueError(f"Input parameters must be float32, got constraint_mask: {constraint_mask_arr_like.data_type()}")

        if constraint_mask_arr_like.isnan() or constraint_mask_arr_like.isinf():
            raise ValueError("Input parameter constraint_mask contains NaN or inf values")

        constraint_linear_weights_arr_like = None
        if constraint_linear_weights is not None:
            constraint_linear_weights_arr_like = self._array_like_factory.create_minimal(constraint_linear_weights)

            if constraint_linear_weights_arr_like.data_type() != np.float32:
                raise ValueError(f"Input parameters must be float32, got Constraint linear weights: {constraint_linear_weights.data_type()}")

            if constraint_linear_weights_arr_like.isnan() or constraint_linear_weights_arr_like.isinf():
                raise ValueError("Input parameter constraint_linear_weights contains NaN or inf values")

            constraint_linear_weights_arr_like.reshape_to_2d()

        constraint_bounds_arr_like.reshape_to_2d()

        self._quad_constraints.add_constraint(
            num_variables=len(self._variables),
            quad_constraint_weights=constraint_mask_arr_like,
            quad_constraint_bounds=constraint_bounds_arr_like,
            quad_constraint_linear_weights=constraint_linear_weights_arr_like
        )


    def optimize(
        self,
        *,
        beta: List[float] = [1, 0.5, 0.33, 0.25, 0.2, 0.16, 0.14, 0.125],
        coupling_mult: float = 0.5,
        timeout_in_secs: float = 10.0,
        num_chains: int = 8,
        num_engines: int = 1,
        penalty_scaling: float = None,
        precision: Precision = Precision.AUTO,
        num_buckets: int = 10,
        optimality_gap: float = 1e-4,
        presolve_ratio: float = 0.1
    ) -> OptimizeResponse:
        """
        Optimize this model. Issue a solve request and wait for it to complete.

        Notes
        -----
        All of the files used during this computation will be cleaned at the end.
        For more information on how to tune those parameters, visit

        `The tuning guide <https://docs.titanq.infinityq.io/user-guide/parameter_tuning_guide>`_

        `TitanQ API documentation <https://docs.titanq.infinityq.io/>`_

        Parameters
        ----------
        beta
            Scales the problem by this factor (inverse of temperature). Beta values can then be
            adjusted to see if a better objective function value can be obtained.
            A lower beta allows for easier escape from local minima, while a higher beta
            is more likely to respect penalties and constraints.

            `Beta values tuning guide <https://docs.titanq.infinityq.io/user-guide/parameter_tuning_guide#beta>`_

            Range: List of [0, 20000]

            Recommended values: List of [0.004...2]

            NOTE: Beta values should be provided in descending order

            >>> import numpy as np
            >>> num_chains = 8
            >>> beta = (1/(np.linspace(2, 50, num_chains, dtype=np.float32))).tolist()

        coupling_mult
            Strength of parameter that keeps multiple logical copies of variables to have the
            same ground state solution. Heuristic to be tuned for a particular problem. Small values
            of this parameter will lead to an incorrect solution while large values will take a long
            time to converge to the correct solution.

            `coupling_mult tuning guide <https://docs.titanq.infinityq.io/user-guide/parameter_tuning_guide#coupling_mult>`_

            Range: [0, 100]

            Recommended values: [0.05...1.0]

        timeout_in_secs
            Maximum time (in second) the computation can take.

            `timeout_in_secs tuning guide <https://docs.titanq.infinityq.io/user-guide/parameter_tuning_guide#timeout_in_secs>`_

            Range: [0.1, 600]

            NOTE: Currently there is no other stop criteria. All computations will run up to the
            timeout value.

        num_chains
            Number of parallel chains running computation. Only the best result of all
            chains is returned.

            `num_chains tuning guide <https://docs.titanq.infinityq.io/user-guide/parameter_tuning_guide#num_chains--num_engines>`_

            Recommended values: [8, 16, 32]

            NOTE: ``num_chains`` * ``num_engines`` cannot exceed 512

        num_engines
            Number of independent batches of chains to run the computation. The best result
            of the batch of chains in each engine is returned.

            `num_engines tuning guide <https://docs.titanq.infinityq.io/user-guide/parameter_tuning_guide#num_chains--num_engines>`_

            Range: [1, 512]

            NOTE: ``num_chains`` * ``num_engines`` cannot exceed 512

        penalty_scaling
            Scaling factor for constraint penalty violations. Increasing this value results
            in stronger constraint enforcement at the cost of increasing the odds of becoming
            trapped in local minima.

            Range: penalty_scaling > 0

            NOTE: If None, a value will be inferred from the objective function of the problem.

        precision
            Some problems may need a higher precision implementation to converge properly such
            as when problem weights exhibit a high dynamic range. This flag allows this higher
            precision (but slightly slower speed) implementation to be used when ``Precision.HIGH``
            is set. Setting ``Precision.STANDARD`` uses a medium precision perfect for general use
            and offering the best speed/efficiency. The default setting ``Precision.AUTO`` will
            inspect the problem passed in and determine which of ``Precision.AUTO`` or
            ``Precision.STANDARD`` precision to use based on internal metrics.

        num_buckets
            The buckets strategy consists in dividing the range of values of a continuous variable
            into the specified number of buckets.

            `num_buckets tuning guide <https://docs.titanq.infinityq.io/user-guide/parameter_tuning_guide#num_buckets>`_

            Range: num_buckets >= 0

            Recommended values: [1, 2, 3, ..., 9, 10, 20, 30, ..., 90, 100, 200, 300, ..., 900, 1000, ...]

            NOTE: If the value is set to '0', the solver will not use the buckets strategy.

        optimality_gap
            The optimality_gap parameter sets the required accuracy for a solver to consider a solution acceptable,
            the scaled error, dual feasibility, and constraint violation. If the solution meets these conditions,
            the solver terminates. The parameter is typically small but can be adjusted based on the problem's needs.

            `optimality_gap tuning guide <https://docs.titanq.infinityq.io/user-guide/parameter_tuning_guide#optimality_gap>`_

            Recommended range: [0.1, 1e-10]
            NOTE: The LP/QP solver is designed to explore the solution space defined by the provided model until it
            finds a solution that is better than the specified gap, as it's not always feasible to terminate with the
            exact gap requirement.

        presolve_ratio
            The presolve_ratio parameter determines the proportion of the solver's allocated runtime dedicated to the presolve phase before
            the main optimization phase begins. It is expressed as a decimal from 0 to 1, representing the fraction of the total solver time.
            For example, if presolve_ratio = 0.1, then 10% of the solver's total time is allocated to presolving, leaving 90% for the main solver.
            The default value for presolve_ratio is 0.1.

            The presolve phase is an initial computational step designed to generate a starting solution for the main solver. Since presolve
            relies on heuristic techniques, it does not guarantee a good quality starting solution. Depending on the problem structure, it may
            significantly improve performance or, in some cases, introduce additional overhead without a meaningful benefit.

            `presolve_ratio tuning guide <https://docs.titanq.infinityq.io/user-guide/parameter_tuning_guide#presolve_ratio>`_


        Returns
        -------
        OptimizeResponse
            Optimized response data object

        Raises
        ------
        MissingVariableError
            If no variable have been added to the model.
        MissingObjectiveError
            If no objective matrices have been added to the model.
        FailedComputationError
            If an error was returned by the solver instead of a result.
            The exception will contain the solver's error message.

        Examples
        --------
        basic solve
            >>> response = model.optimize(timeout_in_secs=60)
        multiple engine
            >>> response = model.optimize(timeout_in_secs=60, num_engines=2)
        custom values
            >>> response = model.optimize(beta=[0.1], coupling_mult=0.75, num_chains=8)
        print values
            >>> print("-" * 15, "+", "-" * 26, sep="")
            >>> print("Ising energy   | Result vector")
            >>> print("-" * 15, "+", "-" * 26, sep="")
            >>> for ising_energy, result_vector in response.result_items():
            >>>     print(f"{ising_energy: <14f} | {result_vector}")
        """
        if len(self._variables) == 0:
            raise errors.MissingVariableError("Cannot optimize before adding a variable to the model.")

        if self._objective is None:
            raise errors.MissingObjectiveError("Cannot optimize before adding an objective to the model.")

        # initialize the storage clients
        self._storage_client.init()

        result, metrics = self._solve(beta, coupling_mult, timeout_in_secs, num_chains, num_engines, penalty_scaling, precision, num_buckets, optimality_gap, presolve_ratio)
        return OptimizeResponse(self._variables, result, metrics)

    def _solve(
        self,
        beta: List[float],
        coupling_mult: float,
        timeout_in_secs: float,
        num_chains: int,
        num_engines: int,
        penalty_scaling: Optional[float],
        precision: Precision,
        num_buckets: int,
        optimality_gap: float,
        presolve_ratio: float
    ) -> Tuple[np.ndarray, Dict[str, Any]]:
        """
        Issue a solve request and wait for it to complete.

        Returns
        -------
        The result numpy array and the metric json object.
        """
        with self._event_scope(is_optimization=True) as event_emitter:
            # Preparing data for upload, it concatenate every ArrayLike into
            # the right format and also tag the constraints (needed for the manifest)
            with event_emitter.emit_with_progress(PreparingDataEvent()):
                bias = self._objective.bias()
                weights =  self._objective.weights()
                variable_bounds = self._array_like_factory.create_numpy(np.array([v.variable_bounds() for v in self._variables]))

                constraint_weights = self._constraints.weights()
                constraint_bounds = self._constraints.bounds()

                quad_constraint_weights = self._quad_constraints.weights()
                quad_constraint_bounds = self._quad_constraints.bounds()
                quad_constraint_lin_weights = self._quad_constraints.linear_weights()

                if constraint_weights is not None and constraint_bounds is not None:
                    for mask, bounds in zip(constraint_weights.iter_nonzero_row_values(), constraint_bounds):
                        mask_numpy = self._array_like_factory.create_numpy(mask)
                        bounds_numpy = self._array_like_factory.create_numpy(bounds)
                        self._manifest_builder.add_constraint_type(get_constraint_type(mask_numpy, bounds_numpy))


                # Build request with input and output files
                input_files_reader: Dict[str, BytesReaderWithCallback] = {}
                request = Request(
                    input=self._storage_client.request_input_builder(
                        bias=_add_bytes_reader_and_return(input_files_reader, "bias", bias),
                        variable_bounds=_add_bytes_reader_and_return(input_files_reader, "variable_bounds", variable_bounds),
                        weights=_add_bytes_reader_and_return(input_files_reader, "weights", weights),
                        constraint_weights=_add_bytes_reader_and_return(input_files_reader, "constraint_weights", constraint_weights),
                        constraint_bounds=_add_bytes_reader_and_return(input_files_reader, "constraint_bounds", constraint_bounds),
                        quad_constraint_weights=_add_bytes_reader_and_return(input_files_reader, "quad_constraint_weights", quad_constraint_weights),
                        quad_constraint_bounds=_add_bytes_reader_and_return(input_files_reader, "quad_constraint_bounds", quad_constraint_bounds),
                        quad_constraint_linear_weights=_add_bytes_reader_and_return(input_files_reader, "quad_constraint_lin_weights", quad_constraint_lin_weights),
                        manifest=Manifest(
                            has_cardinality_constraint=self._manifest_builder.has_cardinality_constraint(),
                            has_set_partitioning_constraint=self._manifest_builder.has_set_partitioning_constraint(),
                            has_equality_constraint=self._manifest_builder.has_equality_constraint(),
                            has_inequality_constraint=self._manifest_builder.has_inequality_constraint()
                        ),
                    ),
                    output=self._storage_client.request_output_builder(),
                    parameters=Parameters(
                        timeout_in_secs=timeout_in_secs,
                        variable_types=''.join(v.vtype()._api_str() for v in self._variables),

                        beta=beta,
                        constant_term=self._objective.constant_term(),
                        coupling_mult=coupling_mult,
                        num_buckets=num_buckets,
                        num_chains=num_chains,
                        num_engines=num_engines,
                        optimality_gap=optimality_gap,
                        penalty_scaling=penalty_scaling,
                        precision=str(precision),
                        presolve_ratio=presolve_ratio,
                    )
                )

            # upload input files
            event_emitter.emit(UploadStartEvent())
            with event_emitter.emit_with_progress(UploadEvent(input_files_reader)):
                self._titanq_client.upload_input(request.input)

            # request to TitanQ API
            with event_emitter.emit_with_progress(SendingProblemEvent()):
                solve_response = self._titanq_client.solve_request(request)

            # retrieve computation ID
            computation_id = solve_response.body.api_response.computation_id
            with titanq_error_including_computation_id(computation_id):
                return self._handle_results(event_emitter, request, computation_id)

    def _handle_results(
        self,
        event_emitter: EventEmitter,
        request: Request,
        computation_id: str
    ) -> Tuple[np.ndarray, Dict[str, Any]]:
        """Handle getting back a result"""
        event_emitter.emit(GotComputationIDEvent(computation_id))

        waiting_event = WaitingForResultEvent()
        with event_emitter.emit_with_progress(waiting_event):
            try:
                self._titanq_client.wait_for_result(
                    computation_id=computation_id,
                    timeout_in_sec=None, # run indefinitely
                    on_update=lambda status_list: waiting_event.update_status_list(status_list)
                )
            except MissingFinishedStatusError:
                # computation has not finished, an error file should be uploaded instead
                event_emitter.emit(ComputationFailedEvent())
                error = self._download_failure_result(event_emitter, request)
                raise ComputationFailedError(error)

        result = self._download_success_result(event_emitter, request)

        event_emitter.emit(OptimizationCompletedEvent())
        return result.result, result.metrics.model_dump()

    def _download_failure_result(self, event_emitter: EventEmitter, request: Request) -> Response.Result.Error:
        """ downloads the failure results and raises it as a FailedComputationError. """
        result_bytes_reader = BytesReaderWithCallback()
        result_length = self._titanq_client.result_content_length(request)
        with event_emitter.emit_with_progress(DownloadResultEvent("error", result_length, result_bytes_reader)):
            try:
                return self._titanq_client.download_error(request, result_bytes_reader)
            except EmptyResultError:
                raise UnknownError()

    def _download_success_result(self, event_emitter: EventEmitter, request: Request) -> Response.Result:
        """ downloads the success results and returns it"""
        result_bytes_reader = BytesReaderWithCallback()
        result_length = self._titanq_client.result_content_length(request)
        with event_emitter.emit_with_progress(DownloadResultEvent("result", result_length, result_bytes_reader)):
            try:
                return self._titanq_client.download_result(request, result_bytes_reader)
            except EmptyResultError:
                raise UnknownError()


def _add_bytes_reader_and_return(
    input_dict: Dict[str, BytesReaderWithCallback],
    array_name: str,
    array: Optional[ArrayLike] = None,
) -> Optional[BytesReaderWithCallback]:  # noqa: F821
    if array is None:
        return None

    bytes_reader = BytesReaderWithCallback(array.to_bytes())
    input_dict[array_name] = bytes_reader
    return bytes_reader
