import asyncio

from sqlalchemy import Column, DateTime, Identity, Integer, MetaData, String, Table
from sqlalchemy.ext.asyncio import create_async_engine

from src.config import settings


DATABASE_URL = settings.DATABASE_URL

engine = create_async_engine(DATABASE_URL)

metadata = MetaData()

event = Table(
    "event",
    metadata,
    Column("id", Integer, Identity(), primary_key=True),
    Column("product", String, nullable=False),
    Column("pennkey", String, nullable=True),
    Column("datapoint", String, nullable=False),
    Column("value", String, nullable=False),
    Column("timestamp", DateTime, nullable=False),
)


# Create all tables in the metadata
async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(metadata.create_all)


asyncio.run(create_tables())
