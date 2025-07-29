# Copyright (c) 2025, InfinityQ Technology, Inc.

from dataclasses import dataclass
from typing import Any, Dict, List, Optional
import uuid

from numpy.typing import NDArray
from pydantic import BaseModel, ConfigDict, Field, SerializeAsAny, SerializerFunctionWrapHandler, model_serializer

from titanq._api.model._util import StrTruncatedOnDisplay
from titanq._api.model.local_file import InputFiles, LocalFile
from titanq._api.model.location import Location


class Parameters(BaseModel):
    model_config = ConfigDict(validate_assignment=True)

    variable_types: StrTruncatedOnDisplay
    timeout_in_secs: float
    beta: Optional[List[float]] = None
    coupling_mult: Optional[float] = None
    num_chains: Optional[int] = None
    num_buckets: Optional[int] = None
    num_engines: Optional[int] = None
    penalty_scaling: Optional[float] = None
    precision: Optional[str] = None
    constant_term: Optional[float] = None
    optimality_gap: Optional[float] = None
    presolve_ratio: Optional[float] = None

class Manifest(BaseModel):
    has_cardinality_constraint: bool
    has_set_partitioning_constraint: bool
    has_equality_constraint: bool
    has_inequality_constraint: bool


class Request(BaseModel):
    class Input(BaseModel):
        location: SerializeAsAny[Location]
        files: InputFiles
        manifest: Manifest

        @model_serializer(mode='wrap')
        def inplace_serialization(self, nxt: SerializerFunctionWrapHandler) -> Dict[str, Any]:
            """
            Change the serialization method so the top level key are not added

            e.g. {"top_key": {key_data}} -> {key_data}
            """
            dump: Dict[str, Any] = nxt(self)
            return {
                **dump.pop('location'),
                **dump.pop('files'),
                **dump
            }

        def upload_missing_local_data(self):
            # using model_dump() here (pydantic recommandation) is not possible since we
            # exclude the 'data' field. This is another approach in order to obtain all fields
            for field in self.files.__annotations__:
                value = getattr(self.files, field)
                if isinstance(value, LocalFile):
                    self.location.upload(value.remote_name, value.data)

                    # change value of LocalFile to simply a str since the data have been uploaded
                    # this make sure calling this method again will not upload the data twice
                    setattr(self.files, field, value.remote_name)


    class Output(BaseModel):
        location: SerializeAsAny[Location]
        result_archive_file_name: StrTruncatedOnDisplay

        @model_serializer(mode='wrap')
        def inplace_serialization(self, nxt: SerializerFunctionWrapHandler) -> Dict[str, Any]:
            dump: Dict[str, Any] = nxt(self)
            return {
                **dump.pop('location'),
                **dump,
            }


    input: Input
    output: Output
    parameters: Parameters


@dataclass
class Response:
    class ApiResponse(BaseModel):
        computation_id: uuid.UUID
        status: str
        message: str

    @dataclass
    class Result:
        class Metrics(BaseModel):
            computation_id: str
            solver_used: str
            computation_metrics: Dict[str, Any]
            parameters_used: Parameters
            problem_shape: Dict[str, Optional[List[int]]]


        class Error(BaseModel):
            error: str


        result:  Optional[NDArray] = None
        metrics: Optional[Metrics] = None
        error:   Optional[Error]   = None

    api_response: ApiResponse
    result: Optional[Result] = Field(None, exclude=True)
