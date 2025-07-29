from io import BytesIO
from typing import Callable, List, Optional

import pandas as pd


class DataFrameUploader(BytesIO):
    def __init__(self, df: pd.DataFrame, chunk_size: int = 100_000, cb: Optional[Callable[[int], None]] = None):
        super().__init__()
        self._df = df
        self._chunk_size = chunk_size
        self._cb = cb
        self._offsets: List[int] = list(range(0, len(self._df), self._chunk_size))
        self._current_offset: int = 0

    def __len__(self):
        if not hasattr(self, "_len"):
            _buf = BytesIO()
            self._df[(offset := self._offsets[0]) : offset + self._chunk_size].to_csv(_buf, index=False, header=True)
            self._len = len(_buf.getvalue()) * len(self._offsets)
        return self._len

    def set_callback(self, cb: Callable[[int], None]) -> None:
        self._cb = cb

    def read(self, n=-1) -> bytes:
        chunk = BytesIO.read(self, n)
        if not chunk and self._current_offset < len(self._offsets):
            if n < 0:
                self._df.to_csv(self, index=False)
                self._current_offset = len(self._offsets)
            else:
                self._df[(offset := self._offsets[self._current_offset]) : offset + self._chunk_size].to_csv(
                    self, index=False, header=self._current_offset == 0
                )
                self._current_offset += 1
            self.seek(0)
            chunk = BytesIO.read(self, n)
        if self._cb:
            self._cb(len(chunk))
        return chunk
