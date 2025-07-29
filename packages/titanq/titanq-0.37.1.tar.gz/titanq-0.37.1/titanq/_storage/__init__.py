# Copyright (c) 2025, InfinityQ Technology, Inc.

from abc import ABC, abstractmethod
from io import BytesIO
from typing import Optional

from titanq._api.model.solve import Manifest, Request


class StorageClient(ABC):

    @abstractmethod
    def init(self) -> None:
        """Initialize the storage client"""

    @abstractmethod
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
        """Builds the input request"""
        pass

    @abstractmethod
    def request_output_builder(self) -> Request.Output:
        """Builds the output request"""
        pass