# Copyright (c) 2025, InfinityQ Technology, Inc.

import abc
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, Mapping, Optional, Tuple
from urllib.parse import urljoin

from pydantic import BaseModel, ValidationError
import requests

from titanq import errors
from titanq._api.model.problem import Problem


_AUTHORIZATION_HEADER = "Authorization"
_TRACE_ID_HEADER = 'X-Correlation-Id'
_USER_AGENT_HEADER = 'User-Agent'


@dataclass
class HttpRequest:
    method: str
    url: str
    headers: Dict[str, str] = field(default_factory=dict)
    body: Optional[BaseModel] = None
    query_param: Optional[BaseModel] = None


@dataclass
class HttpMetadata:
    status_code: int
    headers: Mapping[str, str]


class HttpClient(abc.ABC):
    @abc.abstractmethod
    def do(self, http_request: HttpRequest) -> Tuple[bytes, HttpMetadata]: ...


class HTTPMethod(str, Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    PATCH = "PATCH"
    HEAD = "HEAD"
    OPTIONS = "OPTIONS"


class BasicHttpClient(HttpClient):

    def __init__(self, base_server_address: str) -> None:
        self._base_server_address = base_server_address

    def do(self, http_request: HttpRequest) -> Tuple[bytes, HttpMetadata]:
        response = requests.request(
            method=http_request.method,
            headers=http_request.headers,
            url=urljoin(self._base_server_address, http_request.url),
            json=http_request.body.model_dump(exclude_unset=True) if http_request.body else None,
            params=http_request.query_param.model_dump(exclude_unset=True) if http_request.query_param else None,
        )

        # check if the result is a problem
        try:
            Problem.model_validate_json(response.content).raise_()
        except ValidationError:
            pass

        # if not a problem
        try:
            return response.content, HttpMetadata(
                status_code=response.status_code,
                headers=response.headers
            )
        except ValidationError:
            raise errors.UnexpectedServerResponseError(
                 f"Failed to parse the response from the TitanQ server. The raw response is: {response.content}"
            )


class HttpClientWithDefaultHeader(HttpClient):
    """HttpClient decorator that add an header on each request"""
    def __init__(self, client: HttpClient, key: str, value: str) -> None:
        self._key = key
        self._value = value
        self._client = client


    def do(self, http_request: HttpRequest) -> Tuple[bytes, HttpMetadata]:
        http_request.headers[self._key] = self._value
        return self._client.do(http_request)


class HttpClientWithAuthorization(HttpClientWithDefaultHeader):
    def __init__(self, client: HttpClient, api_key: str) -> None:
        super().__init__(client, _AUTHORIZATION_HEADER, api_key)


class HttpClientWithSession(HttpClientWithDefaultHeader):
    def __init__(self, client: HttpClient, trace_id: str) -> None:
        super().__init__(client, _TRACE_ID_HEADER, trace_id)


class HttpClientWithUserAgent(HttpClientWithDefaultHeader):
    def __init__(self, client: HttpClient, product_name: str, product_version: str) -> None:
        super().__init__(
            client,
            _USER_AGENT_HEADER,
            HttpClientWithUserAgent._user_agent_str(product_name, product_version)
        )

    @classmethod
    def _user_agent_str(_cls, product_name: str, product_version: str):
        request_user_agent = requests.utils.default_headers().get(_USER_AGENT_HEADER, '')
        user_agent = f"{product_name}/{product_version} " + request_user_agent
        return user_agent.rstrip()