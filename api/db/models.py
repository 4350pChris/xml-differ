from datetime import datetime

from beanie import Document


class Law(Document):
    """
    Represents a law document in the database.
    """
    name: str
    date: datetime
    version: int
    content: str
