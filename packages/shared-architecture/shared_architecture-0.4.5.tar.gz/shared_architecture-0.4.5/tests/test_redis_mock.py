# tests/test_redis_mock.py

import pytest
import asyncio
from shared_architecture.connection_manager import ConnectionManager

@pytest.mark.asyncio
async def test_redis_tick_data_store_and_retrieve():
    cm = ConnectionManager()
    redis = cm.get_redis()
    await redis.hset("tick:NSE:NIFTY", "price", "22000")
    value = await redis.hget("tick:NSE:NIFTY", "price")
    assert value == "22000"

@pytest.mark.asyncio
async def test_redis_tick_data_not_found():
    cm = ConnectionManager()
    redis = cm.get_redis()
    value = await redis.hget("tick:NSE:INVALID", "price")
    assert value is None