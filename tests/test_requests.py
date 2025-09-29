import json
import random
from datetime import datetime

import pytest
import requests

from tests.test_token import get_tokens, get_user_token


# b2b should return 200
# active user should:
# pk = request.pk -> 200
# pk != request.pk -> 400
# inactive user should return 400+


def make_request(payload, access_token):
    url = "http://localhost:80/analytics/"
    submit_payload = json.dumps(payload)
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}",
    }

    try:
        response = requests.post(url, headers=headers, data=submit_payload)
    except Exception as e:
        if "ConnectionError" in str(e):
            return (-2, "Please make sure the server is running.")
        return (-1, str(e))
    return (response.status_code, response.text)


@pytest.mark.asyncio(loop_scope="module")
async def test_b2b_result():
    payload = {
        "product": random.randint(1, 10),
        "pennkey": "test_usr",
        "timestamp": int(datetime.now().timestamp()),
        "data": [{"key": "user.click", "value": str(random.randint(1, 1000))},],
    }
    (token, _) = get_tokens()
    (code, string) = make_request(payload, token)
    assert code == 200


@pytest.mark.asyncio(loop_scope="module")
async def test_user_invalid_token():
    payload = {
        "product": random.randint(1, 10),
        "pennkey": "test_usr",
        "timestamp": int(datetime.now().timestamp()),
        "data": [{"key": "user.click", "value": str(random.randint(1, 1000))},],
    }
    token = "INVALID_VALUE"
    (code, string) = make_request(payload, token)
    assert code == 403


@pytest.mark.asyncio(loop_scope="module")
async def test_user_pennkey_not_matching_pk():
    payload = {
        "product": random.randint(1, 10),
        "pennkey": "test_usr",
        "timestamp": int(datetime.now().timestamp()),
        "data": [{"key": "user.click", "value": str(random.randint(1, 1000))},],
    }
    (token, _) = get_user_token()
    (code, string) = make_request(payload, token)
    data = json.loads(string)
    assert (
        code == 403
        and data["detail"] == "User account access tokens can only record their Pennkey"
    )


@pytest.mark.asyncio(loop_scope="module")
async def test_user_pennkey_working():
    (token, username) = get_user_token()
    payload = {
        "product": random.randint(1, 10),
        "pennkey": username,
        "timestamp": int(datetime.now().timestamp()),
        "data": [{"key": "user.click", "value": str(random.randint(1, 1000))},],
    }
    (code, _) = make_request(payload, token)
    assert code == 200
