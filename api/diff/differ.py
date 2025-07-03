from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Literal

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
    ) -> str:
        raise NotImplementedError("Subclasses should implement this method.")


class XmlToHtmlDiffStrategy(DiffStrategy):
    def __call__(
        self, left: ET.Element, right: ET.Element, options: DifferOptions
    ) -> str:
        formatter = HTMLFormatter()
        edits = xmldiff_main.diff_trees(
            left,
            right,
            formatter=formatter,
            diff_options={**options.__dict__, "ignored_attrs": ["Font", "Size"]},
        )
        return edits.__str__()


def diff_files(
    diff_strategy: DiffStrategy, options: DifferOptions, left: str, right: str
) -> str:
    left_tree = ET.ElementTree(ET.fromstring(left))
    right_tree = ET.ElementTree(ET.fromstring(right))

    return diff_strategy(left_tree, right_tree, options)
