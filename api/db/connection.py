import os
from contextlib import asynccontextmanager
from logging import info

from beanie import init_beanie
from fastapi import FastAPI
from .models import Law
from motor.motor_asyncio import AsyncIOMotorClient

CONNECTION_STRING = os.environ['MONGODB_URI']

@asynccontextmanager
async def db_lifespan(app: FastAPI):
    # Startup
    info("Connecting to database cluster at %s", CONNECTION_STRING)
    app.mongodb_client = AsyncIOMotorClient(CONNECTION_STRING)
    app.database = app.mongodb_client.get_database("laws")
    await init_beanie(database=app.database, document_models=[Law])
    ping_response = await app.database.command("ping")
    if int(ping_response["ok"]) != 1:
        raise Exception("Problem connecting to database cluster.")
    else:
        info("Connected to database cluster.")

    yield

    # Shutdown
    app.mongodb_client.close()
