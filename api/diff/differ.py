from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Literal, List

from lxml import etree as ET
from xmldiff import main as xmldiff_main

from diff.formatter import HTMLFormatter


@dataclass
class DifferOptions:
    fast_match: bool
    F: float
    ratio_mode: Literal["accurate", "fast", "faster"]


class DiffStrategy(ABC):
    @abstractmethod
    def __call__(
        self, left: ET.Element, right: ET.Element, options: DifferOptions
    ) -> List[str]:
        raise NotImplementedError("Subclasses should implement this method.")


class XmlToHtmlDiffStrategy(DiffStrategy):
    def __call__(
        self, left: ET.Element, right: ET.Element, options: DifferOptions
    ) -> List[str]:
        formatter = HTMLFormatter()
        edits = xmldiff_main.diff_trees(
            left,
            right,
            formatter=formatter,
            diff_options={
                **options.__dict__,
                "ignored_attrs": ["Font", "Size", "builddate", "doknr"],
            },
        )
        return [edits.__str__()]


class XmlToSplitHtmlDiffStrategy(XmlToHtmlDiffStrategy):
    def _remove_nodes(self, edit_html: str, tag_name: str):
        tree = ET.ElementTree(ET.fromstring(edit_html))
        ET.strip_elements(tree, tag_name, with_tail=False)

        return ET.tostring(tree.getroot(), encoding="unicode")

    def __call__(
        self, left: ET.Element, right: ET.Element, options: DifferOptions
    ) -> List[str]:
        edit_html = super().__call__(left, right, options)[0]

        left_tree_str = self._remove_nodes(edit_html, "ins")
        right_tree_str = self._remove_nodes(edit_html, "del")

        return [left_tree_str, right_tree_str]


def diff_files(
    diff_strategy: DiffStrategy, options: DifferOptions, left: str, right: str
) -> List[str]:
    left_tree = ET.ElementTree(ET.fromstring(left))
    right_tree = ET.ElementTree(ET.fromstring(right))

    return diff_strategy(left_tree, right_tree, options)
