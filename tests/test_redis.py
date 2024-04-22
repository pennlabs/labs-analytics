import pytest

from src.models import RedisEvent
from src.redis import get_by_key, set_redis_keys


@pytest.mark.asyncio
async def test_redis():
    data = [
        {"key": "test_key", "value": "test_value"},
        {"key": "test_key2", "value": "test_value2"},
    ]

    payload = [RedisEvent(**d) for d in data]
    await set_redis_keys(payload)
    assert await get_by_key("test_key") == b"test_value"
