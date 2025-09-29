import json
from datetime import datetime
from typing import Optional

from redis.asyncio import Redis
from src.config import settings
from src.models import AnalyticsTxn, RedisEvent


redis_client: Redis = Redis.from_url(str(settings.REDIS_URL))


async def set_redis_keys(
    data: list[RedisEvent], *, is_transaction: bool = False
) -> None:
    async with redis_client.pipeline(transaction=is_transaction) as pipe:
        for redis_data in data:
            await pipe.set(redis_data.key, redis_data.value)
        await pipe.execute()


async def set_redis_from_tx(tx: AnalyticsTxn) -> None:
    data = tx.build_redis_data()
    await set_redis_keys(data)


async def set_redis_access_token(token: str, data: str | None) -> None:
    dataObj = json.loads(data) if data else None
    active = dataObj["active"] if dataObj else False
    # don't store the entire object for memory sake
    stored_data = (
        {
            "active": dataObj["active"],
            "exp": dataObj["exp"],
            "user": {"username": dataObj["user"]["username"]},
        }
        if active
        else {"active": False}
    )
    # implication: active = true ==> exp > now
    # add a 5-second buffer for inactive tokens to reduce load to platform
    ttl = int(dataObj["exp"] - datetime.now().timestamp()) if active else 5
    async with redis_client.pipeline(transaction=False) as pipe:
        await pipe.set(f"USER.{token}", json.dumps(stored_data), ex=ttl)
        await pipe.execute()


async def get_by_key(key: str) -> Optional[str]:
    return await redis_client.get(key)


async def delete_by_key(key: str) -> None:
    return await redis_client.delete(key)
