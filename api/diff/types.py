from abc import ABC, abstractmethod
from collections.abc import Iterable
from dataclasses import dataclass
from typing import Any

from lxml import etree

@dataclass
class Edit:
    action: str
    parameters: dict[str, Any]

@dataclass
class Diff:
    left_index: int
    right_index: int
    edits: list

class DiffStrategy(ABC):
    @abstractmethod
    def __call__(self, left: etree._Element, right: etree._Element) -> Iterable[Edit]:
        raise NotImplementedError("Subclasses should implement this method.")
