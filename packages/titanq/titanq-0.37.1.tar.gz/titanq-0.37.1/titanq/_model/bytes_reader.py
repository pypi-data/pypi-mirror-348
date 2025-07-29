# Copyright (c) 2025, InfinityQ Technology, Inc.

from io import BytesIO
from typing import Callable
from typing_extensions import override

class BytesReaderWithCallback(BytesIO):

    def __init__(self, initial_bytes = b""):
        super().__init__(initial_bytes)
        self._callback_update = None
        self._registered_total_size = 0

    def set_callback(self, c: Callable[['BytesReaderWithCallback'], None] = None) -> None:
        self._callback_update = c

    @override
    def read(self, size = -1):
        data = super().read(size)
        if self._callback_update:
            self._callback_update(self)
        return data

    @override
    def write(self, buffer):
        data = super().write(buffer)
        if self._callback_update:
            self._callback_update(self)
        return data

    @override
    def close(self) -> None:
        # keep the latest total size before closing
        self._registered_total_size = self.getbuffer().nbytes
        super().close()

    def total_size(self) -> int:
        """Return the total number of bytes in the buffer."""
        return self._registered_total_size if self.closed else self.getbuffer().nbytes