# Copyright (c) 2025, InfinityQ Technology, Inc.

from datetime import datetime
from io import BytesIO
from typing import Optional

from titanq._api.model.local_file import InputFiles, LocalFile
from titanq._api.model.location import S3Location
from titanq._api.model.solve import Manifest, Request
from titanq._storage import StorageClient


class S3Storage(StorageClient):
    """Storage client using S3 bucket from AWS"""

    def __init__(self, access_key: str, secret_key: str, bucket_name: str):
        self._access_key = access_key
        self._secret_key = secret_key
        self._bucket_name = bucket_name

        timestamp = datetime.now().isoformat()
        self._remote_folder = f"titanq_sdk/{timestamp}"

    def init(self) -> None:
        self._location = S3Location(bucket_name=self._bucket_name, access_key_id=self._access_key, secret_access_key=self._secret_key)

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
        files = InputFiles(
            bias_file_name=LocalFile(remote_name=self._get_full_filename("bias"), data=bias),
            variable_bounds_file_name=LocalFile(remote_name=self._get_full_filename("variable_bounds"), data=variable_bounds)
        )

        if weights is not None:
            files.weights_file_name = LocalFile(remote_name=self._get_full_filename("weights"), data=weights)
        if constraint_weights is not None:
            files.constraint_weights_file_name = LocalFile(remote_name=self._get_full_filename("constraint_weights"), data=constraint_weights)
        if constraint_bounds is not None:
            files.constraint_bounds_file_name = LocalFile(remote_name=self._get_full_filename("constraint_bounds"), data=constraint_bounds)
        if quad_constraint_weights is not None:
            files.quad_constraint_weights_file_name = LocalFile(remote_name=self._get_full_filename("quad_constraint_weights"), data=quad_constraint_weights)
        if quad_constraint_bounds is not None:
            files.quad_constraint_bounds_file_name = LocalFile(remote_name=self._get_full_filename("quad_constraint_bounds"), data=quad_constraint_bounds)
        if quad_constraint_linear_weights is not None:
            files.quad_constraint_linear_weights_file_name = LocalFile(remote_name=self._get_full_filename("quad_constraint_linear_weights"), data=quad_constraint_linear_weights)

        return Request.Input(location=self._location, files=files, manifest=manifest)

    def request_output_builder(self) -> Request.Output:
        return Request.Output(
            location=self._location,
            result_archive_file_name=self._get_full_filename("result"),
        )

    def _get_full_filename(self, filename: str) -> str:
        return f"{self._remote_folder}/{filename}"