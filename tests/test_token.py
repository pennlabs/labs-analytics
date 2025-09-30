# Test to generate jwt token from Penn Labs platforms
import os

import pytest
import requests

from src.auth import verify_auth


ATTEST_URL = "https://platform.pennlabs.org/identity/attest/"

# Using Penn Basics DLA Account for testing, will not work if you don't have that in .env
CLIENT_ID: str = os.environ.get("TESTING_CLIENT_ID") or ""
CLIENT_SECRET: str = os.environ.get("TESTING_CLIENT_SECRET") or ""
ACCESS_TOKEN: str = os.environ.get("TESTING_USER_ACCESS_TOKEN") or ""
ACCESS_TOKEN_USER: str = os.environ.get("TESTING_USERNAME") or ""


def test_env_vars():
    assert os.environ.get("TESTING_CLIENT_ID") is not None
    assert os.environ.get("TESTING_CLIENT_SECRET") is not None
    assert os.environ.get("TESTING_USER_ACCESS_TOKEN") is not None
    assert os.environ.get("TESTING_USERNAME") is not None


def get_tokens():
    response = requests.post(ATTEST_URL, auth=(CLIENT_ID, CLIENT_SECRET))
    if response.status_code == 200:
        content = response.json()
        token = content["access"]
        refresh = content["refresh"]
        return (token, refresh)
    return ("", "")


def get_user_token():
    return (ACCESS_TOKEN, ACCESS_TOKEN_USER)


def test_get_tokens():
    token, refresh = get_tokens()
    print(token)
    assert token != ""
    assert refresh != ""


@pytest.mark.asyncio(loop_scope="module")
async def test_auth_b2b_token():
    token, _ = get_tokens()
    assert await verify_auth(token) is not None
