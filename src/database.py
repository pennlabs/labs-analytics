from typing import Any
import asyncio
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
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.dialects.postgresql import UUID

from .config import settings
# from constants import DB_NAMING_CONVENTION

DATABASE_URL = str(settings.DATABASE_URL)

engine = create_async_engine(DATABASE_URL)

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

asyncio.run(create_tables())