from typing import Optional

from redis.asyncio import Redis
from src.config import settings
from src.models import RedisEvent
from src.schemas import AnalyticsTxn

redis_client: Redis = Redis.from_url(str(settings.REDIS_URL))


async def set_redis_keys(data: list[RedisEvent], *, is_transaction: bool = False) -> None:
    async with redis_client.pipeline(transaction=is_transaction) as pipe:
        for redis_data in data:
            await pipe.set(redis_data.key, redis_data.value)
        await pipe.execute()


async def set_redis_from_tx(tx: AnalyticsTxn) -> None:
    data = tx.build_redis_data()
    await set_redis_keys(data)


async def get_by_key(key: str) -> Optional[str]:
    return await redis_client.get(key)


async def delete_by_key(key: str) -> None:
    return await redis_client.delete(key)
