from collections.abc import AsyncGenerator

from fastapi import UploadFile

from .diff.differ import DiffStrategy, diff_files
from .diff.types import Diff
from .diff.xmldiff_strat import XmldiffStrategy


class Differ:
    def __init__(self, diff_strategy: DiffStrategy):
        self.diff_strategy = diff_strategy

    async def __call__(
        self, left: UploadFile, right: UploadFile
    ) -> AsyncGenerator[Diff]:
        left_content = await left.read()
        right_content = await right.read()
        return diff_files(self.diff_strategy, left_content, right_content)


diffs_dep = Differ(XmldiffStrategy())
