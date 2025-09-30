import os

import sentry_sdk
from fastapi import Depends, FastAPI, HTTPException, Request

from database import query
from src.auth import verify_auth
from src.models import AnalyticsTxn
from src.redis import set_redis_from_tx


sentry_sdk.init(
    dsn=os.getenv("SENTRY_DSN", ""),
    # Add data like request headers and IP for users,
    # see https://docs.sentry.io/platforms/python/data-management/data-collected/ for more info
    send_default_pii=True,
)


app = FastAPI()


@app.post("/analytics/")
async def store_data(request: Request, token: dict = Depends(verify_auth)):
    try:
        body = await request.json()
        txn = AnalyticsTxn(**body)
        if token.get("username") and token["username"] != txn.pennkey:
            raise HTTPException(
                status_code=403,
                detail="User account access tokens can only record their Pennkey",
            )
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    await set_redis_from_tx(txn)
    # should invalidate cache if applies, given a certain buffer (probably 1min)
    return {"message": "Data stored successfully!"}


# probably shouldn't allow general token querying, so break this out into two separate dependencies
@app.get("/count")
async def get_count(
    request: Request,
    token: dict = Depends(verify_auth),
    pennkey: str | None = None,
    key: str | None = None,
    after: int | None = None,
    before: int | None = None,
    product: int | None = None,
):
    await query()
    return {"message": "done"}
    # perform query
    # cache?
    # return value
