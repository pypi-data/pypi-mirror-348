# Copyright (c) 2025, InfinityQ Technology, Inc.

from typing import Dict, List, Optional
from typing_extensions import override, Self

import logging

from titanq._event.sink import ContentBuilder, DefinedProgress, Sink, UndefinedProgress
from titanq._util.decorators import chainable


# Configure the logger
logging.basicConfig(
    format='[%(asctime)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    level=logging.INFO
)


class TextContentBuilder(ContentBuilder[str]):

    def __init__(self):
        self._content = ""

    @override
    def build(self) -> str:
        return self._content.strip()

    @override
    @chainable
    def set_color(self, color: str) -> Self:
        # no coloring for text based output
        pass

    @override
    @chainable
    def add_emoji(self, emoji: str) -> Self:
        # no emoji for text based output
        pass

    @override
    @chainable
    def add_text(self, text: str) -> Self:
        self._content += text

    @override
    @chainable
    def add_whitespace(self) -> Self:
        self._content += " "

    @override
    @chainable
    def add_tailing_spinner(self) -> Self:
        # no spinner animation for text based output
        pass


class TextDefinedProgress(DefinedProgress[str]):

    def __init__(self):
        self._progress_tasks: Dict[int, int] = {}
        self._content = None

    @override
    def add_task(self, renderable: str, total: int) -> int:
        self._content = renderable
        return 0 # unused, just return 0

    @override
    def content(self) -> str:
        return self._content

    @override
    def update(self, handle: int, new_value: int, renderable: Optional[str] = None) -> None:
        pass

    @override
    def finalize(self) -> None:
        pass


class TextUndefinedProgress(UndefinedProgress[str]):

    def __init__(self):
        # keep track if a log was already logged
        self._already_logged = []

    @override
    def update(self, renderable: str, additional_renderables: Optional[List[str]] = None) -> str:
        if renderable not in self._already_logged:
            self._already_logged.append(renderable)
            return renderable

        if additional_renderables:
            for renderable in additional_renderables:
                if renderable not in self._already_logged:
                    self._already_logged.append(renderable)
                    return renderable

        return ""


class TextSink(Sink[str]):
    """The TextSink is just a simple python logger."""

    def __init__(
        self,
        version: str,
        show_header: bool,
        start_separator: Optional[str] = None
    ):
        """
        Initialize a simple text sink logger.

        :param version: Version shown in the sink
        :param show_header: If True, will show a header in the startup
        :param start_separator: Separator text to include if set that will be shown in the startup
        """
        self._version = version
        self._show_header = show_header
        self._start_separator = start_separator

    @override
    def start(self) -> None:
        if self._start_separator is not None:
            logging.info(f"Using TitanQ SDK {self._version}")
        logging.info(f"------------------------ {self._start_separator} ------------------------")

    @override
    def stop(self) -> None:
        pass

    @override
    def display(self, renderable: str, with_timestamp: Optional[bool] = True) -> None:
        # if nothing, do not display
        if renderable != "":
            logging.info(renderable)

    @override
    def content_builder(self) -> ContentBuilder[str]:
        return TextContentBuilder()

    @override
    def defined_progress(self) -> DefinedProgress[str]:
        return TextDefinedProgress()

    @override
    def undefined_progress(self) -> UndefinedProgress[str]:
        return TextUndefinedProgress()