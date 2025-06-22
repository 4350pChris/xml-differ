import os
from logging import getLogger

from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from .models import Law

logger = getLogger(__name__)

CONNECTION_STRING = os.environ["MONGODB_URI"]


async def init_db():
    # Startup
    logger.info("Connecting to database at %s", CONNECTION_STRING)
    mongodb_client = AsyncIOMotorClient(CONNECTION_STRING)
    database = mongodb_client.get_database("laws")
    await init_beanie(database=database, document_models=[Law])

    return mongodb_client


def close_db(mongodb_client: AsyncIOMotorClient):
    # Shutdown
    logger.info("Closing database connection")
    mongodb_client.close()
    return mongodb_client
