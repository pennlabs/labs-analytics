import asyncio
import json
from datetime import datetime

import asyncpg
from redis.asyncio import Redis

from settings.config import DB_SETTINGS, REDIS_BATCH_SIZE, REDIS_URL


async def batch_insert(events):
    # TODO: Ensure number of events does not exceed SQL max statement tokens
    BATCH_INSERT_COMMAND = """
        INSERT INTO event (product, pennkey, datapoint, value, timestamp)
        VALUES ($1, $2, $3, $4, $5)
        """

    try:
        conn = await asyncpg.connect(**DB_SETTINGS)
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

    # await redis.flushall()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
