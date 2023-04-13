import pytest
import databases.redis



def test_redis_connection():
    assert redis.RedisConnector() == True
