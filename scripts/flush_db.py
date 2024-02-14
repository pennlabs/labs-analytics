from redis.asyncio import Redis
import asyncio
from settings.config import DB_SETTINGS, REDIS_URL, REDIS_BATCH_SIZE
import psycopg2
from datetime import datetime

def batch_insert(events):
    # TODO: Ensure number of events does not exceed SQL max statement tokens
    BATCH_INSERT_COMMAND = """
        INSERT INTO Event (pennkey, event, data, timestamp)
        VALUES (%s, %s, %s, %s);
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
            pennkey, event = key.decode('utf-8').split("::")
            data_bytes = await redis.get(key)
            data, timestamp_str = data_bytes.decode("utf-8").split("::")
            timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S.%f")
        except ValueError:
            print("flush_db: invalid key")
            continue
        
        events.append((pennkey, event, data, timestamp))

    batch_insert(events)

    # Clear cache upon successful data flush
    await redis.flushall()
        
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())