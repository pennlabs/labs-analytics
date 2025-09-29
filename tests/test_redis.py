import json
from datetime import datetime

import pytest

from src.models import RedisEvent
from src.redis import get_by_key, set_redis_access_token, set_redis_keys


@pytest.mark.asyncio(loop_scope="module")
async def test_redis():
    data = [
        {"key": "test_key", "value": "test_value"},
        {"key": "test_key2", "value": "test_value2"},
    ]

    payload = [RedisEvent(**d) for d in data]
    await set_redis_keys(payload)
    assert await get_by_key("test_key") == b"test_value"


@pytest.mark.asyncio(loop_scope="module")
async def test_access_token_redis_valid():
    token = "abcd"
    data = {
        "active": True,
        "exp": datetime.now().timestamp() + 30,
        "user": {"username": "bfranklin"},
    }

    await set_redis_access_token(token, json.dumps(data))
    val = await get_by_key(token)
    obj = json.loads(val)
    assert val is not None
    assert obj["active"]


@pytest.mark.asyncio(loop_scope="module")
async def test_access_token_redis_invalid():
    token = "abcd"
    data = {
        "active": False,
        "exp": datetime.now().timestamp() - 30,
        "user": {"username": "bfranklin"},
    }
    await set_redis_access_token(token, json.dumps(data))
    val = await get_by_key(token)
    obj = json.loads(val)
    assert val is not None
    assert not obj["active"]
