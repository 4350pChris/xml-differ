from collections.abc import AsyncGenerator
from datetime import date

from .db.models import Law, Paragraph
from .diff.differ import DiffStrategy, diff_files
from .diff.types import Diff
from .diff.xmldiff_strat import XmldiffStrategy
from .routers.response_models import LawDetailProjection


class Differ:
    def __init__(self, diff_strategy: DiffStrategy):
        self.diff_strategy = diff_strategy

    async def __call__(
        self, law_id: str, left: date, right: date
    ) -> AsyncGenerator[Diff]:
        law = await Law.get(
            law_id, fetch_links=True, projection_model=LawDetailProjection
        )
        left_version = [version for version in law.versions if version.date == left]
        right_version = [version for version in law.versions if version.date == right]
        left_paragraph = await Paragraph.find_one(
            Paragraph.version._id == left_version[0].id
        )
        right_paragraph = await Paragraph.find_one(
            Paragraph.version._id == right_version[0].id
        )
        return diff_files(
            self.diff_strategy, left_paragraph.content, right_paragraph.content
        )


diffs_dep = Differ(XmldiffStrategy())
