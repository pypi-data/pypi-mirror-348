# Copyright (c) 2025, InfinityQ Technology, Inc.

from datetime import datetime
from enum import Enum
from typing import List, Optional
from typing_extensions import override, Self

from pyfiglet import Figlet
from rich.columns import Columns
from rich.console import Group, RenderableType
from rich.live import Live
from rich.panel import Panel
from rich.progress import Progress, TextColumn, TimeElapsedColumn, BarColumn, TaskProgressColumn
from rich.rule import Rule
from rich.spinner import Spinner, SPINNERS
from rich.table import Table
from rich.text import Text
from rich.tree import Tree

from titanq._event import Sink
from titanq._event.sink import ContentBuilder, DefinedProgress, UndefinedProgress
from titanq._event.sink.display_util import generate_word_animation
from titanq._util.decorators import chainable


# append rich library spinners our titanq animation
SPINNERS["titanq"] = {
    "interval": 120,
    "frames": generate_word_animation("TITANQ")
}


class PrettyTextRenderableTag(Enum):
    """
    Enums for any 'PrettyTextRenderable' tag.
    Needed to distinguish a renderable from another.
    """
    HEADER_CONTENT = 1
    UNDEFINED_PROGRESS_CONTENT = 2
    DEFINED_PROGRESS_CONTENT = 3
    TEXT_CONTENT = 4


class PrettyTextRenderable:
    """Wrapper arround rich 'RenderableType' that also contains a tag."""

    def __init__(self, content: RenderableType, tag: PrettyTextRenderableTag):
        self._content = content
        self._tag = tag

    def content(self) -> RenderableType:
        """The content of the renderable"""
        return self._content

    def tag(self) -> PrettyTextRenderableTag:
        """The tag of the renderable"""
        return self._tag


class PrettyTextContentBuilder(ContentBuilder[PrettyTextRenderable]):

    def __init__(self):
        self._content: Text = Text()
        self._color: Optional[str] = None
        self._spinner: Spinner = None

    @override
    def build(self) -> PrettyTextRenderable:
        # color the content only if set
        if self._color:
            self._content.stylize_before(self._color)

        if self._spinner:
            table = Table.grid(padding=(0, 1))
            table.add_row(self._content, self._spinner)
            return PrettyTextRenderable(table, PrettyTextRenderableTag.TEXT_CONTENT)

        return PrettyTextRenderable(self._content, PrettyTextRenderableTag.TEXT_CONTENT)

    @override
    @chainable
    def set_color(self, color: str) -> Self:
        self._color = color

    @override
    @chainable
    def add_emoji(self, emoji: str) -> Self:
        emoji = Text.from_markup(emoji)
        self._content.append(emoji)

    @override
    @chainable
    def add_text(self, text: str) -> Self:
        self._content.append(text)

    @override
    @chainable
    def add_whitespace(self) -> Self:
        self._content.append(" ")

    @override
    @chainable
    def add_tailing_spinner(self) -> Self:
        self._spinner = Spinner("titanq", style="magenta")


class PrettyTextDefinedProgress(DefinedProgress[PrettyTextRenderable]):

    def __init__(self):
        self._progress = Progress(
            TextColumn("{task.description}"),
            BarColumn(),
            TaskProgressColumn(),
            TimeElapsedColumn(),
        )

        # needed to keep track which update is it for
        self._progress_tasks: List[int] = []

    @override
    def add_task(self, renderable: PrettyTextRenderable, total: int) -> int:
        return self._progress.add_task(renderable.content(), total=total, time=datetime.now().strftime("[%H:%M:%S]"))

    @override
    def content(self) -> PrettyTextRenderable:
        return PrettyTextRenderable(self._progress, PrettyTextRenderableTag.DEFINED_PROGRESS_CONTENT)

    @override
    def update(self, handle: int, new_value: int, renderable: Optional[PrettyTextRenderable] = None) -> None:
        if renderable is not None:
            self._progress.update(handle, completed=new_value, description=renderable.content())
        else:
            self._progress.update(handle, completed=new_value)

    @override
    def finalize(self) -> None:
        # stop all tasks, whatever the status
        for task in self._progress_tasks:
            self._progress.stop_task(task)

        # stop the progress bar
        self._progress.stop()


class PrettyTextUndefinedProgress(UndefinedProgress[PrettyTextRenderable]):

    @override
    def update(self, renderable: PrettyTextRenderable, additional_renderables: Optional[List[PrettyTextRenderable]] = None) -> PrettyTextRenderable:
        grid = Table.grid(padding=(0, 1))
        tree = Tree(label=renderable.content(), guide_style="dim")
        grid.add_row(tree)

        if additional_renderables:
            for renderable in additional_renderables:
                tree.add(renderable.content())

        return PrettyTextRenderable(grid, PrettyTextRenderableTag.UNDEFINED_PROGRESS_CONTENT)


class DisplayHandler:

    def __init__(self):
        self._live = Live(refresh_per_second=10)
        self._live_entries: Group = Group()

        self._previous_tag: PrettyTextRenderableTag = None

    def start(self) -> None:
        """Start the display handler."""
        self._live.start()

    def stop(self) -> None:
        """Stops the display handler."""
        # ensure that last frame is sent (especially for Jupyter as sometime the last frame is not sent)
        self._live.refresh()
        self._live.stop()

    def update(self, entry: RenderableType, tag: PrettyTextRenderableTag) -> None:
        """Update the display content."""
        # case where we want to update the last undefined progress content,
        # instead of adding a new entry.
        if self._is_previous_and_current_tag_undefined_progress(tag):
            self._update_last(entry)
        # when creating a defined progress renderable, a renderable is updated multiple times for the same entry.
        elif self._is_previous_and_current_tag_defined_progress(tag):
            self._update_last(entry)
        else:
            self._add_new(entry)

        # update with newest tag
        self._previous_tag = tag

    def _is_previous_and_current_tag_undefined_progress(self, tag) -> bool:
        return (
            self._previous_tag is PrettyTextRenderableTag.UNDEFINED_PROGRESS_CONTENT and
            tag is PrettyTextRenderableTag.UNDEFINED_PROGRESS_CONTENT
        )

    def _is_previous_and_current_tag_defined_progress(self, tag: PrettyTextRenderableTag):
        return (
            self._previous_tag is PrettyTextRenderableTag.DEFINED_PROGRESS_CONTENT and
            tag is PrettyTextRenderableTag.DEFINED_PROGRESS_CONTENT)

    def _add_new(self, entry: RenderableType) -> None:
        """Adds a new entry to the display"""
        self._live_entries.renderables.append(entry)
        self._live.update(self._live_entries)

    def _update_last(self, entry: RenderableType) -> None:
        """
        Updates the last entry of the display.
        Meaning it will remove it and set the new one
        """
        self._live_entries.renderables.pop()
        self._add_new(entry)


class PrettyTextSink(Sink[PrettyTextRenderable]):
    """
    The PrettyTextSink utilizes rich library to enhance the output and make it
    as beautiful as possible and pleasing for the end-users.

    It offers features such as Emoji's support, colors and some progress bars.
    """

    def __init__(self,
        version: str,
        show_header: bool,
        start_separator: Optional[str] = None
    ):
        """
        Initialize the pretty sink logger.

        :param version: Version shown in the sink
        :param show_header: If True, will show a header in the startup
        :param start_separator: Separator text to include if set that will be shown in the startup
        """
        self._version = version
        self._show_header = show_header
        self._start_separator = start_separator

        self._display_handler = DisplayHandler()

    @override
    def start(self) -> None:
        self._display_handler.start()
        self._start_display()

    @override
    def stop(self) -> None:
        self._display_handler.stop()

    @override
    def display(self, renderable: PrettyTextRenderable, with_timestamp: Optional[bool] = True) -> None:
        timestamp = Text(datetime.now().strftime("[%H:%M:%S]"), style="dim #39c5cf")

        columns = Columns([renderable.content()])
        if with_timestamp:
            columns.renderables.insert(0, timestamp)

        self._display_handler.update(columns, renderable.tag())

    @override
    def content_builder(self) -> ContentBuilder[PrettyTextRenderable]:
        return PrettyTextContentBuilder()

    @override
    def defined_progress(self) -> DefinedProgress[PrettyTextRenderable]:
        return PrettyTextDefinedProgress()

    @override
    def undefined_progress(self) -> UndefinedProgress[PrettyTextRenderable]:
        return PrettyTextUndefinedProgress()

    def _start_display(self) -> None:
        """What will be displayed when starting up"""
        if self._show_header:
            self.display(self._banner(version=self._version), with_timestamp=False)

        # display a separator that would indicate what optimization we are at
        if self._start_separator is not None:
            self._display_handler.update(
                Rule(self._start_separator, style=None),
                PrettyTextRenderableTag.TEXT_CONTENT
            )

    def _banner(self, version: str) -> PrettyTextRenderable:
        """
        Displays a banner.
        """
        #╭───────────────────── vX.Y.Z ──────────────────────╮
        #│      _________________              _______       │
        #│      ___  __/__(_)_  /______ _________  __ \      │
        #│      __  /  __  /_  __/  __ `/_  __ \  / / /      │
        #│      _  /   _  / / /_ / /_/ /_  / / / /_/ /       │
        #│      /_/    /_/  \__/ \__,_/ /_/ /_/\___\_\       │
        #│                                                   │
        #│                                                   │
        #╰───────────────────────────────────────────────────╯
        panel = Panel.fit(
            Figlet(font='speed').renderText("TitanQ"), style="purple",
            title=f"[italic bold purple]{version}[/]",
            padding=(0, 6),  # (top_bottom, left_right)
            border_style="purple",
        )
        return PrettyTextRenderable(panel, "header")
