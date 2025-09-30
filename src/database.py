# fmt: off
from sqlalchemy import Column, DateTime, Identity, Integer, MetaData, String, Table, select
from sqlalchemy.ext.asyncio import create_async_engine

from src.config import settings


# fmt: on


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
    Column("value", String, nullable=True),
    Column("timestamp", DateTime, nullable=False),
)


async def query():
    statement = select(event).where(event.c.pennkey == "melitski")
    async with engine.begin() as conn:
        res = await conn.execute(statement)
        print(res["datapoint"])
