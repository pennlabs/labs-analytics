import asyncio
import json
import sys
from datetime import datetime

import asyncpg
from redis.asyncio import Redis

from settings.config import DATABASE_URL, REDIS_BATCH_SIZE, REDIS_URL


async def batch_insert(events):
    BATCH_INSERT_COMMAND = """
        INSERT INTO event (product, pennkey, datapoint, value, timestamp)
        VALUES ($1, $2, $3, $4, $5)
        """

    try:
        conn = await asyncpg.connect(dsn=DATABASE_URL)
        # This is probably? sql injection safe, see:
        # https://github.com/MagicStack/asyncpg/blob/master/asyncpg/connection.py#L1901
        await conn.executemany(BATCH_INSERT_COMMAND, events)
    except Exception as error:
        print(f"Error: {error}")


async def main():
    redis = await Redis.from_url(str(REDIS_URL))

    items = redis.scan_iter(count=REDIS_BATCH_SIZE)

    events = list()

    # Async operation to perform Redis retrieval and computation in parallel
    async for key in items:
        try:
            data_bytes = await redis.get(key)
            data = data_bytes.decode("utf-8").replace("'", '"')
            json_string = json.dumps(data)
            data = json.loads(json.loads(json_string))
        except ValueError as e:
            print(e)
            print("flush_db: invalid key")
            continue

        events.append(
            (
                data.get("product"),
                data["pennkey"],
                data["datapoint"],
                data["value"],
                datetime.fromtimestamp(data["timestamp"]),
            )
        )

    await batch_insert(events)

    await redis.flushall()


async def redis_count():
    redis = await Redis.from_url(str(REDIS_URL))
    return await redis.dbsize()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    count = loop.run_until_complete(redis_count())
    print(f"{count} items found in redis")
    while count > 0:
        loop.run_until_complete(main())
        count -= REDIS_BATCH_SIZE
        count = max(count, 0)
        print(f"{count} items left in redis")
    print("Redis flushed")
