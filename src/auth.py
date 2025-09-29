import json

import requests
from fastapi import Depends, HTTPException, Request
from jwcrypto import jwk, jwt

from src.config import settings
from src.redis import get_by_key, set_redis_access_token


# The URL to the JWKS endpoint
JWKS_URL = settings.JWKS_URL
INTROSPECT_URL = settings.INTROSPECT_URL


def get_jwk():
    if settings.JWKS_CACHE:
        key = settings.JWKS_CACHE
        return key

    # Make a request to get the JWKS
    try:
        response = requests.get(JWKS_URL)
        jwks = jwk.JWKSet.from_json(response.text)
        settings.JWKS_CACHE = jwks
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return settings.JWKS_CACHE


def get_token_from_header(request: Request):
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        raise HTTPException(status_code=401, detail="Authorization header missing")
    try:
        scheme, token = auth_header.split()
        if scheme.lower() != "bearer":
            raise HTTPException(status_code=401, detail="Wrong authentication scheme")
        return token
    except ValueError:
        raise HTTPException(
            status_code=401, detail="Invalid authorization header format"
        )


async def verify_auth(token: str = Depends(get_token_from_header)):
    try:
        # Load the public key
        public_key = get_jwk()
        # Decode and verify the JWT
        decoded_token = jwt.JWT(key=public_key, jwt=token)
        return json.loads(decoded_token.claims)
    except ValueError:
        # check to see if platform introspect returns a positive result
        # note that the token itself should have the "introspection" scope
        # (so that it can inspect itself)
        cached_token = await get_by_key(token)
        if cached_token:
            data = json.loads(cached_token)
            if not data["active"]:
                raise HTTPException(status_code=403, detail="Token cached as not valid")
            return data["user"]
        else:
            headers = {"Authorization": f"Bearer {token}"}
            response = requests.get(f"{INTROSPECT_URL}?token={token}", headers=headers)
            if response.status_code != 200 or not response.json()["active"]:
                await set_redis_access_token(token, None)
                raise HTTPException(
                    status_code=403, detail="Unable to verify the token provided."
                )
            else:
                await set_redis_access_token(token, response.text)
            return response.json()["user"]
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))
