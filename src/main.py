import hashlib
import os

from fastapi import FastAPI, Request

from src.redis import RedisData, delete_by_key, get_by_key, set_redis_key

app = FastAPI()


@app.post("/analytics/")
async def store_data(request: Request):
    random_bytes = os.urandom(16)
    body_bytes = await request.body()
    hash_key = hashlib.sha256(random_bytes).hexdigest()[:16]

    # Create a RedisData instance with the request body and a 5 minute TTL
    RedisD = RedisData(key=hash_key, value=body_bytes, ttl=300)

    # Store the request body in Redis using the hash as the key
    await set_redis_key(RedisD)

    return {"message": "Data stored successfully in Redis", "key": hash_key}
