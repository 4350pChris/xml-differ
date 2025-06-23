from datetime import datetime
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

    class Settings:
        indexes = [
            [
                ("index", pymongo.ASCENDING),
                ("title", pymongo.TEXT),
            ]
        ]


class LawVersion(Document):
    """
    Represents a version of a law document.
    """

    date: Indexed(datetime)
    paragraphs: List[Link[Paragraph]]


class Law(Document):
    """
    Represents a law document in the database.
    """

    name: Indexed(str)
    short_title: Optional[str] = None
    long_title: Optional[str] = None
    versions: List[Link[LawVersion]]
