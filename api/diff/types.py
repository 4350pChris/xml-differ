from abc import ABC, abstractmethod
from collections.abc import Iterable
from dataclasses import dataclass
from typing import List

from lxml import etree


@dataclass
class Edit(ABC):
    action: str


@dataclass
class InsertNode(Edit):
    target: str
    tag: str
    position: int


@dataclass
class DeleteNode(Edit):
    node: str


@dataclass
class RenameNode(Edit):
    node: str
    tag: str


@dataclass
class MoveNode(Edit):
    node: str
    target: str
    position: int


@dataclass
class UpdateTextIn(Edit):
    node: str
    text: str


@dataclass
class UpdateTextAfter(Edit):
    node: str
    text: str


@dataclass
class UpdateAttrib(Edit):
    node: str
    name: str
    value: str


@dataclass
class DeleteAttrib(Edit):
    node: str
    name: str


@dataclass
class InsertAttrib(Edit):
    node: str
    name: str
    value: str


@dataclass
class RenameAttrib(Edit):
    node: str
    oldname: str
    newname: str


@dataclass
class InsertComment(Edit):
    target: str
    position: int
    text: str


@dataclass
class InsertNamespace(Edit):
    prefix: str
    uri: str


@dataclass
class DeleteNamespace(Edit):
    prefix: str


@dataclass
class Diff:
    left_index: int
    right_index: int
    edits: List[
        InsertNode | DeleteNode | RenameNode | MoveNode | UpdateTextIn | UpdateTextAfter | UpdateAttrib | DeleteAttrib | InsertAttrib | RenameAttrib | InsertComment | InsertNamespace | DeleteNamespace]


class DiffStrategy(ABC):
    @abstractmethod
    def __call__(self, left: etree._Element, right: etree._Element) -> Iterable[Edit]:
        raise NotImplementedError("Subclasses should implement this method.")
