# Copyright (c) 2025, InfinityQ Technology, Inc.

"""
Progress events are some type of events that would occur over a timeline with
some progress updates.
"""

import copy
from typing import Dict, Literal, Optional
from typing_extensions import override

from titanq._event import ProgressEvent, Event
from titanq._event.sink import ContentBuilder, DefinedProgress, Sink
from titanq._model.bytes_reader import BytesReaderWithCallback
from titanq._util.human_readables import bytes_size_human_readable


_DATA_TRANSFER_WAITING_EMOJI = ":hourglass_not_done:"
_DATA_TRANSFER_COMPLETED_EMOJI = ":hourglass:"


class UploadEvent(ProgressEvent):
    """Progress event when TitanQ is uploading some files."""

    def __init__(self, files: Dict[str, BytesReaderWithCallback]):
        self._files = { f: None for f in files.items()}
        self._defined_progress: DefinedProgress = None

    @override
    def start(self, sink: Sink) -> Event:
        self._defined_progress = sink.defined_progress()
        for key in self._files:
            file_name, reader = key
            cb = sink.content_builder()
            _data_transfer_update_content(cb, file_name, "upload", False)
            task_id = self._defined_progress.add_task(cb.build(), reader.total_size())

            reader.set_callback(
                lambda reader, task_id = task_id, cb = cb: self._defined_progress.update(
                    handle=task_id,
                    new_value=reader.tell(),
                    # we need to deepcopy the content builder as it should have no reference to the initial one
                    renderable=_data_transfer_append_size_content(copy.deepcopy(cb), reader.total_size(), reader.tell()).build()
            ))
            self._files[key] = task_id
            sink.display(self._defined_progress.content())

    @override
    def end(self, sink: Sink) -> Event:
        if self._defined_progress:
            for (file_name, reader), task_id in filter(lambda value: value[1] is not None, self._files.items()):
                update_content = sink.content_builder()
                _data_transfer_update_content(update_content, file_name, "upload", True)
                _data_transfer_append_size_content(update_content, reader.total_size())

                self._defined_progress.update(task_id, reader.total_size(), update_content.build())

            self._defined_progress.finalize()


class DownloadResultEvent(ProgressEvent):
    """Progress event when TitanQ is downloading results."""

    def __init__(self, file_name: str, total_size: int, bytes_reader: BytesReaderWithCallback):
        self._file_name = file_name
        self._total_size = total_size
        self._bytes_reader = bytes_reader

        self._defined_progress: DefinedProgress = None
        self._task_id = None

    @override
    def start(self, sink: Sink) -> Event:
        self._defined_progress = sink.defined_progress()

        cb = sink.content_builder()
        _data_transfer_update_content(cb, self._file_name, "download", False)
        self._task_id = self._defined_progress.add_task(cb.build(), self._total_size)

        self._bytes_reader.set_callback(
            lambda reader, task_id = self._task_id, cb = cb: self._defined_progress.update(
                handle=task_id,
                new_value=reader.tell(),
                renderable=_data_transfer_append_size_content(copy.deepcopy(cb), self._total_size, reader.tell()).build()
            )
        )
        sink.display(self._defined_progress.content())

    @override
    def end(self, sink: Sink) -> Event:
        if self._defined_progress is not None and self._task_id is not None:
            cb = sink.content_builder()
            _data_transfer_update_content(cb, self._file_name, "download", True)
            _data_transfer_append_size_content(cb, self._total_size)

            self._defined_progress.update(self._task_id, self._total_size, cb.build())
            self._defined_progress.finalize()


def _data_transfer_update_content(
    content_builder: ContentBuilder,
    file_name: str,
    data_transfer_type: Literal['download', 'upload'],
    finished: bool,
) -> ContentBuilder:
    """Formats the text for a data transfer event"""
    data_transfer_key_word_start = "Downloading" if data_transfer_type == "download" else "Uploading"
    data_transfer_key_word_end = "Downloaded" if data_transfer_type == "download" else "Uploaded"
    (content_builder
        .add_emoji(_DATA_TRANSFER_COMPLETED_EMOJI if finished else _DATA_TRANSFER_WAITING_EMOJI)
        .add_whitespace()
    )
    if finished:
        return content_builder.add_text(f"{file_name} file {data_transfer_key_word_end}")
    else:
        return content_builder.add_text(f"{data_transfer_key_word_start} {file_name} file...")


def _data_transfer_append_size_content(
    content_builder: ContentBuilder,
    total_bytes: int,
    current_bytes: Optional[int] = None,
) -> ContentBuilder:
    """
    Appends to data transfer text the current and total size.

    if current bytes is set:
        '(34.1MB/68.2MB)'
    if current_bytes is not set
        '(68.2MB)'
    """
    hr_total_bytes = bytes_size_human_readable(total_bytes)

    content_builder.add_whitespace()
    if current_bytes is not None:
        hr_current_bytes = bytes_size_human_readable(current_bytes)
        return content_builder.add_text(f"({hr_current_bytes}/{hr_total_bytes})")
    else:
        return content_builder.add_text(f"({hr_total_bytes})")