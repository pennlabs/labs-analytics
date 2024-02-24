from datetime import datetime, timedelta
from typing import Optional

from jose import JWTError, jwt

from src.config import settings
from src.models import Client


def authenticate_client(client: Client) -> Client:
    return client


def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, str(settings.JWT_SECRET), algorithm=settings.JWT_ALG
    )
    return encoded_jwt
