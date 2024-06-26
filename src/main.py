from fastapi import Depends, FastAPI, HTTPException, Request

from src.auth import verify_jwt
from src.models import AnalyticsTxn
from src.redis import set_redis_from_tx


app = FastAPI()


@app.post("/analytics/")
async def store_data(request: Request, token: dict = Depends(verify_jwt)):
    try:
        body = await request.json()
        txn = AnalyticsTxn(**body)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    await set_redis_from_tx(txn)
    return {"message": "Data stored successfully!"}
