from logging import getLogger

from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from db.models import Law, Paragraph, LawVersion

logger = getLogger(__name__)


async def init_db(connection_string: str):
    # Startup
    logger.info("Connecting to database at %s", connection_string)
    mongodb_client = AsyncIOMotorClient(connection_string)
    database = mongodb_client.get_database("laws")
    await init_beanie(database=database, document_models=[Paragraph, LawVersion, Law])

    return mongodb_client


def close_db(mongodb_client: AsyncIOMotorClient):
    # Shutdown
    logger.info("Closing database connection")
    mongodb_client.close()
    return mongodb_client
