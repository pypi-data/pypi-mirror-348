# Copyright (c) 2025, InfinityQ Technology, Inc.

from typing import List, Optional
from typing_extensions import override, Self

from titanq._event.sink import ContentBuilder, DefinedProgress, Sink, UndefinedProgress
from titanq._util.decorators import chainable



class NoOpContentBuilder(ContentBuilder[str]):

    @override
    def build(self) -> str: ...

    @override
    @chainable
    def set_color(self, color: str) -> Self: ...

    @override
    @chainable
    def add_emoji(self, emoji: str) -> Self: ...

    @override
    @chainable
    def add_text(self, text: str) -> Self:...

    @override
    @chainable
    def add_whitespace(self) -> Self: ...

    @override
    @chainable
    def add_tailing_spinner(self) -> Self: ...


class NoOpDefinedProgress(DefinedProgress[str]):

    @override
    def add_task(self, renderable: str, total: int) -> int: ...

    @override
    def content(self) -> str: ...

    @override
    def update(self, handle: int, new_value: int, renderable: Optional[str] = None) -> None: ...

    @override
    def finalize(self) -> None: ...


class NoOpUndefinedProgress(UndefinedProgress[str]):

    def update(self, renderable: str, additional_renderables: Optional[List[str]] = None) -> str: ...


class NoOpSink(Sink):
    """A sink that output nothing"""

    @override
    def start(self) -> None:
        pass

    @override
    def stop(self) -> None:
        pass

    @override
    def display(self, renderable: str, with_timestamp: Optional[bool] = True) -> None:
        pass

    @override
    def content_builder(self) -> ContentBuilder[str]:
        return NoOpContentBuilder()

    @override
    def defined_progress(self) -> DefinedProgress[str]:
        return NoOpDefinedProgress()

    @override
    def undefined_progress(self) -> UndefinedProgress[str]:
        return NoOpUndefinedProgress()