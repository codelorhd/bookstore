import aioredis
from utils.const import TESTING, TEST_REDIS_URL
from aioredis.commands import Redis


redis: Redis = None


async def check_test_redis():
    global redis
    if TESTING:
        redis = await aioredis.create_redis_pool(TEST_REDIS_URL)