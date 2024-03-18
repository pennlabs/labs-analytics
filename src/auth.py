import requests
from fastapi import Depends, HTTPException, Request
from jwcrypto import jwk, jwt

from src.config import settings

# The URL to the JWKS endpoint
JWKS_URL = settings.JWKS_URL

def get_jwk():
    if settings.JWKS_CACHE:
        key = jwk.json_decode(settings.JWKS_CACHE).get("keys")[0]
        return jwk.JWK(**key) 

    # Make a request to get the JWKS
    jwks = ""
    try:
        jwks = requests.get(JWKS_URL).text
        settings.JWK_CACHE = jwk.json_encode(jwks)
    except:
        settings.JWKS_CACHE = ""
    # Assuming there's only one key in the set
    key = jwk.json_decode(jwks).get("keys")[0]
    return jwk.JWK(**key)


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
