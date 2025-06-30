from lxml import etree as ET

from diff.types import DiffStrategy


def diff_files(diff_strategy: DiffStrategy, left: str, right: str):
    left_tree = ET.ElementTree(ET.fromstring(left))
    right_tree = ET.ElementTree(ET.fromstring(right))

    return diff_strategy(left_tree, right_tree)
