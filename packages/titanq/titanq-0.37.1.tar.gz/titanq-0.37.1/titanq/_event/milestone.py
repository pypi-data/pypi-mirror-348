# Copyright (c) 2025, InfinityQ Technology, Inc.

"""
Milestone events are some type of events that would just occur at some point.
Nothing special about them, they just happen and something is instantly done.
"""

from typing_extensions import override

from titanq._event import Event
from titanq._event.sink import Sink


class UploadStartEvent(Event):
    """Milestone event when the SDK is starting to upload some files."""

    @override
    def output(self, sink: Sink) -> None:
        sink.display(
            sink.content_builder()
                .add_emoji(":outbox_tray:")
                .add_whitespace()
                .add_text("Starting data upload")
                .build()
        )


class GotComputationIDEvent(Event):
    """Milestone event when the SDK has obtained the computation ID from TitanQ"""

    def __init__(self, computation_id: str):
        self._computation_id = computation_id

    @override
    def output(self, sink: Sink):
        sink.display(
            sink.content_builder()
                .add_emoji(":id:")
                .add_whitespace()
                .add_text(f"Computation ID: {self._computation_id}")
                .build()
        )


class OptimizationCompletedEvent(Event):
    """Milestone event when the SDK has finished optimizing."""

    @override
    def output(self, sink: Sink) -> None:
        sink.display(
            sink.content_builder()
                .add_emoji(":white_check_mark:")
                .add_whitespace()
                .add_text("Optimization completed!")
                .build()
        )


class ComputationFailedEvent(Event):
    """Milestone event when the SDK has acknowledged that the computation has failed."""

    @override
    def output(self, sink: Sink) -> None:
        sink.display(
            sink.content_builder()
                .add_emoji(":exclamation:")
                .add_whitespace()
                .add_text("Computation failed")
                .build()
        )