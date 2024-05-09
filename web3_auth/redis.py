import redis

from demo.settings import REDIS_HOST, REDIS_PORT, REDIS_TIME_TO_LIVE


class RedisClient:
    def __init__(self):
        self.redis = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT)
        self.redis_ttl = REDIS_TIME_TO_LIVE

    def set_with_global_ttl(self, key, value):
        self.redis.set(key, value, ex=self.redis_ttl)

    def get_by_key(self, key):
        return self.redis.get(key)

    def delete_by_key(self, key):
        self.redis.delete(key)
