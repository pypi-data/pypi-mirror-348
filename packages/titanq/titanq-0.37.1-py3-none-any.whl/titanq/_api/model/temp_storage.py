# Copyright (c) 2025, InfinityQ Technology, Inc.

from pydantic import BaseModel, ConfigDict, Field


class DualUrl(BaseModel):
    """ Contains a download and an upload url """
    download: str
    upload: str


class _DualUrlIterable(BaseModel):
    """ Will create an iterator for a class composed with DualUrl's """
    def __iter__(self):
        return iter((getattr(self, f) for f in self.model_fields_set))


class TempStorageInput(_DualUrlIterable):
    weights: DualUrl = Field(alias="weights")
    bias: DualUrl = Field(alias="bias")
    variable_bounds: DualUrl = Field(alias="variable_bounds")
    constraint_weights: DualUrl = Field(alias="constraint_weights")
    constraint_bounds: DualUrl = Field(alias="constraint_bounds")
    quad_constraint_weights: DualUrl = Field(alias="quad_constraint_weights")
    quad_constraint_bounds: DualUrl = Field(alias="quad_constraint_bounds")
    quad_constraint_linear_weights: DualUrl = Field(alias="quad_constraint_linear_weights")

    # necessary for test cases
    model_config = ConfigDict(populate_by_name=True)


class TempStorageOutput(_DualUrlIterable):
    result: DualUrl = Field(alias="result")

    # necessary for test cases
    model_config = ConfigDict(populate_by_name=True)


class TempStorageResponse(BaseModel):
    input: TempStorageInput
    output: TempStorageOutput
