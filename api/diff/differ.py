from abc import ABC, abstractmethod
from lxml import etree as ET
from xmldiff import main as xmldiff_main

from diff.formatter import HTMLFormatter


class DiffStrategy(ABC):
    @abstractmethod
    def __call__(self, left: ET.Element, right: ET.Element, fast_match: bool) -> str:
        raise NotImplementedError("Subclasses should implement this method.")


class XmlToHtmlDiffStrategy(DiffStrategy):
    def __call__(self, left: ET.Element, right: ET.Element, fast_match: bool) -> str:
        formatter = HTMLFormatter()
        edits = xmldiff_main.diff_trees(
            left,
            right,
            formatter=formatter,
            diff_options={"fast_match": fast_match, "ignored_attrs": ["Font", "Size"]},
        )
        return edits.__str__()


def diff_files(
    diff_strategy: DiffStrategy, fast_match: bool, left: str, right: str
) -> str:
    left_tree = ET.ElementTree(ET.fromstring(left))
    right_tree = ET.ElementTree(ET.fromstring(right))

    return diff_strategy(left_tree, right_tree, fast_match)
