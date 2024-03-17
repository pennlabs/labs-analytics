import requests
from fastapi import Depends, HTTPException, Request
from jose import JWTError, jwk, jwt

# The URL to the JWKS endpoint
JWKS_URL = "https://<your-issuer-domain>/path/to/jwks"

# Your expected audience value and issuer URL
AUDIENCE = "<your-audience>"
ISSUER = "<your-issuer>"


def get_jwk():
    # Make a request to get the JWKS
    jwks = requests.get(JWKS_URL).json()
    # Assuming there's only one key in the set
    return jwk.construct(jwks["keys"][0])


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
        public_key = get_jwk().public_key()
        # Decode and verify the JWT
        decoded_token = jwt.decode(
            token, public_key, algorithms=["RS256"], audience=AUDIENCE, issuer=ISSUER
        )
        return decoded_token
    except JWTError as e:
        raise HTTPException(status_code=401, detail=str(e))
