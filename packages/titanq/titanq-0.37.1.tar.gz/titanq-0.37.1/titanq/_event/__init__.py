# Copyright (c) 2025, InfinityQ Technology, Inc.

from abc import ABC, abstractmethod
from contextlib import contextmanager
import logging
from typing import Optional

from titanq._event.sink import Sink
from titanq._event.sink.no_op import NoOpSink
from titanq._event.sink.pretty_text import PrettyTextSink
from titanq._event.sink.text import TextSink


log = logging.getLogger("TitanQ")


# GLOBALS
_banner_already_shown = False # wether the banner has already been shown
_optimization_counter = 1 # number of optimization already done


class Event(ABC):
    """A simple event that would occur at some point."""

    @abstractmethod
    def output(self, sink: Sink) -> None:
        """Output self to the sink."""


class ProgressEvent(ABC):
    """An event that indicates an event is tied to some kind of progress"""

    @abstractmethod
    def start(self, sink: Sink) -> None:
        pass

    @abstractmethod
    def end(self, sink: Sink) -> None:
        pass


class EventEmitter():
    """
    A class responsible for emitting events to subscribed output sinks.
    """

    def __init__(self, sink: Sink):
        self._sink = sink

    def start(self) -> None:
        """Starts the event emitter"""
        self._sink.start()

    def emit(self, event: Event) -> None:
        """Emit an event to the subscribed sinks."""
        try:
            event.output(self._sink)
        except Exception as ex:
            log.debug(f"Event failed to emit with {type(self._sink)}", ex)

    @contextmanager
    def emit_with_progress(self, event: ProgressEvent):
        try:
            event.start(self._sink)
        except Exception as ex:
            log.debug(f"Progress event failed to start with {type(self._sink)}", ex)

        yield

        try:
            event.end(self._sink)
        except Exception as ex:
            log.debug(f"Progress event failed to end with {type(self._sink)}", ex)

    def stop(self) -> None:
        """Stops the event emitter"""
        self._sink.stop()


def create_sink(log_mode: Optional[str], is_optimization: bool) -> EventEmitter:
    """Setup all sinks based on the given mode and returns the EventEmitter"""
    # having it as a lazy import fixes the circular import
    from titanq import __version__ as titanq_version

    global _banner_already_shown
    global _optimization_counter

    start_separator = f"Optimization # {_optimization_counter}" if is_optimization else None

    if log_mode in (None, "off"):
        sink = NoOpSink()
    elif log_mode == "pretty":
        sink = PrettyTextSink(version=titanq_version, show_header=not _banner_already_shown, start_separator=start_separator)
    elif log_mode == "text":
        sink = TextSink(version=titanq_version, show_header=not _banner_already_shown, start_separator=start_separator)
    else:
        raise ValueError(f"Unsupported log_mode: {log_mode}")

    # update global variables
    _banner_already_shown = True
    if is_optimization:
        _optimization_counter += 1

    return EventEmitter(sink)