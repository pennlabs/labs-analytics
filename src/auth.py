import requests
from fastapi import Depends, HTTPException, Request
from jwcrypto import jwk, jwt

from src.config import settings


# The URL to the JWKS endpoint
JWKS_URL = settings.JWKS_URL


def get_jwks():
    if settings.JWKS_CACHE:
        # Check to make sure we have a cached JWK for each key, otherwise refetch all.
        missing = False
        for key in settings.JWKS_URL.keys():
            if key not in settings.JWKS_CACHE:
                missing = True
        if not missing:
            return settings.JWKS_CACHE
    # Make a request to get the JWKS
    for key in settings.JWKS_URL:
        try:
            response = requests.get(JWKS_URL)
            jwks = jwk.JWKSet.from_json(response.text)
            settings.JWKS_CACHE[key] = jwks
        except Exception as e:
            del settings.JWKS_CACHE[key]
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
    public_keys = get_jwks()
    for key in public_keys:
        try:
            decoded_token = jwt.JWT(key=key, jwt=token)
            return decoded_token.claims
        except Exception:
            pass
    raise HTTPException(status_code=401, detail="Failed to verify JWT token")
