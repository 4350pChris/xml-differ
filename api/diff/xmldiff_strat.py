from typing import Iterable, NamedTuple
from lxml import etree
from xmldiff import main as xmldiff_main
from xmldiff.actions import InsertNamespace, DeleteNamespace, InsertComment, InsertNode, UpdateAttrib, RenameAttrib, \
    InsertAttrib, DeleteAttrib, MoveNode, RenameNode, UpdateTextIn, UpdateTextAfter, DeleteNode

from .types import DiffStrategy, Edit

def tree_diff_to_edit(tree_diff: NamedTuple) -> Edit:
    return Edit(action=type(tree_diff).__name__, parameters=tree_diff._asdict())


class XmldiffStrategy(DiffStrategy):
    def __call__(self, left: etree._Element, right: etree._Element) -> Iterable[Edit]:
        edits = xmldiff_main.diff_trees(left, right)
        return [tree_diff_to_edit(d) for d in edits]