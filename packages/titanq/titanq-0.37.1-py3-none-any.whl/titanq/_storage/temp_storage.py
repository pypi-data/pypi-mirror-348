# Copyright (c) 2025, InfinityQ Technology, Inc.

from io import BytesIO
from typing import List, Optional
from titanq._api.client import Client
from titanq._api.model.local_file import InputFiles, LocalFile
from titanq._api.model.location import TempStorageLocation
from titanq._api.model.solve import Manifest, Request
from titanq._api.model.temp_storage import DualUrl
from titanq._storage import StorageClient


class TempStorage(StorageClient):
    """Temp storage client using the temp storage from InfinityQ"""

    def __init__(self, titanq_client: Client):
        self._titanq_client = titanq_client

    def init(self) -> None:
        self._tempstorage = self._titanq_client.temp_storage()

    def request_input_builder(
        self,
        bias: BytesIO,
        variable_bounds: BytesIO,
        weights: Optional[BytesIO] = None,
        constraint_weights: Optional[BytesIO] = None,
        constraint_bounds: Optional[BytesIO] = None,
        quad_constraint_weights: Optional[BytesIO] = None,
        quad_constraint_bounds: Optional[BytesIO] = None,
        quad_constraint_linear_weights: Optional[BytesIO] = None,
        manifest: Optional[Manifest] = None,
    ) -> Request.Input:
        temp_storage_input = self._tempstorage.body.input

        files = InputFiles(
            bias_file_name=LocalFile(remote_name=temp_storage_input.bias.download, data=bias),
            variable_bounds_file_name=LocalFile(remote_name=temp_storage_input.variable_bounds.download, data=variable_bounds)
        )
        urls: List[DualUrl] = [temp_storage_input.bias, temp_storage_input.variable_bounds]

        if weights is not None:
            files.weights_file_name = LocalFile(remote_name=temp_storage_input.weights.download, data=weights)
            urls.append(temp_storage_input.weights)

        if constraint_weights is not None:
            files.constraint_weights_file_name = LocalFile(remote_name=temp_storage_input.constraint_weights.download, data=constraint_weights)
            urls.append(temp_storage_input.constraint_weights)

        if constraint_bounds is not None:
            files.constraint_bounds_file_name = LocalFile(remote_name=temp_storage_input.constraint_bounds.download, data=constraint_bounds)
            urls.append(temp_storage_input.constraint_bounds)

        if quad_constraint_weights is not None:
            files.quad_constraint_weights_file_name = LocalFile(remote_name=temp_storage_input.quad_constraint_weights.download, data=quad_constraint_weights)
            urls.append(temp_storage_input.quad_constraint_weights)

        if quad_constraint_bounds is not None:
            files.quad_constraint_bounds_file_name = LocalFile(remote_name=temp_storage_input.quad_constraint_bounds.download, data=quad_constraint_bounds)
            urls.append(temp_storage_input.quad_constraint_bounds)

        if quad_constraint_linear_weights is not None:
            files.quad_constraint_linear_weights_file_name = LocalFile(remote_name=temp_storage_input.quad_constraint_linear_weights.download, data=quad_constraint_linear_weights)
            urls.append(temp_storage_input.quad_constraint_linear_weights)

        return Request.Input(location=TempStorageLocation(urls), files=files, manifest=manifest)

    def request_output_builder(self) -> Request.Output:
        return Request.Output(
            location=TempStorageLocation([self._tempstorage.body.output.result]),
            result_archive_file_name=self._tempstorage.body.output.result.upload
        )