import requests
from fastapi import Depends, HTTPException, Request
from jwcrypto import jwk, jwt

from src.config import settings


# The URL to the JWKS endpoint
JWKS_URL = settings.JWKS_URL


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


def verify_jwt(token: str = Depends(get_token_from_header)):
    try:
        # Load the public key
        public_key = get_jwk()
        # Decode and verify the JWT
        decoded_token = jwt.JWT(key=public_key, jwt=token)
        return decoded_token.claims
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))
