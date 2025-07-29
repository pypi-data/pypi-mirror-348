# Copyright (c) 2024, InfinityQ Technology, Inc.

####################################
# Errors specific to the TitanQ SDK.
####################################

from contextlib import contextmanager
from typing import Optional


class TitanqError(Exception):
    """
    Base TitanQ error, optionally can be instantiated with a computation id
    """

    def __init__(self, message: str = "", computation_id: Optional[str] = None):
        self.original_message = message
        self.computation_id = computation_id
        super().__init__(self._compose_message())

    def with_computation_id(self, computation_id: str) -> 'TitanqError':
        return type(self)(self.original_message, computation_id=computation_id)

    def _compose_message(self):
        if self.computation_id:
            return f"computation ID: {self.computation_id}: {self.original_message}"
        return self.original_message

    def __str__(self):
        return self._compose_message()


@contextmanager
def titanq_error_including_computation_id(id: str):
    """Computation manager that will include a 'TitanqError' with a computation id"""
    try:
        yield
    except TitanqError as e:
        raise e.with_computation_id(id) from e


#######################
# SERVER RELATED ERRORS
#######################
class ClientError(TitanqError):
    """Base client-side http error"""

class NotEnoughCreditsError(ClientError):
    """Not enough credits left"""

    def __init__(self, message="Not enough credits left", *args, **kwargs):
        super().__init__(message, *args, **kwargs)

class BadRequest(ClientError):
    """The request sent to TitanQ is not valid"""

class UnexpectedServerResponseError(TitanqError):
    """Response from the TitanQ server is not as expected"""

class MissingFinishedStatusError(TitanqError):
    """The computation does not include a finished status"""

class ConnectionError(TitanqError):
    """Error due to a connection issue with an external resource"""

class ServerError(TitanqError):
    """Unexpected condition prevented the TitanQ server to fulfill the request"""

class EmptyResultError(TitanqError):
    """Results were downloaded but they are empty"""

class UnsolvableRequestError(TitanqError):
    """TitanQ cannot solve this combination of parameters"""

    def __init__(self, message="TitanQ cannot solve this combination of parameters", *args, **kwargs):
        super().__init__(message, *args, **kwargs)

class ComputationFailedError(TitanqError):
    """The computation failed"""

class UnknownError(TitanqError):
    """An error happened in TitanQ, but the SDK is unable to know what is the source of the problem."""
    def __init__(self, message="TitanQ has experienced an unknown error, please contact (support@infinityq.tech).", *args, **kwargs):
        super().__init__(message, *args, **kwargs)


######################
# MODEL RELATED ERRORS
######################
class MissingTitanqApiKey(TitanqError):
    """TitanQ Api key is missing"""

class MissingVariableError(TitanqError):
    """Variable has not already been registered"""

class VariableAlreadyExist(TitanqError):
    """Variable with the same name already exist"""

class MissingObjectiveError(TitanqError):
    """Objective has not already been registered"""

class ConstraintSizeError(TitanqError):
    """Unexpected number of constraints"""

class ConstraintAlreadySetError(TitanqError):
    """A constraint has already been set"""

class ObjectiveAlreadySetError(TitanqError):
    """An objective has already been set"""

class TautologicalExpressionError(TitanqError):
    """
    Exception raised when an expression is tautological (always true).

    This exception indicates that the provided expression is redundant
    and does not add meaningful constraints or information.
    """
    def __init__(self, message="The provided expression is tautological and always evaluates to True, regardless of the variable values.", *args, **kwargs):
        super().__init__(message, *args, **kwargs)

class ContradictoryExpressionError(TitanqError):
    """
    Exception raised when an expression is contradictory (always false).

    This exception indicates that the provided expression is invalid
    as it represents an impossible condition.
    """
    def __init__(self, message="The provided expression is contradictory and always evaluates to False, regardless of the variable values.", *args, **kwargs):
        super().__init__(message, *args, **kwargs)


####################
# MPS RELATED ERRORS
####################
class MpsParsingError(TitanqError):
    """Base class for any error related to the MPS files parsing module"""

class MpsConfiguredModelError(MpsParsingError):
    """Passed model is already configured"""

class MpsMissingValueError(MpsParsingError):
    """A required value is missing"""

class MpsMissingSectionError(MpsParsingError):
    """A required section is missing"""

class MpsMalformedFileError(MpsParsingError):
    """The file is malformed"""

class MpsUnexpectedValueError(MpsParsingError):
    """Found an unexpected value"""

class MpsUnsupportedError(MpsParsingError):
    """Found an unsupported value"""
