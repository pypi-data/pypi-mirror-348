# Copyright (c) 2025, InfinityQ Technology, Inc.

from contextlib import contextmanager
from dataclasses import dataclass
from io import BytesIO
import time
from typing import Any, Callable, Generator, Generic, List, Optional, Tuple, TypeVar
import uuid
from zipfile import ZipFile

import numpy as np
from numpy.typing import NDArray

from titanq._api.http_client import (
    BasicHttpClient,
    HTTPMethod,
    HttpClient,
    HttpClientWithAuthorization,
    HttpClientWithSession,
    HttpClientWithUserAgent,
    HttpRequest,
    HttpMetadata
)
from titanq._api.model.credits import GetCreditsResponse
from titanq._api.model.history import ComputationHistoryRequest, ComputationHistoryResponse, Status
from titanq._api.model import solve
from titanq._api.model.temp_storage import TempStorageResponse
from titanq._util.timeout import get_dynamic_wait_interval
from titanq.errors import EmptyResultError, MissingFinishedStatusError, ServerError


_API_VERSION = "v1"

_SOLVE_PATH = "solve"
_COMUTATIONS_HISTORY_PATH = "computations"
_TEMP_STORAGE_PATH = "temp_storage"
_CREDITS_PATH = "credits"

DONE_STATUS = 'done'
FINISHED_STATUS = 'finished'

T = TypeVar('T')


@dataclass
class Response(Generic[T]):
    http_metadata: HttpMetadata
    body: T


class Client:
    def __init__(
        self,
        base_server_address: str,
        api_key: str,
        name: str,
        version: str,
    ) -> None:
        self._api_key = api_key

        http_client: HttpClient = BasicHttpClient(base_server_address)
        http_client = HttpClientWithAuthorization(http_client, self._api_key)
        http_client = HttpClientWithUserAgent(http_client, name, version)

        self._http_client: HttpClient = http_client

    @contextmanager
    def session(self) -> Generator[uuid.UUID, Any, Any]:
        """
        Context manager that group all request together to make it easier to debug on the backend side

        The id of the group is yield by this context manager
        """
        old_client = self._http_client
        trace_id = uuid.uuid4()

        try:
            self._http_client = HttpClientWithSession(self._http_client, str(trace_id))
            yield trace_id
        finally:
            self._http_client = old_client

    def computation_history(self, request: ComputationHistoryRequest) -> Response[ComputationHistoryResponse]:
        """ Obtain all status/history of a computation from the request itself. """
        body, metadata = self._http_client.do(HttpRequest(
            method=HTTPMethod.GET,
            url=f"/{_API_VERSION}/{_COMUTATIONS_HISTORY_PATH}",
            query_param=request,
        ))

        return Response(
            http_metadata=metadata,
            body=ComputationHistoryResponse.model_validate_json(body),
        )

    def upload_input(self, input: solve.Request.Input) -> None:
        """ Uploads the necessary input if any."""
        input.upload_missing_local_data()

    def solve_request(self, request: solve.Request) -> Response[solve.Response]:
        """ Sends the solve request."""
        body, metadata = self._http_client.do(HttpRequest(
            method=HTTPMethod.POST,
            url=f"/{_API_VERSION}/{_SOLVE_PATH}",
            body=request,
        ))

        return Response(
            http_metadata=metadata,
            body=solve.Response(solve.Response.ApiResponse.model_validate_json(body)),
        )

    def wait_for_result(
        self,
        computation_id: uuid.UUID,
        timeout_in_sec: Optional[float] = None,
        on_update: Callable[[List[Status]], None] = None,
    ):
        """
        Waits for results to be available, will return an error if any, if not will return None

        :param computation_id: computation id to be used to fetch the statuses
        :param timeout_in_sec: if set, will stop when timeout is reached, if not will not end until the status
            indicate the computation is done.
        :param on_update: on each update, a callback function will be called with all statuses

        :raises TimeoutError: timeout has been reached
        :raises FailedComputationError: the computation failed to complete
        """
        # wait until the response is uploaded, unless a timeout is set
        start_time = time.time()
        while True:
            if timeout_in_sec is not None and time.time() < start_time + timeout_in_sec:
                break

            status_response = self.computation_history(ComputationHistoryRequest(id=computation_id))
            if status_response.http_metadata.status_code != 200:
                raise ServerError(f"Computation history request returned an unexpected http status: {status_response.http_metadata.status_code}.")

            history = status_response.body

            # History should contain only 1 element since we request to filter by
            # the computation id, unless the computation_id is wrong
            if len(history) == 0:
                raise ServerError("Computation history returned no computation.")
            if len(history) > 1:
                raise ServerError("Computation history returned more than 1 computation while only a single computation was requested.")

            # if the user has provided a callback function
            if on_update is not None:
                on_update(history[0].status)

            done, finished = _status_includes_final_state(history[0].status)

            # computation is done, end the waiting
            if done:
                if not finished:
                    raise MissingFinishedStatusError()

                return

            time.sleep(get_dynamic_wait_interval(start_time))

        raise TimeoutError(f"Timeout reached ({timeout_in_sec}s) while waiting for computation to end.")

    def result_content_length(self, request: solve.Request) -> int:
        """ Returns the content length of the result """
        return request.output.location.download_content_length(request.output.result_archive_file_name)

    def download_result(self, request: solve.Request, bytes_reader: BytesIO) -> solve.Response.Result:
        """ Download a computation's response in the given request output location """
        request.output.location.download(request.output.result_archive_file_name, bytes_reader)
        if len(bytes_reader.getvalue()) == 0:
            raise EmptyResultError("The computation ended but there is no response in the output location.")

        with ZipFile(bytes_reader) as zipFile:
            return solve.Response.Result(
                result =_extract_array_from_zip(zipFile, 'result.npy'),
                metrics=_extract_json_from_zip(zipFile, 'metrics.json', solve.Response.Result.Metrics.model_validate_json),
            )

    def download_error(self, request: solve.Request, bytes_reader: BytesIO) -> solve.Response.Result.Error:
        request.output.location.download(request.output.result_archive_file_name, bytes_reader)
        if len(bytes_reader.getvalue()) == 0:
            raise EmptyResultError("The computation ended but there is no response in the output location.")

        with ZipFile(bytes_reader) as zipFile:
            return solve.Response.Result.Error(
                error=_extract_json_from_zip(zipFile, "error.json", solve.Response.Result.Error.model_validate_json).error,
            )

    def temp_storage(self) -> Response[TempStorageResponse]:
        body, metadata = self._http_client.do(HttpRequest(
            method=HTTPMethod.GET,
            url=f"/{_API_VERSION}/{_TEMP_STORAGE_PATH}",
        ))

        return Response(
            http_metadata=metadata,
            body=TempStorageResponse.model_validate_json(body),
        )

    def get_credits(self) ->Response[GetCreditsResponse]:
        body, metadata = self._http_client.do(HttpRequest(
            method=HTTPMethod.GET,
            url=f"/{_API_VERSION}/{_CREDITS_PATH}",
        ))

        return Response(
            http_metadata=metadata,
            body=GetCreditsResponse.model_validate_json(body)
        )

def _status_includes_final_state(status: List[Status]) -> Tuple[bool, bool]:
    """
    Return if the status list of a computation includes 'done' state (the final state).

    If it also returns whether the computation has succeeded or not.
    """
    done = False
    finished = False
    for s in status:
        if s.status == DONE_STATUS:
            done = True
        elif s.status == FINISHED_STATUS:
            # no finished status indicates no result were uploaded
            finished = True

    return done, finished


def _extract_json_from_zip(zipFile: ZipFile, filename: str, parse: Callable[[bytes], T]) -> T:
    """ Returns a validated json object from a zipped json file """
    try:
        with zipFile.open(filename) as f:
            return parse(f.read())
    except KeyError:
        raise RuntimeError(f"result archive does not contain {filename}")


def _extract_array_from_zip(zipFile: ZipFile, filename: str) -> NDArray[np.float32]:
    """ returns an NDArray object from a zipped .npy file """
    try:
        with zipFile.open(filename) as f:
            return np.load(f)
    except KeyError:
        raise RuntimeError(f"result archive does not contain {filename}")