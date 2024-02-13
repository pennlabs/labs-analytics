import asyncio
from fastapi import FastAPI, Request
from redis.asyncio import Redis

app = FastAPI()

# Assuming Redis is running on localhost and default port, adjust as necessary
REDIS_URL = "redis://localhost:6379"

@app.on_event("startup")
async def startup_event():
    app.state.redis = await Redis.from_url(REDIS_URL)

@app.on_event("shutdown")
async def shutdown_event():
    await app.state.redis.close()

@app.post("/analytics/")
async def store_data(request: Request):
    body = await request.json()

    tasks = [app.state.redis.set(key, value) for key, value in body.items()]
    await asyncio.gather(*tasks)

    return {"message": "Jobs submitted to Redis"}
