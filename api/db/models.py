from datetime import datetime
from typing import Optional

import pymongo
from beanie import Document


class Law(Document):
    """
    Represents a law document in the database.
    """

    name: str
    short_title: Optional[str] = None
    long_title: Optional[str] = None
    date: datetime
    content: str

    class Settings:
        indexes = [
            [
                ("name", pymongo.TEXT),
                ("date", pymongo.ASCENDING),
            ]
        ]
