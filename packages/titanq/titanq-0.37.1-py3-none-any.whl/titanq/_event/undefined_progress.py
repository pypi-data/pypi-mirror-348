# Copyright (c) 2025, InfinityQ Technology, Inc.

"""
Progress events are some type of events that would occur over a timeline with
some progress updates.
"""

from typing import Any, List, Optional, TypeVar
from typing_extensions import override

from titanq._api.model.history import Status
from titanq._event import Event, ProgressEvent
from titanq._event.sink import ContentBuilder, Sink, UndefinedProgress

T = TypeVar('T')


_WAITING_UNDEFINED_PROGRESS_COLOR = "orange3"


class PreparingDataEvent(ProgressEvent):
    """Undefined progress event when the SDK is preparing data."""

    def __init__(self):
        self._undefined_progress: UndefinedProgress = None

    @override
    def start(self, sink: Sink) -> Event:
        self._undefined_progress = sink.undefined_progress()
        sink.display(
            self._undefined_progress.update(
                renderable=self._preparing_content_builder(sink)
                    .set_color(_WAITING_UNDEFINED_PROGRESS_COLOR)
                    .add_tailing_spinner()
                    .build()
            )
        )

    @override
    def end(self, sink: Sink) -> Event:
        sink.display(
            self._undefined_progress.update(
                renderable=self._preparing_content_builder(sink).build()
            )
        )
        sink.display(
            sink.content_builder()
                .add_emoji(":package:")
                .add_whitespace()
                .add_text("Data prepared for TitanQ")
                .build()
        )

    def _preparing_content_builder(self, sink: Sink) -> ContentBuilder:
        return (
            sink.content_builder()
                .add_emoji(":hammer:")
                .add_whitespace()
                .add_text("Preparing data for TitanQ")
        )


class SendingProblemEvent(ProgressEvent):
    """Undefined progress event when the SDK is sending a request to TitanQ."""

    def __init__(self):
        self._undefined_progress: UndefinedProgress = None

    @override
    def start(self, sink: Sink) -> Event:
        self._undefined_progress = sink.undefined_progress()
        sink.display(
            self._undefined_progress.update(
                renderable=self._preparing_content_builder(sink)
                    .set_color(_WAITING_UNDEFINED_PROGRESS_COLOR)
                    .add_tailing_spinner()
                    .build()
            )
        )

    @override
    def end(self, sink: Sink) -> Event:
        sink.display(
            self._undefined_progress.update(
                renderable=self._preparing_content_builder(sink).build()
            )
        )
        sink.display(
            sink.content_builder()
                .add_emoji(":envelope_with_arrow:")
                .add_whitespace()
                .add_text("Request received by TitanQ")
                .build()
        )

    def _preparing_content_builder(self, sink: Sink) -> ContentBuilder:
        return (
            sink.content_builder()
                .add_emoji(":rocket:")
                .add_whitespace()
                .add_text("Sending request to TitanQ")
        )


class WaitingForResultEvent(ProgressEvent):
    """Undefined progress event when the SDK is waiting after the results."""

    def __init__(self):
        self._undefined_progress: UndefinedProgress = None
        self._latest_status_list = None # keep in memory the latest
        self._sink = None

    def update_status_list(self, status_list: List[Status]):
        """Updates the status list displayed in this event"""
        if self._sink:
            self._on_status_updates(self._sink, status_list)

    @override
    def start(self, sink: Sink) -> Event:
        self._sink = sink
        self._undefined_progress = sink.undefined_progress()

    @override
    def end(self, sink: Sink) -> Event:
        sink.display(
            self._undefined_progress.update(
                renderable=sink.content_builder()
                    .add_emoji(":brain:")
                    .add_whitespace()
                    .add_text("TitanQ is working its magic")
                    .build(),
                additional_renderables=self._build_status_content(sink, self._latest_status_list)
            )
        )
        sink.display(
            sink.content_builder()
                .add_emoji(":bulb:")
                .add_whitespace()
                .add_text("Solution received from TitanQ")
                .build()
        )

    def _on_status_updates(self, sink: Sink, status_list: Optional[List[Status]] = None) -> None:
        self._latest_status_list = status_list
        sink.display(
            self._undefined_progress.update(
                renderable=sink.content_builder()
                    .set_color(_WAITING_UNDEFINED_PROGRESS_COLOR)
                    .add_emoji(":brain:")
                    .add_whitespace()
                    .add_text("TitanQ is working its magic")
                    .add_tailing_spinner()
                    .build(),
                additional_renderables=self._build_status_content(sink, self._latest_status_list, with_colors=True)
        ))

    def _build_status_content(
        self,
        sink: Sink,
        status_list: Optional[List[Status]] = None,
        with_colors: bool = False,
    ) -> List[Any]:
        if status_list is None:
            return None

        content_list = []
        for i, status in enumerate(status_list):
            content_builder = (
                sink.content_builder()
                    .add_text("Status update: ")
                    .add_text(status.status)
                    .add_whitespace()
                    .add_text("(")
                    .add_text(status.timestamp.strftime("%H:%M:%S"))
                    .add_text(")")
            )

            if with_colors:
                if "failed" in status.status:
                    content_builder.set_color("red")
                if "finished" in status.status:
                    content_builder.set_color("green")
                elif i == len(status_list) - 1: # last item
                    content_builder.set_color("blue")

            content_list.append(content_builder.build())
        return content_list


class BuildingFromMPSEvent(ProgressEvent):
    """Undefined progress event when the SDK building the model from an mps file."""

    def __init__(self, file_name: str):
        self._file_name = file_name
        self._undefined_progress: UndefinedProgress = None

    @override
    def start(self, sink: Sink) -> Event:
        self._undefined_progress = sink.undefined_progress()
        sink.display(
            self._undefined_progress.update(
                renderable=self._preparing_content_builder(sink)
                    .set_color(_WAITING_UNDEFINED_PROGRESS_COLOR)
                    .add_tailing_spinner()
                    .build()
            )
        )

    @override
    def end(self, sink: Sink) -> Event:
        sink.display(
            self._undefined_progress.update(
                renderable=self._preparing_content_builder(sink).build()
            )
        )
        sink.display(
            sink.content_builder()
                .add_emoji(":wrench:")
                .add_whitespace()
                .add_text(f"Model built from MPS file ({self._file_name})")
                .build()
        )

    def _preparing_content_builder(self, sink: Sink) -> ContentBuilder:
        return (
            sink.content_builder()
                .add_emoji(":wrench:")
                .add_whitespace()
                .add_text(f"Loading and building model from MPS file ({self._file_name})")
        )

