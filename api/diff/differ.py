from abc import ABC, abstractmethod
from lxml import etree as ET
from xmldiff import main as xmldiff_main

from diff.formatter import HTMLFormatter


class DiffStrategy(ABC):
    @abstractmethod
    def __call__(self, left: ET.Element, right: ET.Element):
        raise NotImplementedError("Subclasses should implement this method.")


class XmlToHtmlDiffStrategy(DiffStrategy):
    def __call__(self, left: ET.Element, right: ET.Element) -> str:
        formatter = HTMLFormatter()
        edits = xmldiff_main.diff_trees(
            left, right, formatter=formatter, diff_options={"fast_match": True}
        )
        return edits.__str__()


def diff_files(diff_strategy: DiffStrategy, left: str, right: str):
    left_tree = ET.ElementTree(ET.fromstring(left))
    right_tree = ET.ElementTree(ET.fromstring(right))

    return diff_strategy(left_tree, right_tree)
