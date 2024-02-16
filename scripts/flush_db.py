from redis.asyncio import Redis
import asyncio

REDIS_URL = "redis://localhost:6379"
REDIS_BATCH_SIZE = 1000

async def main():
    redis = await Redis.from_url(REDIS_URL)
    
    items = redis.scan_iter(count=REDIS_BATCH_SIZE)
    count = 0
    
    # Async operation to perform Redis retrieval and computation in parallel
    async for key in items:
        # TODO: write to database here, should be in batches
        print(key)
        count += 1

    print(count)
    await redis.flushall()
        
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())