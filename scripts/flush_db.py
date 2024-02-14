from redis.asyncio import Redis
import asyncio
from settings.config import DB_SETTINGS, REDIS_URL, REDIS_BATCH_SIZE
import psycopg2

def batch_insert(events):
    BATCH_INSERT_COMMAND = """
        INSERT INTO Event (user, event, data)
        VALUES (%s, %s, %s);
    """
    
    try:
        with psycopg2.connect(**DB_SETTINGS) as conn:
            with conn.cursor() as cursor:
                cursor.executemany(BATCH_INSERT_COMMAND, events)
    except (psycopg2.DatabaseError, Exception) as error:
        print(f"Error: {error}")

async def main():
    redis = await Redis.from_url(REDIS_URL)
    
    items = redis.scan_iter(count=REDIS_BATCH_SIZE)

    events = list()
    # Async operation to perform Redis retrieval and computation in parallel
    async for key in items:
        try:
            pennkey, event = key.split(":")
        except ValueError:
            print("flush_db: invalid key")
            continue

        data = await redis.get(key)
        events.append((pennkey, event, data))

    batch_insert(events)

    # Clear cache upon successful data flush
    await redis.flushall()
        
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())