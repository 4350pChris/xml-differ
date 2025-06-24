from typing import Iterable

from lxml import etree as ET

from .types import DiffStrategy, Edit


def diff_files(diff_strategy: DiffStrategy, left: str, right: str) -> Iterable[Edit]:
    left_tree = ET.ElementTree(ET.fromstring(left))
    right_tree = ET.ElementTree(ET.fromstring(right))

    # matches = match_paragraphs(left_tree, right_tree)
    return diff_strategy(left_tree, right_tree)
