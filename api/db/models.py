from datetime import datetime
from typing import Optional, List

import pymongo
from beanie import Document, Link


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


class Law(Document):
    """
    Represents a law document in the database.
    """

    name: str
    short_title: Optional[str] = None
    long_title: Optional[str] = None
    date: datetime
    paragraphs: List[Link[Paragraph]]

    class Settings:
        indexes = [
            [
                ("name", pymongo.TEXT),
                ("date", pymongo.ASCENDING),
            ]
        ]
