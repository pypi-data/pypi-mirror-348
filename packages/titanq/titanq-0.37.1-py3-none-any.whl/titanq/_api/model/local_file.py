# Copyright (c) 2025, InfinityQ Technology, Inc.

from io import BytesIO
from typing import Annotated, Optional, Union

from pydantic import AfterValidator, BaseModel, ConfigDict, Field, SerializeAsAny, field_serializer, model_serializer

from titanq._api.model._util import UrlTruncatedOnDisplay


# FileName is either a Str or an URL.
# It Has a validation that will cast it into an URL if needed
# Meaning a simple string can alway be use when setting it
FileName = Annotated[
    Union[str, UrlTruncatedOnDisplay],
    AfterValidator(lambda s: UrlTruncatedOnDisplay(s) if s.startswith("http") else s),
]
InputFile = SerializeAsAny[Union[FileName, 'LocalFile']]


class LocalFile(BaseModel):
    """ A local file for numpy arrays """
    remote_name: FileName
    data: BytesIO = Field(exclude=True)

    model_config = ConfigDict(arbitrary_types_allowed=True)

    @model_serializer
    def serialize_model_as_str(self) -> str:
        if isinstance(self.remote_name, UrlTruncatedOnDisplay):
            return self.remote_name.non_obfuscated_value()
        return self.remote_name


class InputFiles(BaseModel):
    """ Input files for any location type """
    bias_file_name: InputFile
    variable_bounds_file_name: InputFile
    weights_file_name: Optional[InputFile] = None
    constraint_weights_file_name: Optional[InputFile] = None
    constraint_bounds_file_name: Optional[InputFile] = None
    quad_constraint_weights_file_name: Optional[InputFile] = None
    quad_constraint_bounds_file_name: Optional[InputFile] = None
    quad_constraint_linear_weights_file_name: Optional[InputFile] = None

    # We need to explicit the serialization because how Union[] work with pydantic
    @field_serializer("*")
    def serialize_input_file(self, value):
        if isinstance(value, UrlTruncatedOnDisplay):
            return value.non_obfuscated_value()
        return value