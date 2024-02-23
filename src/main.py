from fastapi import FastAPI, HTTPException, Request

from src.redis import set_redis_from_tx
from src.schemas import AnalyticsTxn

app = FastAPI()

@app.post("/analytics/")
async def store_data(request: Request):
    try:
        body = await request.json()
        txn = AnalyticsTxn(**body)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    await set_redis_from_tx(txn)n
    return {"message": "Data stored successfully!"}