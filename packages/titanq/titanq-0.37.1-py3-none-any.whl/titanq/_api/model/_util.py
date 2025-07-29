# Copyright (c) 2025, InfinityQ Technology, Inc.

import copy
from typing import Any, Callable, Dict, Generic, Type, TypeVar, Union
from urllib.parse import ParseResult, urlparse

from numpy.typing import NDArray
from scipy.sparse import sparray
from pydantic import GetCoreSchemaHandler, PydanticSchemaGenerationError
from pydantic_core import core_schema
import wrapt


T = TypeVar('T')

class Obfuscated(Generic[T], wrapt.ObjectProxy):
    """
    Obfuscate is a class made to be use as base class to make the child class
    obfuscated when stringified but still serialized normally by pydantic dump functions
    """
    def __init_subclass__(cls, obfuscation: Union[str, Callable[[T], str]] = "<hidden>"):
        # Get parameter passed in [].
        # the first one is the base type that will be obfuscated on print
        base = next(base.__args__[0] for base in cls.__orig_bases__ if hasattr(base, "__args__"))

        # define both __str__ and __repr__ so the data is obfuscated
        if isinstance(obfuscation, Callable):
            def obfuscation_func(self):
                return obfuscation(self.__wrapped__)
        else:
            def obfuscation_func(_):
                return obfuscation

        setattr(cls, "__str__", obfuscation_func)
        setattr(cls, "__repr__", obfuscation_func)

        # This is related to pydantic
        # It make sure the value get cast into an Obfuscated version after it has been initialized.
        # This mean a user can pass an instance of the base class (e.g. str instead of SecretStr)
        # It also make sure the full value is dump by pydantic.
        @classmethod
        def __get_pydantic_core_schema__(cls, source: Type[Any], handler: GetCoreSchemaHandler) -> core_schema.CoreSchema:
            try:
                schema = handler(base)
            except PydanticSchemaGenerationError:
                schema = handler.generate_schema(base)
            return core_schema.no_info_after_validator_function(
                cls,
                schema,
                serialization=core_schema.plain_serializer_function_ser_schema(Obfuscated.non_obfuscated_value)
            )

        setattr(cls, "__get_pydantic_core_schema__", __get_pydantic_core_schema__)


    def non_obfuscated_value(self):
        return self.__wrapped__

    def __deepcopy__(self, memo):
        return type(self)(copy.deepcopy(self.__wrapped__, memo))


def _truncate_if_longer_than(threshold: int, suffix: str = ""):
    def truncate(value: str):
        if not value:
            return ''

        if len(value) <= threshold:
            return value
        return value[:threshold - len(suffix)] + suffix

    return truncate


def _truncate_url(url):
    parsed:ParseResult = urlparse(url)
    host = parsed.hostname

    truncated = f"{parsed.scheme}://{host}{parsed.path}"

    return truncated if str(url) == truncated else truncated + "..."


class StrTruncatedOnDisplay(Obfuscated[str], obfuscation=_truncate_if_longer_than(25, suffix="...")):...
class UrlTruncatedOnDisplay(Obfuscated[str], obfuscation=_truncate_url): ...
class ArrayLikeTruncatedOnDisplay(Obfuscated[Union[NDArray, sparray]], obfuscation=lambda a: f"<ArrayLike | shape={a.shape}>"): ...

class SecretJson(Obfuscated[Dict[str, Any]], obfuscation=lambda _: "<secret>"):...
class SecretStr(Obfuscated[str], obfuscation=lambda _: "<secret>"):...