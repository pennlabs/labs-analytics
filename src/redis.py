from datetime import datetime, timedelta
from typing import Optional

from redis.asyncio import Redis
from src.config import settings
from src.models import CustomModel

redis_client: Redis = Redis.from_url(str(settings.REDIS_URL))


class Event(CustomModel):
    key: bytes | str
    value: bytes | str


class AnalyticsTxn(CustomModel):
    product: int
    pennkey: Optional[str] = None
    timestamp: datetime
    data: list[Event]


async def set_redis_key(redis_data: Event, *, is_transaction: bool = False) -> None:
    async with redis_client.pipeline(transaction=is_transaction) as pipe:
        await pipe.set(redis_data.key, redis_data.value)
        await pipe.execute()


# set multiple keys in single transaction
async def set_redis_keys(tx_data: AnalyticsTxn, *, is_transaction: bool = False) -> None:
    async with redis_client.pipeline(transaction=is_transaction) as pipe:
        for event in tx_data.data:
            await pipe.set(event.key, event.value)
        # await pipe.set(redis_data.key, redis_data.value)
        # if redis_data.ttl:
        # await pipe.expire(redis_data.key, redis_data.ttl)

        await pipe.execute()


async def get_by_key(key: str) -> Optional[str]:
    return await redis_client.get(key)


async def delete_by_key(key: str) -> None:
    return await redis_client.delete(key)
