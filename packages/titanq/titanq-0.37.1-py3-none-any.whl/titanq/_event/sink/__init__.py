# Copyright (c) 2025, InfinityQ Technology, Inc.

from abc import ABC, abstractmethod
from typing import Generic, List, Optional, TypeVar
from typing_extensions import Self

T = TypeVar("T")


class ContentBuilder(ABC, Generic[T]):
    """
    This class builds some content to eventually be displayed.

    Usage example:
    >>>    content_builder = (
                ConcreteContentBuilder()
                .content_builder.add_emoji("👋")
                .content_builder.add_whitespace()
                .content_builder.add_text("Hello, World!")
        )

        content_builder.build()
        # "👋 Hello, World!"
    """

    @abstractmethod
    def build(self) -> T:
        """Builds the content."""

    @abstractmethod
    def set_color(self, color: str) -> Self:
        """Sets the color of the content."""

    @abstractmethod
    def add_emoji(self, emoji: str) -> Self:
        """Add an emoji to the content."""

    @abstractmethod
    def add_text(self, text: str) -> Self:
        """Add a text to the content."""

    @abstractmethod
    def add_whitespace(self) -> Self:
        """Add a whitespace to the content."""

    @abstractmethod
    def add_tailing_spinner(self) -> Self:
        """Add a spinner animation in the end of the content."""


class DefinedProgress(ABC, Generic[T]):
    """
    This class manages a process of a defined progress.

    Usage example:
        tasks = { "some task": 500 }
        defined_progress = ConcreteDefinedProgress(tasks)
        defined_progress.update("some task", 50)

        defined_progress.finalize()
    """
    @abstractmethod
    def add_task(self, renderable: T, total: int) -> int:
        """Adds a task and return a handle to use with further methods."""

    @abstractmethod
    def content(self) -> T:
        """Returns the content of the defined progress"""

    @abstractmethod
    def update(self, handle: int, new_value: int, renderable: Optional[T] = None) -> None:
        """Update the progress builder process."""

    @abstractmethod
    def finalize(self) -> None:
        """Finalize the progress building process."""


class UndefinedProgress(ABC, Generic[T]):
    """
    This class manages a process of a defined progress.

    Usage example:
        undefined_progress = ConcreteUndefinedProgress()

        undefined_progress.update("Hello, World")
    """

    @abstractmethod
    def update(self, renderable: T, additional_renderables: Optional[List[T]] = None) -> T:
        """
        Update the undefined progress with some renderable(s).

        Optionally, the sink can take additional renderables as a list.

        :param renderable: the main renderable to be displayed
        :param additional_renderables: A list of additional renderables to be displayed
        """


class Sink(ABC, Generic[T]):
    """
    Abstract class of a Sink type object. A Sink is any output type that you could
    use to transfer information from somewhere to another destination.

    As an example, a logger is a Sink.
    """

    @abstractmethod
    def start(self) -> None:
        """Starts the sink."""

    @abstractmethod
    def stop(self) -> None:
        """Stops the sink."""

    @abstractmethod
    def display(self, renderable: T, with_timestamp: Optional[bool] = True) -> None:
        """
        Display the content from a renderable.

        :param with_timestamp: If False, will not show any timestamp
        """

    @abstractmethod
    def content_builder(self) -> ContentBuilder[T]:
        """Returns a content builder to be able to build an output."""

    @abstractmethod
    def defined_progress(self) -> DefinedProgress[T]:
        """
        Returns a defined progress to be able to build and update an output.
        Multiple tasks can be assigned to a defined progress.
        """

    @abstractmethod
    def undefined_progress(self) -> UndefinedProgress[T]:
        """
        Returns an undefined progress to be able to build an output.
        Only a single task can be assigned to an undefined progress.
        """