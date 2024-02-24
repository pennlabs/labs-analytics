from datetime import timedelta

from fastapi import Depends, FastAPI, HTTPException, Request

from auth import create_access_token
from src.config import settings
from src.database import get_client
from src.models import Client, Product, Token
from src.redis import set_redis_from_tx
from src.schemas import AnalyticsTxn, AuthRequest

app = FastAPI()


@app.post("/analytics/")
async def store_data(request: Request):
    try:
        body = await request.json()
        txn = AnalyticsTxn(**body)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    await set_redis_from_tx(txn)
    return {"message": "Data stored successfully!"}


@app.post("/token", response_model=Token)
async def login_for_access_token(form: AuthRequest = Depends()):
    # Hash the secret and compare it to the hashed secret in the database
    client = Client(
        client_id=form.client_id, secret=form.secret, product=Product(form.product)
    )
    # get client data from database
    try:
        db_client = get_client(client)
    except Exception:
        # invalid client_id
        raise HTTPException(status_code=400, detail="Invalid client id")

    if not client.verify_client(db_client[0], db_client[1]):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    token_expires = timedelta(minutes=settings.JWT_EXP)
    access_token = create_access_token(
        data={"sub": form.client_id}, expires_delta=token_expires
    )
    return Token(access_token=access_token, token_type="bearer")
