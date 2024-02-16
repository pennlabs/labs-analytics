import hashlib
import os

from fastapi import FastAPI, Request
from redis.asyncio import Redis

from src.redis import RedisData, delete_by_key, get_by_key, set_redis_key

app = FastAPI()


@app.post("/analytics/")
async def store_data(request: Request):
    body = await request.json()

    # Create a RedisData instance with the request body and a 5 minute TTL
    RedisD = RedisData(key=hash_key, value=body_bytes, ttl=300)

    # Store the request body in Redis using the hash as the key
    await set_redis_key(RedisD)

    return {"message": "Jobs submitted to Redis"}
