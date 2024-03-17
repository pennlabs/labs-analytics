import asyncio
from typing import Any

from settings.config import DATABASE_URL
from sqlalchemy import (
    Boolean,
    Column,
    CursorResult,
    DateTime,
    ForeignKey,
    Identity,
    Insert,
    Integer,
    LargeBinary,
    MetaData,
    Select,
    String,
    Table,
    Update,
    func,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

engine = create_async_engine(str(DATABASE_URL))

metadata = MetaData()

event = Table(
    "event",
    metadata,
    Column("id", Integer, Identity(), primary_key=True),
    Column("product", String, nullable=False),
    Column("pennkey", String, nullable=False),
    Column("datapoint", String, nullable=False),
    Column("value", String, nullable=False),
    Column("timestamp", DateTime, nullable=False),
)


# Create all tables in the metadata
async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(metadata.create_all)


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "create":
        asyncio.run(create_tables())
        print("Tables created")
    else:
        print("No action taken")
