from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi_utilities import repeat_at

from src.config import settings

from src.auth import verify_jwt
from src.models import AnalyticsTxn
from src.redis import set_redis_from_tx, redis_count
from src.database import flush


app = FastAPI(
    title="Labs Analytics API",
    version="1.0.0",
    description="Unified Asynchronous API Engine for Penn Labs",
)


@app.post("/analytics/")
async def store_data(request: Request, token: dict = Depends(verify_jwt)):
    try:
        body = await request.json()
        txn = AnalyticsTxn(**body)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    await set_redis_from_tx(txn)
    return {"message": "success"}


@app.on_event("startup")
@repeat_at(cron="0 0 * * *")
async def flush_db():
    count = await redis_count()
    print(f"{count} items found in redis")
    while count > 0:
        await flush()
        count -= settings.REDIS_BATCH_SIZE
        count = max(count, 0)
        print(f"{count} items left in redis")
    print("Redis flushed")
