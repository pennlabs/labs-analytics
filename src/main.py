import hashlib
import json
from datetime import datetime

from fastapi import FastAPI, Request

from src.redis import Event, delete_by_key, get_by_key, set_redis_key

app = FastAPI()


@app.post("/analytics/")
async def store_data(request: Request):
    body = await request.json()
    timestamp = datetime.now()
    key = hashlib.md5(f"{timestamp}{body}".encode()).hexdigest()
    data = Event(key=key, value=body)
    await set_redis_key(data)

    return {"message": "Data stored successfully!"}
