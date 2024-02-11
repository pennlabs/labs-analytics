import hashlib
import os

from aioredis import Redis
from fastapi import FastAPI, Request

app = FastAPI()

# Assuming Redis is running on localhost and default port, adjust as necessary
REDIS_URL = "redis://localhost:6379"

@app.on_event("startup")
async def startup_event():
    app.state.redis = await Redis.from_url(REDIS_URL)

@app.on_event("shutdown")
async def shutdown_event():
    app.state.redis.close()
    await app.state.redis.wait_closed()

@app.post("/analytics/")
async def store_data(request: Request):
    random_bytes = os.urandom(16)
    body_bytes = await request.body()
    hash_key = hashlib.sha256(random_bytes).hexdigest()[:16]

    # Store the request body in Redis using the hash as the key
    await app.state.redis.set(hash_key, body_bytes)

    return {"message": "Data stored successfully in Redis", "key": hash_key}
