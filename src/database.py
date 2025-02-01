import json
from datetime import datetime

from sqlalchemy import (
    Column,
    DateTime,
    Identity,
    Integer,
    MetaData,
    String,
    Table,
    insert,
)
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from src.config import settings
from src.redis import redis_client
from src.config import settings


DATABASE_URL = str(settings.DATABASE_URL)  # Ensure DATABASE_URL is a string

engine = create_async_engine(DATABASE_URL)

metadata = MetaData()

event = Table(
    "event",
    metadata,
    Column("id", Integer, Identity(), primary_key=True),
    Column("product", String, nullable=False),
    Column("pennkey", String, nullable=True),
    Column("datapoint", String, nullable=False),
    Column("value", String, nullable=True),
    Column("timestamp", DateTime, nullable=False),
)


# Create all tables in the metadata
async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(metadata.create_all)


# Create an async session
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


async def batch_insert(events):
    async with async_session() as session:
        async with session.begin():
            await session.execute(insert(event), events)
        await session.commit()


async def flush():
    items = redis_client.scan_iter(count=settings.REDIS_BATCH_SIZE)
    events = list()
    async for key in items:
        try:
            data_bytes = await redis_client.get(key)
            data = data_bytes.decode("utf-8").replace("'", '"')
            json_string = json.dumps(data)
            data = json.loads(json.loads(json_string))
        except ValueError as e:
            print(e)
            print("flush_db: invalid key")
            continue
        events.append(
            {
                "product": data.get("product"),
                "pennkey": data["pennkey"],
                "datapoint": data["datapoint"],
                "value": data["value"],
                "timestamp": datetime.fromtimestamp(data["timestamp"]),
            }
        )

    await batch_insert(events)
    await redis_client.flushall()
