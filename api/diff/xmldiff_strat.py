from collections.abc import Iterable
from typing import NamedTuple

from lxml import etree
from xmldiff import main as xmldiff_main

from diff.types import (
    DeleteAttrib,
    DeleteNamespace,
    DeleteNode,
    DiffStrategy,
    Edit,
    InsertAttrib,
    InsertComment,
    InsertNamespace,
    InsertNode,
    MoveNode,
    RenameAttrib,
    RenameNode,
    UpdateAttrib,
    UpdateTextAfter,
    UpdateTextIn,
)

ACTION_TO_CLASS = {
    "InsertNode": InsertNode,
    "DeleteNode": DeleteNode,
    "RenameNode": RenameNode,
    "MoveNode": MoveNode,
    "UpdateTextIn": UpdateTextIn,
    "UpdateTextAfter": UpdateTextAfter,
    "UpdateAttrib": UpdateAttrib,
    "DeleteAttrib": DeleteAttrib,
    "InsertAttrib": InsertAttrib,
    "RenameAttrib": RenameAttrib,
    "InsertComment": InsertComment,
    "InsertNamespace": InsertNamespace,
    "DeleteNamespace": DeleteNamespace,
}


def tree_diff_to_edit(tree_diff: NamedTuple) -> Edit:
    action = type(tree_diff).__name__
    cls = ACTION_TO_CLASS.get(action)
    if cls is None:
        raise ValueError(f"Unknown action: {action}")
    return cls(action=action, **tree_diff._asdict())


class XmldiffStrategy(DiffStrategy):
    def __call__(self, left: etree._Element, right: etree._Element) -> Iterable[Edit]:
        edits = xmldiff_main.diff_trees(left, right)
        return [tree_diff_to_edit(d) for d in edits]
