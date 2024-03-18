# Test to generate jwt token from Penn Labs platforms
import os
import requests
from src.auth import verify_jwt

ATTEST_URL = "https://platform.pennlabs.org/identity/attest/"

CLIENT_ID:str = os.environ.get('CLIENT_ID') or ""
CLIENT_SECRET:str = os.environ.get('CLIENT_SECRET') or ""

def test_env_vars():
    assert os.environ.get('CLIENT_ID') is not None
    assert os.environ.get('CLIENT_SECRET') is not None

def get_tokens():
    response = requests.post(
        ATTEST_URL, auth=(CLIENT_ID, CLIENT_SECRET)
    )
    if response.status_code == 200:
        content = response.json()
        token = content['access']
        refresh = content['refresh']
        return (token, refresh)
    return ("","")

def test_get_tokens():
    token, refresh = get_tokens()
    assert get_tokens() is not None

def test_auth():
    token, _ = get_tokens()
    assert verify_jwt(token) is not None
