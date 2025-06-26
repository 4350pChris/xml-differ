from datetime import date
from typing import Optional, List

import pymongo
from beanie import Document, Link, Indexed


class Paragraph(Document):
    """
    Represents a paragraph in a law document.
    """

    index: int
    title: str
    content: str

    def same_as(self, other):
        return self.title == other.title

    class Settings:
        indexes = [[("version.$id", pymongo.ASCENDING), ("index", pymongo.ASCENDING)]]


class LawVersion(Document):
    date: Indexed(date)
    paragraphs: List[Link[Paragraph]]


class Law(Document):
    """
    Represents a law document in the database.
    """

    name: Indexed(str)
    short_title: Optional[str] = None
    long_title: Optional[str] = None
    versions: List[Link[LawVersion]]
