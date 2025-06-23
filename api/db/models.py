from datetime import date
from typing import Optional, List

import pymongo
from beanie import Document, Link, Indexed


class LawVersion(Document):
    date: Indexed(date)


class Paragraph(Document):
    """
    Represents a paragraph in a law document.
    """

    version: Link[LawVersion]
    index: int
    title: str
    content: str

    class Settings:
        indexes = [
            [
                ("version", pymongo.ASCENDING),
                ("index", pymongo.ASCENDING),
            ]
        ]


class Law(Document):
    """
    Represents a law document in the database.
    """

    name: Indexed(str)
    short_title: Optional[str] = None
    long_title: Optional[str] = None
    versions: List[Link[LawVersion]]
